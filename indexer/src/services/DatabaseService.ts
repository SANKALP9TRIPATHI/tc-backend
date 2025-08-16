import { Pool } from "pg";
import { config } from "../utils/config";
import { logger } from "../utils/logger";

export class DatabaseService {
  private pool: Pool;

  constructor() {
    this.pool = new Pool(config.db);
  }

  async saveTransaction(data: any) {
    const query = `
      INSERT INTO transactions (user_address, tx_hash, amount, timestamp)
      VALUES ($1, $2, $3, $4)
      ON CONFLICT DO NOTHING;
    `;
    await this.pool.query(query, [data.user, data.hash, data.amount, data.timestamp]);
    logger.info(`Saved transaction ${data.hash}`);
  }

  async saveStaking(data: any) {
    const query = `
      INSERT INTO staking (user_address, amount, timestamp)
      VALUES ($1, $2, $3)
      ON CONFLICT DO NOTHING;
    `;
    await this.pool.query(query, [data.user, data.amount, data.timestamp]);
    logger.info(`Saved staking for ${data.user}`);
  }

  async saveDeFi(data: any) {
    const query = `
      INSERT INTO defi_interactions (user_address, protocol, action, amount, timestamp)
      VALUES ($1, $2, $3, $4, $5)
      ON CONFLICT DO NOTHING;
    `;
    await this.pool.query(query, [
      data.user,
      data.protocol,
      data.action,
      data.amount,
      data.timestamp
    ]);
    logger.info(`Saved DeFi interaction for ${data.user}`);
  }
}
