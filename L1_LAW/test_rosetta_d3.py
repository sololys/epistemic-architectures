#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhetstester for Rosetta D3 (208B) & Ed25519 Gate (test_rosetta_d3.py):
  - Test 01: Offisielle RFC 8032 Ed25519 Test Vectors 1 & 2 (eksakt deterministisk verifikasjon).
  - Test 02: Registry A (KILL) – Frittstående Unicode og uforankrede hash-kjeder avvises.
  - Test 03: Registry B (HOLD) – 208B Rosetta-konvolutt uten L3 HIL låses til HOLD_OPEN_AS_SOFTWARE_DEMONSTRATION.
  - Test 04: 208B Rosetta-konvolutt med L3 HIL og Ed25519-verifikasjon (PASS_ROSETTA_D3_AUTHENTIC).
  - Test 05: Bit-flip i 208B konvolutt avvises av Ed25519-verifikasjonen (KILL_ED25519_SIGNATURE_INVALID).
  - Test 06: Alternativ A-brudd ('●' i suffiks) nektes D3-forsegling.
"""

import hashlib
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../ENGINES/micro_engines")))

from rosetta_d3_gate import (
    RosettaD3Gate,
    ed25519_publickey,
    ed25519_sign,
    ed25519_verify,
)


class TestRosettaD3Gate(unittest.TestCase):

    # RFC 8032 Section 7.1 Test Vector 1 (Empty message)
    RFC8032_TV1_SEED = bytes.fromhex(
        "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60"
    )
    RFC8032_TV1_PUB = bytes.fromhex(
        "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
    )
    RFC8032_TV1_SIG = bytes.fromhex(
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
        "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
    )

    # RFC 8032 Section 7.1 Test Vector 2 (1-byte message 0x72)
    RFC8032_TV2_SEED = bytes.fromhex(
        "4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb"
    )
    RFC8032_TV2_PUB = bytes.fromhex(
        "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c"
    )
    RFC8032_TV2_MSG = bytes.fromhex("72")
    RFC8032_TV2_SIG = bytes.fromhex(
        "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da"
        "085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"
    )

    def test_01_rfc8032_ed25519_deterministic_test_vectors(self) -> None:
        """Verifiserer eksakt bit-identitet mot RFC 8032 Test Vector 1 og 2."""
        self.assertEqual(ed25519_publickey(self.RFC8032_TV1_SEED), self.RFC8032_TV1_PUB)
        self.assertEqual(ed25519_sign(self.RFC8032_TV1_SEED, b""), self.RFC8032_TV1_SIG)
        self.assertTrue(ed25519_verify(self.RFC8032_TV1_PUB, b"", self.RFC8032_TV1_SIG))

        self.assertEqual(ed25519_publickey(self.RFC8032_TV2_SEED), self.RFC8032_TV2_PUB)
        self.assertEqual(ed25519_sign(self.RFC8032_TV2_SEED, self.RFC8032_TV2_MSG), self.RFC8032_TV2_SIG)
        self.assertTrue(ed25519_verify(self.RFC8032_TV2_PUB, self.RFC8032_TV2_MSG, self.RFC8032_TV2_SIG))

    def test_02_registry_a_rejects_standalone_unicode_and_unanchored_hashes(self) -> None:
        """Registry A (KILL): Frittstående Unicode og uforankrede hash-kjeder avvises."""
        r_unicode = RosettaD3Gate.reject_standalone_unicode_or_hash_chain("✓(○ → ∅ → □ → ◇ → ●)#! ▸")
        self.assertEqual(r_unicode.gate_verdict, "KILL")
        self.assertEqual(r_unicode.registry_a_status, "KILL_REGISTRY_A_VIOLATION")
        self.assertIsNone(r_unicode.envelope_208b)

    def test_03_registry_b_locks_software_demo_to_hold_in_208b_envelope(self) -> None:
        """Registry B (HOLD): 208B Rosetta-konvolutt uten L3 HIL får HOLD_OPEN_AS_SOFTWARE_DEMONSTRATION."""
        gate = RosettaD3Gate(self.RFC8032_TV1_SEED)
        genesis = gate.prev_chain_hash
        receipt = gate.seal_d3_envelope(
            ky_glyph_expr="✓(○ → ∅ → □ → ◇ → ●)#! ▸",
            monotonic_seq=1,
            l3_silicon_witnessed=False,
        )
        self.assertEqual(receipt.gate_verdict, "HOLD")
        self.assertEqual(receipt.registry_a_status, "PASS_ROSETTA_ED25519")
        self.assertEqual(receipt.registry_b_status, "HOLD_OPEN_AS_SOFTWARE_DEMONSTRATION")
        self.assertIsNotNone(receipt.envelope_208b)
        self.assertEqual(len(receipt.envelope_208b), 208)

        ok, msg = RosettaD3Gate.verify_d3_envelope(receipt.envelope_208b, genesis, min_seq_exclusive=0)
        self.assertTrue(ok, msg)

    def test_04_rosetta_208b_with_l3_hil_and_chain_continuity(self) -> None:
        """Verifiserer kjedet 208B Rosetta-konvolutt med Ed25519 og L3 HIL."""
        gate = RosettaD3Gate(self.RFC8032_TV2_SEED)
        h0 = gate.prev_chain_hash
        r1 = gate.seal_d3_envelope("✓(○ → ∅ → □ → ◇ → ●)#! ▸", monotonic_seq=1, l3_silicon_witnessed=True)
        self.assertEqual(r1.gate_verdict, "OPEN")
        self.assertEqual(r1.registry_b_status, "PASS_L3_SILICON_WITNESSED")

        ok1, _ = RosettaD3Gate.verify_d3_envelope(r1.envelope_208b, h0, min_seq_exclusive=0)
        self.assertTrue(ok1)

        h1 = bytes.fromhex(r1.envelope_sha256)
        r2 = gate.seal_d3_envelope("✓(○ → ∅ → □ → ◇ → ●)#! ▸", monotonic_seq=2, l3_silicon_witnessed=True)
        ok2, _ = RosettaD3Gate.verify_d3_envelope(r2.envelope_208b, h1, min_seq_exclusive=1)
        self.assertTrue(ok2)

    def test_05_tampered_208b_envelope_rejected_by_ed25519(self) -> None:
        """Bit-flip i 208B Rosetta-konvolutten fanges av Ed25519-verifikasjonen."""
        gate = RosettaD3Gate(self.RFC8032_TV1_SEED)
        h0 = gate.prev_chain_hash
        r1 = gate.seal_d3_envelope("✓(○ → ∅ → □ → ◇ → ●)#! ▸", monotonic_seq=1, l3_silicon_witnessed=False)
        corrupted = bytearray(r1.envelope_208b)
        corrupted[80] ^= 0x01  # Flipp 1 bit i ky_glyph_sha256
        ok, reason = RosettaD3Gate.verify_d3_envelope(bytes(corrupted), h0, min_seq_exclusive=0)
        self.assertFalse(ok)
        self.assertEqual(reason, "KILL_ED25519_SIGNATURE_INVALID")

    def test_06_option_a_suffix_bullet_blocked_from_d3_seal(self) -> None:
        """Alternativ A: '●' i suffiks nektes D3-forsegling."""
        gate = RosettaD3Gate(self.RFC8032_TV1_SEED)
        bad = gate.seal_d3_envelope("✓(○ → ∅ → □ → ◇ → ●)#● ▸", monotonic_seq=1)
        self.assertEqual(bad.gate_verdict, "KILL")
        self.assertIsNone(bad.envelope_208b)


if __name__ == "__main__":
    unittest.main()
