import { DE_API_BASE_URL } from '$lib/constants';
import { promptTemplate } from '$lib/utils';



function transformModelData(input) {
	const models = input?.data?.map(model => {
			return {
					"name": model.id.replace("luchenyu/", ""),
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

// const host = "http://8.219.75.114:8081"

const host = window.location.hostname === 'localhost' ? "":"http://"+window.location.hostname
	const format_res = {

		models: [
			{
				"name": "Ali General Large Model (Qwen2-72B)",
				"model": "Qwen2-72B",
				"modified_at": new Date().toISOString(),
				"size": 0, // 需要根据实际数据填充
				"digest": "", // 需要根据实际数据填充
				"details": {
						"parent_model": "",
						"format": "", // 需要根据实际数据填充
						"family": "",
						"families": [],
						"parameter_size": "",
						"quantization_level": ""
				},
				"expires_at": "0001-01-01T00:00:00Z",
				"urls": [
						// "https://chat.degpt.ai/qwen2-72b/v1"
					host+	"/modelapi"
						// "http://122.99.183.53:1042/v1"
				],
				"source": '27 language support, surpport long texts of up to 128 tokens.'
				
			},
			
			{
				"name": "Meta General Large Model (Llama3-8B)",
				"model": "Llama3-8B",
				"modified_at": new Date().toISOString(),
				"size": 0, // 需要根据实际数据填充
				"digest": "", // 需要根据实际数据填充
				"details": {
						"parent_model": "",
						"format": "", // 需要根据实际数据填充
						"family": "",
						"families": [],
						"parameter_size": "",
						"quantization_level": ""
				},
				"expires_at": "0001-01-01T00:00:00Z",
				"urls": [
						// "https://chat.degpt.ai/llama3-8b/v1"
					host+	"/modelapi"
						// "http://122.99.183.51:7080/v1"
					],
						"source": 'Multimodal capabilities, wide applicability, excellent performance, and developer-friendly design.'
					// info?.source
		},
		{
			"name": "Meta General Large Model (LIama3 70B)",

			"model": "Llama3-70B",
			"modified_at": new Date().toISOString(),
			"size": 0, // 需要根据实际数据填充
			"digest": "", // 需要根据实际数据填充
			"details": {
					"parent_model": "",
					"format": "", // 需要根据实际数据填充
					"family": "",
					"families": [],
					"parameter_size": "",
					"quantization_level": ""
			},
			"expires_at": "0001-01-01T00:00:00Z",
			"urls": [
					// "https://chat.degpt.ai/llama3-70b/v1"
					host+	"/modelapi"
					// "http://122.99.183.53:1042/v1"
			],
			"source": 'Exemplary performance,low error rate,diverse responses.'
			
	},
		{
			"name": "General Large Model (Yi1.5-34B)",
			"model": "Yi1.5-34B",
			"modified_at": new Date().toISOString(),
			"size": 0, // 需要根据实际数据填充
			"digest": "", // 需要根据实际数据填充
			"details": {
					"parent_model": "",
					"format": "", // 需要根据实际数据填充
					"family": "",
					"families": [],
					"parameter_size": "",
					"quantization_level": ""
			},
			"expires_at": "0001-01-01T00:00:00Z",
			"urls": [
					// "https://chat.degpt.ai/yi15-34b/v1"
					host+	"/modelapi"
					// "http://122.99.183.51:6080/v1"
			],
			"source": 'Powerful encoding, and instruction-following capabilities.'
	},
	// Google通用大模型(Gemma2)代码大模型(Codestral)




// 122.99.183.53:1042  llama3-70b
// 122.99.183.51:6080 yi15-34b
// 122.99.183.51:7080 llama3-8b
// 122.99.183.52:1042 qwen15-110b

// {
// 	"name": "Qwen1.5-110B",
// 	"model": "Qwen1.5-110B",
// 	"modified_at": new Date().toISOString(),
// 	"size": 0, // 需要根据实际数据填充
// 	"digest": "", // 需要根据实际数据填充
// 	"details": {
// 			"parent_model": "",
// 			"format": "", // 需要根据实际数据填充
// 			"family": "",
// 			"families": [],
// 			"parameter_size": "",
// 			"quantization_level": ""
// 	},
// 	"expires_at": "0001-01-01T00:00:00Z",
// 	"urls": [
// 		"https://chat.degpt.ai/qwen1.5-110b/v1"
// 		// "http://122.99.183.52:1042/v1"
// 	]
// },

		]
	}
		

	


	return (format_res?.models ?? [])
		.map((model) => ({ id: model.model, name: model.name ?? model.model, ...model }))
		// .sort((a, b) => {
		// 	return a.name.localeCompare(b.name);
		// });
};

// // 获取De的所有模型列表
// export const getDeModels = async (token: string = '') => {
// 	let error = null;

// 	const res = await fetch(`${DE_API_BASE_URL}/models`, {
// 		method: 'GET',
// 		headers: {
// 			Accept: 'application/json',
// 			'Content-Type': 'application/json',
// 			...(token && { authorization: `Bearer ${token}` })
// 		}
// 	})
// 		.then(async (res) => {
// 			// console.log(123, await res.json());
			
// 			// if (!res.ok) throw await res.json();
// 			// console.log("res.json();", res.json(), res);
			
// 			return res.json();
		
// 		})
// 		.catch((err) => {
// 			console.log(err);
// 			if ('detail' in err) {
// 				error = err.detail;
// 			} else {
// 				error = 'Server connection failed';
// 			}
// 			return null;
// 		});

// 		console.log("res", res);
		

// 	const format_res = transformModelData(res)
// 	console.log(format_res);
	

// 	if (error) {
// 		throw error;
// 	}

// 	return (format_res?.models ?? [])
// 		.map((model) => ({ id: model.model, name: model.name ?? model.model, ...model }))
// 		.sort((a, b) => {
// 			return a.name.localeCompare(b.name);
// 		});
// };



// 和De的模型对话
export const generateDeOpenAIChatCompletion = async (
	token: string = '',
	body: object,
	url: string = DE_API_BASE_URL
): Promise<[Response | null, AbortController]> => {
	const controller = new AbortController();
	let error = null;

	console.log("generateDeOpenAIChatCompletion url:", url,`${url}/v0/chat/completion`, body);
	
	debugger

	const res = await fetch(`${url}/v0/chat/completion`, {
		signal: controller.signal,
		method: 'POST',
		headers: {
			// Authorization: `Bearer ${token}`,
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			...body,
			project: 'DecentralGPT',
			node_id: "16Uiu2HAm5cygUrKCBxtNSMKKvgdr1saPM6XWcgnPyTvK4sdrARGL",
			stream: true,

				// "node_id": "16Uiu2HAm5cygUrKCBxtNSMKKvgdr1saPM6XWcgnPyTvK4sdrARGL",
				// "project": "DecentralGPT",
				// "model": "Llama3-70B",
				// "messages": [
				// 	{
				// 		"role": "system",
				// 		"content": "You are a helpful assistant."
				// 	},
				// 	{
				// 		"role": "user",
				// 		"content": "Hello"
				// 	}
				// ],
				// "stream": true
			
		})
	}).catch((err) => {
		console.log("err", err);
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

	console.log("generateDeTitle", url, );

	const res = await fetch(`${url}/v0/chat/completion`, {
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