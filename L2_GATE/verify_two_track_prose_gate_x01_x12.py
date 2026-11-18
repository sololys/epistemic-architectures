#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic L1 Verifier: Two-Track Prose Consequence Gate (X.01-X.12)
=======================================================================
Surface          : L2_GATE/verify_two_track_prose_gate_x01_x12.py
Companion Notes  : L3_NOTES/REALISERINGSGRAMMATIKK_OG_PROSAENS_SUBTRAKTIVE_GEOMETRI.md
                   L3_NOTES/18_GODELS_INCOMPLETENESS_PHYSICAL_WITNESS.md
                   L3_NOTES/24_FAIL_CLOSED_COGNITIVE_FRICTION_ODYSSEUS_PACT.md
Dependencies     : Python Standard Library ONLY (ast, dataclasses, enum, fractions, hashlib, json, os, pathlib, tempfile, unittest)
Arithmetic       : Exact integer and rational arithmetic over Q (fractions.Fraction); zero floating-point operations
Epistemic Tier   : L1 Deterministic Software Verifier (PHYSICAL_AUTHORITY = NONE)
Epistemic Bound  : INSPIRED_BY != IMPLEMENTS != PROVES
Legal Boundary   : MATHEMATICS != LEGAL_MANDATE (0% algorithmic legal capacity; Level 01 human sovereignty preserved)
Ledger Disclaimer: Append-only SHA-256 hash chain on POSIX storage; not physical WORM hardware
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest


STANDALONE_COMMIT_AUTHORITY = "NONE"
PHYSICAL_AUTHORITY = "NONE"

# 7-tuple SI base dimension: (kg, m, s, A, K, mol, cd)
SIDim = tuple[int, int, int, int, int, int, int]

DIM_DIMENSIONLESS: SIDim = (0, 0, 0, 0, 0, 0, 0)
DIM_LENGTH_M: SIDim      = (0, 1, 0, 0, 0, 0, 0)
DIM_TIME_S: SIDim        = (0, 0, 1, 0, 0, 0, 0)
DIM_FREQ_HZ: SIDim       = (0, 0, -1, 0, 0, 0, 0)
DIM_VELOCITY_M_S: SIDim  = (0, 1, -1, 0, 0, 0, 0)
DIM_CURRENT_DENS: SIDim  = (0, -2, 0, 1, 0, 0, 0)

SPEED_OF_LIGHT_M_S = Fraction(299_792_458, 1)
MAX_ECHO_JACCARD = Fraction(4, 5)


def require_strict_int(val: int, name: str) -> int:
    if isinstance(val, bool) or not isinstance(val, int):
        raise TypeError(f"STRICT_INT_REQUIRED::{name}")
    return val


def require_strict_fraction(val: Fraction, name: str) -> Fraction:
    if not isinstance(val, Fraction):
        raise TypeError(f"STRICT_FRACTION_REQUIRED::{name}")
    return val


class GateState(Enum):
    KILL = "KILL"                        # 0 mV DC: Grounded cutoff
    HOLD = "HOLD"                        # 0 mV DC: Reversible workshop / Odysseus rest lock
    ESCALATED_P_EXT = "ESCALATED_P_EXT"  # 0 mV DC: Internal HOLD deadline expired (P_int -> P_ext)
    KLAR = "KLAR"                        # 0 mV DC: Dry contact inside F awaiting external witness
    REST_RESET = "REST_RESET"            # 0 mV DC: Witnessed rest recovery appended to SHA-256 chain
    OPEN = "OPEN"                        # 5000 mV DC: Simulated L1 commit exclusively via W_ext outside F


def state_millivolts_dc(state: GateState) -> int:
    if state is GateState.OPEN:
        return 5000
    return 0


class OntologicalCarrier(Enum):
    OBS_SOMATIC = "OBS_SOMATIC"          # Lived somatic friction, breath, fatigue
    LEX_SOVEREIGN = "LEX_SOVEREIGN"      # Normative pact, legal/social accountability (Level 01)
    LAW_FORMAL_PHYS = "LAW_FORMAL_PHYS"  # Formal mathematical theorem or two-channel physical bound


PROOF_CLAIM_TOKENS = frozenset({"beviser", "bevist", "garanterer", "teorem", "lovfestet"})
UNIVERSAL_SCOPE_TOKENS = frozenset({
    "alltid", "aldri", "ingen", "intet", "enhver", "ethvert",
    "alle", "umulig", "utelukket", "uunngåelig", "nødvendigvis",
    "ufravikelig", "ufravikelige",
})
EXISTENTIAL_VERBS = frozenset({"finnes", "eksisterer", "forekommer", "gis", "gjelder"})
NEGATION_OR_UNIVERSAL_MODIFIERS = frozenset({"ikke", "aldri", "ingen", "intet", "alltid"})
WORM_CLAIM_TOKENS = frozenset({"worm", "worm-innskrift", "worm-innskriften", "worm-logg", "worm-kjede"})
RUBBER_STAMP_TOKENS = frozenset({"ja", "ok", "okay", "yes", "true", "1", "ack", "godkjent", "bekreftet", "signert"})
FALSIFIER_MARKERS = frozenset({
    "<", ">", "<=", ">=", "!=", "==", "ppm", "hz", "mv", "v", "bar", "nm", "ns", "ms",
    "mikrom", "k", "j", "w", "m", "avvises", "faller", "ryker", "opphører", "svikter",
    "overstiger", "mangler", "dersom", "hvis", "ved", "underkjennes",
})
NORWEGIAN_STOPWORDS = frozenset({
    "og", "i", "på", "av", "til", "for", "med", "uten", "som", "en", "et", "ei",
    "den", "det", "de", "er", "var", "blir", "kan", "må", "skal", "vil", "har",
    "om", "ut", "inn", "fra", "over", "under", "mot", "ved", "seg", "sin", "sitt",
    "sine", "ikke", "kun", "bare", "eller", "men", "når", "der", "her", "slik", "at",
})
NO_INFLECTION_SUFFIXES = (
    "hetene", "heten", "heter", "elsene", "elsen", "elser",
    "ingene", "ingen", "inger", "ene", "ane", "ens", "ets",
    "en", "et", "er", "ar", "a", "e",
)
TECHNICAL_BASE_STEMS = frozenset({
    "først", "under", "mellom", "gjennom", "samme", "enhver", "hvert", "innen",
    "gass", "vann", "reaktor", "strøm", "spenning", "linj", "felt", "magnet",
    "magnetfelt", "kjern", "kjernespinn", "molekyl", "nitrogen", "hydrogen",
    "ammoniakk", "karbid", "sulfid", "svovel", "elektrod", "membran", "puls",
    "pulset", "drift", "klyng", "vakuum", "kvarts", "prisme", "speil", "laser",
    "foton", "klokk", "terskel", "stup", "broen", "signal", "måling", "kontroll",
    "skarp", "tynn", "høye", "fritt", "åpen", "lukket", "deler", "måles", "krever",
    "ligger", "viser", "bevarer", "brutt", "spaltet", "setning", "system", "port",
    "slus", "mennesk", "vitn", "ansvar", "arbeid", "grense", "formell", "fysisk",
    "null", "volt", "millivolt", "sekund", "meter", "prosent", "promille", "joule",
    "newton", "hertz", "tekst", "linje", "rommet", "nåløy", "bevis", "lov",
})


