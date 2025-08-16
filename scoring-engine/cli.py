"""
Simple CLI to:
- load an example feature manifest (JSON)
- normalize features (based on provided min/max ranges)
- compute normalized ints 0..10000
- compute deterministic score using weights
- compute featuresHash for the manifest
"""

import json
import argparse
from utils import canonicalize_manifest, features_hash_from_manifest, normalize_feature_linear, to_fixed_int
from deterministic import compute_score

# Example normalization ranges per-feature (tune these for production)
FEATURE_RANGES = {
    # feature_name: (min_val, max_val)
    "on_time_repayment_rate": (0.0, 1.0),   # fraction
    "default_count": (0.0, 10.0),           # count (lower is better, we will invert)
    "debt_utilization": (0.0, 5.0),         # e.g., 0.0..5.0 (500% utilization)
    "avg_balance_usd": (0.0, 1_000_000.0),
    "staking_tenure_days": (0.0, 3650.0),
    "gov_participation": (0.0, 1.0),
    "activity_consistency": (0.0, 1.0)
}

# Example weight mapping (names sorted deterministically)
EXAMPLE_WEIGHTS = {
    "on_time_repayment_rate": 3000,  # 30.00
    "default_count": 2500,
    "debt_utilization": 1500,
    "avg_balance_usd": 1000,
    "staking_tenure_days": 500,
    "gov_participation": 800,
    "activity_consistency": 700
}

def invert_linear_norm(x: float, min_v: float, max_v: float) -> float:
    """Some features are 'lower is better' (e.g., default_count). invert before mapping to 0..1"""
    linear = normalize_feature_linear(x, min_v, max_v)
    return 1.0 - linear

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default="../sample_data/example_features.json", help="Path to raw features JSON")
    args = parser.parse_args()

    with open(args.features, "r") as f:
        raw = json.load(f)

    # Map features to a deterministic ordered list
    feature_keys = sorted(EXAMPLE_WEIGHTS.keys())
    normalized_ints = []
    normalized_floats = []

    normalized_manifest = {"features": []}
    for k in feature_keys:
        raw_val = raw.get(k, 0.0)
        min_v, max_v = FEATURE_RANGES[k]
        # handle 'lower is better' for some features:
        if k in ("default_count", "debt_utilization"):
            norm = invert_linear_norm(raw_val, min_v, max_v)
        else:
            norm = normalize_feature_linear(raw_val, min_v, max_v)
        normalized_floats.append(norm)
        fixed = to_fixed_int(norm, scale=10000)
        normalized_ints.append(fixed)
        normalized_manifest["features"].append(fixed)

    # compute score
    weights_list = [EXAMPLE_WEIGHTS[k] for k in feature_keys]
    score = compute_score(normalized_ints, weights_list)

    # manifest -> featuresHash
    manifest = {
        "wallet": raw.get("wallet", "0x0"),
        "features": normalized_manifest["features"],
        "feature_keys": feature_keys,
        "timestamp": raw.get("timestamp", 0)
    }
    canonical = canonicalize_manifest(manifest)
    feat_hash = features_hash_from_manifest(manifest)

    print("Canonical Manifest:", canonical)
    print("FeaturesHash:", feat_hash)
    print("Normalized ints (0..10000):", normalized_ints)
    print("Weights:", weights_list)
    print("Deterministic score (0..10000):", score)
    print("Score as percent: {:.2f}".format(score / 100.0))


if __name__ == "__main__":
    main()
