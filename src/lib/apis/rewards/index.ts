import { WEBUI_API_BASE_URL } from "$lib/constants";

export const creatWalletCheck = async (token: string, id: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/creat_wallet_check`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      id
    })
  })
    .then(async (res) => {
      return await res.json();
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

export const inviteCheck = async (token: string, id: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/invite_check`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      id
    })
  })
    .then(async (res) => {
      return await res.json();
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

export const clockIn = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/clock_in`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      authorization: `Bearer ${token}`,
    },
  })
    .then(async (res) => {
      return await res.json();
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

export const clockInCheck = async (token: string, id: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/clock_in_check`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      id
    })
  })
    .then(async (res) => {
      return await res.json();
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

export const getRewardsCount = async (token: string) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/reward_count`, {
    method: "GET",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      authorization: `Bearer ${token}`,
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

export const getRewardsHistory = async (token: string, page: Object) => {
  let error = null;

  const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/reward_history`, {
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

export const getInviteRewardTotal = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/invite_total`, {
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

export const syncRegisterReward = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/sync_regist_rewards`, {
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

export const syncInviteReward = async (
	token: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/rewards/sync_invite_rewards`, {
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