def si_add(a: SIDim, b: SIDim) -> SIDim:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3], a[4] + b[4], a[5] + b[5], a[6] + b[6])


def si_sub(a: SIDim, b: SIDim) -> SIDim:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3], a[4] - b[4], a[5] - b[5], a[6] - b[6])


def tokenize_clean(text: str) -> list[str]:
    out: list[str] = []
    for raw in text.lower().replace("—", " ").replace("–", " ").replace(";", " ").split():
        cleaned = raw.strip(".,;:!?()[]{}«»\"'`/\\")
        if cleaned:
            out.append(cleaned)
    return out


def content_words(text: str) -> set[str]:
    return {w for w in tokenize_clean(text) if len(w) >= 3 and w not in NORWEGIAN_STOPWORDS}


def stem_norwegian(token: str) -> str:
    w = token.strip(".,;:!?()[]{}«»\"'—–-/`").lower()
    if len(w) <= 4:
        return w
    for suf in NO_INFLECTION_SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def has_negated_existential_window(tokens: list[str], max_gap: int = 2) -> bool:
    n = len(tokens)
    for i, tok in enumerate(tokens):
        if tok in EXISTENTIAL_VERBS:
            for j in range(i + 1, min(n, i + 2 + max_gap)):
                if tokens[j] in NEGATION_OR_UNIVERSAL_MODIFIERS:
                    return True
    return False


