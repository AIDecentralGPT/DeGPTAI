import { WEBUI_API_BASE_URL } from '$lib/constants';

// 获取第三方搜索结果
export const thirdSearch = async (token: string, keyword: string, type: string) => {

  let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/third/search`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
    body: JSON.stringify({
			keyword: keyword,
			type: type
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

// 获取网站内容
export const getWebContent = async (token: string, url: string) => {

  let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/third/check_web`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
    body: JSON.stringify({
			url: url
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