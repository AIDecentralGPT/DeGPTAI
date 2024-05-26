import { DE_API_BASE_URL } from '$lib/constants';
import { promptTemplate } from '$lib/utils';



function transformModelData(input) {
	const models = input.data.map(model => {
			return {
					"name": model.id,
					"model": model.id,
					"modified_at": new Date(model.created * 1000).toISOString(),
					"size": 0, // 需要根据实际数据填充
					"digest": "", // 需要根据实际数据填充
					"details": {
							"parent_model": model.parent,
							"format": "", // 需要根据实际数据填充
							"family": "",
							"families": [],
							"parameter_size": "",
							"quantization_level": ""
					},
					"expires_at": "0001-01-01T00:00:00Z",
					"urls": [
							0 // 需要根据实际数据填充
					]
			};
	});

	return { models };
}



// 获取De的所有模型列表
export const getDeModels = async (token: string = '') => {
	let error = null;

	const res = await fetch(`${DE_API_BASE_URL}/models`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			...(token && { authorization: `Bearer ${token}` })
		}
	})
		.then(async (res) => {
			console.log(123, res);
			
			// if (!res.ok) throw await res.json();
			// console.log("res.json();", res.json(), res);
			
			return res.json();
		
		})
		.catch((err) => {
			console.log(err);
			if ('detail' in err) {
				error = err.detail;
			} else {
				error = 'Server connection failed';
			}
			return null;
		});

		console.log("res", res);
		

	const format_res = transformModelData(res)
	console.log(format_res);
	

	if (error) {
		throw error;
	}

	return (format_res?.models ?? [])
		.map((model) => ({ id: model.model, name: model.name ?? model.model, ...model }))
		.sort((a, b) => {
			return a.name.localeCompare(b.name);
		});
};



// 和De的模型对话
export const generateDeOpenAIChatCompletion = async (
	token: string = '',
	body: object,
	url: string = DE_API_BASE_URL
): Promise<[Response | null, AbortController]> => {
	const controller = new AbortController();
	let error = null;

	console.log("generateDeOpenAIChatCompletion url:", url);
	

	const res = await fetch(`${url}/chat/completions`, {
		signal: controller.signal,
		method: 'POST',
		headers: {
			Authorization: `Bearer ${token}`,
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			...body,
			stream: true
		})
	}).catch((err) => {
		console.log(err);
		error = err;
		return null;
	});

	if (error) {
		throw error;
	}

	return [res, controller];
};


export const generateDeTitle = async (
	token: string = '',
	template: string,
	model: string,
	prompt: string,
	url: string = DE_API_BASE_URL
) => {
	let error = null;

	template = promptTemplate(template, prompt);

	console.log(template);

	const res = await fetch(`${url}/chat/completions`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			model: model,
			messages: [
				{
					role: 'user',
					content: template
				}
			],
			stream: false,
			// Restricting the max tokens to 50 to avoid long titles
			max_tokens: 50
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			if ('detail' in err) {
				error = err.detail;
			}
			return null;
		});

	if (error) {
		throw error;
	}

	return res?.choices[0]?.message?.content.replace(/["']/g, '') ?? 'New Chat';
};