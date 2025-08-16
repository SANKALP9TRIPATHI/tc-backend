// src/mapping.ts
import { BigInt, Bytes, log } from "@graphprotocol/graph-ts";
import {
  AttestationPosted as AttestationPostedEvent
} from "../generated/ScoreRegistry/ScoreRegistry";
import { WeightsUpdated as WeightsUpdatedEvent } from "../generated/ScoreCalculator/ScoreCalculator";

import { Wallet, Attestation, FeatureManifest, ScoreCalculatorUpdate } from "../generated/schema";
import { toHexString } from "./scoring-utils";

export function handleAttestationPosted(event: AttestationPostedEvent): void {
  // event params: (address indexed wallet, address indexed attestor, bytes32 featuresHash, uint16 score, uint256 timestamp)
  let walletAddr = event.params.wallet.toHexString();
  let attestorAddr = event.params.attestor;
  let featuresHash = event.params.featuresHash;
  let score = event.params.score;
  let timestamp = event.params.timestamp;

  // Attestation entity id: combine txHash and logIndex for uniqueness
  let txHash = event.transaction.hash;
  let logIndex = event.logIndex.toI32();
  let attestationId = txHash.toHexString() + "-" + logIndex.toString();

  // load or create Wallet entity
  let wallet = Wallet.load(walletAddr);
  if (wallet == null) {
    wallet = new Wallet(walletAddr);
    wallet.attestationCount = 0;
    wallet.createdAt = event.block.timestamp;
  }

  // create Attestation
  let a = new Attestation(attestationId);
  a.wallet = wallet.id;
  a.attestor = attestorAddr;
  a.featuresHash = featuresHash;
  a.score = score;
  a.metadata = ""; // metadata not available in typed event - might be added via logs or contract
  a.timestamp = timestamp;
  a.txHash = txHash;
  a.save();

  // update wallet
  wallet.latestScore = score as i32;
  wallet.latestAttestation = a.id;
  wallet.attestationCount = wallet.attestationCount + 1;
  wallet.save();

  // Create a FeatureManifest entity (if not exists) so indexing node can later resolve IPFS manifest
  let featuresId = toHexString(featuresHash);
  let fm = FeatureManifest.load(featuresId);
  if (fm == null) {
    fm = new FeatureManifest(featuresId);
    fm.featuresHash = featuresHash;
    fm.manifestURI = ""; // offchain indexer should populate manifestURI by matching featuresHash -> IPFS
    fm.createdAt = event.block.timestamp;
    fm.save();
  }
}

export function handleWeightsUpdated(event: WeightsUpdatedEvent): void {
  // event: WeightsUpdated(uint16[] newWeights)
  let updater = event.transaction.from;
  let updateId = event.transaction.hash.toHexString() + "-" + event.logIndex.toString();
  let su = new ScoreCalculatorUpdate(updateId);
  su.updater = updater;
  // We cannot directly store array in GraphQL scalar — serialize to JSON-like string
  let weights = event.params.newWeights;
  let weightStr = "[";
  for (let i = 0; i < weights.length; i++) {
    weightStr += weights[i].toString();
    if (i < weights.length - 1) {
      weightStr += ",";
    }
  }
  weightStr += "]";
  su.weights = weightStr;
  su.timestamp = event.block.timestamp;
  su.txHash = event.transaction.hash;
  su.save();
}
