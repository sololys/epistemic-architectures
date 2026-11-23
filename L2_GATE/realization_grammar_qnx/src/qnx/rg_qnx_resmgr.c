/*
 * QNX Neutrino 8.0 Resource Manager: /dev/realization_gate
 * Implementerer Realiseringsgrammatikk v1.0 (D1.2 / D1.5 / D2 / D3).
 */

#include <errno.h>
#include <devctl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/iofunc.h>
#include <sys/dispatch.h>
#include <sys/mman.h>
#include <sys/neutrino.h>
#include <sys/procmgr.h>
#include <hw/inout.h>

#include "rg_grammar.h"

#define RG_DEV_PATH             "/dev/realization_gate"
#define RG_HW_CLAMP_PORT        0x00E9u
#define RG_D2_TIMEOUT_NS        60000000ULL

typedef struct {
	rg_candidate_t        cand;
	rg_admissibility_in_t adm;
	uint8_t               simulate_d2_timeout;
	uint8_t               simulate_d2_observed;
	uint8_t               simulate_d2_partial;
	uint8_t               reserved;
	uint32_t              method_code;
} rg_ipc_req_t;

typedef struct {
	rg_gate_verdict_t       verdict;
	rg_realization_status_t realization_status;
	rg_witness_record_t     witness;
} rg_ipc_rep_t;

#define DCMD_RG_EVALUATE __DIOTF(_DCMD_MISC, 0x42, rg_ipc_req_t)

static rg_engine_t g_eng;
static uintptr_t   g_hw_io = MAP_DEVICE_FAILED;

static inline void rg_hw_write_u8(uintptr_t handle, uint8_t val)
{
	if (handle == MAP_DEVICE_FAILED)
		return;
#ifdef __X86_64__
	out8((uint16_t)handle, val);
#else
	out8(handle, val);
#endif
}

static uint64_t rg_monotonic_ns(void)
{
	struct timespec ts;

	if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0)
		return 0u;
	return ((uint64_t)ts.tv_sec * 1000000000ULL) + (uint64_t)ts.tv_nsec;
}

static int rg_sandbox_and_clamp_boot(void)
{
	uint64_t zero_tol = 0ULL;
	uint64_t old_tol  = 0ULL;
	uint32_t deny_lock = PROCMGR_ADN_ROOT | PROCMGR_ADN_NONROOT |
			     PROCMGR_AOP_DENY | PROCMGR_AOP_LOCK;

	if (ThreadCtl(_NTO_TCTL_IO_LEVEL, (void *)_NTO_IO_LEVEL_1) == -1)
		return -1;
	g_hw_io = mmap_device_io(1, RG_HW_CLAMP_PORT);
	if (g_hw_io == MAP_DEVICE_FAILED)
		return -1;
	rg_hw_write_u8(g_hw_io, 0x00u);

	(void)procmgr_timer_tolerance(0, &zero_tol, &old_tol);
	if (mlockall(MCL_CURRENT | MCL_FUTURE) != 0) {
		rg_hw_write_u8(g_hw_io, 0x00u);
		return -1;
	}

	if (procmgr_ability(0,
			    deny_lock | PROCMGR_AID_SPAWN,
			    deny_lock | PROCMGR_AID_FORK,
			    deny_lock | PROCMGR_AID_PATHSPACE,
			    deny_lock | PROCMGR_AID_IO,
			    deny_lock | PROCMGR_AID_MEM_PHYS,
			    deny_lock | PROCMGR_AID_CLOCKSET,
			    deny_lock | PROCMGR_AID_DEFAULT_TIMER_TOLERANCE,
			    PROCMGR_AID_EOL) != 0) {
		rg_hw_write_u8(g_hw_io, 0x00u);
		return -1;
	}

	errno = 0;
	if (ThreadCtl(_NTO_TCTL_IO_LEVEL, (void *)_NTO_IO_LEVEL_2) != -1 ||
	    errno != EPERM) {
		rg_hw_write_u8(g_hw_io, 0x00u);
		return -1;
	}

	return 0;
}

