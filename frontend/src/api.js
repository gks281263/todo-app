const API = "http://localhost:8000/api";

async function request(path, opts = {}) {
  const res = await fetch(API + path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `${res.status} ${res.statusText}`);
  }
  return res.status === 204 ? null : res.json();
}

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
