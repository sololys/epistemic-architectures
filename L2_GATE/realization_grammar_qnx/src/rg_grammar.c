#include "rg_grammar.h"
#include <string.h>

static const uint32_t K256[64] = {
	0x428a2f98u, 0x71374491u, 0xb5c0fbcfu, 0xe9b5dba5u,
	0x3956c25bu, 0x59f111f1u, 0x923f82a4u, 0xab1c5ed5u,
	0xd807aa98u, 0x12835b01u, 0x243185beu, 0x550c7dc3u,
	0x72be5d74u, 0x80deb1feu, 0x9bdc06a7u, 0xc19bf174u,
	0xe49b69c1u, 0xefbe4786u, 0x0fc19dc6u, 0x240ca1ccu,
	0x2de92c6fu, 0x4a7484aau, 0x5cb0a9dcu, 0x76f988dau,
	0x983e5152u, 0xa831c66du, 0xb00327c8u, 0xbf597fc7u,
	0xc6e00bf3u, 0xd5a79147u, 0x06ca6351u, 0x14292967u,
	0x27b70a85u, 0x2e1b2138u, 0x4d2c6dfcu, 0x53380d13u,
	0x650a7354u, 0x766a0abbu, 0x81c2c92eu, 0x92722c85u,
	0xa2bfe8a1u, 0xa81a664bu, 0xc24b8b70u, 0xc76c51a3u,
	0xd192e819u, 0xd6990624u, 0xf40e3585u, 0x106aa070u,
	0x19a4c116u, 0x1e376c08u, 0x2748774cu, 0x34b0bcb5u,
	0x391c0cb3u, 0x4ed8aa4au, 0x5b9cca4fu, 0x682e6ff3u,
	0x748f82eeu, 0x78a5636fu, 0x84c87814u, 0x8cc70208u,
	0x90befffau, 0xa4506cebu, 0xbef9a3f7u, 0xc67178f2u
};

static inline uint32_t rotr32(uint32_t x, unsigned int n)
{
	return (x >> n) | (x << (32u - n));
}

static void sha256_transform(uint32_t st[8], const uint8_t blk[64])
{
	uint32_t w[64];
	uint32_t a, b, c, d, e, f, g, h;
	unsigned int i;

	for (i = 0u; i < 16u; i++) {
		w[i] = ((uint32_t)blk[i * 4u] << 24) |
		       ((uint32_t)blk[i * 4u + 1u] << 16) |
		       ((uint32_t)blk[i * 4u + 2u] << 8) |
		       ((uint32_t)blk[i * 4u + 3u]);
	}
	for (i = 16u; i < 64u; i++) {
		uint32_t s0 = rotr32(w[i - 15u], 7u) ^ rotr32(w[i - 15u], 18u) ^ (w[i - 15u] >> 3);
		uint32_t s1 = rotr32(w[i - 2u], 17u) ^ rotr32(w[i - 2u], 19u) ^ (w[i - 2u] >> 10);
		w[i] = w[i - 16u] + s0 + w[i - 7u] + s1;
	}

	a = st[0]; b = st[1]; c = st[2]; d = st[3];
	e = st[4]; f = st[5]; g = st[6]; h = st[7];

	for (i = 0u; i < 64u; i++) {
		uint32_t S1  = rotr32(e, 6u) ^ rotr32(e, 11u) ^ rotr32(e, 25u);
		uint32_t ch  = (e & f) ^ ((~e) & g);
		uint32_t t1  = h + S1 + ch + K256[i] + w[i];
		uint32_t S0  = rotr32(a, 2u) ^ rotr32(a, 13u) ^ rotr32(a, 22u);
		uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
		uint32_t t2  = S0 + maj;

		h = g; g = f; f = e; e = d + t1;
		d = c; c = b; b = a; a = t1 + t2;
	}

	st[0] += a; st[1] += b; st[2] += c; st[3] += d;
	st[4] += e; st[5] += f; st[6] += g; st[7] += h;
}

