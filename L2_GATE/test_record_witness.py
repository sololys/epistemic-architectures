#!/usr/bin/env python3
"""Regression & concurrency tests for L2_GATE.evaluate_boundaries and L2_GATE.record_witness."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from L2_GATE import evaluate_boundaries
from L2_GATE.record_witness import (
    _read_and_verify_chain_locked,
    build_precommit_attestation,
    record_witness_entry,
)
import os


class WitnessGateAndConcurrencyTests(unittest.TestCase):
    def test_evaluate_boundaries_cli_exit_codes_distinguish_hold_from_ready(self) -> None:
        # Default gate is HOLD_READY_FOR_W2 -> exit 0
        self.assertEqual(evaluate_boundaries.main(), 0)

        # Plain HOLD (envelope exceeded -> verdict == "HOLD", NOT ready for W2) -> exit 2
        hold_payload = evaluate_boundaries.evaluate_gate(envelope_max=Fraction(1, 1))
        self.assertEqual(hold_payload["verdict"], "HOLD")
        with mock.patch.object(evaluate_boundaries, "evaluate_gate", return_value=hold_payload):
            self.assertEqual(evaluate_boundaries.main(), 2)

        # Hard boundary breach -> verdict == "KILL" -> exit 1
        kill_payload = dict(hold_payload, verdict="KILL")
        with mock.patch.object(evaluate_boundaries, "evaluate_gate", return_value=kill_payload):
            self.assertEqual(evaluate_boundaries.main(), 1)

    def test_bare_w_ext_id_is_rejected_without_bound_attestation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            st_path = Path(tmp) / "latest_state.json"
            log_path = Path(tmp) / "audit_log.jsonl"

            with self.assertRaisesRegex(RuntimeError, "W2_BARE_ID_REJECTED_KILL"):
                record_witness_entry(
                    timestamp="2026-11-27T23:00:00Z",
                    w_ext_id="L01-UNATTESTED",
                    attest_file="",
                    state_path=st_path,
                    log_path=log_path,
                )
            self.assertFalse(st_path.exists())
            self.assertFalse(log_path.exists())

    def test_plain_hold_gate_cannot_issue_open_even_with_attestation_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            st_path = Path(tmp) / "latest_state.json"
            log_path = Path(tmp) / "audit_log.jsonl"
            att_path = Path(tmp) / "att.json"

            hold_gate = evaluate_boundaries.evaluate_gate(envelope_max=Fraction(1, 1))
            self.assertEqual(hold_gate["verdict"], "HOLD")
            att = build_precommit_attestation(
                w_ext_id="L01-OP-01",
                candidate_sha256=hold_gate["candidate_sha256"],
                gate_sha256=hold_gate["gate_sha256"],
                prev_hash="0" * 64,
            )
            att_path.write_text(json.dumps(att), encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "GATE_NOT_READY_FOR_W2_KILL"):
                record_witness_entry(
                    timestamp="2026-11-27T23:00:00Z",
                    w_ext_id="L01-OP-01",
                    attest_file=str(att_path),
                    state_path=st_path,
                    log_path=log_path,
                    gate_evaluator=lambda: hold_gate,
                )

    def test_valid_bound_attestation_opens_once_and_blocks_replay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            st_path = Path(tmp) / "latest_state.json"
            log_path = Path(tmp) / "audit_log.jsonl"
            att_path = Path(tmp) / "att.json"

            # 1. Record initial HOLD entry
            st_hold, rec_hold = record_witness_entry(
                timestamp="2026-11-27T23:01:00Z",
                w_ext_id="",
                attest_file="",
                state_path=st_path,
                log_path=log_path,
            )
            self.assertEqual(st_hold["state"], "HOLD")
            self.assertEqual(st_hold["v_dc_mv"], 0)

            # 2. Build bound pre-commit attestation tied to candidate, gate_sha256, and prev_hash
            gate_ready = evaluate_boundaries.evaluate_gate()
            self.assertEqual(gate_ready["verdict"], "HOLD_READY_FOR_W2")
            att = build_precommit_attestation(
                w_ext_id="L01-SIGNED-01",
                candidate_sha256=gate_ready["candidate_sha256"],
                gate_sha256=gate_ready["gate_sha256"],
                prev_hash=rec_hold["sha256"],
            )
            att_path.write_text(json.dumps(att), encoding="utf-8")

            st_open, rec_open = record_witness_entry(
                timestamp="2026-11-27T23:02:00Z",
                w_ext_id="L01-SIGNED-01",
                attest_file=str(att_path),
                state_path=st_path,
                log_path=log_path,
            )
            self.assertEqual(st_open["state"], "OPEN")
            self.assertEqual(st_open["v_dc_mv"], 5000)
            self.assertEqual(rec_open["prev_hash"], rec_hold["sha256"])

            # 3. Replaying the exact same attestation fails closed because prev_hash moved!
            with self.assertRaisesRegex(RuntimeError, "W2_ATTESTATION_REPLAY_OR_HEAD_MISMATCH_KILL"):
                record_witness_entry(
                    timestamp="2026-11-27T23:03:00Z",
                    w_ext_id="L01-SIGNED-01",
                    attest_file=str(att_path),
                    state_path=st_path,
                    log_path=log_path,
                )

    def test_concurrent_multiprocess_witness_writers_preserve_linear_hash_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            st_path = Path(tmp) / "latest_state.json"
            log_path = Path(tmp) / "audit_log.jsonl"
            script = ROOT / "L2_GATE" / "record_witness.py"

            procs = [
                subprocess.Popen(
                    [
                        sys.executable,
                        "-B",
                        str(script),
                        "--timestamp",
                        f"2026-11-27T23:10:0{i}Z",
                        "--state-out",
                        str(st_path),
                        "--log-out",
                        str(log_path),
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                for i in range(8)
            ]
            for p in procs:
                out, err = p.communicate(timeout=15)
                self.assertEqual(p.returncode, 0, msg=f"Writer failed: {err}")

            lines = [ln for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
            self.assertEqual(len(lines), 8)

            fd = os.open(str(log_path), os.O_RDONLY)
            try:
                tail_sha = _read_and_verify_chain_locked(fd)
            finally:
                os.close(fd)
            last_rec = json.loads(lines[-1])
            self.assertEqual(tail_sha, last_rec["sha256"])


if __name__ == "__main__":
    unittest.main()
