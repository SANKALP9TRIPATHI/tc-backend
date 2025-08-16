import dotenv from "dotenv";
dotenv.config();

export const config = {
  graphEndpoint: process.env.GRAPH_ENDPOINT || "",
  rpcEndpoint: process.env.RPC_ENDPOINT || "",
  db: {
    user: process.env.DB_USER || "postgres",
    password: process.env.DB_PASSWORD || "",
    host: process.env.DB_HOST || "localhost",
    port: Number(process.env.DB_PORT) || 5432,
    database: process.env.DB_NAME || "credit_score"
  }
};
