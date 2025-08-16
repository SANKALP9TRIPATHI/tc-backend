"""
Stubbed ZK proof generator client.

This module demonstrates where to:
- prepare inputs for the circuit (e.g. normalized features, weights, public threshold)
- call circom/snarkjs or other tooling to produce a proof
- collect the proof bytes and any public inputs for on-chain verification.

For local dev we show a simulated flow. Replace `run_snarkjs_prove` with actual system calls.
"""

import json
import subprocess
import os
from typing import Dict, Any


def prepare_circuit_input(manifest: Dict[str, Any], weights: Dict[str, int], threshold: int) -> Dict[str, Any]:
    """
    Prepare the JSON inputs consumed by a circom circuit.
    manifest: canonicalized manifest (raw numbers or normalized ints)
    weights: mapping feature -> weight (int 0..10000)
    threshold: int 0..10000 (public)
    """
    inputs = {
        "features": manifest["features"],  # e.g., list of ints 0..10000
        "weights": [weights[k] for k in sorted(weights.keys())],
        "threshold": threshold
    }
    return inputs


def run_snarkjs_prove(circuit_dir: str, input_json_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Example wrapper around snarkjs commands (very high-level).
    Expects compiled circuit and zkey already present in circuit_dir.
    WARNING: This function is a stub; it calls shell commands and you should harden paths in production.
    """
    # Example commands (assuming snarkjs installed in environment):
    # snarkjs groth16 prove circuit_final.zkey input.json proof.json public.json
    zkey = os.path.join(circuit_dir, "circuit_final.zkey")
    proof_json = os.path.join(output_dir, "proof.json")
    public_json = os.path.join(output_dir, "public.json")
    cmd = ["snarkjs", "groth16", "prove", zkey, input_json_path, proof_json, public_json]
    subprocess.run(cmd, check=True)
    with open(proof_json, "r") as f:
        proof = json.load(f)
    with open(public_json, "r") as f:
        public = json.load(f)
    return {"proof": proof, "public": public}
