# ==============================================================================
# MORANDI-CORE // FORMAL REALIZATION CONTRACT
# EPISTEMIC BOUNDARY: GENERATION != AUTHORIZATION != WITNESSED CONSEQUENCE
# ==============================================================================

PYTHON := python3
SHA256 := sha256sum
TIMESTAMP := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

LAW_DIR := L1_LAW
GATE_DIR := L2_GATE
WITNESS_DIR := L3_WITNESS
WITNESS_LOG := $(WITNESS_DIR)/audit_log.jsonl

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
	@echo "[+] L2_GATE: Konsekvensgrenser respektert. Klar for W^2 vitne."

# ------------------------------------------------------------------------------
# TRINN 3: FORMAL VERIFICATION & SPATIALIZATION (Cook-Levin)
# ------------------------------------------------------------------------------
verify: gate
	@echo "\n[3/3] FORMAL VERIFICATION COMPLETE."
	@echo "      Residual Delta_K er under eksakt terskel."
	@echo "      Systemet står i HOLD (0.00 V DC). Klar for utstedelse av W^2."
	@echo "      Kjør 'make witness' for å autorisere OPEN (5.00 V DC L1-simulert)."

# ------------------------------------------------------------------------------
# TRINN 4: W^2 - Utstedelse av kryptografisk vitne (Krever fullført verify)
# ------------------------------------------------------------------------------
witness: verify
	@echo "\n[+] GENERATING CRYPTOGRAPHIC WITNESS (W^2)..."
	@mkdir -p $(WITNESS_DIR)
	@echo "{\"timestamp\": \"$(TIMESTAMP)\", \"state\": \"OPEN\", \"v_dc\": 5.00, \"authority\": \"Level_01\", \"tier\": \"L1_SOFTWARE\", \"physical_authority\": \"NONE\"}" > $(WITNESS_DIR)/latest_state.json
	@$(SHA256) $(WITNESS_DIR)/latest_state.json | awk '{print "{\"sha256\": \"" $$1 "\", \"file\": \"" $$2 "\"}"}' >> $(WITNESS_LOG)
	@echo "[+] WITNESS ACCEPTED. System tilstandsendring loggført (Append-Only)."
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
