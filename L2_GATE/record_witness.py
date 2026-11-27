#!/usr/bin/env python3
"""
L2_GATE // Fail-Closed W^2 Witness Recorder & Exclusive POSIX WAL Appender (0 Float)
====================================================================================
Enforces:
1. Gate evaluation must explicitly report HOLD_READY_FOR_W2 before simulated OPEN.
2. A bare W_EXT_ID string never authorizes OPEN; a verified pre-commit attestation
   binding (w_ext_id, candidate_sha256, gate_sha256, prev_hash) is mandatory.
3. Exclusive file lock (fcntl.flock LOCK_EX) wraps the entire tail-read, chain
   verification, hash computation, append, fsync, and state-snapshot update.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Callable, Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from L2_GATE.evaluate_boundaries import evaluate_gate

HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
W_EXT_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")


def canonical_sha256(payload: Dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_precommit_attestation(
    w_ext_id: str,
    candidate_sha256: str,
    gate_sha256: str,
    prev_hash: str,
) -> Dict[str, str]:
    w_clean = w_ext_id.strip()
    if not W_EXT_ID_RE.fullmatch(w_clean):
        raise ValueError("Invalid w_ext_id format.")
    for label, digest in (
        ("candidate_sha256", candidate_sha256),
        ("gate_sha256", gate_sha256),
        ("prev_hash", prev_hash),
    ):
        if not isinstance(digest, str) or not HEX64_RE.fullmatch(digest):
            raise ValueError(f"Invalid 64-hex digest for {label}.")

    body: Dict[str, str] = {
        "authority": "Level_01",
        "candidate_sha256": candidate_sha256,
        "contract": "MORANDI_W2_PRECOMMIT_v1",
        "gate_sha256": gate_sha256,
        "gate_verdict": "HOLD_READY_FOR_W2",
        "prev_hash": prev_hash,
        "w_ext_id": w_clean,
    }
    body_sha = canonical_sha256(body)
    return dict(body, attestation_sha256=body_sha)


def _read_and_verify_chain_locked(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        buf = os.read(fd, 65536)
        if not buf:
            break
        chunks.append(buf)
    raw_text = b"".join(chunks).decode("utf-8")
    lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
    if not lines:
        return "0" * 64

    prev_sha = ""
    for lineno, line in enumerate(lines, 1):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"WITNESS_LEDGER_CORRUPT_KILL: invalid JSON on line {lineno}") from exc
        if not isinstance(rec, dict):
            raise RuntimeError(f"WITNESS_LEDGER_CORRUPT_KILL: non-object record on line {lineno}")
        rec_sha = rec.get("sha256", "")
        if not isinstance(rec_sha, str) or not HEX64_RE.fullmatch(rec_sha):
            raise RuntimeError(f"WITNESS_LEDGER_CORRUPT_KILL: invalid sha256 on line {lineno}")

        if "prev_hash" in rec:
            expected_prev = prev_sha if lineno > 1 else "0" * 64
            if rec["prev_hash"] != expected_prev:
                raise RuntimeError(
                    f"WITNESS_LEDGER_CORRUPT_KILL: broken prev_hash link on line {lineno}"
                )
            body = {k: v for k, v in rec.items() if k != "sha256"}
            expected_rec_sha = canonical_sha256(body)
            if not hmac.compare_digest(rec_sha, expected_rec_sha):
                raise RuntimeError(
                    f"WITNESS_LEDGER_CORRUPT_KILL: record hash mismatch on line {lineno}"
                )
        prev_sha = rec_sha
    return prev_sha


def _validate_attestation_file(
    attest_path: Path,
    expected_w_ext_id: str,
    gate_result: Dict[str, Any],
    expected_prev_hash: str,
) -> str:
    if not attest_path.is_file():
        raise RuntimeError("W2_ATTESTATION_MISSING_KILL: attestation file does not exist.")
    try:
        att = json.loads(attest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("W2_ATTESTATION_INVALID_JSON_KILL: unreadable attestation JSON.") from exc

    if not isinstance(att, dict):
        raise RuntimeError("W2_ATTESTATION_SCHEMA_KILL: attestation root must be an object.")

    required_keys = {
        "attestation_sha256",
        "authority",
        "candidate_sha256",
        "contract",
        "gate_sha256",
        "gate_verdict",
        "prev_hash",
        "w_ext_id",
    }
    if set(att.keys()) != required_keys:
        raise RuntimeError("W2_ATTESTATION_SCHEMA_KILL: unexpected or missing attestation fields.")

    if att["contract"] != "MORANDI_W2_PRECOMMIT_v1" or att["authority"] != "Level_01":
        raise RuntimeError("W2_ATTESTATION_AUTHORITY_KILL: invalid contract or authority.")
    if att["w_ext_id"] != expected_w_ext_id:
        raise RuntimeError("W2_ATTESTATION_ID_MISMATCH_KILL: w_ext_id mismatch.")
    if att["gate_verdict"] != "HOLD_READY_FOR_W2":
        raise RuntimeError("W2_ATTESTATION_VERDICT_KILL: attestation not bound to HOLD_READY_FOR_W2.")
    if att["candidate_sha256"] != gate_result.get("candidate_sha256"):
        raise RuntimeError("W2_ATTESTATION_CANDIDATE_MISMATCH_KILL: candidate_sha256 mismatch.")
    if att["gate_sha256"] != gate_result.get("gate_sha256"):
        raise RuntimeError("W2_ATTESTATION_GATE_MISMATCH_KILL: gate_sha256 mismatch.")
    if att["prev_hash"] != expected_prev_hash:
        raise RuntimeError("W2_ATTESTATION_REPLAY_OR_HEAD_MISMATCH_KILL: prev_hash mismatch.")

    provided_sha = att["attestation_sha256"]
    if not isinstance(provided_sha, str) or not HEX64_RE.fullmatch(provided_sha):
        raise RuntimeError("W2_ATTESTATION_DIGEST_FORMAT_KILL: invalid attestation_sha256.")

    expected_att = build_precommit_attestation(
        w_ext_id=expected_w_ext_id,
        candidate_sha256=gate_result["candidate_sha256"],
        gate_sha256=gate_result["gate_sha256"],
        prev_hash=expected_prev_hash,
    )
    if not hmac.compare_digest(provided_sha, expected_att["attestation_sha256"]):
        raise RuntimeError("W2_ATTESTATION_DIGEST_MISMATCH_KILL: attestation digest invalid.")
    return provided_sha


def record_witness_entry(
    timestamp: str,
    w_ext_id: str,
    attest_file: str,
    state_path: Path,
    log_path: Path,
    gate_evaluator: Callable[[], Dict[str, Any]] = evaluate_gate,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    ts_clean = timestamp.strip()
    if not ts_clean:
        raise RuntimeError("INVALID_TIMESTAMP_KILL: timestamp must be non-empty.")

    w_clean = w_ext_id.strip()
    att_clean = attest_file.strip()

    gate_res = gate_evaluator()
    gate_verdict = gate_res.get("verdict")
    if gate_verdict == "KILL":
        raise RuntimeError("GATE_VERDICT_KILL: consequence gate vetoed transition.")
    if gate_verdict not in ("HOLD", "HOLD_READY_FOR_W2"):
        raise RuntimeError(f"GATE_UNKNOWN_VERDICT_KILL: {gate_verdict!r}")

    requesting_open = bool(w_clean or att_clean)
    if requesting_open:
        if not w_clean or not W_EXT_ID_RE.fullmatch(w_clean):
            raise RuntimeError("W2_INVALID_ID_KILL: valid W_EXT_ID required when requesting OPEN.")
        if not att_clean:
            raise RuntimeError(
                "W2_BARE_ID_REJECTED_KILL: W_EXT_ID alone cannot authorize OPEN; W_EXT_ATTEST_FILE required."
            )
        if gate_verdict != "HOLD_READY_FOR_W2":
            raise RuntimeError(
                f"GATE_NOT_READY_FOR_W2_KILL: gate reported {gate_verdict!r}, cannot issue OPEN."
            )

    log_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    fd = os.open(str(log_path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        prev_hash = _read_and_verify_chain_locked(fd)

        if requesting_open:
            attest_sha = _validate_attestation_file(
                Path(att_clean),
                expected_w_ext_id=w_clean,
                gate_result=gate_res,
                expected_prev_hash=prev_hash,
            )
            state = "OPEN"
            v_dc = "5.00"
            v_dc_mv = 5000
            authority = "Level_01"
        else:
            attest_sha = ""
            state = "HOLD"
            v_dc = "0.00"
            v_dc_mv = 0
            authority = "NONE"

        st_obj: Dict[str, Any] = {
            "attestation_sha256": attest_sha,
            "authority": authority,
            "candidate_sha256": gate_res["candidate_sha256"],
            "gate_sha256": gate_res["gate_sha256"],
            "gate_verdict": gate_verdict,
            "physical_authority": "NONE",
            "state": state,
            "tier": "L1_SOFTWARE",
            "timestamp": ts_clean,
            "v_dc": v_dc,
            "v_dc_mv": v_dc_mv,
            "w_ext_id": w_clean,
        }
        st_raw = (json.dumps(st_obj, sort_keys=True) + "\n").encode("utf-8")
        st_sha = hashlib.sha256(st_raw).hexdigest()

        rec_body: Dict[str, Any] = {
            "attestation_sha256": attest_sha,
            "authority": authority,
            "candidate_sha256": gate_res["candidate_sha256"],
            "file": str(state_path),
            "gate_sha256": gate_res["gate_sha256"],
            "gate_verdict": gate_verdict,
            "prev_hash": prev_hash,
            "state": state,
            "state_sha256": st_sha,
            "timestamp": ts_clean,
            "v_dc": v_dc,
            "w_ext_id": w_clean,
        }
        rec_sha = canonical_sha256(rec_body)
        rec = dict(rec_body, sha256=rec_sha)
        rec_line = (json.dumps(rec, sort_keys=True) + "\n").encode("utf-8")

        os.lseek(fd, 0, os.SEEK_END)
        written = 0
        while written < len(rec_line):
            n = os.write(fd, rec_line[written:])
            if n <= 0:
                raise RuntimeError("WITNESS_WRITE_SHORT_KILL")
            written += n
        os.fsync(fd)

        tmp_state = state_path.with_name(f".{state_path.name}.tmp.{os.getpid()}")
        tmp_state.write_bytes(st_raw)
        os.replace(tmp_state, state_path)

        return st_obj, rec
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed L1 W^2 witness recorder.")
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--w-ext-id", default="")
    parser.add_argument("--attest-file", default="")
    parser.add_argument("--state-out", required=True)
    parser.add_argument("--log-out", required=True)
    args = parser.parse_args(argv)

    try:
        record_witness_entry(
            timestamp=args.timestamp,
            w_ext_id=args.w_ext_id,
            attest_file=args.attest_file,
            state_path=Path(args.state_out),
            log_path=Path(args.log_out),
        )
    except Exception as exc:
        print(f"[!] WITNESS_GATE_REJECTED (0.00 V DC): {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
