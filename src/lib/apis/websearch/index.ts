import { WEBUI_API_BASE_URL } from '$lib/constants';

// 获取tavily搜索结果
export const tavilySearch = async (token: string, keywords: string) => {

  let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/tavily/search`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
    body: JSON.stringify({
			keywords: keywords
		})
	}).then(async (res) => {
		if (!res.ok) 
      throw await res.json();
    return res.json();
  }).then((json) => {
		return json;
	}).catch((err) => {
		console.log(err);
		return null;
	});
	if (error) {
		throw error;
	}
	return res;
};