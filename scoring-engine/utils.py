"""
Utilities for canonicalizing feature manifests, computing featuresHash, and
helpers for normalization.
"""

import json
from eth_utils import keccak, to_hex
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP


def canonicalize_manifest(manifest: Dict[str, Any]) -> str:
    """
    Produce a deterministic JSON string from a dict by:
    - sorting keys
    - using separators without whitespace
    - using smallest necessary representation for numbers
    """
    return json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def features_hash_from_manifest(manifest: Dict[str, Any]) -> str:
    """
    Compute keccak256 hash (0x-prefixed hex) of canonicalized manifest bytes.
    This matches the convention used by the contracts/subgraph for featuresHash.
    """
    canonical = canonicalize_manifest(manifest)
    h = keccak(text=canonical)
    return to_hex(h)  # 0x-prefixed


def to_fixed_int(value: float, scale: int = 10000) -> int:
    """
    Convert a float in [0..1] or other to scaled integer. Caller must ensure input bounds.
    This helper uses bankers rounding to nearest integer.
    """
    dec = Decimal(value) * Decimal(scale)
    # round half up
    dec = dec.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return int(dec)


def normalize_feature_linear(value: float, min_val: float, max_val: float) -> float:
    """
    Normalize raw feature value to [0.0, 1.0] using linear scaling with clipping.
    """
    if max_val == min_val:
        return 0.0
    v = (value - min_val) / (max_val - min_val)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v
