function SourceCard({ source }) {
  const fileName = source.source || "Source";

  const extension = fileName
    .split(".")
    .pop()
    .toUpperCase();

  return (
    <div className="source-card">
      <div className="source-file-icon">
        {extension}
      </div>

      <div className="source-info">
        <strong>{fileName}</strong>

        <span>
          Page {source.page}
        </span>
      </div>

      <div className="source-score">
        {Math.round((source.score || 0) * 100)}%
      </div>
    </div>
  );
}

export default SourceCard;