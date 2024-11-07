import { DE_API_BASE_URL } from "$lib/constants";
import { promptTemplate } from "$lib/utils";

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

        model: "Llama-3.1-Nemotron-70B",
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
        source: "Exemplary performance,low error rate,diverse responses.",
      },
      {
        name: "Ali LLM (Qwen2-72B)",
        model: "Qwen2.5-72B",
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
        source: "27 language support, surpport long texts of up to 128 tokens.",
      },

      {
        name: "Google LLM (Gemma-2-27B)",
        model: "NVLM-D-72B",
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
        source: "Exemplary performance,low error rate,diverse responses.",
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
        source: "Code completion and generation, error detection and repair.",
      },
    ],
  };
  return (format_res?.models ?? []).map((model) => ({
    id: model.model,
    name: model.name ?? model.model,
    ...model,
  }));
};

// 和De的模型对话
export const generateDeOpenAIChatCompletion = async (
  token: string = "",
  body: object,
  url: string = DE_API_BASE_URL
): Promise<[Response | null, AbortController]> => {
  const controller = new AbortController();
  setTimeout(() => controller.abort(), 120000);

  let error = null;

  // console.log("generateDeOpenAIChatCompletion url:", url,`${url}/v0/chat/completion`, body);

  const res = await fetch(`${url}/v0/chat/completion/proxy`, {
    signal: controller.signal,
    method: "POST",
    headers: {
      // Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ...body,
      project: "DecentralGPT",
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

  const res = await fetch(`${url}/v0/chat/completion/proxy`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",

      // Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      model: model,
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
