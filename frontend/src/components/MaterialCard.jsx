function MaterialCard({ file }) {
  const extension =
    file.name
      ?.split(".")
      .pop()
      ?.toUpperCase() || "FILE";

  return (
    <div className="material-card">
      <div className="material-icon">
        {extension}
      </div>

      <div className="material-info">
        <h3>{file.name}</h3>

        <p>
          {file.chunks} indexed chunks
        </p>
      </div>

      <div className="material-status">
        <span>✓</span>
        Ready
      </div>
    </div>
  );
}

export default MaterialCard;