void rg_sha256(const uint8_t *data, size_t len, uint8_t out_hash[32])
{
	uint32_t st[8] = {
		0x6a09e667u, 0xbb67ae85u, 0x3c6ef372u, 0xa54ff53au,
		0x510e527fu, 0x9b05688cu, 0x1f83d9abu, 0x5be0cd19u
	};
	uint8_t blk[64];
	size_t off = 0u;
	size_t rem;
	uint64_t bitlen = (uint64_t)len * 8u;
	unsigned int i;

	while (off + 64u <= len) {
		sha256_transform(st, data + off);
		off += 64u;
	}
	rem = len - off;
	memset(blk, 0, sizeof(blk));
	if (rem > 0u)
		memcpy(blk, data + off, rem);
	blk[rem] = 0x80u;
	if (rem >= 56u) {
		sha256_transform(st, blk);
		memset(blk, 0, sizeof(blk));
	}
	for (i = 0u; i < 8u; i++)
		blk[56u + i] = (uint8_t)((bitlen >> (56u - 8u * i)) & 0xFFu);
	sha256_transform(st, blk);

	for (i = 0u; i < 8u; i++) {
		out_hash[i * 4u]      = (uint8_t)((st[i] >> 24) & 0xFFu);
		out_hash[i * 4u + 1u] = (uint8_t)((st[i] >> 16) & 0xFFu);
		out_hash[i * 4u + 2u] = (uint8_t)((st[i] >> 8) & 0xFFu);
		out_hash[i * 4u + 3u] = (uint8_t)(st[i] & 0xFFu);
	}
}

static uint64_t abs_diff_i64(int64_t a, int64_t b)
{
	if (a >= b)
		return (uint64_t)a - (uint64_t)b;
	return (uint64_t)b - (uint64_t)a;
}

void rg_engine_init(rg_engine_t *eng, uint64_t now_ns)
{
	if (!eng)
		return;
	eng->latched_state           = RG_HOLD;
	eng->last_monotonic_ns       = now_ns;
	eng->witness_seq             = 0u;
	eng->last_realization_status = RG_REAL_NONE;
	memset(eng->witness_head, 0, sizeof(eng->witness_head));
}

bool rg_advance_phase(rg_candidate_t *cand, rg_phase_t next_phase)
{
	if (!cand)
		return false;
	if ((unsigned int)next_phase != (unsigned int)cand->phase + 1u)
		return false;
	cand->phase = next_phase;
	return true;
}

rg_match_outcome_t rg_eval_match(int64_t observed, int64_t target,
				 uint64_t epsilon, bool tolerance_enabled)
{
	uint64_t delta;

	if (observed == target)
		return RG_MATCH;
	if (!tolerance_enabled)
		return RG_UNRESOLVED;
	delta = abs_diff_i64(observed, target);
	if (delta <= epsilon)
		return RG_WITHIN_TOLERANCE;
	return RG_UNRESOLVED;
}

bool rg_eval_split(const rg_admissibility_in_t *in)
{
	if (!in || !in->split_requested)
		return false;
	return in->split_authorized && in->split_admissible && in->structure_preserved;
}

rg_gate_verdict_t rg_evaluate_gate(rg_engine_t *eng,
				   const rg_candidate_t *cand,
				   const rg_admissibility_in_t *adm,
				   uint64_t now_ns)
{
	rg_gate_verdict_t v;

	memset(&v, 0, sizeof(v));
	v.passage       = RG_KILL;
	v.match_outcome = RG_UNRESOLVED;

	if (!eng || !cand || !adm) {
		v.reason = RG_REASON_HARD_BREACH;
		return v;
	}
	if (eng->latched_state == RG_KILL) {
		v.passage = RG_KILL;
		v.reason  = RG_REASON_KILL_LATCHED;
		return v;
	}
	if (now_ns < eng->last_monotonic_ns) {
		eng->latched_state = RG_KILL;
		v.passage          = RG_KILL;
		v.reason           = RG_REASON_CLOCK_REGRESSION;
		return v;
	}
	eng->last_monotonic_ns = now_ns;

	if (cand->phase != RG_PHASE_D1_2_STRUCT) {
		eng->latched_state = RG_KILL;
		v.passage          = RG_KILL;
		v.reason           = RG_REASON_SHORTCUT_FORBIDDEN;
		return v;
	}
	if (adm->hard_boundary_breach) {
		eng->latched_state = RG_KILL;
		v.passage          = RG_KILL;
		v.reason           = RG_REASON_HARD_BREACH;
		return v;
	}
	if (adm->candidate_rejected) {
		eng->latched_state = RG_HOLD;
		v.passage          = RG_HOLD;
		v.reason           = RG_REASON_CANDIDATE_REJECTED;
		return v;
	}

	v.match_outcome = rg_eval_match(adm->observed_val, adm->target_val,
					adm->epsilon, adm->tolerance_contract_enabled);
	if (adm->split_requested) {
		v.split_granted = rg_eval_split(adm);
		if (!v.split_granted) {
			eng->latched_state = RG_HOLD;
			v.passage          = RG_HOLD;
			v.reason           = RG_REASON_UNVALIDATED_SPLIT;
			return v;
		}
	}
	if (v.match_outcome == RG_UNRESOLVED) {
		eng->latched_state = RG_HOLD;
		v.passage          = RG_HOLD;
		v.reason           = RG_REASON_UNRESOLVED_EVIDENCE;
		return v;
	}
	if (!adm->a_struct || !adm->a_epist || !adm->a_oper) {
		eng->latched_state = RG_HOLD;
		v.passage          = RG_HOLD;
		v.reason           = RG_REASON_UNRESOLVED_EVIDENCE;
		return v;
	}
	if (!adm->a_auth) {
		eng->latched_state = RG_HOLD;
		v.passage          = RG_HOLD;
		v.reason           = RG_REASON_NOT_AUTHORIZED;
		return v;
	}

	eng->latched_state      = RG_OPEN;
	v.passage               = RG_OPEN;
	v.reason                = RG_REASON_AUTHORIZED_OPEN;
	v.transition_authorized = true;
	v.actuator_enable       = true;
	return v;
}

