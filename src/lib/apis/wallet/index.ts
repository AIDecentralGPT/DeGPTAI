// import { WEBUI_API_BASE_URL } from '$lib/constants';




// export const openProServices = async (
// 	tx: string,
// 	amount: number,
// ) => {
// 	let error = null;

// 	const res = await fetch(`${WEBUI_API_BASE_URL}/walletInfo`, {
// 		method: 'POST',
// 		headers: {
// 			Accept: 'application/json',
// 			'Content-Type': 'application/json',
// 			authorization: `Bearer ${token}`
// 		},
// 		body: JSON.stringify({
// 			command: `/${command}`,
// 			title: title,
// 			content: content
// 		})
// 	})
// 		.then(async (res) => {
// 			if (!res.ok) throw await res.json();
// 			return res.json();
// 		})
// 		.then((json) => {
// 			return json;
// 		})
// 		.catch((err) => {
// 			console.log(err);
// 			return null;
// 		});

// 	if (error) {
// 		throw error;
// 	}

// 	return res;
// };
