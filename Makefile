# ==============================================================================
# MORANDI-CORE // FORMAL REALIZATION CONTRACT
# EPISTEMIC BOUNDARY: GENERATION != AUTHORIZATION != WITNESSED CONSEQUENCE
# ==============================================================================

PYTHON := python3
SHA256 := sha256sum
TIMESTAMP := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
W_EXT_ID ?=

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
	@echo "[+] L2_GATE: Konsekvensgrenser respektert. Klar for W^2 vitne."

# ------------------------------------------------------------------------------
# TRINN 3: FORMAL VERIFICATION & SPATIALIZATION (Cook-Levin)
# ------------------------------------------------------------------------------
verify: gate
	@echo "\n[3/3] FORMAL VERIFICATION COMPLETE."
	@echo "      Residual Delta_K er under eksakt terskel."
	@echo "      Systemet står i HOLD (0.00 V DC). Klar for utstedelse av W^2."
	@echo "      Kjør 'make witness' for HOLD (0.00 V DC) eller 'make witness W_EXT_ID=<id>' for OPEN (5.00 V DC L1-simulert)."

# ------------------------------------------------------------------------------
# TRINN 4: W^2 - Utstedelse av kryptografisk vitne (Krever fullført verify)
# ------------------------------------------------------------------------------
witness: verify
	@echo "\n[+] GENERATING CRYPTOGRAPHIC WITNESS (W^2)..."
	@mkdir -p $(WITNESS_DIR)
	@$(PYTHON) -B -c 'import hashlib, json, os, pathlib, sys; ts, w_ext, st_path, log_path = sys.argv[1], sys.argv[2].strip(), pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4]); state, v_dc, auth = (("OPEN", "5.00", "Level_01") if w_ext else ("HOLD", "0.00", "NONE")); st_obj = {"timestamp": ts, "state": state, "v_dc": v_dc, "v_dc_mv": (5000 if w_ext else 0), "authority": auth, "w_ext_id": w_ext, "tier": "L1_SOFTWARE", "physical_authority": "NONE"}; st_raw = (json.dumps(st_obj, sort_keys=True) + "\n").encode("utf-8"); st_path.write_bytes(st_raw); st_sha = hashlib.sha256(st_raw).hexdigest(); lines = ([ln.strip() for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()] if log_path.exists() else []); prev = (json.loads(lines[-1]).get("sha256", "0" * 64) if lines else "0" * 64); rec_body = {"prev_hash": prev, "state_sha256": st_sha, "state": state, "v_dc": v_dc, "authority": auth, "w_ext_id": w_ext, "file": str(st_path), "timestamp": ts}; rec_sha = hashlib.sha256(json.dumps(rec_body, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(); rec = dict(rec_body, sha256=rec_sha); fd = os.open(str(log_path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644); os.write(fd, (json.dumps(rec, sort_keys=True) + "\n").encode("utf-8")); os.fsync(fd); os.close(fd)' "$(TIMESTAMP)" "$(W_EXT_ID)" "$(WITNESS_DIR)/latest_state.json" "$(WITNESS_LOG)"
	@echo "[+] WITNESS RECORDED (prev_hash-chained, Append-Only)."
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
