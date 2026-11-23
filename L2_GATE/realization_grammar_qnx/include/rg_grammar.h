#ifndef RG_GRAMMAR_H
#define RG_GRAMMAR_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

/*
 * REALISERINGSGRAMMATIKK v1.0 — Flyttallsfri C11-kontrakt (0 float)
 *
 *   GENERATE != VALIDATE != AUTHORIZE != REALIZE != WITNESS
 *   OPEN releases. HOLD preserves. KILL protects. (KILL > HOLD > OPEN)
 */

typedef enum {
	RG_PHASE_D0_RAW        = 0u,
	RG_PHASE_D1_REVERSIBLE = 1u,
	RG_PHASE_D1_2_STRUCT   = 2u,
	RG_PHASE_D1_5_GATE     = 3u,
	RG_PHASE_D2_COMMIT     = 4u,
	RG_PHASE_D3_WITNESS    = 5u
} rg_phase_t;

typedef enum {
	RG_KILL = 0x00u, /* Fail-closed vern / klebrig laas */
	RG_HOLD = 0x3Cu, /* Bevarer kandidat ved 0.00 V DC  */
	RG_OPEN = 0xA5u  /* Frigir overgangsautoritet       */
} rg_passage_t;

typedef enum {
	RG_MATCH            = 1u,
	RG_WITHIN_TOLERANCE = 2u,
	RG_UNRESOLVED       = 3u
} rg_match_outcome_t;

typedef enum {
	RG_REAL_NONE                  = 0u,
	RG_REAL_INTENT_RECORDED       = 1u,
	RG_REAL_DISPATCHED            = 2u,
	RG_REAL_OBSERVED_COMPLETE     = 3u,
	RG_REAL_OBSERVED_PARTIAL      = 4u,
	RG_REAL_CONSEQUENCE_UNCERTAIN = 5u
} rg_realization_status_t;

typedef enum {
	RG_REASON_NONE                = 0u,
	RG_REASON_AUTHORIZED_OPEN     = 1u,
	RG_REASON_SHORTCUT_FORBIDDEN  = 2u,
	RG_REASON_HARD_BREACH         = 3u,
	RG_REASON_CLOCK_REGRESSION    = 4u,
	RG_REASON_KILL_LATCHED        = 5u,
	RG_REASON_CANDIDATE_REJECTED  = 6u,
	RG_REASON_UNRESOLVED_EVIDENCE = 7u,
	RG_REASON_UNVALIDATED_SPLIT   = 8u,
	RG_REASON_NOT_AUTHORIZED      = 9u,
	RG_REASON_TIMEOUT_UNCERTAIN   = 10u
} rg_reason_t;

typedef struct {
	uint64_t   id;
	int64_t    payload;
	uint32_t   version;
	uint32_t   origin;
	rg_phase_t phase;
} rg_candidate_t;

typedef struct {
	bool     a_struct;
	bool     a_epist;
	bool     a_oper;
	bool     a_auth;
	bool     hard_boundary_breach;
	bool     candidate_rejected;

	int64_t  observed_val;
	int64_t  target_val;
	uint64_t epsilon;
	bool     tolerance_contract_enabled;

	bool     split_requested;
	bool     split_authorized;
	bool     split_admissible;
	bool     structure_preserved;
} rg_admissibility_in_t;

typedef struct {
	rg_passage_t       passage;
	rg_match_outcome_t match_outcome;
	rg_reason_t        reason;
	bool               transition_authorized;
	bool               split_granted;
	bool               actuator_enable;
} rg_gate_verdict_t;

typedef struct {
	uint64_t                seq;
	uint64_t                candidate_id;
	uint64_t                monotonic_ns;
	rg_passage_t            passage;
	rg_reason_t             reason;
	rg_realization_status_t claim_status;
	rg_realization_status_t observed_status;
	bool                    has_physical_observation;
	uint32_t                method_code;
	uint8_t                 prev_hash[32];
	uint8_t                 hash[32];
} rg_witness_record_t;

typedef struct {
	rg_passage_t            latched_state;
	uint64_t                last_monotonic_ns;
	uint64_t                witness_seq;
	uint8_t                 witness_head[32];
	rg_realization_status_t last_realization_status;
} rg_engine_t;

void rg_engine_init(rg_engine_t *eng, uint64_t now_ns);
bool rg_advance_phase(rg_candidate_t *cand, rg_phase_t next_phase);
rg_match_outcome_t rg_eval_match(int64_t observed, int64_t target,
				 uint64_t epsilon, bool tolerance_enabled);
bool rg_eval_split(const rg_admissibility_in_t *in);
rg_gate_verdict_t rg_evaluate_gate(rg_engine_t *eng,
				   const rg_candidate_t *cand,
				   const rg_admissibility_in_t *adm,
				   uint64_t now_ns);
rg_realization_status_t rg_realize_transition(rg_engine_t *eng,
					      const rg_gate_verdict_t *verdict,
					      bool dispatched_ok,
					      bool timed_out,
					      bool observation_received,
					      bool partial_effect);
void rg_witness_append(rg_engine_t *eng,
		       uint64_t candidate_id,
		       uint64_t now_ns,
		       rg_passage_t passage,
		       rg_reason_t reason,
		       rg_realization_status_t claim_status,
		       rg_realization_status_t observed_status,
		       bool has_physical_observation,
		       uint32_t method_code,
		       rg_witness_record_t *out_rec);
void rg_sha256(const uint8_t *data, size_t len, uint8_t out_hash[32]);

#endif /* RG_GRAMMAR_H */