static int rg_io_devctl(resmgr_context_t *ctp, io_devctl_t *msg, RESMGR_OCB_T *ocb)
{
	int status;
	rg_ipc_req_t req;
	rg_ipc_rep_t rep;
	uint64_t now_ns;
	struct sigevent ev;
	uint64_t timeout_ns = RG_D2_TIMEOUT_NS;
	bool d2_timed_out = false;

	status = iofunc_devctl_default(ctp, msg, ocb);
	if (status != _RESMGR_DEFAULT)
		return status;
	if (msg->i.dcmd != DCMD_RG_EVALUATE)
		return ENOSYS;
	if (msg->i.nbytes < sizeof(req))
		return EINVAL;

	memcpy(&req, _DEVCTL_DATA(msg->i), sizeof(req));
	memset(&rep, 0, sizeof(rep));

	now_ns = rg_monotonic_ns();
	rep.verdict = rg_evaluate_gate(&g_eng, &req.cand, &req.adm, now_ns);

	if (rep.verdict.passage != RG_OPEN || !rep.verdict.actuator_enable) {
		rg_hw_write_u8(g_hw_io, 0x00u);
		rep.realization_status = RG_REAL_NONE;
	} else {
		SIGEV_UNBLOCK_INIT(&ev);
		(void)TimerTimeout(CLOCK_MONOTONIC,
				   _NTO_TIMEOUT_SEND | _NTO_TIMEOUT_REPLY,
				   &ev, &timeout_ns, NULL);

		d2_timed_out = (req.simulate_d2_timeout != 0u);
		if (d2_timed_out) {
			rg_hw_write_u8(g_hw_io, 0x00u);
			rep.realization_status = rg_realize_transition(
				&g_eng, &rep.verdict, true, true, false, false);
		} else {
			rg_hw_write_u8(g_hw_io, 0x01u);
			rep.realization_status = rg_realize_transition(
				&g_eng, &rep.verdict, true, false,
				req.simulate_d2_observed != 0u,
				req.simulate_d2_partial != 0u);
		}
	}

	rg_witness_append(&g_eng,
			  req.cand.id,
			  now_ns,
			  rep.verdict.passage,
			  rep.verdict.reason,
			  rep.verdict.passage == RG_OPEN ? RG_REAL_DISPATCHED : RG_REAL_NONE,
			  rep.realization_status,
			  (req.simulate_d2_observed != 0u && !d2_timed_out),
			  req.method_code,
			  &rep.witness);

	msg->o.ret_val = EOK;
	msg->o.nbytes  = sizeof(rep);
	memcpy(_DEVCTL_DATA(msg->o), &rep, sizeof(rep));
	MsgReply(ctp->rcvid, EOK, &msg->o, sizeof(msg->o) + sizeof(rep));

	printf("[rg_qnx_resmgr] seq=%llu | passage=0x%02X | real=%u | reason=%u | head=%02x%02x%02x%02x\n",
	       (unsigned long long)rep.witness.seq,
	       (unsigned int)rep.verdict.passage,
	       (unsigned int)rep.realization_status,
	       (unsigned int)rep.verdict.reason,
	       rep.witness.hash[0], rep.witness.hash[1],
	       rep.witness.hash[2], rep.witness.hash[3]);
	fflush(stdout);

	return _RESMGR_NOREPLY;
}

int main(void)
{
	int chid;
	dispatch_t *dpp;
	resmgr_attr_t rattr;
	resmgr_connect_funcs_t cfuncs;
	resmgr_io_funcs_t ifuncs;
	iofunc_attr_t attr;
	dispatch_context_t *ctp;

	rg_engine_init(&g_eng, rg_monotonic_ns());

	chid = ChannelCreate(_NTO_CHF_FIXED_PRIORITY | _NTO_CHF_DISCONNECT);
	if (chid == -1)
		return EXIT_FAILURE;

	dpp = dispatch_create_channel(chid, 0);
	if (!dpp)
		return EXIT_FAILURE;

	memset(&rattr, 0, sizeof(rattr));
	rattr.nparts_max   = 1;
	rattr.msg_max_size = 2048;

	iofunc_func_init(_RESMGR_CONNECT_NFUNCS, &cfuncs, _RESMGR_IO_NFUNCS, &ifuncs);
	ifuncs.devctl = rg_io_devctl;
	iofunc_attr_init(&attr, S_IFNAM | 0660, 0, 0);

	if (resmgr_attach(dpp, &rattr, RG_DEV_PATH, _FTYPE_ANY, 0,
			  &cfuncs, &ifuncs, &attr) == -1)
		return EXIT_FAILURE;

	if (rg_sandbox_and_clamp_boot() != 0)
		return EXIT_FAILURE;

	ctp = dispatch_context_alloc(dpp);
	if (!ctp) {
		rg_hw_write_u8(g_hw_io, 0x00u);
		return EXIT_FAILURE;
	}

	while (1) {
		ctp = dispatch_block(ctp);
		if (!ctp) {
			rg_hw_write_u8(g_hw_io, 0x00u);
			break;
		}
		dispatch_handler(ctp);
	}

	return EXIT_SUCCESS;
}
