// import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getTransactions = async (address: string) => {
  let error = null;

  const res = await Promise.all([
    fetch(
      `https://blockscout-testnet.dbcscan.io/api/v2/addresses/${address}/transactions`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }
    ),
    fetch(`https://blockscout-testnet.dbcscan.io/api/v2/addresses/${address}/token-transfers?type=`, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }),
  ]);

  if (!res[0].ok || !res[1].ok) {
    error = await res[0].json();
    throw error;
  }

  const json = await Promise.all([res[0].json(), res[1].json()]);
  return json;
};