const API = "/api";

async function request(path, opts = {}) {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json", ...opts.headers };
  
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(API + path, { ...opts, headers });
  
  if (!res.ok) {
    if (res.status === 401 && token) {
      // Token expired or invalid
      localStorage.removeItem("token");
      window.dispatchEvent(new Event("auth-expired"));
    }
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `${res.status} ${res.statusText}`);
  }
  return res.status === 204 ? null : res.json();
}

export const register = (email, password) =>
  request("/auth/register", { method: "POST", body: JSON.stringify({ email, password }) });

export const login = (email, password) =>
  request("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });

export const getTodos = (page, pageSize, status) => {
  let qs = `?page=${page}&page_size=${pageSize}`;
  if (status) qs += `&status=${status}`;
  return request(`/todos${qs}`);
};

export const createTodo = (data) =>
  request("/todos", { method: "POST", body: JSON.stringify(data) });

export const updateTodo = (id, data) =>
  request(`/todos/${id}`, { method: "PATCH", body: JSON.stringify(data) });

export const deleteTodo = (id) =>
  request(`/todos/${id}`, { method: "DELETE" });
