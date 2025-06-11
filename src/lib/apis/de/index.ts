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
      // 基础模型
      {
        name: "DeepSeek V3",
        model: "deepseek-chat",
        textmodel: "deepseek-chat",
        think: false,
        tip: "DeepSeek V3",
        support: "text",
        type: 1,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "DouBao-1.5-pro",
        model: "doubao-1.5-vision-pro-250328",
        textmodel: "doubao-1.5-vision-pro-250328",
        think: false,
        tip: "DouBao-1.5-pro",
        support: "text",
        type: 1,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
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
      // 高级模型
      {
        name: "GPT-4o",
        model: "gpt-4o",
        textmodel: "gpt-4o",
        think: false,
        tip: "GPT-4o",
        support: "text",
        type: 2,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Grok3",
        model: "grok-3",
        textmodel: "grok-3",
        think: false,
        tip: "Grok3",
        support: "text",
        type: 2,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Gemini 2.5 Flash",
        model: "gemini-2.5-flash-preview-05-20",
        textmodel: "gemini-2.5-flash-preview-05-20",
        think: false,
        tip: "Gemini 2.5 Flash",
        support: "text",
        type: 2,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "GPT-4.1",
        model: "gpt-4.1",
        textmodel: "gpt-4.1",
        think: false,
        tip: "GPT-4.1",
        support: "text",
        type: 2,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Gemini 2.5 Pro",
        model: "gemini-2.5-pro-preview-06-05",
        textmodel: "gemini-2.5-pro-preview-06-05",
        think: false,
        tip: "Gemini 2.5 Pro",
        support: "text",
        type: 2,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Claude 3.7 Sonnet",
        model: "claude-3-7-sonnet-20250219",
        textmodel: "claude-3-7-sonnet-20250219",
        think: false,
        tip: "Claude 3.7 Sonnet",
        support: "text",
        type: 2,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "DeepSeek R1",
        model: "deepseek-reasoner",
        textmodel: "deepseek-reasoner",
        think: true,
        tip: "DeepSeek R1",
        support: "text",
        type: 2,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "GPT o3",
        model: "o3",
        textmodel: "o3",
        think: false,
        tip: "GPT o3",
        support: "text",
        type: 2,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      // 顶级模型
      {
        name: "Claude 4 Sonnet",
        model: "claude-sonnet-4-20250514",
        textmodel: "claude-sonnet-4-20250514",
        think: false,
        tip: "Claude 4 Sonnet",
        support: "text",
        type: 3,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Claude 4 Opus",
        model: "claude-opus-4-20250514",
        textmodel: "claude-opus-4-20250514",
        think: false,
        tip: "Claude 4 Opus",
        support: "text",
        type: 3,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Claude 4 Opus Thinking",
        model: "claude-opus-4-20250514",
        textmodel: "claude-opus-4-20250514",
        think: true,
        tip: "Claude 4 Opus Thinking",
        support: "text",
        type: 3,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Claude 4 Sonnet Thinking",
        model: "claude-sonnet-4-20250514",
        textmodel: "claude-sonnet-4-20250514",
        think: true,
        tip: "Claude 4 Sonnet Thinking",
        support: "text",
        type: 3,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "GPT o4-mini",
        model: "gpt-4o-mini",
        textmodel: "gpt-4o-mini",
        think: false,
        tip: "GPT o4-mini",
        support: "text",
        type: 3,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "GPT o4-mini high",
        model: "gpt-4o-mini-high",
        textmodel: "gpt-4o-mini-high",
        think: false,
        tip: "GPT o4-mini high",
        support: "text",
        type: 3,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "GPT 4.5",
        model: "gpt-4.5",
        textmodel: "gpt-4.5",
        think: false,
        tip: "GPT 4.5",
        support: "text",
        type: 3,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "GPT o4 Pro",
        model: "gpt-o4-mini-pro",
        textmodel: "gpt-o4-mini-pro",
        think: false,
        tip: "GPT o4 Pro",
        support: "text",
        type: 3,
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
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