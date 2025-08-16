import Web3 from "web3";
import { config } from "../utils/config";

export class RPCService {
  private web3: Web3;

  constructor() {
    this.web3 = new Web3(new Web3.providers.HttpProvider(config.rpcEndpoint));
  }

  async getAccountBalance(address: string) {
    return await this.web3.eth.getBalance(address);
  }
}
