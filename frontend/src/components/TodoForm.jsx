import { useState } from "react";

const blank = { title: "", description: "", status: "pending", due_date: "" };

export default function TodoForm({ initial, onSave, onCancel }) {
  const [form, setForm] = useState(initial || blank);
  const [saving, setSaving] = useState(false);

  const editing = !!initial;

  function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);

    // strip empty optional fields before sending
    const payload = { ...form };
    if (!payload.due_date) delete payload.due_date;
    if (!payload.description) delete payload.description;

    onSave(payload)
      .then(() => { if (!editing) setForm(blank); })
      .finally(() => setSaving(false));
  }

  const update = (field) => (e) =>
    setForm({ ...form, [field]: e.target.value });

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <input
        type="text"
        placeholder="What needs to be done?"
        value={form.title}
        onChange={update("title")}
        required
        maxLength={200}
      />
      <textarea
        placeholder="Notes"
        value={form.description}
        onChange={update("description")}
        rows={2}
      />
      <div className="form-row">
        <select value={form.status} onChange={update("status")}>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        <input type="date" value={form.due_date} onChange={update("due_date")} />
        <button type="submit" disabled={saving}>
          {editing ? "Save" : "Add"}
        </button>
        {onCancel && <button type="button" onClick={onCancel} className="btn-cancel">Cancel</button>}
      </div>
    </form>
  );
}
