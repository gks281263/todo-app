import { useState, useEffect, useCallback } from "react";
import { getTodos, createTodo, updateTodo, deleteTodo } from "./api";
import TodoForm from "./components/TodoForm";
import TodoItem from "./components/TodoItem";
import Pagination from "./components/Pagination";
import Auth from "./components/Auth";
import "./App.css";

const PER_PAGE = 10;

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("user"));
    } catch {
      return null;
    }
  });

  const [todos, setTodos] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleLogin = (newToken, newUser) => {
    localStorage.setItem("token", newToken);
    localStorage.setItem("user", JSON.stringify(newUser));
    setToken(newToken);
    setUser(newUser);
    setPage(1);
  };

  const handleLogout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
    setTodos([]);
  }, []);

  useEffect(() => {
    const handleAuthExpired = () => handleLogout();
    window.addEventListener("auth-expired", handleAuthExpired);
    return () => window.removeEventListener("auth-expired", handleAuthExpired);
  }, [handleLogout]);

  const refresh = useCallback(() => {
    if (!token) return;
    setLoading(true);
    getTodos(page, PER_PAGE, filter)
      .then((data) => {
        setTodos(data.items);
        setTotal(data.total);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [page, filter, token]);

  useEffect(() => { refresh(); }, [refresh]);

  async function handleCreate(data) {
    await createTodo(data);
    setPage(1); // go back to first page to see the new item
    refresh();
  }

  async function handleUpdate(id, data) {
    await updateTodo(id, data);
    refresh();
  }

  async function handleDelete(id) {
    if (!confirm("Delete this todo?")) return;
    await deleteTodo(id);
    refresh();
  }

  if (!token) {
    return <Auth onLogin={handleLogin} />;
  }

  return (
    <div className="container">
      <header className="app-header">
        <h1>Todos</h1>
        <div className="user-controls">
          <span className="user-email">{user?.email}</span>
          <button onClick={handleLogout} className="btn-link logout-btn">Logout</button>
        </div>
      </header>

      <TodoForm onSave={handleCreate} />

      <div className="toolbar">
        <select value={filter} onChange={(e) => { setFilter(e.target.value); setPage(1); }}>
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      {error && <p className="error">{error}</p>}

      {loading ? (
        <p className="loading">Loading...</p>
      ) : todos.length === 0 ? (
        <p className="empty">Nothing here yet.</p>
      ) : (
        <ul className="todo-list">
          {todos.map((t) => (
            <TodoItem key={t.id} todo={t} onUpdate={handleUpdate} onDelete={handleDelete} />
          ))}
        </ul>
      )}

      <Pagination page={page} total={total} pageSize={PER_PAGE} onPageChange={setPage} />
    </div>
  );
}
