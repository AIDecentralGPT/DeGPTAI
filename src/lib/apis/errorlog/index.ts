import { WEBUI_API_BASE_URL } from '$lib/constants';


export const addErrorLog = async (name: string, err: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/errorlog/add`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name: name,
			err: err
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};