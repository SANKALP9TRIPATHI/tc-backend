// src/scoring-utils.ts
import { Bytes } from "@graphprotocol/graph-ts";

export function toHexString(b: Bytes): string {
  // returns 0x-prefixed hex
  return b.toHexString();
}
