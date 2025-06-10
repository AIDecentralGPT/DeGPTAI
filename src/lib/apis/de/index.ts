import { promptTemplate } from "$lib/utils";
import { WEBUI_API_BASE_URL } from '$lib/constants';

// 获取De的所有请求节点
export const getDeBaseUrls = async () => {

  const baseUrls = [
    {
      name: "America",
      url: WEBUI_API_BASE_URL,
    },
    {
      name: "Singapore",
      url: WEBUI_API_BASE_URL,
    },
    {
      name: "Korea",
      url: WEBUI_API_BASE_URL,
    }
  ];
  return baseUrls;
};

// 获取De的所有模型列表
export const getDeModels = async (token: string = "") => {

  const format_res = {
    models: [
      // {
      //   name: "Llama 3.1",
      //   model: "Llama-3.1-405B",
      //   tip: "Llama 3.1",
      //   desc: "Suitable for most tasks"
      // },
      {
        name: "Qwen O3",
        model: "Qwen3-235B-A22B-FP8-think",
        textmodel: "qwen3-235b-a22b",
        think: true,
        tip: "Qwen O3",
        support: "text",
        desc: "Deep thinking,mathematical and writing abilities ≈ o3."
      },
      {
        name: "Qwen3",
        model: "Qwen3-235B-A22B-FP8",
        textmodel: "qwen3-235b-a22b",
        think: false,
        tip: "Qwen3",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "GPT 4.1",
        model: "GPT 4.1",
        textmodel: "gpt-4.1",
        think: false,
        tip: "GPT 4.1",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "O4 mini",
        model: "O4 mini",
        textmodel: "o4-mini",
        think: false,
        tip: "O4 mini",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "O3",
        model: "O3",
        textmodel: "03",
        think: false,
        tip: "O3",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Gemini 2.0",
        model: "gemini-2.0-flash",
        textmodel: "gemini-2.0-flash",
        think: false,
        tip: "Gemini 2.0",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Claude 4",
        model: "claude-opus-4-20250514",
        textmodel: "claude-opus-4-20250514",
        think: false,
        tip: "Claude 4",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "DeepSeek Chat",
        model: "deepseek-chat",
        textmodel: "deepseek-chat",
        think: false,
        tip: "DeepSeek Chat",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "DeepSeek Reasoner",
        model: "deepseek-reasoner",
        textmodel: "deepseek-reasoner",
        think: true,
        tip: "DeepSeek Reasoner",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Doubao Thinking",
        model: "doubao-1.5-thinking-pro-250415",
        textmodel: "doubao-1.5-thinking-pro-250415",
        think: true,
        tip: "Doubao Thinking",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Doubao Vision",
        model: "doubao-1.5-vision-pro-250328",
        textmodel: "doubao-1.5-vision-pro-250328",
        think: false,
        tip: "Doubao Pro",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Doubao 32K",
        model: "doubao-1-5-pro-32k-250115",
        textmodel: "doubao-1-5-pro-32k-250115",
        think: false,
        tip: "Doubao 32K",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Grok3",
        model: "grok-3",
        textmodel: "grok-3",
        think: false,
        tip: "Grok3",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Grok3 Mini",
        model: "grok-3-mini",
        textmodel: "grok-3-mini",
        think: false,
        tip: "Grok3 Mini",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      }
      // {
      //   name: "DeepSeek V3",
      //   model: "DeepSeek-V3-0324",
      //   tip: "DeepSeek V3",
      //   support: "text",
      //   desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      // },
      // {
      //   name: "DeepSeek R1",
      //   model: "DeepSeek-R1",
      //   tip: "DeepSeek R1",
      //   support: "text",
      //   desc: "Deep thinking,mathematical and writing abilities ≈ o3"
      // },
      // {
      //   name: "Llama4",
      //   model: "Llama-4-Scout-Instruct",
      //   tip: "Llama4",
      //   support: "image",
      //   desc: "Suitable for most tasks, taking photos to solve math problems."
      // }
      // {
      //   name: "Pixtral Large 1.0",
      //   model: "Pixtral-124B",
      //   tip: "Pixtral Large 1.0",
      //   support: "image",
      //   desc: "Support image recognition"
      // }
      // {
      //   name: "sana",
      //   model: "sana",
      //   tip: "sana",
      //   support: "image",
      //   desc: "Support image recognition"
      // }
      // {
      //   name: "Qwen 2.5",
      //   model: "Qwen2.5-72B",
      //   tip: "Qwen 2.5",
      //   support: "text",
      //   desc: "Suitable for most tasks"
      // },
      // {
      //   name: "Nemotron 3.1",
      //   model: "Llama-3.1-Nemotron-70B",
      //   tip: "Nemotron 3.1",
      //   support: "text",
      //   desc: "Suitable for most tasks"
      // },
      // {
      //   name: "Nvidia 3.1",
      //   model: "NVLM-D-72B",
      //   tip: "Nvidia 3.1",
      //   support: "image",
      //   desc: "Support image recognition"
      // },
      // {
      //   name: "Deepseek coder2.0",
      //   model: "DeepSeek-Coder-V2",
      //   tip: "Deepseek coder2.0",
      //   support: "text",
      //   desc: "Optimize code writing"
      // },
      // {
      //   name: "Codestral 0.1", 
      //   model: "Codestral-22B-v0.1",
      //   tip: "Codestral 0.1",
      //   desc: "Optimize code writing"
      // },
      // {
      //   name: "Qwen 2.5 Code",
      //   model: "Qwen2.5-Coder-32B",
      //   tip: "Qwen 2.5 Code",
      //   support: "text",
      //   desc: "Optimize code writing"
      // }
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
  url: string,
): Promise<[Response | null, AbortController]> => {

  let controller: any;
  let res: any;
  let error = null;

  let urlObjs = await getDeBaseUrls();
  let index = urlObjs.findIndex(item => item.url === url);
  if (index !== -1) {
    // 移除该元素
    let koreaItem = urlObjs.splice(index, 1)[0];
    // 将该元素添加到数组的开头
    urlObjs.unshift(koreaItem);
  }

  let repeatUrl = urlObjs[0];
  let errorUrl = [];
  for (const urlObj of urlObjs) {
    controller = new AbortController();
    try {
      res = await getDeOpenAIChatCompletion(urlObj, body, controller, true, token);
      if (res.status == 200) {
        break;
      } else {
        throw new Error("error");
      } 
    } catch (err) {
      controller.abort();
      if (err?.message == "error") {
        errorUrl.push(urlObj);
      }
      if (urlObj.name === urlObjs[urlObjs.length-1].name) {
        try {
          let checkUrl = urlObjs.filter(item =>!errorUrl.includes(item));
          if (checkUrl.length > 0 && !checkUrl.includes(repeatUrl)) {
            repeatUrl = checkUrl[0];
          }
          controller = new AbortController();
          res = await getDeOpenAIChatCompletion(repeatUrl, body, controller, false);
          if (res.status == 200) {
            break;
          } else {
            throw new Error("error");
          }
        } catch(err) {
          error = err;
          res = null;
        }
      }
    }
  }
  

  if (error) {
    throw error;
  }
  
  return [res, controller];
};

// ai会话请求封装
const getDeOpenAIChatCompletion = async (
  urlObj: any,
  body: Object,
  controller: any,
  timeFlag: boolean,
  token:  string = ""
) => {
  let res: any;
  let overallTimeout = null
  if (timeFlag) {
    overallTimeout = setTimeout(() => {
      controller.abort();
      throw new Error('timeout');
    }, 10000);
  }
  res = await fetch(`${urlObj.url}/chat/completion/proxy`, {
    signal: controller.signal,
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ...body,
      project: "DecentralGPT",
      stream: true,
    }),
  }).finally(() => {
    if (overallTimeout) {
      clearTimeout(overallTimeout);
    }
  });

  return res;
}

