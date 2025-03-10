import { WEBUI_API_BASE_URL } from '$lib/constants';

// Get third search results
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