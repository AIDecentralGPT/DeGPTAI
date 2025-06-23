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
        desc: "Suitable for reasoning and writing",
        modelicon: "/static/icon/deepseek.png",
        modelinfo: ""
      },
      {
        name: "DouBao 1.6 (Tiktok)",
        model: "doubao-seed-1-6-250615",
        textmodel: "doubao-seed-1-6-250615",
        think: false,
        tip: "DouBao 1.6 (Tiktok)",
        support: "image",
        type: 1,
        desc: "Multimodal, suitable for daily tasks",
        modelicon: "/static/icon/doubao.png",
        modelinfo: ""
      },
      {
        name: "Qwen3 (阿里云)",
        model: "Qwen3-235B-A22B-FP8",
        textmodel: "qwen3-235b-a22b",
        think: false,
        tip: "Qwen3 (阿里云)",
        support: "text",
        type: 1,
        desc: "Strong language skills",
        modelicon: "/static/icon/qwen.png",
        modelinfo: ""
      },
      {
        name: "Qwen3 Thinking (阿里云)",
        model: "Qwen3-235B-A22B-FP8-think",
        textmodel: "qwen3-235b-a22b",
        think: true,
        tip: "Qwen3 Thinking (阿里云)",
        support: "text",
        type: 1,
        desc: "Enhanced reasoning, suitable for complex tasks",
        modelicon: "/static/icon/qwen.png",
        modelinfo: ""
      },
      {
        name: "GPT-4o mini (OpenAI)",
        model: "gpt-4o-mini",
        textmodel: "gpt-4o-mini",
        think: false,
        tip: "GPT-4o mini (OpenAI)",
        support: "image",
        type: 1,
        desc: "Lightweight general-purpose model with fast response speed",
        modelicon: "/static/icon/gpt3.png",
        modelinfo: ""
      },
      // 高级模型
      {
        name: "GPT-4o (OpenAI)",
        model: "gpt-4o",
        textmodel: "gpt-4o",
        think: false,
        tip: "GPT-4o (OpenAI)",
        support: "text",
        type: 2,
        desc: "Multimodal, suitable for most tasks",
        modelicon: "/static/icon/gpt_round.png",
        modelinfo: ""
      },
      {
        name: "GPT-4.1 mini(Google)",
        model: "gpt-4.1-mini",
        textmodel: "gpt-4.1-mini",
        think: false,
        tip: "GPT-4.1 mini(Google)",
        support: "text",
        type: 2,
        desc: "Well-suited for handling daily tasks",
        modelicon: "/static/icon/gpt_round.png",
        modelinfo: ""
      },
      {
        name: "DeepSeek R1",
        model: "deepseek-reasoner",
        textmodel: "deepseek-reasoner",
        think: true,
        tip: "DeepSeek R1",
        support: "text",
        type: 2,
        desc: "Strong writing and coding skills",
        modelicon: "/static/icon/deepseek.png",
        modelinfo: ""
      },
      {
        name: "Gemini 2.5 Flash(Google)",
        model: "gemini-2.5-flash-preview-05-20",
        textmodel: "gemini-2.5-flash-preview-05-20",
        think: false,
        tip: "Gemini 2.5 Flash(Google)",
        support: "text",
        type: 2,
        desc: "Multimodal with fast response",
        modelicon: "/static/icon/gemini.png",
        modelinfo: ""
      },
      {
        name: "Grok 3 (Elon Musk)",
        model: "grok-3",
        textmodel: "grok-3",
        think: false,
        tip: "Grok 3 (Elon Musk)",
        support: "image",
        type: 2,
        desc: "Expert in Q&A, lively expression style",
        modelicon: "/static/icon/grok.png",
        modelinfo: ""
      },
      {
        name: "Claude 3.7 Sonnet (Anthropic)",
        model: "claude-3-7-sonnet-20250219",
        textmodel: "claude-3-7-sonnet-20250219",
        think: false,
        tip: "Claude 3.7 Sonnet (Anthropic)",
        support: "text",
        type: 2,
        desc: "Strong writing ability, high stability",
        modelicon: "/static/icon/claude.png",
        modelinfo: ""
      },
      {
        name: "DouBao 1.6 Thinking (Tiktok)",
        model: "doubao-seed-1-6-thinking-250615",
        textmodel: "doubao-seed-1-6-thinking-250615",
        think: true,
        tip: "DouBao 1.6 Thinking (Tiktok)",
        support: "image",
        type: 2,
        desc: "Multimodal with enhanced reasoning",
        modelicon: "/static/icon/doubao.png",
        modelinfo: ""
      },
      // 顶级模型
      {
        name: "GPT o3 (OpenAI)",
        model: "o3-mini",
        textmodel: "o3-mini",
        think: false,
        tip: "GPT o3 (OpenAI)",
        support: "text",
        type: 3,
        desc: "Using advanced reasoning",
        modelicon: "/static/icon/gpt_round.png",
        modelinfo: ""
      },
      {
        name: "GPT-4.1 (OpenAI)",
        model: "gpt-4.1",
        textmodel: "gpt-4.1",
        think: false,
        tip: "GPT-4.1 (OpenAI)",
        support: "text",
        type: 3,
        desc: "Good at fast coding and analysis",
        modelicon: "/static/icon/gpt_round.png",
        modelinfo: ""
      },
      {
        name: "GPT 4.5 (OpenAI)",
        model: "gpt-4.5-preview",
        textmodel: "gpt-4.5-preview",
        think: false,
        tip: "GPT 4.5 (OpenAI)",
        support: "text",
        type: 3,
        desc: "Skilled in writing and generating ideas",
        modelicon: "/static/icon/gpt_round.png",
        modelinfo: ""
      },
      {
        name: "Claude 4 Sonnet (Anthropic)",
        model: "claude-sonnet-4-20250514",
        textmodel: "claude-sonnet-4-20250514",
        think: false,
        tip: "Claude 4 Sonnet (Anthropic)",
        support: "text",
        type: 3,
        desc: "Strong general capabilities, stable writing",
        modelicon: "/static/icon/claude.png",
        modelinfo: ""
      },
      {
        name: "Claude 4Opus (Anthropic)",
        model: "claude-opus-4-20250514",
        textmodel: "claude-opus-4-20250514",
        think: false,
        tip: "Claude 4Opus (Anthropic)",
        support: "text",
        type: 3,
        desc: "Strongest in coding, suitable for complex tasks",
        modelicon: "/static/icon/claude.png",
        modelinfo: ""
      },
      {
        name: "Claude 4 Opus Thinking (Anthropic)",
        model: "claude-opus-4-20250514-think",
        textmodel: "claude-opus-4-20250514",
        think: true,
        tip: "Claude 4 Opus Thinking (Anthropic)",
        support: "text",
        type: 3,
        desc: "Deep reasoning enhancement",
        modelicon: "/static/icon/claude.png",
        modelinfo: ""
      },
      {
        name: "Claude 4 Sonnet Thinking (Anthropic)",
        model: "claude-sonnet-4-20250514-think",
        textmodel: "claude-sonnet-4-20250514",
        think: true,
        tip: "Claude 4 Sonnet Thinking (Anthropic)",
        support: "text",
        type: 3,
        desc: "Enhanced contextual understanding and structural reasoning",
        modelicon: "/static/icon/claude.png",
        modelinfo: ""
      },
      {
        name: "Grok 3 Thinking (Elon Musk)",
        model: "grok-3-mini",
        textmodel: "grok-3-mini",
        think: true,
        tip: "Grok 3 Thinking (Elon Musk)",
        support: "image",
        type: 3,
        desc: "Strengthened logical reasoning and knowledge expression",
        modelicon: "/static/icon/grok.png",
        modelinfo: ""
      },
      {
        name: "Gemini 2.5 Pro",
        model: "gemini-2.5-pro-preview-06-05",
        textmodel: "gemini-2.5-pro-preview-06-05",
        think: false,
        tip: "Gemini 2.5 Pro",
        support: "text",
        type: 3,
        desc: "Powerful multimodal capabilities, proficient in graphics, text, and code",
        modelicon: "/static/icon/gemini.png",
        modelinfo: ""
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