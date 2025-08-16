"""
Deterministic scoring implementation that mirrors ScoreCalculator.sol logic.

Inputs:
- normalized_features: list[int] each in range 0..10000 (fixed point 2 decimals)
- weights: list[int] each in range 0..10000 (fixed point)
Output:
- final_score: int in range 0..10000

Computation:
acc = sum(weights[i] * features[i])
sumWeights = sum(weights)
finalScore = acc // sumWeights
This matches the Solidity logic: integer arithmetic, no floating rounding on-chain.
"""

from typing import List


def compute_score(normalized_features: List[int], weights: List[int]) -> int:
    if len(normalized_features) != len(weights):
        raise ValueError("Feature and weight length mismatch")
    if len(weights) == 0:
        raise ValueError("No weights set")
    acc = 0
    for f, w in zip(normalized_features, weights):
        # both f and w expected to be <= 10000, product <= 1e8 fits in Python int easily
        acc += int(f) * int(w)
    sum_weights = sum(int(w) for w in weights)
    if sum_weights == 0:
        raise ValueError("Sum of weights is zero")
    final_score = acc // sum_weights  # integer division like solidity
    # final_score should be in 0..10000
    return int(final_score)
