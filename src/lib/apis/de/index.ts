import { promptTemplate } from "$lib/utils";

// 获取De的所有请求节点
export const getDeBaseUrls = async () => {

  const baseUrls = [
    {
      name: "America",
      url: "https://usa-chat.degpt.ai/api",
    },
    {
      name: "Singapore",
      url: "https://singapore-chat.degpt.ai/api",
    },
    // {
    //   name: "Europe",
    //   url: "https://malaysia-chat.degpt.ai/api",
    // },
    {
      name: "Korea",
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
        name: "Llama 3.1",
        model: "Llama-3.1-405B",
        tip: "Llama 3.1",
        desc: "Suitable for most tasks"
      },
      // Ali LLM (Qwen2.5-72B)
      {
        name: "Qwen 2.5",
        model: "Qwen2.5-72B",
        tip: "Qwen 2.5",
        desc: "Suitable for most tasks"
      },
      // Nvidia LLM(Nemotron 70B)
      {
        name: "Nemotron 3.1", 
        model: "Llama-3.1-Nemotron-70B",
        tip: "Nemotron 3.1",
        desc: "Suitable for most tasks"
      },
      // Nvidia LLM(Nvidia 3.1)
      {
        name: "Nvidia 3.1",
        model: "NVLM-D-72B",
        tip: "Nvidia 3.1",
        desc: "Support image recognition"
      },
      // DeepSeek(Coder V2)
      {
        name: "Deepseek coder2.0", 
        model: "DeepSeek-Coder-V2",
        tip: "Deepseek coder2.0",
        desc: "Optimize code writing"
      },
      // Code LLM (Codestral-22B-v0.1)
      // {
      //   name: "Codestral 0.1", 
      //   model: "Codestral-22B-v0.1",
      //   tip: "Codestral 0.1",
      //   desc: "Optimize code writing"
      // },
      {
        name: "Qwen 2.5 Code", 
        model: "Qwen2.5-Coder-32B",
        tip: "Qwen 2.5 Code",
        desc: "Optimize code writing"
      }
    ],
  };
  return (format_res?.models ?? []).map((model) => ({
    id: model.model,
    name: model.name ?? model.model,
    ...model,
  }));
};

// 和De的模型对话给提问内容添加一个简语
export const generateDeOpenAIChatCompletion = async (
  token: string = "",
  body: object,
  url: string
): Promise<[Response | null, AbortController]> => {
  const controller = new AbortController();
  setTimeout(() => controller.abort(), 300000);

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

// 型对话给提问内容添加一个简语
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
    res?.choices[0]?.message?.content.replace(/["']/g, "") ?? "New Chat"
  );
};