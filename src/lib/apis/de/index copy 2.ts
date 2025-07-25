import { DE_API_BASE_URL } from "$lib/constants";
import { promptTemplate } from "$lib/utils";
import { models, settings, user } from "$lib/stores";
import { get } from "svelte/store";

function transformModelData(input) {
  const models = input?.data?.map((model) => {
    return {
      name: model.id.replace("luchenyu/", ""),
      model: model.id,
      modified_at: new Date(model.created * 1000).toISOString(),
      size: 0, // 需要根据实际数据填充
      digest: "", // 需要根据实际数据填充
      details: {
        parent_model: model.parent,
        format: "", // 需要根据实际数据填充
        family: "",
        families: [],
        parameter_size: "",
        quantization_level: "",
      },
      expires_at: "0001-01-01T00:00:00Z",
      urls: [
        0, // 需要根据实际数据填充
      ],
    };
  });

  return { models };
}

// 获取De的所有模型列表
export const getDeModels = async (token: string = "") => {
  let error = null;

  const host = "https://chat.degpt.ai";

  // const host =
  //   window.location.hostname === "localhost"
  //     ? "/modelapi"
  //     : "https://chat.degpt.ai";

  // Ali通用大模型 Qwen2-72B
  // Meta通用大模型 LIama3 70B
  // Google通用大模型Gemma2
  // 代码大模型 Codestral

  const format_res = {
    models: [
      // Meta LLM(LIama3.1-405B)
      {
        name: "Meta LLM (Llama-3.1-405B)",

        model: "Llama-3.1-405B",
        modified_at: new Date().toISOString(),
        size: 0, // 需要根据实际数据填充
        digest: "", // 需要根据实际数据填充
        details: {
          parent_model: "",
          format: "", // 需要根据实际数据填充
          family: "",
          families: [],
          parameter_size: "",
          quantization_level: "",
        },
        expires_at: "0001-01-01T00:00:00Z",
        urls: [
          // "https://chat.degpt.ai/llama3-70b/v1"
          host + "/api",
          // "http://122.99.183.53:1042/v1"
        ],
        source: "Exemplary performance,low error rate,diverse responses.",
        nodeList: ["16Uiu2HAmBcP2Zv51z4VA8UnHRNRjatyHcv4TSuU6pXixLELP1U7F"],
      },
      {
        name: "Ali LLM (Qwen2-72B)",
        model: "Qwen2-72B",
        modified_at: new Date().toISOString(),
        size: 0, // 需要根据实际数据填充
        digest: "", // 需要根据实际数据填充
        details: {
          parent_model: "",
          format: "", // 需要根据实际数据填充
          family: "",
          families: [],
          parameter_size: "",
          quantization_level: "",
        },
        expires_at: "0001-01-01T00:00:00Z",
        urls: [
          // "https://chat.degpt.ai/qwen2-72b/v1"
          host + "/api",
          // "http://122.99.183.53:1042/v1"
        ],
        source: "27 language support, surpport long texts of up to 128 tokens.",
        nodeList: ["16Uiu2HAmPKuJU5VE2PCnydyUn1VcTN2Lt59UDJFFEiRbb7h1x4CV"],
      },

      {
        name: "Google LLM (Gemma-2-27B)",

        model: "Gemma-2-27B",
        modified_at: new Date().toISOString(),
        size: 0, // 需要根据实际数据填充
        digest: "", // 需要根据实际数据填充
        details: {
          parent_model: "",
          format: "", // 需要根据实际数据填充
          family: "",
          families: [],
          parameter_size: "",
          quantization_level: "",
        },
        expires_at: "0001-01-01T00:00:00Z",
        urls: [
          // "https://chat.degpt.ai/llama3-70b/v1"
          host + "/api",
          // "http://122.99.183.53:1042/v1"
        ],
        source: "Exemplary performance,low error rate,diverse responses.",
        nodeList: ["16Uiu2HAmPKuJU5VE2PCnydyUn1VcTN2Lt59UDJFFEiRbb7h1x4CV"],
      },

      // Mistral LLM(Large2-123B)
      {
        name: "Code LLM (Codestral-22B-v0.1)",
        model: "Codestral-22B-v0.1",
        modified_at: new Date().toISOString(),
        size: 0, // 需要根据实际数据填充
        digest: "", // 需要根据实际数据填充
        details: {
          parent_model: "",
          format: "", // 需要根据实际数据填充
          family: "",
          families: [],
          parameter_size: "",
          quantization_level: "",
        },
        expires_at: "0001-01-01T00:00:00Z",
        urls: [host + "/api"],
        source: "Code completion and generation, error detection and repair.",
        nodeList: ["16Uiu2HAmPKuJU5VE2PCnydyUn1VcTN2Lt59UDJFFEiRbb7h1x4CV"],
      },
    ],
  };
  return (format_res?.models ?? []).map((model) => ({
    id: model.model,
    name: model.name ?? model.model,
    ...model,
  }));
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
  token: string = "",
  body: object,
  url: string = DE_API_BASE_URL
): Promise<[Response | null, AbortController]> => {
  const controller = new AbortController();
  setTimeout(() => controller.abort(), 30000);

  let error = null;

  // console.log("generateDeOpenAIChatCompletion url:", url,`${url}/v0/chat/completion`, body);

  /**获取node列表 */
  const model = body?.model;
  const globalModelsSetted = get(models);
  const nodeList = globalModelsSetted?.filter((item) => {
    return item?.model === model;
  })?.[0]?.nodeList;

  const res = await fetch(`${url}/v0/chat/completion`, {
    signal: controller.signal,
    method: "POST",
    headers: {
      // Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ...body,
      project: "DecentralGPT",
      node_id: nodeList?.[0],
      stream: true,
    }),
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
  token: string = "",
  template: string,
  model: string,
  prompt: string,
  url: string = DE_API_BASE_URL
) => {
  let error = null;

  template = promptTemplate(template, prompt);

  console.log("generateDeTitle", url);

  /**获取node列表 */
  const globalModelsSetted = get(models);
  const nodeList = globalModelsSetted?.filter((item) => {
    return item?.model === model;
  })?.[0]?.nodeList;

  console.log("generateDeTitle 222", nodeList);

  const res = await fetch(`${url}/v0/chat/completion`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",

      // Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      model: model,
      node_id: nodeList?.[0],
      messages: [
        {
          role: "user",
          content: template,
        },
      ],
      stream: false,
      project: "DecentralGPT",
      // Restricting the max tokens to 50 to avoid long titles
      max_tokens: 50,
    }),
  })
    .then(async (res) => {
      // if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      if ("detail" in err) {
        error = err.detail;
      }
      return null;
    });

  if (error) {
    throw error;
  }

  return (
    res?.data?.choices[0]?.message?.content.replace(/["']/g, "") ?? "New Chat"
  );
};

export const getDeModelNodeList = async (
  url: string = DE_API_BASE_URL,
  modelId
) => {
  let error = null;

  console.log("getDeModelNodeList", url);

  const res = await fetch(`${url}/v0/ai/projects/peers`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      project: "DecentralGPT",
      // "model": "Codestral-22B-v0.1"
      model: modelId,
    }),
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      if ("detail" in err) {
        error = err.detail;
      }
      return null;
    });

  if (error) {
    throw error;
  }

  console.log("res", res?.data);

  return res;
};
