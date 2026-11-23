#include <stdio.h>
#include <string.h>
#include "rg_grammar.h"

static int pass_cnt = 0;
static int fail_cnt = 0;

static void check(const char *name, bool cond)
{
	if (cond) {
		printf("[PASS] %s\n", name);
		pass_cnt++;
	} else {
		printf("[FAIL] %s\n", name);
		fail_cnt++;
	}
}

static rg_candidate_t make_d12_candidate(uint64_t id)
{
	rg_candidate_t c = { .id = id, .payload = 42, .version = 1u, .origin = 1u, .phase = RG_PHASE_D0_RAW };
	(void)rg_advance_phase(&c, RG_PHASE_D1_REVERSIBLE);
	(void)rg_advance_phase(&c, RG_PHASE_D1_2_STRUCT);
	return c;
}

static rg_admissibility_in_t make_valid_adm(void)
{
	rg_admissibility_in_t a;
	memset(&a, 0, sizeof(a));
	a.a_struct                   = true;
	a.a_epist                    = true;
	a.a_oper                     = true;
	a.a_auth                     = true;
	a.observed_val               = 100;
	a.target_val                 = 100;
	a.epsilon                    = 0u;
	a.tolerance_contract_enabled = false;
	return a;
}

int main(void)
{
	rg_engine_t eng;
	rg_candidate_t cand;
	rg_admissibility_in_t adm;
	rg_gate_verdict_t v;
	rg_witness_record_t w1, w2;

	rg_engine_init(&eng, 1000u);
	cand = (rg_candidate_t){ .id = 1u, .payload = 7, .version = 1u, .origin = 1u, .phase = RG_PHASE_D0_RAW };
	bool s1 = !rg_advance_phase(&cand, RG_PHASE_D1_2_STRUCT);
	bool s2 = !rg_advance_phase(&cand, RG_PHASE_D2_COMMIT);
	adm = make_valid_adm();
	v = rg_evaluate_gate(&eng, &cand, &adm, 1010u);
	check("T01 Forbudte snarveier (D0->D1.2 / D0->D2) laaser KILL",
	      s1 && s2 && v.passage == RG_KILL && v.reason == RG_REASON_SHORTCUT_FORBIDDEN && !v.transition_authorized);

	rg_engine_init(&eng, 1000u);
	cand = make_d12_candidate(2u);
	adm = make_valid_adm();
	adm.a_auth = false;
	v = rg_evaluate_gate(&eng, &cand, &adm, 1020u);
	check("T02 Invariant III: A_valid uten autorisasjon -> HOLD",
	      v.passage == RG_HOLD && v.reason == RG_REASON_NOT_AUTHORIZED && !v.transition_authorized);

	rg_engine_init(&eng, 1000u);
	cand = make_d12_candidate(3u);
	adm = make_valid_adm();
	adm.a_epist              = false;
	adm.hard_boundary_breach = true;
	v = rg_evaluate_gate(&eng, &cand, &adm, 1030u);
	check("T03 Prioritet KILL > HOLD: HOLD skjolder aldri brutt hard grense",
	      v.passage == RG_KILL && v.reason == RG_REASON_HARD_BREACH && !v.actuator_enable);

	rg_engine_init(&eng, 1000u);
	cand = make_d12_candidate(4u);
	adm = make_valid_adm();
	adm.candidate_rejected = true;
	v = rg_evaluate_gate(&eng, &cand, &adm, 1040u);
	bool rej_hold = (v.passage == RG_HOLD && v.reason == RG_REASON_CANDIDATE_REJECTED);
	adm.candidate_rejected = false;
	v = rg_evaluate_gate(&eng, &cand, &adm, 1050u);
	check("T04 REJECT forblir i HOLD (ikke klebrig KILL)",
	      rej_hold && v.passage == RG_OPEN && v.transition_authorized);

	rg_engine_init(&eng, 1000u);
	cand = make_d12_candidate(5u);
	adm = make_valid_adm();
	adm.observed_val               = 103;
	adm.target_val                 = 100;
	adm.epsilon                    = 5u;
	adm.tolerance_contract_enabled = false;
	v = rg_evaluate_gate(&eng, &cand, &adm, 1060u);
	bool tol_off = (v.passage == RG_HOLD && v.match_outcome == RG_UNRESOLVED && !v.split_granted);

	adm.tolerance_contract_enabled = true;
	v = rg_evaluate_gate(&eng, &cand, &adm, 1070u);
	bool tol_on = (v.passage == RG_OPEN && v.match_outcome == RG_WITHIN_TOLERANCE && !v.split_granted);

	adm.split_requested     = true;
	adm.split_authorized    = true;
	adm.split_admissible    = true;
	adm.structure_preserved = false;
	v = rg_evaluate_gate(&eng, &cand, &adm, 1080u);
	bool split_deny = (v.passage == RG_HOLD && v.reason == RG_REASON_UNVALIDATED_SPLIT && !v.split_granted);
	check("T05 Invariant X & XI: Toleranse-kontrakt og FAIL_EQUALITY !=> SPLIT",
	      tol_off && tol_on && split_deny);

	rg_engine_init(&eng, 1000u);
	cand = make_d12_candidate(6u);
	adm = make_valid_adm();
	v = rg_evaluate_gate(&eng, &cand, &adm, 1090u);
	rg_realization_status_t r_intent = rg_realize_transition(&eng, &v, false, false, false, false);
	rg_realization_status_t r_disp   = rg_realize_transition(&eng, &v, true,  false, false, false);
	check("T06 Invariant IV: OPEN -> INTENT_RECORDED -> DISPATCHED (!=> OBSERVED)",
	      v.passage == RG_OPEN && r_intent == RG_REAL_INTENT_RECORDED && r_disp == RG_REAL_DISPATCHED);

	rg_realization_status_t r_to = rg_realize_transition(&eng, &v, true, true, false, false);
	check("T07 Invariant IX: TIMEOUT -> CONSEQUENCE_UNCERTAIN -> HOLD (UNKNOWN != ZERO)",
	      r_to == RG_REAL_CONSEQUENCE_UNCERTAIN && eng.latched_state == RG_HOLD);

	rg_engine_init(&eng, 1000u);
	cand = make_d12_candidate(8u);
	adm = make_valid_adm();
	v = rg_evaluate_gate(&eng, &cand, &adm, 1100u);
	rg_witness_append(&eng, cand.id, 1100u, v.passage, v.reason,
			  RG_REAL_DISPATCHED, RG_REAL_OBSERVED_COMPLETE, false, 1u, &w1);
	bool claim_vs_obs = (w1.claim_status == RG_REAL_DISPATCHED &&
			     w1.observed_status == RG_REAL_NONE &&
			     !w1.has_physical_observation);

	adm.hard_boundary_breach = true;
	v = rg_evaluate_gate(&eng, &cand, &adm, 1110u);
	rg_witness_append(&eng, cand.id, 1110u, RG_OPEN, RG_REASON_AUTHORIZED_OPEN,
			  RG_REAL_OBSERVED_COMPLETE, RG_REAL_OBSERVED_COMPLETE, true, 2u, &w2);
	bool chained = (memcmp(w2.prev_hash, w1.hash, 32u) == 0 &&
			memcmp(w2.hash, w1.hash, 32u) != 0 &&
			eng.latched_state == RG_KILL);
	check("T08 Invariant VI-VIII: Passivt SHA-256-vitne (W_claim != W_obs, kjedet, 0 makt)",
	      claim_vs_obs && chained);

	printf("RESULTAT: %d PASS / %d FAIL\n", pass_cnt, fail_cnt);
	return fail_cnt == 0 ? 0 : 1;
}
