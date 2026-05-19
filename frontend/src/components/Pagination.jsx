export default function Pagination({ page, total, pageSize, onPageChange }) {
  const lastPage = Math.ceil(total / pageSize) || 1;
  if (lastPage <= 1) return null;

  return (
    <div className="pagination">
      <button disabled={page <= 1} onClick={() => onPageChange(page - 1)}>Prev</button>
      <span>{page} / {lastPage}</span>
      <button disabled={page >= lastPage} onClick={() => onPageChange(page + 1)}>Next</button>
    </div>
  );
}
