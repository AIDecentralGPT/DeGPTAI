import { promptTemplate } from "$lib/utils";

// Obtain all request nodes of De
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
    {
      name: "Korea",
      url: "https://korea-chat.degpt.ai/api",
    }
  ];
  return baseUrls;
};

// Get a list of all De models
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
        name: "DeepSeek R1",
        model: "DeepSeek-R1",
        tip: "DeepSeek R1",
        support: "text",
        desc: "Think deeply and match the performance of o3 in tasks such as mathematics and creative writing"
      },
      {
        name: "DeepSeek V3",
        model: "DeepSeek-V3",
        tip: "DeepSeek V3",
        support: "text",
        desc: "Suitable for most tasks,Performance comparable to GPT-4o"
      },
      {
        name: "Llama3.3",
        model: "Llama3.3-70B",
        tip: "Llama3.3",
        support: "text",
        desc: "Suitable for most tasks"
      },
      {
        name: "Qwen o1",
        model: "Qwen2.5-VL-72B-Instruct",
        tip: "Qwen o1",
        support: "image",
        desc: "Take photos to solve math problems"
      }
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

// Dialogue with De's model
export const generateDeOpenAIChatCompletion = async (
  token: string = "",
  body: object,
  url: string,
  monitorLog: any
): Promise<[Response | null, AbortController]> => {

  let controller: any;
  let res: any;
  let error = null;

  let urlObjs = await getDeBaseUrls();
  let index = urlObjs.findIndex(item => item.url === url);
  if (index !== -1) {
    // Remove this element
    let koreaItem = urlObjs.splice(index, 1)[0];
    // Add this element to the beginning of the array
    urlObjs.unshift(koreaItem);
  }

  let repeatUrl = urlObjs[0];
  let errorUrl = [];
  for (const urlObj of urlObjs) {
    controller = new AbortController();
    try {
      monitorLog.push({fun: body?.model + "de-send-start" + urlObj.url, time: new Date()});
      res = await getDeOpenAIChatCompletion(urlObj, body, controller, true);
      monitorLog.push({fun: body?.model + "de-send-end" + urlObj.url, time: new Date()});
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
          monitorLog.push({fun: body?.model + "de-last-send-start" + urlObj.url, time: new Date()});
          res = await getDeOpenAIChatCompletion(repeatUrl, body, controller, false);
          monitorLog.push({fun: body?.model + "de-last-send-end" + urlObj.url, time: new Date()});
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

// AI session request encapsulation
const getDeOpenAIChatCompletion = async (
  urlObj: any,
  body: Object,
  controller: any,
  timeFlag: boolean
) => {
  let res: any;
  let overallTimeout = null
  if (timeFlag) {
    overallTimeout = setTimeout(() => {
      controller.abort();
      throw new Error('timeout');
    }, 10000);
  }
  res = await fetch(`${urlObj.url}/v0/chat/completion/proxy`, {
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
  }).finally(() => {
    if (overallTimeout) {
      clearTimeout(overallTimeout);
    }
  });

  return res;
}

// Add a brief sentence to the question in the dialogue
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
    // Remove this element
    let koreaItem = urls.splice(index, 1)[0];
    // Add this element to the beginning of the array
    urls.unshift(koreaItem);
  }

  template = promptTemplate(template, prompt);
  model = model=='DeepSeek-R1' ? 'Llama3.3-70B' : model;
  for (const domain of urls) {
    try {
      const result = await fetch(`${domain.url}/v0/chat/completion/proxy`, {
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
        })
      });
      res = await result.json();
      break;
    } catch (err) {
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


// Obtain the final word for the question
export const generateSearchKeyword = async (
  messages: Object,
  url: string
) => {
  let error = null;
  let res: any;

  let urls = await getDeBaseUrls();
  let index = urls.findIndex(item => item.url === url);
  if (index !== -1) {
    // Remove this element
    let koreaItem = urls.splice(index, 1)[0];
    // Add this element to the beginning of the array
    urls.unshift(koreaItem);
  }
  let model = 'Llama3.3-70B';
  for (const domain of urls) {
    try {
      const result = await fetch(`${domain.url}/v0/chat/completion/proxy`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: model,
          // node_id: nodeList?.[0],
          messages: messages,
          stream: false,
          project: "DecentralGPT",
          // Restricting the max tokens to 50 to avoid long titles
          max_tokens: 50,
        })
      });
      res = await result.json();
      break;
    } catch (err) {
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