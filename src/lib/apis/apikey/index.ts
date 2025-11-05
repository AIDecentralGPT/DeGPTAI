import { WEBUI_API_BASE_URL } from '$lib/constants';

export const addApiKey = async (token: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/apikey/add`, {
			method: 'POST',
			headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
			}
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

	return res ? res : [];
};

export const getList = async (token: string,page:number, search: string = "", status: string = "") => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/apikey/list?skip=${page}&limit=10&search=${search}&status=${status}`, {
			method: 'GET',
			headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
			}
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

	return res ? res : [];
};

export const switchStatus = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/apikey/${id}/status`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
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
