import { WEBUI_API_BASE_URL } from '$lib/constants';

type DataForm = {
	name: string;
	start_time: string;
	end_time: string;
};

export const addRewardDate = async (token: string, data: DataForm) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/rewarddate/add`, {
			method: 'POST',
			headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
			},
			body: JSON.stringify(data)
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

	const res = await fetch(`${WEBUI_API_BASE_URL}/rewarddate/list?skip=${page}&limit=10&search=${search}&status=${status}`, {
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

export const getById = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/${userId}`, {
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

	return res;
};

export const deleteById = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/${id}`, {
		method: 'DELETE',
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

export const updateById = async (token: string, id: string, data: DataForm) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/${id}/update`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify(data)
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

export const switchStatus = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/rewarddate/${id}/status`, {
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