rg_realization_status_t rg_realize_transition(rg_engine_t *eng,
					      const rg_gate_verdict_t *verdict,
					      bool dispatched_ok,
					      bool timed_out,
					      bool observation_received,
					      bool partial_effect)
{
	if (!eng || !verdict)
		return RG_REAL_NONE;
	if (verdict->passage != RG_OPEN || !verdict->transition_authorized) {
		eng->last_realization_status = RG_REAL_NONE;
		return RG_REAL_NONE;
	}
	if (!dispatched_ok) {
		eng->last_realization_status = RG_REAL_INTENT_RECORDED;
		return RG_REAL_INTENT_RECORDED;
	}
	if (timed_out) {
		eng->latched_state           = RG_HOLD;
		eng->last_realization_status = RG_REAL_CONSEQUENCE_UNCERTAIN;
		return RG_REAL_CONSEQUENCE_UNCERTAIN;
	}
	if (!observation_received) {
		eng->last_realization_status = RG_REAL_DISPATCHED;
		return RG_REAL_DISPATCHED;
	}
	if (partial_effect) {
		eng->last_realization_status = RG_REAL_OBSERVED_PARTIAL;
		return RG_REAL_OBSERVED_PARTIAL;
	}
	eng->last_realization_status = RG_REAL_OBSERVED_COMPLETE;
	return RG_REAL_OBSERVED_COMPLETE;
}

static void put_be64(uint8_t *p, uint64_t v)
{
	unsigned int i;
	for (i = 0u; i < 8u; i++)
		p[i] = (uint8_t)((v >> (56u - 8u * i)) & 0xFFu);
}

static void put_be32(uint8_t *p, uint32_t v)
{
	p[0] = (uint8_t)((v >> 24) & 0xFFu);
	p[1] = (uint8_t)((v >> 16) & 0xFFu);
	p[2] = (uint8_t)((v >> 8) & 0xFFu);
	p[3] = (uint8_t)(v & 0xFFu);
}

void rg_witness_append(rg_engine_t *eng,
		       uint64_t candidate_id,
		       uint64_t now_ns,
		       rg_passage_t passage,
		       rg_reason_t reason,
		       rg_realization_status_t claim_status,
		       rg_realization_status_t observed_status,
		       bool has_physical_observation,
		       uint32_t method_code,
		       rg_witness_record_t *out_rec)
{
	uint8_t buf[68];
	uint8_t digest[32];

	if (!eng)
		return;

	eng->witness_seq += 1u;

	memcpy(buf, eng->witness_head, 32u);
	put_be64(buf + 32, eng->witness_seq);
	put_be64(buf + 40, candidate_id);
	put_be64(buf + 48, now_ns);
	buf[56] = (uint8_t)passage;
	buf[57] = (uint8_t)reason;
	buf[58] = (uint8_t)claim_status;
	buf[59] = (uint8_t)(has_physical_observation ? observed_status : RG_REAL_NONE);
	buf[60] = (uint8_t)(has_physical_observation ? 1u : 0u);
	buf[61] = 0u;
	buf[62] = 0u;
	buf[63] = 0u;
	put_be32(buf + 64, method_code);

	rg_sha256(buf, sizeof(buf), digest);

	if (out_rec) {
		out_rec->seq                      = eng->witness_seq;
		out_rec->candidate_id             = candidate_id;
		out_rec->monotonic_ns             = now_ns;
		out_rec->passage                  = passage;
		out_rec->reason                   = reason;
		out_rec->claim_status             = claim_status;
		out_rec->observed_status          = has_physical_observation ? observed_status : RG_REAL_NONE;
		out_rec->has_physical_observation = has_physical_observation;
		out_rec->method_code              = method_code;
		memcpy(out_rec->prev_hash, eng->witness_head, 32u);
		memcpy(out_rec->hash, digest, 32u);
	}

	memcpy(eng->witness_head, digest, 32u);
}
