# ==============================================================================
# MORANDI-CORE // FORMAL REALIZATION CONTRACT
# EPISTEMIC BOUNDARY: GENERATION != AUTHORIZATION != WITNESSED CONSEQUENCE
# ==============================================================================

PYTHON := python3
SHA256 := sha256sum
TIMESTAMP := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
W_EXT_ID ?=
W_EXT_ATTEST_FILE ?=

LAW_DIR := L1_LAW
GATE_DIR := L2_GATE
WITNESS_DIR := L3_WITNESS
WITNESS_LOG ?= $(WITNESS_DIR)/audit_log.jsonl

.PHONY: all law gate verify witness kill clean

# Standardtilstand er absolutt stillhet.
# Avviser implisitt generering uten eksplisitt autorisasjon.
all:
	@echo "[!] FATAL: Implicit execution is a violation of the Sovereignty Invariant."
	@echo "    Requires explicit target: make verify"
	@exit 1

# ------------------------------------------------------------------------------
# TRINN 1: L1_LAW - Matematisk og logisk fundament (Ingen I/O)
# ------------------------------------------------------------------------------
law:
	@echo "\n[1/3] EXECUTING L1_LAW (PURE FUNCTIONS)..."
	@$(PYTHON) -m unittest discover -s $(LAW_DIR) -p "*_pure.py" || ($(MAKE) kill && exit 1)
	@echo "[+] L1_LAW: Deterministisk utfall verifisert."

# ------------------------------------------------------------------------------
# TRINN 2: L2_GATE - Tilstandsevaluering og Projeksjon (Pi_K)
# ------------------------------------------------------------------------------
gate: law
	@echo "\n[2/3] EVALUATING L2_GATE (PROJECTION Pi_K)..."
	@$(PYTHON) $(GATE_DIR)/evaluate_boundaries.py || ($(MAKE) kill && exit 1)
	@$(PYTHON) $(GATE_DIR)/verify_ky_nash_and_dual_clock_gate.py || ($(MAKE) kill && exit 1)
	@$(PYTHON) $(GATE_DIR)/verify_two_track_prose_gate_x01_x12.py || ($(MAKE) kill && exit 1)
	@$(PYTHON) $(GATE_DIR)/verify_sosionomos_xor_rox_gate.py || ($(MAKE) kill && exit 1)
	@$(PYTHON) $(GATE_DIR)/verify_w2_five_proof_chains.py >/dev/null || ($(MAKE) kill && exit 1)
	@$(PYTHON) -m unittest $(GATE_DIR)/test_record_witness.py >/dev/null || ($(MAKE) kill && exit 1)
	@echo "[+] L2_GATE: Konsekvensgrenser respektert. Klar for W^2 vitne."

# ------------------------------------------------------------------------------
# TRINN 3: FORMAL VERIFICATION & SPATIALIZATION (Cook-Levin)
# ------------------------------------------------------------------------------
verify: gate
	@echo "\n[3/3] FORMAL VERIFICATION COMPLETE."
	@echo "      Residual Delta_K er under eksakt terskel."
	@echo "      Systemet står i HOLD (0.00 V DC). Klar for utstedelse av W^2."
	@echo "      Kjør 'make witness' for HOLD (0.00 V DC) eller 'make witness W_EXT_ID=<id> W_EXT_ATTEST_FILE=<json>' for OPEN (5.00 V DC L1-simulert)."

# ------------------------------------------------------------------------------
# TRINN 4: W^2 - Utstedelse av kryptografisk vitne (Krever fullført verify)
# ------------------------------------------------------------------------------
witness: verify
	@echo "\n[+] GENERATING CRYPTOGRAPHIC WITNESS (W^2)..."
	@mkdir -p $(WITNESS_DIR)
	@$(PYTHON) -B $(GATE_DIR)/record_witness.py --timestamp "$(TIMESTAMP)" --w-ext-id "$(W_EXT_ID)" --attest-file "$(W_EXT_ATTEST_FILE)" --state-out "$(WITNESS_DIR)/latest_state.json" --log-out "$(WITNESS_LOG)" || ($(MAKE) kill && exit 1)
	@echo "[+] WITNESS RECORDED (LOCK_EX + fsync prev_hash-chained, Append-Only)."
	@cat $(WITNESS_DIR)/latest_state.json

# ------------------------------------------------------------------------------
# JORDING OG AVSKJÆRING
# ------------------------------------------------------------------------------
kill:
	@echo "\n[!] INITIATING FAIL-CLOSED ISOLATION..."
	@echo "[!] SYSTEM FORCED TO KILL STATE (0.00 V DC)."
	@exit 1

clean:
	@echo "\n[-] RENSER ARTIFAKTER (Gjenoppretter passiv tilstand)..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -f $(WITNESS_DIR)/latest_state.json
	@echo "[-] Huset er stramt."
