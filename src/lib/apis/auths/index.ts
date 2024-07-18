import { WEBUI_API_BASE_URL } from "$lib/constants";
import { user } from "$lib/stores";

export const getSessionUser = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
    .then(async (res) => {
      if (!res.ok) throw await res.json();
      return res.json();
    })
    .catch((err) => {
      console.log(err);
      error = err.detail;
      localStorage.removeItem('token')
      printSignIn()

      return null;
    });

  if (error) {
    throw error;
  }

  return res;
};

// // 免登身份校验（根据设备id）
// export const fingerprintSignIn = async (visiterId: string, ) => {
// 	let error = null;

// 	const res = await fetch(`${WEBUI_API_BASE_URL}/auths/fingerprintSignIn`, {
// 		method: 'POST',
// 		headers: {
// 			'Content-Type': 'application/json'
// 		},
// 		body: JSON.stringify({
// 			// email: email,
// 			// password: password
// 			visitor_id: visiterId,
// 		})
// 	})
// 		.then(async (res) => {
// 			if (!res.ok) throw await res.json();
// 			return res.json();
// 		})
// 		.catch((err) => {
// 			console.log(err);

// 			error = err.detail;
// 			return null;
// 		});

// 	if (error) {
// 		throw error;
// 	}

// 	return res;
// };

// 免登身份校验（根据设备id）
export const fingerprintSignIn = async (visiterId: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/signin`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: "",
      password: "",
      visiter_id: visiterId,
    }),
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

export const userSignIn = async (email: string, password: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/signin`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
      password: password,
    }),
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

export const userSignUp = async (
  name: string,
  email: string,
  password: string,
  profile_image_url: string
) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      email: email,
      password: password,
      profile_image_url: profile_image_url,
      id: localStorage.visitor_id,
    }),
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

export const printSignIn = async () => {

  
  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/printSignIn`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: localStorage.visitor_id,
    }),
  });



  // // 每次指纹登录后都删除pair
  // localStorage.removeItem("pair");

  const userInfo = await res.json()

  user.set(userInfo)

  return userInfo;
};

// 登录钱包
export const walletSignIn = async (payload: {
	address: string,
  nonce: string,
  address_type: string,
  data?: any,
  signature: string,
  id: string,
  device_id: string,
  inviter_id?:string
}) => {
  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/walletSignIn`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return await res.json();
};

export const addUser = async (
  token: string,
  name: string,
  email: string,
  password: string,
  role: string = "user"
) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/add`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token && { authorization: `Bearer ${token}` }),
    },
    body: JSON.stringify({
      name: name,
      email: email,
      password: password,
      role: role,
    }),
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

export const updateUserProfile = async (
  token: string,
  name: string,
  profileImageUrl: string
) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/update/profile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token && { authorization: `Bearer ${token}` }),
    },
    body: JSON.stringify({
      name: name,
      profile_image_url: profileImageUrl,
    }),
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

export const updateUserPassword = async (
  token: string,
  password: string,
  newPassword: string
) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/update/password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token && { authorization: `Bearer ${token}` }),
    },
    body: JSON.stringify({
      password: password,
      new_password: newPassword,
    }),
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

export const getSignUpEnabledStatus = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/signup/enabled`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
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

export const getDefaultUserRole = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/signup/user/role`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
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

export const updateDefaultUserRole = async (token: string, role: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/signup/user/role`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      role: role,
    }),
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

export const toggleSignUpEnabledStatus = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/signup/enabled/toggle`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
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

export const getJWTExpiresDuration = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/token/expires`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
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

export const updateJWTExpiresDuration = async (
  token: string,
  duration: string
) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/token/expires/update`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      duration: duration,
    }),
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

export const createAPIKey = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/api_key`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
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
  return res.api_key;
};

export const getAPIKey = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/api_key`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
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
  return res.api_key;
};

export const deleteAPIKey = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/auths/api_key`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
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
