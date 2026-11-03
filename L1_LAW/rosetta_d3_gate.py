#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE: rosetta_d3_gate.py
CLASSIFICATION: KY Realization Grammar v1.5-MASTER // Rosetta D3 (208B) & Ed25519 Gate
STATE ANCHOR: 0xABCDEF00
EPISTEMIC BOUNDARY: INSPIRED_BY != IMPLEMENTS != PROVES (Zero external dependencies)

Håndhever:
  1. Eksakt 208-byte binær Rosetta v1.5 D3-konvolutt:
       - magic            : 4B  uint32 (0xABCDEF00)
       - schema_version   : 2B  uint16 (0x0105)
       - registry_a_flags : 1B  uint8  (0x01 = Rosetta+Ed25519 anchored)
       - registry_b_flags : 1B  uint8  (0x00 = HOLD/SOFTWARE_DEMO, 0x01 = L3_HIL_WITNESSED)
       - monotonic_seq    : 8B  uint64 (C > C_hw)
       - prev_chain_hash  : 32B SHA-256
       - ky_glyph_sha256  : 32B SHA-256 (over kanonisk Unicode glyph-streng)
       - ky_ascii_sha256  : 32B SHA-256 (over kanonisk ASCII-streng, D1.2 bijeksjon)
       - ed25519_pubkey   : 32B RFC 8032 offentlig nøkkel
       - ed25519_sig      : 64B RFC 8032 deterministisk signatur over byte 0..143
       Totalt             : 4 + 2 + 1 + 1 + 8 + 32 + 32 + 32 + 32 + 64 = 208 bytes.
  2. Ren Python-implementasjon av RFC 8032 Ed25519 (GF(2^255 - 19)) uten tredjepartsbiblioteker.
  3. Registry A (KILL): Avviser frittstående Unicode og uforankrede hash-kjeder.
  4. Registry B (HOLD): Låser kravstatus til OPEN_AS_SOFTWARE_DEMONSTRATION når L3 HIL mangler.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
import struct
import sys
from typing import Optional, Tuple

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from ky_parser import KYEngine


ROSETTA_D3_FORMAT = "<IHBBQ32s32s32s32s64s"
ROSETTA_D3_UNSIGNED_FORMAT = "<IHBBQ32s32s32s32s"
assert struct.calcsize(ROSETTA_D3_FORMAT) == 208, "Rosetta D3 envelope must be 208 bytes"
assert struct.calcsize(ROSETTA_D3_UNSIGNED_FORMAT) == 144, "Unsigned prefix must be 144 bytes"

LOCUS_ANCHOR_MAGIC = 0xABCDEF00
ROSETTA_SCHEMA_V1_5 = 0x0105


# ============================================================================
# 1. PURE-PYTHON RFC 8032 ED25519 IMPLEMENTATION (Zero External Dependencies)
# ============================================================================

_B = 256
_Q = 2**255 - 19
_L = 2**252 + 27742317777372353535851937790883648493


def _inv(x: int) -> int:
    return pow(x, _Q - 2, _Q)


