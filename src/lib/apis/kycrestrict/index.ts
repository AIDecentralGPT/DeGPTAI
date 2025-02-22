import { WEBUI_API_BASE_URL } from '$lib/constants';

export const checkKyc = async (token: string) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/kyc/check_kyc`, {
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


export const bindCaptcha = async (token: string, captcha_code: string) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/kyc/bind_captcha`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
    body: JSON.stringify({
			captcha_code: captcha_code
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

export const bindTracking = async (token: string, tracking: string) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/kyc/bind_tracking`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
    body: JSON.stringify({
			tracking: tracking
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