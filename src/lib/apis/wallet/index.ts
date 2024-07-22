// import { WEBUI_API_BASE_URL } from '$lib/constants';




export const getTransactions = async (
	address: string
) => {
	let error = null;

	const res = await fetch(`https://blockscout-testnet.dbcscan.io/api/v2/addresses/${address}/transactions`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
	
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};
