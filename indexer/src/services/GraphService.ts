import { ApolloClient, InMemoryCache, gql, HttpLink } from "@apollo/client";
import fetch from "node-fetch";
import { config } from "../utils/config";

export class GraphService {
  private client: ApolloClient<any>;

  constructor() {
    this.client = new ApolloClient({
      link: new HttpLink({ uri: config.graphEndpoint, fetch }),
      cache: new InMemoryCache()
    });
  }

  async fetchTransactions() {
    const query = gql`
      {
        transactions(first: 50, orderBy: timestamp, orderDirection: desc) {
          id
          from
          to
          value
          timestamp
        }
      }
    `;
    const result = await this.client.query({ query });
    return result.data.transactions;
  }
}
