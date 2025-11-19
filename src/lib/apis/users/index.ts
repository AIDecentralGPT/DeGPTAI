import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getUsersInvited = async (token: string, inviter_id: string) => {
	let error = null;


	const res = await fetch(`${WEBUI_API_BASE_URL}/users/invited`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};


export const getUserPermissions = async (token: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/permissions/user`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const updateUserPermissions = async (token: string, permissions: object) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/permissions/user`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			...permissions
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const updateUserRole = async (token: string, id: string, role: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/update/role`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			id: id,
			role: role
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getUsers = async (token: string,page:number, role: string = "", search: string = "", verified: string = "", channel: string = "") => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users?skip=${page}&limit=10&role=${role}&search=${search}&verified=${verified}&channel=${channel}`, {
			method: 'GET',
			headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
			}
	})

		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res ? res : [];
};

export const getUserById = async (token: string, userId: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/${userId}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const deleteUserById = async (token: string, userId: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/${userId}`, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

type UserUpdateForm = {
	profile_image_url: string;
	email: string;
	name: string;
	password: string;
};

export const updateUserById = async (token: string, userId: string, user: UserUpdateForm) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/${userId}/update`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			profile_image_url: user.profile_image_url,
			email: user.email,
			name: user.name, // 存放钱包地址
			password: user.password !== '' ? user.password : undefined
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};



export const openProServices = async (
	token: string,
	tx: string,
	amount: number,
	vip: string,
	viptime: string,
	binanceflag: boolean
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/pro`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			tx,
			amount,
			vip,
			viptime,
			binanceflag
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};



export const isPro = async (
	token: string,
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/is_pro`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},

	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};


export const getUserInfo = async (
	token: string,
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/get_user_info`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},

	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const updateUserModels = async (
	token: string,
	models: string,
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/update/models`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			models
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const updateUserLanguage = async (
	token: string,
	language: string,
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/update/language`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			language
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getDisperTotal = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/disper/total`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getDisperUser = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/disper/user`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getThirdTotal = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/third/total`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getdisperVip = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/disper/vip`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getRewardsTotal = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/users/regist/total`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getThirdPage = async (token: string, page: Object) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/users/third/list`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(page)
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .then((json) => {
      return json;
    })
    .catch((err) => {
      console.log(err);
      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

export const getDailyUserLine = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/daily/line`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};
