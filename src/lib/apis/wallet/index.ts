import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getTransactions = async (address: string) => {
  let error = null;

  const res = await Promise.all([
    fetch(
      `https://www.dbcscan.io/api/v2/addresses/${address}/transactions`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }
    ),
    fetch(`https://www.dbcscan.io/api/v2/addresses/${address}/token-transfers?type=`, {
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

// 获取dbc汇率
export const getDbcRate = async (token: string) => {

  let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/dbc_rate`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
	}).then(async (res) => {
		if (!res.ok) 
      throw await res.json();
    return res.json();
  }).then((json) => {
		return json;
	}).catch((err) => {
		console.log(err);
		return null;
	});
	if (error) {
		throw error;
	}
	return res;
};

// 获取dgc汇率
export const getDgcRate = async (token: string) => {

  let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/dgc_rate`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
	}).then(async (res) => {
		if (!res.ok) 
      throw await res.json();
    return res.json();
  }).then((json) => {
		return json;
	}).catch((err) => {
		console.log(err);
		return null;
	});
	if (error) {
		throw error;
	}
	return res;
};