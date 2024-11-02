import { DE_API_BASE_URL } from "$lib/constants";
import { promptTemplate } from "$lib/utils";

// 获取De的所有模型列表
export const getDeModels = async (token: string = "") => {

  const format_res = {
    models: [
      // Meta LLM(LIama3.1-405B)
      // {
      //   name: "Meta LLM (Llama-3.1-405B)",
      //   model: "Llama-3.1-405B",
      // },
      // Ali LLM (Qwen2-72B)
      {
        name: "Ali LLM (Qwen2.5-72B)",
        model: "Qwen2.5-72B",
      },
      // Nvidia LLM(Nemotron 70B)
      {
        name: "Nvidia LLM(Nemotron 70B)",
        model: "Llama-3.1-Nemotron-70B"
      },
      // Nvidia LLM(Nvidia 3.1)
      {
        name: "Nvidia LLM(Nvidia 3.1)",
        model: "NVLM-D-72B"
      },
      // Nvidia LLM(Nemotron 70B)
      {
        name: "DeepSeek(Coder V2)",
        model: "DeepSeek-Coder-V2"
      },
      // Code LLM (Codestral-22B-v0.1)
      {
        name: "Code LLM (Codestral-22B-v0.1)",
        model: "Codestral-22B-v0.1",
      }
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
    },
    body: JSON.stringify({
      model: model,
      // node_id: nodeList?.[0],
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