// 型对话给提问内容添加一个简语
export const generateDeTitle = async (
  token: string = "",
  template: string,
  model: string,
  prompt: string,
  url: string
) => {
  let error = null;
  let res: any;

  let urls = await getDeBaseUrls();
  let index = urls.findIndex(item => item.url === url);
  if (index !== -1) {
    // 移除该元素
    let koreaItem = urls.splice(index, 1)[0];
    // 将该元素添加到数组的开头
    urls.unshift(koreaItem);
  }

  template = promptTemplate(template, prompt);
  model = 'qwen3-235b-a22b';
  for (const domain of urls) {
    try {
      const result = await fetch(`${domain.url}/chat/completion/proxy`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
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
          enable_thinking: false
        })
      });
      res = await result.json();
      break;
    } catch (err) {
      console.log("会话TITLE-ERROR", "域名：" + domain.name + "请求失败");
      if (domain.name == urls[urls.length - 1].name) {
        error = err;
      }
    }
  }

  if (error) {
    throw error;
  }

  return (
    res?.choices[0]?.message?.content.replace(/["']/g, "") ?? "New Chat"
  );
};


// 获取最后提问的词语
export const generateSearchKeyword = async (
  token: string = "",
  messages: Object,
  content: string,
  url: string
) => {
  let error = null;
  let res: any;

  let urls = await getDeBaseUrls();
  let index = urls.findIndex(item => item.url === url);
  if (index !== -1) {
    // 移除该元素
    let koreaItem = urls.splice(index, 1)[0];
    // 将该元素添加到数组的开头
    urls.unshift(koreaItem);
  }
  let model = 'qwen3-235b-a22b';
  for (const domain of urls) {
    try {
      const result = await fetch(`${domain.url}/chat/completion/proxy`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          model: model,
          // node_id: nodeList?.[0],
          messages: messages,
          stream: false,
          project: "DecentralGPT",
          // Restricting the max tokens to 50 to avoid long titles
          max_tokens: 50,
          enable_thinking: false
        })
      });
      res = await result.json();
      break;
    } catch (err) {
      console.log("会话TITLE-ERROR", "域名：" + domain.name + "请求失败");
      if (domain.name == urls[urls.length - 1].name) {
        error = err;
      }
    }
  }

  if (error) {
    throw error;
  }
  return (
    res?.choices[0]?.message?.content.replace(/["']/g, "") ?? content
  );
};