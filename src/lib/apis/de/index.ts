import { promptTemplate } from "$lib/utils";

// 获取De的所有请求节点
export const getDeBaseUrls = async () => {

  const baseUrls = [
    {
      name: "North America",
      url: "https://usa-chat.degpt.ai/api",
    },
    {
      name: "Asia",
      url: "https://singapore-chat.degpt.ai/api",
    },
    {
      name: "Europe",
      url: "https://malaysia-chat.degpt.ai/api",
    },
    {
      name: "Others",
      url: "https://korea-chat.degpt.ai/api",
    }
  ];
  return baseUrls;
};

// 获取De的所有模型列表
export const getDeModels = async (token: string = "") => {

  const format_res = {
    models: [
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
  url: string
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
  url: string
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