def parse_source_entries(law_or_source: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for part in law_or_source.split("+"):
        item = part.strip()
        if not item:
            continue
        if ":" in item:
            head, detail = item.split(":", 1)
            entries.append((head.strip().upper(), detail.strip()))
        else:
            entries.append((item.upper(), ""))
    return entries


@dataclass(frozen=True)
class RationalBound:
    var_name: str
    si_dim: SIDim
    low: Fraction
    high: Fraction
    low_closed: bool = True
    high_closed: bool = True
    is_measurement: bool = False

    def __post_init__(self) -> None:
        require_strict_fraction(self.low, f"{self.var_name}.low")
        require_strict_fraction(self.high, f"{self.var_name}.high")
        if self.low > self.high or (self.low == self.high and not (self.low_closed and self.high_closed)):
            raise ValueError(f"INVALID_RATIONAL_INTERVAL::{self.var_name}")


def intersect_bounds(a: RationalBound, b: RationalBound) -> RationalBound | None:
    if a.si_dim != b.si_dim:
        raise ValueError(f"SI_DIM_MISMATCH::{a.var_name}")
    if a.low > b.low:
        low, low_closed = a.low, a.low_closed
    elif b.low > a.low:
        low, low_closed = b.low, b.low_closed
    else:
        low, low_closed = a.low, (a.low_closed and b.low_closed)

    if a.high < b.high:
        high, high_closed = a.high, a.high_closed
    elif b.high < a.high:
        high, high_closed = b.high, b.high_closed
    else:
        high, high_closed = a.high, (a.high_closed and b.high_closed)

    if low > high or (low == high and not (low_closed and high_closed)):
        return None
    return RationalBound(a.var_name, a.si_dim, low, high, low_closed, high_closed)


def is_subset_bound(meas: RationalBound, law: RationalBound) -> bool:
    if meas.low < law.low or (meas.low == law.low and meas.low_closed and not law.low_closed):
        return False
    if meas.high > law.high or (meas.high == law.high and meas.high_closed and not law.high_closed):
        return False
    return True


@dataclass(frozen=True)
class QuotientLaw:
    ratio_var: str
    numerator_var: str
    denominator_var: str
    scale: Fraction = Fraction(1, 1)


@dataclass(frozen=True)
class ProductLaw:
    product_var: str
    left_var: str
    right_var: str
    scale: Fraction = Fraction(1, 1)


@dataclass(frozen=True)
class MeasurementChannel:
    channel_id: str
    modality_family: str


@dataclass(frozen=True)
class PhysicalTrack:
    bounds: tuple[RationalBound, ...] = ()
    quotient_laws: tuple[QuotientLaw, ...] = ()
    product_laws: tuple[ProductLaw, ...] = ()
    requires_empirical_yield: bool = False
    channels: tuple[MeasurementChannel, ...] = ()


@dataclass(frozen=True)
class SkeletonTrack:
    step_id: str
    claim: str
    premise_domain: frozenset[str]
    negated_domains: frozenset[str]
    law_or_source: str
    fracture_bound: str
    carrier: OntologicalCarrier = OntologicalCarrier.LAW_FORMAL_PHYS
    upstream_refs: tuple[str, ...] = ()
    ai_authority_share: Fraction = Fraction(0, 1)

    def __post_init__(self) -> None:
        require_strict_fraction(self.ai_authority_share, f"{self.step_id}.ai_authority_share")


@dataclass(frozen=True)
class CandidateLine:
    prose_surface: str
    skeleton: SkeletonTrack
    prose_refs: tuple[str, ...] = ()
    co_generative_strike: bool = False
    decompiled_from_hold: bool = False
    claims_internal_open_before_witness: bool = False


@dataclass(frozen=True)
class ExternalWitness:
    witness_id: str
    evidence_id: str
    counter_bound: str
    elapsed_ms: int

    def __post_init__(self) -> None:
        require_strict_int(self.elapsed_ms, "ExternalWitness.elapsed_ms")


def fsync_directory(file_path: Path) -> None:
    dir_fd = os.open(str(file_path.parent), os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def verify_wal_chain(wal_path: Path) -> tuple[bool, int, str]:
    if not wal_path.exists():
        return True, 0, "0" * 64
    expected_prev = "0" * 64
    count = 0
    for line in wal_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec["prev"] != expected_prev:
            return False, count, "BROKEN_PREV_LINK"
        state = GateState(rec["state"])
        if rec["millivolts_dc"] != state_millivolts_dc(state):
            return False, count, "VOLTAGE_INVARIANT_VIOLATION"
        payload = {
            "prev": rec["prev"],
            "step_id": rec["step_id"],
            "state": rec["state"],
            "millivolts_dc": rec["millivolts_dc"],
            "detail": rec["detail"],
        }
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        if digest != rec["sha256"]:
            return False, count, "DIGEST_MISMATCH"
        expected_prev = digest
        count += 1
    return True, count, expected_prev


class TwoTrackProseGateX01X12:
    """Fail-closed two-track prose consequence compiler (X.01 through X.12)."""

    def __init__(
        self,
        wal_path: Path,
        tau_max_ms: int = 300_000,
        dtau_min_ms: int = 8_000,
        dtau_max_ms: int = 600_000,
        max_consecutive_opens: int = 7,
        min_rest_ms: int = 120_000,
        domain_lexicon: frozenset[str] = TECHNICAL_BASE_STEMS,
    ) -> None:
        self._tau_max_ms = require_strict_int(tau_max_ms, "tau_max_ms")
        self._dtau_min_ms = require_strict_int(dtau_min_ms, "dtau_min_ms")
        self._dtau_max_ms = require_strict_int(dtau_max_ms, "dtau_max_ms")
        self._max_seq = require_strict_int(max_consecutive_opens, "max_consecutive_opens")
        self._min_rest_ms = require_strict_int(min_rest_ms, "min_rest_ms")
        if self._tau_max_ms <= 0 or self._dtau_min_ms <= 0 or self._dtau_min_ms >= self._dtau_max_ms:
            raise ValueError("INVALID_CLOCK_BOUNDS")
        if self._max_seq <= 0 or self._min_rest_ms <= 0:
            raise ValueError("INVALID_ULYSSES_BOUNDS")

        self._wal_path = wal_path
        self._domain_lexicon = {w.lower() for w in domain_lexicon}
        self._verified_ids: set[str] = set()
        self._carrier_by_step: dict[str, OntologicalCarrier] = {}
        self._active_domains: set[str] = set()
        self._forbidden_domains: set[str] = set()
        self._quarantined_tropes: dict[str, str] = {}
        self._quarantine_stems: dict[str, str] = {}
        self._bounds: dict[str, RationalBound] = {}
        self._quotient_laws: list[QuotientLaw] = []
        self._product_laws: list[ProductLaw] = []
        self._locked_modalities: dict[str, str] = {}
        self._pending_klar: tuple[CandidateLine, PhysicalTrack] | None = None
        self._consecutive_opens: int = 0
        self._fatigue_latched: bool = False

        ok, _, head = verify_wal_chain(wal_path)
        if not ok:
            raise RuntimeError(f"CORRUPT_WAL::{head}")
        self._chain_head = head

    @property
    def chain_head(self) -> str:
        return self._chain_head

    def evaluate_in_f(
        self,
        cand: CandidateLine,
        phys: PhysicalTrack = PhysicalTrack(),
        hold_elapsed_ms: int = 0,
    ) -> tuple[GateState, str]:
        elapsed = require_strict_int(hold_elapsed_ms, "hold_elapsed_ms")
        sk = cand.skeleton

        if elapsed > self._tau_max_ms:
            if self._pending_klar is not None and self._pending_klar[0].skeleton.step_id == sk.step_id:
                self._pending_klar = None
            return self._commit(GateState.ESCALATED_P_EXT, sk.step_id, "HOLD_TIMEOUT_ESCALATED_TO_P_EXT")

        if self._pending_klar is not None and self._pending_klar[0].skeleton.step_id != sk.step_id:
            return self._commit(GateState.HOLD, sk.step_id, "ZERO_WINDOW_AIRLOCK_OCCUPIED")

        if cand.claims_internal_open_before_witness:
            return self._commit(GateState.KILL, sk.step_id, "GODEL_AIRGAP_BREACH_INTERNAL_OPEN_CLAIMED")

        if sk.ai_authority_share != Fraction(0, 1):
            return self._commit(GateState.KILL, sk.step_id, "X10_SOVEREIGNTY_INVARIANT_BREACH")

        if cand.co_generative_strike and not cand.decompiled_from_hold:
            return self._commit(GateState.HOLD, sk.step_id, "X02_COGENERATIVE_FREEZE_DECOMPILE_REQUIRED")

        combined_tokens = set(tokenize_clean(cand.prose_surface)) | set(tokenize_clean(sk.claim))
        if (combined_tokens & WORM_CLAIM_TOKENS) and "Hardware_WORM_Verified" not in sk.premise_domain:
            return self._commit(GateState.KILL, sk.step_id, "X01_SOFTWARE_LEDGER_CLAIMED_AS_PHYSICAL_WORM")

        if cand.prose_refs:
            return self._commit(GateState.KILL, sk.step_id, "X04_PROSE_SURFACE_LEAK")

        skel_tokens = tokenize_clean(sk.claim) + tokenize_clean(" ".join(sorted(sk.premise_domain)))
        for tok in skel_tokens:
            if tok in self._quarantined_tropes:
                return self._commit(GateState.KILL, sk.step_id, f"X04_ORTHOGONAL_TROPE_SMUGGLING::{tok}")
            if len(tok) >= 4:
                st = stem_norwegian(tok)
                for q_stem, origin_id in self._quarantine_stems.items():
                    compound_hit = len(q_stem) >= 5 and (tok.startswith(q_stem) or st.endswith(q_stem))
                    if st == q_stem or compound_hit:
                        return self._commit(GateState.KILL, sk.step_id, f"X08_MORPHOLOGICAL_TROPE_SMUGGLING::{tok}<-{q_stem}@{origin_id}")

        if any(ref not in self._verified_ids for ref in sk.upstream_refs):
            return self._commit(GateState.HOLD, sk.step_id, "UNVERIFIED_UPSTREAM_SKELETON")

        if not (sk.claim.strip() and sk.law_or_source.strip() and sk.fracture_bound.strip()):
            return self._commit(GateState.HOLD, sk.step_id, "DELTA_K_INCOMPLETE_SKELETON")
        if not sk.premise_domain:
            return self._commit(GateState.HOLD, sk.step_id, "DELTA_K_EMPTY_PREMISE_DOMAIN")

        entries = parse_source_entries(sk.law_or_source)
        tags = {head for head, _ in entries}
        if not tags or not tags.issubset({"INSPIRED_BY", "IMPLEMENTS", "PROVES"}):
            return self._commit(GateState.HOLD, sk.step_id, "DELTA_K_INVALID_SOURCE_TAG")

        if sk.carrier in (OntologicalCarrier.OBS_SOMATIC, OntologicalCarrier.LEX_SOVEREIGN) and "PROVES" in tags:
            return self._commit(GateState.KILL, sk.step_id, f"X11_CARRIER_CANNOT_PROVE_THEOREM::{sk.carrier.value}")

        upstream_carriers = tuple(self._carrier_by_step[r] for r in sk.upstream_refs)
        if (
            sk.carrier is OntologicalCarrier.LAW_FORMAL_PHYS
            and "PROVES" in tags
            and upstream_carriers
            and all(c is OntologicalCarrier.OBS_SOMATIC for c in upstream_carriers)
        ):
            return self._commit(GateState.KILL, sk.step_id, "X11_SOMATIC_TO_FORMAL_USURPATION")

        if sk.carrier is OntologicalCarrier.LEX_SOVEREIGN:
            has_lex_upstream = any(c is OntologicalCarrier.LEX_SOVEREIGN for c in upstream_carriers)
            has_const_source = any(
                head == "IMPLEMENTS" and detail.lower().startswith(("lex_", "ulysses_", "const_", "arch_axiom"))
                for head, detail in entries
            )
            if upstream_carriers and not has_lex_upstream and not has_const_source:
                return self._commit(GateState.KILL, sk.step_id, "X11_HUMES_GUILLOTINE_IS_TO_OUGHT")

        prose_tok_list = tokenize_clean(cand.prose_surface)
        prose_words = set(prose_tok_list)
        has_proof_verb = bool(prose_words & PROOF_CLAIM_TOKENS)
        has_universal = bool(prose_words & UNIVERSAL_SCOPE_TOKENS)
        has_neg_existential = has_negated_existential_window(prose_tok_list)

        if tags == {"INSPIRED_BY"} and (has_proof_verb or has_universal or has_neg_existential):
            return self._commit(GateState.KILL, sk.step_id, "AESTHETIC_USURPATION")
        if has_proof_verb and "PROVES" not in tags and "IMPLEMENTS" not in tags:
            return self._commit(GateState.KILL, sk.step_id, "X01_PROOF_VERB_WITHOUT_ANCHOR")
        if "INSPIRED_BY" in tags and ("PROVES" in tags or "IMPLEMENTS" in tags) and not sk.negated_domains:
            return self._commit(GateState.KILL, sk.step_id, "X01_MIXED_SOURCE_UNFENCED_DRIFT")
        if has_neg_existential and not sk.negated_domains:
            return self._commit(GateState.KILL, sk.step_id, "X12_NEGATED_EXISTENTIAL_WITHOUT_BOUNDARY")
        if has_universal and not sk.negated_domains:
            return self._commit(GateState.KILL, sk.step_id, "X01_UNBOUNDED_UNIVERSAL_DRIFT")

        clash = sorted((self._active_domains | set(sk.premise_domain)) & (self._forbidden_domains | set(sk.negated_domains)))
        if clash:
            return self._commit(GateState.KILL, sk.step_id, f"X05_DOMAIN_INTERSECTION_EMPTY::{clash[0]}")

        p_state, p_reason = self._check_physical(phys)
        if p_state is not GateState.KLAR:
            return self._commit(p_state, sk.step_id, p_reason)

        self._pending_klar = (cand, phys)
        return self._commit(GateState.KLAR, sk.step_id, f"READY_0MV::{sk.fracture_bound}")

    def _check_physical(self, phys: PhysicalTrack) -> tuple[GateState, str]:
        merged_modalities = dict(self._locked_modalities)
        for ch in phys.channels:
            if ch.channel_id.strip() and ch.modality_family.strip():
                merged_modalities.setdefault(ch.modality_family.strip().upper(), ch.channel_id.strip())
        if phys.requires_empirical_yield and len(merged_modalities) < 2:
            return (GateState.HOLD, "X09_MISSING_ORTHOGONAL_MODALITY")

        working_bounds = dict(self._bounds)
        local_measurements: dict[str, RationalBound] = {}
        for b in phys.bounds:
            if b.var_name in working_bounds:
                prev = working_bounds[b.var_name]
                if b.si_dim != prev.si_dim:
                    return (GateState.KILL, f"X07_SI_DIMENSION_MISMATCH::{b.var_name}")
                inter = intersect_bounds(prev, b)
                if inter is None:
                    return (GateState.KILL, f"X07_RATIONAL_INTERVAL_EMPTY::{b.var_name}")
                if b.is_measurement and not is_subset_bound(b, prev):
                    return (GateState.HOLD, f"X07_UNCERTAINTY_STRADDLES_BOUNDARY::{b.var_name}")
                if not b.is_measurement:
                    working_bounds[b.var_name] = inter
                local_measurements[b.var_name] = b
            else:
                if not b.is_measurement:
                    working_bounds[b.var_name] = b
                local_measurements[b.var_name] = b

        lookup = {**working_bounds, **local_measurements}
        for ql in list(self._quotient_laws) + list(phys.quotient_laws):
            if ql.numerator_var in lookup and ql.denominator_var in lookup and ql.ratio_var in working_bounds:
                num_b, den_b, rat_law = lookup[ql.numerator_var], lookup[ql.denominator_var], working_bounds[ql.ratio_var]
                expected_dim = si_sub(num_b.si_dim, den_b.si_dim)
                if expected_dim != rat_law.si_dim:
                    return (GateState.KILL, f"X07_QUOTIENT_SI_MISMATCH::{ql.ratio_var}")
                if den_b.low <= 0:
                    return (GateState.HOLD, f"X07_NONPOSITIVE_DENOMINATOR::{ql.denominator_var}")
                derived = RationalBound(
                    ql.ratio_var,
                    expected_dim,
                    ql.scale * (num_b.low / den_b.high),
                    ql.scale * (num_b.high / den_b.low),
                    num_b.low_closed and den_b.high_closed,
                    num_b.high_closed and den_b.low_closed,
                    is_measurement=True,
                )
                if intersect_bounds(rat_law, derived) is None:
                    return (GateState.KILL, f"X07_DERIVED_QUOTIENT_VIOLATION::{ql.ratio_var}")
                if not is_subset_bound(derived, rat_law):
                    return (GateState.HOLD, f"X07_DERIVED_QUOTIENT_STRADDLE::{ql.ratio_var}")

        for pl in list(self._product_laws) + list(phys.product_laws):
            if pl.left_var in lookup and pl.right_var in lookup and pl.product_var in working_bounds:
                left_b, right_b, prod_law = lookup[pl.left_var], lookup[pl.right_var], working_bounds[pl.product_var]
                expected_dim = si_add(left_b.si_dim, right_b.si_dim)
                if expected_dim != prod_law.si_dim:
                    return (GateState.KILL, f"X07_PRODUCT_SI_MISMATCH::{pl.product_var}")
                if left_b.low < 0 or right_b.low < 0:
                    return (GateState.HOLD, f"X07_NEGATIVE_FACTOR::{pl.product_var}")
                derived_p = RationalBound(
                    pl.product_var,
                    expected_dim,
                    pl.scale * left_b.low * right_b.low,
                    pl.scale * left_b.high * right_b.high,
                    left_b.low_closed and right_b.low_closed,
                    left_b.high_closed and right_b.high_closed,
                    is_measurement=True,
                )
                if intersect_bounds(prod_law, derived_p) is None:
                    return (GateState.KILL, f"X07_DERIVED_PRODUCT_VIOLATION::{pl.product_var}")
                if not is_subset_bound(derived_p, prod_law):
                    return (GateState.HOLD, f"X07_DERIVED_PRODUCT_STRADDLE::{pl.product_var}")

        return (GateState.KLAR, "0MV_PHYSICAL_PARITY_OK")

    def cross_airgap(self, step_id: str, witness: ExternalWitness) -> tuple[GateState, str]:
        if self._pending_klar is None or self._pending_klar[0].skeleton.step_id != step_id:
            return self._commit(GateState.HOLD, step_id, "AIRGAP_NO_MATCHING_KLAR_FRAME")

        cand, phys = self._pending_klar
        sk = cand.skeleton

        if self._fatigue_latched or self._consecutive_opens >= self._max_seq:
            self._fatigue_latched = True
            return self._commit(GateState.HOLD, sk.step_id, "X10_ULYSSES_FATIGUE_LATCHED_0MV")
        if witness.elapsed_ms < self._dtau_min_ms:
            return self._commit(GateState.HOLD, sk.step_id, "X03_REFLEX_SIGNATURE_BLOCKED")
        if witness.elapsed_ms > self._dtau_max_ms:
            self._fatigue_latched = True
            return self._commit(GateState.HOLD, sk.step_id, "X10_STALE_ATTENTION_LATCHED_0MV")
        if not (witness.witness_id.strip() and witness.evidence_id.strip()):
            return self._commit(GateState.HOLD, sk.step_id, "X03_MISSING_WITNESS_ID")

        w_tokens = tokenize_clean(witness.counter_bound)
        if not w_tokens or set(w_tokens).issubset(RUBBER_STAMP_TOKENS):
            return self._commit(GateState.HOLD, sk.step_id, "X06_RUBBER_STAMP_REJECTED")
        if set(w_tokens) & WORM_CLAIM_TOKENS and "Hardware_WORM_Verified" not in sk.premise_domain:
            return self._commit(GateState.HOLD, sk.step_id, "X06_COUNTER_BOUND_CLAIMS_PHYSICAL_WORM")

        w_content = content_words(witness.counter_bound)
        has_falsifier = bool(set(w_tokens) & FALSIFIER_MARKERS) or any(
            any(ch.isdigit() for ch in tok) for tok in w_tokens
        )
        if len(w_content) < 3 or not has_falsifier:
            return self._commit(GateState.HOLD, sk.step_id, "X06_UNDERSPECIFIED_COUNTER_BOUND")

        f_content = content_words(sk.fracture_bound)
        union_len = len(f_content | w_content)
        if union_len > 0 and Fraction(len(f_content & w_content), union_len) >= MAX_ECHO_JACCARD:
            return self._commit(GateState.HOLD, sk.step_id, "X06_PARROT_OR_TRIVIAL_EDIT_REJECTED")

        self._pending_klar = None
        self._consecutive_opens += 1
        if self._consecutive_opens >= self._max_seq:
            self._fatigue_latched = True

        self._verified_ids.add(sk.step_id)
        self._carrier_by_step[sk.step_id] = sk.carrier
        self._active_domains |= set(sk.premise_domain)
        self._forbidden_domains |= set(sk.negated_domains)

        all_skel_text = " ".join([
            sk.claim,
            " ".join(sorted(sk.premise_domain)),
            " ".join(sorted(sk.negated_domains)),
            sk.fracture_bound,
        ])
        skeleton_all_words = content_words(all_skel_text)
        skel_stems = {stem_norwegian(w) for w in tokenize_clean(all_skel_text) if len(w) >= 4}

        for trope in content_words(cand.prose_surface) - skeleton_all_words - self._domain_lexicon:
            if not any(trope.startswith(dl) for dl in self._domain_lexicon if len(dl) >= 4):
                self._quarantined_tropes.setdefault(trope, sk.step_id)

        for w in tokenize_clean(cand.prose_surface):
            if len(w) < 4 or w in NORWEGIAN_STOPWORDS:
                continue
            st = stem_norwegian(w)
            if len(st) >= 4 and st not in skel_stems and st not in self._domain_lexicon and w not in self._domain_lexicon:
                self._quarantine_stems.setdefault(st, sk.step_id)

        for b in phys.bounds:
            if not b.is_measurement:
                if b.var_name in self._bounds:
                    inter = intersect_bounds(self._bounds[b.var_name], b)
                    if inter is None:
                        raise RuntimeError(f"EMPTY_COMMIT_INTERVAL::{b.var_name}")
                    self._bounds[b.var_name] = inter
                else:
                    self._bounds[b.var_name] = b
        for ql in phys.quotient_laws:
            if ql not in self._quotient_laws:
                self._quotient_laws.append(ql)
        for pl in phys.product_laws:
            if pl not in self._product_laws:
                self._product_laws.append(pl)
        for ch in phys.channels:
            if ch.channel_id.strip() and ch.modality_family.strip():
                self._locked_modalities.setdefault(ch.modality_family.strip().upper(), ch.channel_id.strip())

        return self._commit(GateState.OPEN, sk.step_id, f"OPEN_5000MV::W={witness.witness_id}::E={witness.evidence_id}")

    def witness_rest_reset(self, witness_id: str, rest_elapsed_ms: int) -> tuple[bool, GateState, str]:
        ms = require_strict_int(rest_elapsed_ms, "rest_elapsed_ms")
        if not witness_id.strip() or ms < self._min_rest_ms:
            st, dig = self._commit(GateState.HOLD, "ULYSSES_REST", f"REST_INSUFFICIENT::{ms}<{self._min_rest_ms}")
            return False, st, dig
        self._consecutive_opens = 0
        self._fatigue_latched = False
        st, dig = self._commit(GateState.REST_RESET, "ULYSSES_REST", f"REST_VERIFIED_0MV::W={witness_id}::MS={ms}")
        return True, st, dig

    def _commit(self, state: GateState, step_id: str, detail: str) -> tuple[GateState, str]:
        mv = state_millivolts_dc(state)
        payload = {
            "prev": self._chain_head,
            "step_id": step_id,
            "state": state.value,
            "millivolts_dc": mv,
            "detail": detail,
        }
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        record = json.dumps({**payload, "sha256": digest}, ensure_ascii=False) + "\n"

        created = not self._wal_path.exists()
        fd = os.open(self._wal_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
        try:
            os.write(fd, record.encode("utf-8"))
            os.fsync(fd)
        finally:
            os.close(fd)
        if created:
            fsync_directory(self._wal_path)

        self._chain_head = digest
        return state, digest


class TestTwoTrackProseGateX01X12(unittest.TestCase):
    def test_01_ast_zero_float(self) -> None:
        forbidden = "flo" + "at"
        target = Path(__file__).resolve()
        tree = ast.parse(target.read_text(encoding="utf-8"), filename=str(target))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and type(node.value).__name__ == forbidden:
                self.fail(f"Forbidden literal at line {node.lineno}")
            if isinstance(node, ast.Name) and node.id == forbidden:
                self.fail(f"Forbidden identifier at line {node.lineno}")

    def test_02_galvanic_0mv_invariant_and_dual_clock(self) -> None:
        for st in (GateState.KILL, GateState.HOLD, GateState.ESCALATED_P_EXT, GateState.KLAR, GateState.REST_RESET):
            self.assertEqual(state_millivolts_dc(st), 0)
        self.assertEqual(state_millivolts_dc(GateState.OPEN), 5000)

        with tempfile.TemporaryDirectory() as tmp:
            gate = TwoTrackProseGateX01X12(wal_path=Path(tmp) / "clock.wal.jsonl")
            cand = CandidateLine(
                "Kandidaten avventer kalibrering.",
                SkeletonTrack(
                    "CLK_01",
                    "Måleserie avventer motprøve.",
                    frozenset({"Pending_Calibration"}),
                    frozenset(),
                    "IMPLEMENTS:Dual_Clock",
                    "Faller ved avvik over 2 K.",
                ),
            )
            self.assertIs(gate.evaluate_in_f(cand, hold_elapsed_ms=300_001)[0], GateState.ESCALATED_P_EXT)

    def test_03_physical_stoichiometry_and_causal_lightcone_straddle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            gate = TwoTrackProseGateX01X12(wal_path=Path(tmp) / "phys.wal.jsonl")
            tau_min = Fraction(40, 299_792_458)
            tau_max = Fraction(160, 1_000_000_000)
            lsb = Fraction(15, 1_000_000_000_000)

            l01 = CandidateLine(
                "Karbid-kjernen ligger som en ambolt i buret mens lyskjeglen vokter stupet.",
                SkeletonTrack(
                    "L01",
                    "Janus 8e- låser FE_NH3 <= 3/4 og kausal tur-retur låser tau_rtt i [40/c, 160 ns].",
                    frozenset({"Janus_8e", "Causal_40m"}),
                    frozenset({"Superluminal_Spoof"}),
                    "IMPLEMENTS:Physical_Bounds",
                    "Faller ved FE_NH3 > 3/4 eller tau_rtt < 20/149896229 s.",
                ),
            )
            self.assertIs(
                gate.evaluate_in_f(
                    l01,
                    PhysicalTrack(
                        bounds=(
                            RationalBound("FE_NH3", DIM_DIMENSIONLESS, Fraction(0), Fraction(3, 4)),
                            RationalBound("tau_rtt_s", DIM_TIME_S, tau_min, tau_max),
                            RationalBound("c_vac", DIM_VELOCITY_M_S, SPEED_OF_LIGHT_M_S, SPEED_OF_LIGHT_M_S),
                        ),
                        quotient_laws=(QuotientLaw("FE_NH3", "j_NH3", "j_tot"),),
                        channels=(MeasurementChannel("TDC_15PS", "OPTICAL_TOF_TDC"),),
                    ),
                )[0],
                GateState.KLAR,
            )
            self.assertIs(
                gate.cross_airgap(
                    "L01",
                    ExternalWitness("marius", "EV-01", "Avvises ved åpen-krets NH4+ over 1 mikroM eller kortsluttet prediktor.", 12_000),
                )[0],
                GateState.OPEN,
            )

            # X.08 morphological stem catch ("amboltslag" <- "ambolt")
            morph = CandidateLine(
                "Klyngens amboltslag øker strømmen.",
                SkeletonTrack(
                    "L02_MORPH",
                    "Klyngens amboltslag øker strømtettheten.",
                    frozenset({"Janus_8e"}),
                    frozenset(),
                    "IMPLEMENTS:Cluster_Model",
                    "Faller ved Fe-tap > 1/100.",
                    upstream_refs=("L01",),
                ),
            )
            self.assertIs(gate.evaluate_in_f(morph)[0], GateState.KILL)

            # X.07 derived quotient catch: 820 / 1000 = 41/50 > 3/4
            scalar = CandidateLine(
                "Partiell strøm 82 mA/cm2 måles ved 100 mA/cm2.",
                SkeletonTrack(
                    "L03_SCALAR",
                    "j_NH3 = 820 A/m2 ved j_tot = 1000 A/m2.",
                    frozenset({"Janus_8e"}),
                    frozenset(),
                    "IMPLEMENTS:Faraday_Law",
                    "Faller ved feil > 1/100.",
                    upstream_refs=("L01",),
                ),
            )
            self.assertIs(
                gate.evaluate_in_f(
                    scalar,
                    PhysicalTrack(
                        bounds=(
                            RationalBound("j_NH3", DIM_CURRENT_DENS, Fraction(820), Fraction(820), is_measurement=True),
                            RationalBound("j_tot", DIM_CURRENT_DENS, Fraction(1000), Fraction(1000), is_measurement=True),
                        ),
                    ),
                )[0],
                GateState.KILL,
            )

            # X.07 TDC bin 8895 straddles 40/c -> HOLD; bin 8899 (12 mm quartz) + MECH_INTERLOCK -> KLAR
            straddle = CandidateLine(
                "Flatt speil treffer kvantiseringskanten.",
                SkeletonTrack(
                    "L04_STRADDLE",
                    "TDC-trinn 8895 krysser vakuumgrensen.",
                    frozenset({"Causal_40m"}),
                    frozenset(),
                    "IMPLEMENTS:TDC_Guard",
                    "Faller ved nedre kant < 40/c.",
                    upstream_refs=("L01",),
                ),
            )
            self.assertIs(
                gate.evaluate_in_f(
                    straddle,
                    PhysicalTrack(bounds=(RationalBound("tau_rtt_s", DIM_TIME_S, 8895 * lsb, 8896 * lsb, is_measurement=True),)),
                )[0],
                GateState.HOLD,
            )

            prism = CandidateLine(
                "Tolv millimeter kvartsprisme løfter ekkoet fire trinn inn i sikker sone.",
                SkeletonTrack(
                    "L05_PRISM",
                    "TDC-trinn 8899 med mekanisk sperrekile ligger helt innenfor [40/c, 160 ns].",
                    frozenset({"Causal_40m"}),
                    frozenset(),
                    "IMPLEMENTS:Prism_Clearance",
                    "Faller ved okkupert sone under 5 ms fsync.",
                    upstream_refs=("L01",),
                ),
            )
            self.assertIs(
                gate.evaluate_in_f(
                    prism,
                    PhysicalTrack(
                        bounds=(RationalBound("tau_rtt_s", DIM_TIME_S, 8899 * lsb, 8900 * lsb, is_measurement=True),),
                        requires_empirical_yield=True,
                        channels=(MeasurementChannel("KNIFE_WEDGE", "MECH_INTERLOCK"),),
                    ),
                )[0],
                GateState.KLAR,
            )

    def test_04_ontological_demarcation_v2_negation_and_ulysses_rest_latch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wal = Path(tmp) / "ulysses.wal.jsonl"
            gate = TwoTrackProseGateX01X12(wal_path=wal, max_consecutive_opens=1, min_rest_ms=30_000)

            # Software WORM claim without verified hardware -> KILL
            worm = CandidateLine(
                "Vitnet signerer WORM-innskriften på disk.",
                SkeletonTrack(
                    "WORM_ERR",
                    "Diskloggen er fysisk WORM-innskrift.",
                    frozenset({"Software_SHA256"}),
                    frozenset({"Overwrite"}),
                    "IMPLEMENTS:Ledger",
                    "Faller ved brutt kjede.",
                    OntologicalCarrier.LEX_SOVEREIGN,
                ),
            )
            self.assertIs(gate.evaluate_in_f(worm)[0], GateState.KILL)

            # V2-inverted negated existential without negated_domains -> KILL
            v2 = CandidateLine(
                "Under press finnes det ikke feilfrie vitner.",
                SkeletonTrack(
                    "V2_ERR",
                    "Biologiske vitner kan feile.",
                    frozenset({"Biological_Witness"}),
                    frozenset(),
                    "IMPLEMENTS:Fatigue_Bound",
                    "Faller ved T = 0 K.",
                    OntologicalCarrier.OBS_SOMATIC,
                ),
            )
            self.assertIs(gate.evaluate_in_f(v2)[0], GateState.KILL)

            obs = CandidateLine(
                "Det feilfrie menneskelige vitnet finnes ikke.",
                SkeletonTrack(
                    "EX_01",
                    "Enhver biologisk observatør ved T > 0 K har feilrisiko større enn null.",
                    frozenset({"Biological_Witness"}),
                    frozenset({"AI_Sovereignty_Transfer", "Oracle_Infallibility"}),
                    "IMPLEMENTS:Fatigue_Bound",
                    "Faller dersom linjen siteres som hjemmel for AI-overtakelse.",
                    OntologicalCarrier.OBS_SOMATIC,
                ),
            )
            self.assertIs(gate.evaluate_in_f(obs)[0], GateState.KLAR)
            self.assertIs(
                gate.cross_airgap("EX_01", ExternalWitness("marius", "EV-EX1", "Avvises ved målt nullfeil over 10000 skift.", 11_000))[0],
                GateState.OPEN,
            )

            # Hume's guillotine blocks OBS_SOMATIC -> LEX_SOVEREIGN without constitutional pact
            pat = CandidateLine(
                "Fordi vitnet er slitent opphører vetoretten.",
                SkeletonTrack(
                    "PAT_ERR",
                    "Tretthet opphever borgerens samtykkekrav.",
                    frozenset({"Biological_Witness"}),
                    frozenset(),
                    "IMPLEMENTS:Admin_Rule",
                    "Faller ved puls < 60.",
                    OntologicalCarrier.LEX_SOVEREIGN,
                    ("EX_01",),
                ),
            )
            self.assertIs(gate.evaluate_in_f(pat)[0], GateState.KILL)

            lex = CandidateLine(
                "Tretthet utløser hvilesperre uten fullmaktsoverføring.",
                SkeletonTrack(
                    "EX_02",
                    "Ulysses-pakten fryser porten ved 0 mV DC inntil dokumentert hvile.",
                    frozenset({"Ulysses_Rest_Pact"}),
                    frozenset({"AI_Sovereignty_Transfer"}),
                    "IMPLEMENTS:Ulysses_Constitutional_Pact",
                    "Faller ved spenning over 0 mV under hvilesperre.",
                    OntologicalCarrier.LEX_SOVEREIGN,
                    ("EX_01",),
                ),
            )
            self.assertIs(gate.evaluate_in_f(lex)[0], GateState.KLAR)
            # Latched after 1st OPEN -> HOLD until witness_rest_reset >= 30_000 ms
            self.assertIs(
                gate.cross_airgap("EX_02", ExternalWitness("marius", "EV-EX2", "Opphører ved lukket relé før utløpt hviletid på 30 s.", 12_000))[0],
                GateState.HOLD,
            )
            ok_rest, st_rest, _ = gate.witness_rest_reset("marius", 35_000)
            self.assertTrue(ok_rest)
            self.assertIs(st_rest, GateState.REST_RESET)
            self.assertIs(
                gate.cross_airgap("EX_02", ExternalWitness("marius", "EV-EX2", "Opphører ved lukket relé før utløpt hviletid på 30 s.", 12_000))[0],
                GateState.OPEN,
            )
            ok_chain, _, _ = verify_wal_chain(wal)
            self.assertTrue(ok_chain)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTwoTrackProseGateX01X12)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        return 1
    summary = {
        "arithmetic_domain": "EXACT_INT_AND_RATIONAL_Q",
        "coordinates_enforced": "X.01_TO_X.12",
        "epistemic_boundary": "INSPIRED_BY != IMPLEMENTS != PROVES",
        "legal_authority": "NONE_HUMAN_L01_REQUIRED",
        "modeled_idle_voltage": "0.00 V",
        "tests_passed": result.testsRun,
        "verdict": "HOLD_READY_FOR_W2",
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
