import { WEBUI_BASE_URL } from '$lib/constants';

export const getBackendConfig = async () => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/config`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const defaultBackendConfig = async () => {
	return {
    "status": true,
    "name": "DeGPT",
    "version": "0.1.125",
    "auth": true,
    "default_locale": "en-US",
    "images": false,
    "default_models": "Qwen3-235B-A22B-FP8-think",
    "default_prompt_suggestions": [
				{
					"title": [
							"Webpage Subscription and Data Insights",
							"Automatically crawl the subscribed content on web pages through a large model and conduct data analysis."
					],
					"content": "Please paste the website domain name"
				},
        {
            "title": [
                "Help me study",
                "vocabulary for a college entrance exam"
            ],
            "content": "Help me study vocabulary: write a sentence for me to fill in the blank, and I'll try to pick the correct option."
        },
        {
            "title": [
                "Give me ideas",
                "for what to do with my kids' art"
            ],
            "content": "What are 5 creative things I could do with my kids' art? I don't want to throw them away, but it's also so much clutter."
        },
				{
					"title": [
							"Tell me a fun fact",
							"about the Roman Empire"
					],
					"content": "Tell me a random fun fact about the Roman Empire"
				},
        {
            "title": [
                "Show me a code snippet",
                "of a website's sticky header"
            ],
            "content": "Show me a code snippet of a website's sticky header in CSS and JavaScript."
        },
        {
            "title": [
                "Explain options trading",
                "if I'm familiar with buying and selling stocks"
            ],
            "content": "Explain options trading in simple terms if I'm familiar with buying and selling stocks."
        },
        {
            "title": [
                "Overcome procrastination",
                "give me tips"
            ],
            "content": "Could you start by asking me about instances when I procrastinate the most and then give me some suggestions to overcome it?"
        },
        {
            "title": [
                "Grammar check",
                "rewrite it for better readability "
            ],
            "content": "Check the following sentence for grammar and clarity: '[sentence]'. Rewrite it for better readability while maintaining its original meaning."
        }
    ],
    "trusted_header_auth": false,
    "admin_export_enabled": true
	}
};

export const getChangelog = async () => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/changelog`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getVersionUpdates = async () => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/version/updates`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getModelFilterConfig = async (token: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/config/model/filter`, {
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
			error = err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const updateModelFilterConfig = async (
	token: string,
	enabled: boolean,
	models: string[]
) => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/config/model/filter`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			enabled: enabled,
			models: models
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getWebhookUrl = async (token: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/webhook`, {
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
			error = err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res.url;
};

export const updateWebhookUrl = async (token: string, url: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/webhook`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			url: url
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res.url;
};
