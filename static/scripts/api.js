const BASE_URL = "/api";

async function request(method, route, token = null, body = null) {
  let options = {
    method: method,
    credentials: "include",
    headers: { "Content-Type": "application/json" },
  };
  if (token) {
    options.headers["Authorization"] = `Bearer ${token}`;
  }

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const res = await fetch(`${BASE_URL}${route}`, options);
    return res;
  } catch (err) {
    console.error("Fetch error:", err);
  }
}

export async function login(email, password) {
  let body = {
    email: email,
    password: password,
  };
  return await request("POST", "/auth/login", null, body);
}

export async function createAccount(email, password) {
  let body = {
    email: email,
    password: password,
  };
  return await request("POST", "/auth/register", null, body);
}

export async function getUserData(token) {
  return await request("GET", "/users/me", token, null);
}

export async function register(type, amount, description, token) {
  let body = {
    amount: amount,
    description: description,
  };

  let res = await request("POST", `/records/${type}`, token, body);

  return res;
}

export async function getHistory(token) {
  let res = await request("GET", "/records/history", token);
  return res;
}

export async function getLoginTemplate() {
  return await request("GET", "/login");
}

export async function getAuthenticatedTemplate(token) {
  return await request("GET", "/authenticated", token);
}