_D = (-121665 * _inv(121666)) % _Q
_I = pow(2, (_Q - 1) // 4, _Q)


def _xrecover(y: int) -> int:
    xx = (y * y - 1) * _inv(_D * y * y + 1)
    x = pow(xx, (_Q + 3) // 8, _Q)
    if (x * x - xx) % _Q != 0:
        x = (x * _I) % _Q
    if x % 2 != 0:
        x = _Q - x
    return x


_BY = (4 * _inv(5)) % _Q
_BX = _xrecover(_BY)
_BASE = (_BX % _Q, _BY % _Q, 1, (_BX * _BY) % _Q)
_ZERO = (0, 1, 1, 0)


def _edwards_add(p: Tuple[int, int, int, int], q: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    x1, y1, z1, t1 = p
    x2, y2, z2, t2 = q
    a = ((y1 - x1) * (y2 - x2)) % _Q
    b = ((y1 + x1) * (y2 + x2)) % _Q
    c = (t1 * 2 * _D * t2) % _Q
    d = (z1 * 2 * z2) % _Q
    e = (b - a) % _Q
    f = (d - c) % _Q
    g = (d + c) % _Q
    h = (b + a) % _Q
    return (e * f) % _Q, (g * h) % _Q, (f * g) % _Q, (e * h) % _Q


def _scalarmult(p: Tuple[int, int, int, int], e: int) -> Tuple[int, int, int, int]:
    res = _ZERO
    cur = p
    while e > 0:
        if e & 1:
            res = _edwards_add(res, cur)
        cur = _edwards_add(cur, cur)
        e >>= 1
    return res


def _encodepoint(p: Tuple[int, int, int, int]) -> bytes:
    x, y, z, _ = p
    zi = _inv(z)
    x = (x * zi) % _Q
    y = (y * zi) % _Q
    val = y | ((x & 1) << 255)
    return val.to_bytes(32, "little")


def _decodepoint(s: bytes) -> Optional[Tuple[int, int, int, int]]:
    if len(s) != 32:
        return None
    unclamped = int.from_bytes(s, "little")
    xs = unclamped >> 255
    y = unclamped & ((1 << 255) - 1)
    if y >= _Q:
        return None
    x = _xrecover(y)
    if (x & 1) != xs:
        x = _Q - x
    p = (x, y, 1, (x * y) % _Q)
    if ((-x * x + y * y - 1 - _D * x * x * y * y) % _Q) != 0:
        return None
    return p


def ed25519_publickey(seed_32b: bytes) -> bytes:
    """Utleder 32-byte RFC 8032 offentlig nøkkel fra 32-byte privat frø."""
    assert len(seed_32b) == 32
    h = hashlib.sha512(seed_32b).digest()
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return _encodepoint(_scalarmult(_BASE, a))


def ed25519_sign(seed_32b: bytes, msg: bytes) -> bytes:
    """Produserer 64-byte deterministisk RFC 8032 Ed25519-signatur."""
    assert len(seed_32b) == 32
    h = hashlib.sha512(seed_32b).digest()
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    prefix = h[32:]
    pub = _encodepoint(_scalarmult(_BASE, a))
    r = int.from_bytes(hashlib.sha512(prefix + msg).digest(), "little") % _L
    r_bytes = _encodepoint(_scalarmult(_BASE, r))
    k = int.from_bytes(hashlib.sha512(r_bytes + pub + msg).digest(), "little") % _L
    s = (r + k * a) % _L
    return r_bytes + s.to_bytes(32, "little")


def ed25519_verify(pubkey_32b: bytes, msg: bytes, sig_64b: bytes) -> bool:
    """Verifiserer 64-byte RFC 8032 Ed25519-signatur (fail-closed)."""
    if len(pubkey_32b) != 32 or len(sig_64b) != 64:
        return False
    a_pt = _decodepoint(pubkey_32b)
    r_pt = _decodepoint(sig_64b[:32])
    if a_pt is None or r_pt is None:
        return False
    s = int.from_bytes(sig_64b[32:], "little")
    if s >= _L:
        return False
    k = int.from_bytes(hashlib.sha512(sig_64b[:32] + pubkey_32b + msg).digest(), "little") % _L
    lhs = _scalarmult(_BASE, s)
    rhs = _edwards_add(r_pt, _scalarmult(a_pt, k))
    return _encodepoint(lhs) == _encodepoint(rhs)


# ============================================================================
# 2. ROSETTA D3 (208B) GATE & VERIFIER
# ============================================================================

@dataclass(frozen=True)
class RosettaD3Receipt:
    gate_verdict: str            # 'OPEN' | 'HOLD' | 'KILL'
    registry_a_status: str       # 'PASS_ROSETTA_ED25519' | 'KILL_REGISTRY_A_VIOLATION'
    registry_b_status: str       # 'HOLD_OPEN_AS_SOFTWARE_DEMONSTRATION' | 'PASS_L3_SILICON_WITNESSED' | 'KILL'
    monotonic_seq: int
    d12_bijection_ok: bool
    envelope_208b: Optional[bytes]
    envelope_sha256: str
    reason: str


class RosettaD3Gate:
    """
    Håndhever KY v1.5-MASTER D3-loven:
      - Avviser frittstående Unicode og uforankrede hash-kjeder (Registry A -> KILL).
      - Krever D1.2 bijektivitet mellom Unicode og ASCII.
      - Pakker og verifiserer eksakt 208-byte Rosetta v1.5-konvolutt signert med Ed25519.
      - Håndhever Registry B (HOLD / OPEN_AS_SOFTWARE_DEMONSTRATION når L3 HIL mangler).
    """

    def __init__(self, ed25519_seed_32b: bytes) -> None:
        assert len(ed25519_seed_32b) == 32
        self._seed = ed25519_seed_32b
        self.pubkey = ed25519_publickey(ed25519_seed_32b)
        self.committed_seq: int = 0
        self.prev_chain_hash: bytes = hashlib.sha256(b"ROSETTA_D3_GENESIS_0xABCDEF00").digest()

    @staticmethod
    def reject_standalone_unicode_or_hash_chain(
        raw_unicode_or_hash: str,
        has_rosetta_schema: bool = False,
        has_external_anchor_or_ed25519: bool = False,
    ) -> RosettaD3Receipt:
        """
        Registry A (KILL): Frittstående Unicode eller uforankret SHA-256-kjede alene
        avvises deterministisk som ugyldig D3-bevis.
        """
        if not (has_rosetta_schema and has_external_anchor_or_ed25519):
            return RosettaD3Receipt(
                gate_verdict="KILL",
                registry_a_status="KILL_REGISTRY_A_VIOLATION",
                registry_b_status="KILL",
                monotonic_seq=0,
                d12_bijection_ok=False,
                envelope_208b=None,
                envelope_sha256="0" * 64,
                reason="Registry A (KILL): Standalone Unicode or unanchored hash-chain rejected; D3 requires 208B Rosetta v1.5 + Ed25519/WORM anchor.",
            )
        raise ValueError("Use seal_d3_envelope() for anchored Rosetta v1.5 payloads")

    def seal_d3_envelope(
        self,
        ky_glyph_expr: str,
        monotonic_seq: int,
        l3_silicon_witnessed: bool = False,
    ) -> RosettaD3Receipt:
        """
        Evaluerer KY-uttrykket via KYEngine (D1.2 bijeksjon + Alternativ A), og forsegler
        en 208-byte Ed25519-signert Rosetta v1.5-konvolutt dersom uttrykket er gyldig.
        """
        eval_res = KYEngine.evaluate_glyph_expr(ky_glyph_expr)
        if eval_res.gate != "OPEN" or not eval_res.roundtrip_ok:
            return RosettaD3Receipt(
                gate_verdict="KILL",
                registry_a_status="KILL_REGISTRY_A_VIOLATION",
                registry_b_status="KILL",
                monotonic_seq=monotonic_seq,
                d12_bijection_ok=eval_res.roundtrip_ok,
                envelope_208b=None,
                envelope_sha256="0" * 64,
                reason=f"KY evaluation rejected D3 seal: gate={eval_res.gate}, reasons={eval_res.reasons}",
            )

        if monotonic_seq <= self.committed_seq:
            return RosettaD3Receipt(
                gate_verdict="KILL",
                registry_a_status="KILL_REGISTRY_A_VIOLATION",
                registry_b_status="KILL",
                monotonic_seq=monotonic_seq,
                d12_bijection_ok=True,
                envelope_208b=None,
                envelope_sha256="0" * 64,
                reason=f"Monotonic sequence replay: seq={monotonic_seq} <= committed={self.committed_seq}",
            )

        reg_a_flag = 0x01
        reg_b_flag = 0x01 if l3_silicon_witnessed else 0x00

        glyph_hash = hashlib.sha256(eval_res.expression_unicode.encode("utf-8")).digest()
        ascii_hash = hashlib.sha256(eval_res.expression_ascii.encode("utf-8")).digest()

        unsigned_144b = struct.pack(
            ROSETTA_D3_UNSIGNED_FORMAT,
            LOCUS_ANCHOR_MAGIC,
            ROSETTA_SCHEMA_V1_5,
            reg_a_flag,
            reg_b_flag,
            monotonic_seq,
            self.prev_chain_hash,
            glyph_hash,
            ascii_hash,
            self.pubkey,
        )
        sig_64b = ed25519_sign(self._seed, unsigned_144b)
        envelope_208b = unsigned_144b + sig_64b
        assert len(envelope_208b) == 208

        env_hash = hashlib.sha256(envelope_208b).digest()
        self.prev_chain_hash = env_hash
        self.committed_seq = monotonic_seq

        reg_b_status = (
            "PASS_L3_SILICON_WITNESSED"
            if l3_silicon_witnessed
            else "HOLD_OPEN_AS_SOFTWARE_DEMONSTRATION"
        )
        gate_verdict = "OPEN" if l3_silicon_witnessed else "HOLD"

        return RosettaD3Receipt(
            gate_verdict=gate_verdict,
            registry_a_status="PASS_ROSETTA_ED25519",
            registry_b_status=reg_b_status,
            monotonic_seq=monotonic_seq,
            d12_bijection_ok=True,
            envelope_208b=envelope_208b,
            envelope_sha256=env_hash.hex(),
            reason=f"Sealed 208B Rosetta v1.5 envelope (seq={monotonic_seq}, RegB={reg_b_status})",
        )

    @staticmethod
    def verify_d3_envelope(
        envelope_208b: bytes,
        expected_prev_hash: bytes,
        min_seq_exclusive: int = 0,
    ) -> Tuple[bool, str]:
        """Verifiserer en 208-byte Rosetta v1.5-konvolutt og dens Ed25519-signatur."""
        if len(envelope_208b) != 208:
            return False, f"KILL_ENVELOPE_SIZE: expected 208B, got {len(envelope_208b)}B"

        (
            magic,
            version,
            reg_a_flag,
            _reg_b_flag,
            seq,
            prev_hash,
            _glyph_h,
            _ascii_h,
            pubkey,
            sig,
        ) = struct.unpack(ROSETTA_D3_FORMAT, envelope_208b)

        if magic != LOCUS_ANCHOR_MAGIC or version != ROSETTA_SCHEMA_V1_5 or reg_a_flag != 0x01:
            return False, "KILL_HEADER_MISMATCH: invalid magic, schema version, or Registry A flag"

        if prev_hash != expected_prev_hash:
            return False, "KILL_CHAIN_BROKEN: prev_chain_hash mismatch"

        if seq <= min_seq_exclusive:
            return False, f"KILL_MONOTONIC_REPLAY: seq={seq} <= {min_seq_exclusive}"

        unsigned_144b = envelope_208b[:144]
        if not ed25519_verify(pubkey, unsigned_144b, sig):
            return False, "KILL_ED25519_SIGNATURE_INVALID"

        return True, "PASS_ROSETTA_D3_AUTHENTIC"
