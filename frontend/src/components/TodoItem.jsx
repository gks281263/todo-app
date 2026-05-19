import { useState } from "react";
import TodoForm from "./TodoForm";

const statusLabels = {
  pending: "Pending",
  in_progress: "In Progress",
  completed: "Completed",
};

export default function TodoItem({ todo, onUpdate, onDelete }) {
  const [editing, setEditing] = useState(false);

  if (editing) {
    return (
      <li className="todo-item editing">
        <TodoForm
          initial={{
            title: todo.title,
            description: todo.description || "",
            status: todo.status,
            due_date: todo.due_date || "",
          }}
          onSave={(data) => onUpdate(todo.id, data).then(() => setEditing(false))}
          onCancel={() => setEditing(false)}
        />
      </li>
    );
  }

  return (
    <li className={`todo-item status-${todo.status}`}>
      <div className="todo-content">
        <h3>{todo.title}</h3>
        {todo.description && <p>{todo.description}</p>}
        <div className="todo-meta">
          <span className={`badge ${todo.status}`}>{statusLabels[todo.status]}</span>
          {todo.due_date && <span className="due-date">Due: {todo.due_date}</span>}
        </div>
      </div>
      <div className="todo-actions">
        <button onClick={() => setEditing(true)}>Edit</button>
        <button onClick={() => onDelete(todo.id)} className="btn-delete">Delete</button>
      </div>
    </li>
  );
}
