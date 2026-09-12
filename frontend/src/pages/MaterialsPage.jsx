import MaterialCard from "../components/MaterialCard";

function MaterialsPage({
  uploadedFiles,
  uploading,
  fileInputRef,
  handleFileSelect,
}) {
  return (
    <div className="secondary-page">
      <div className="page-heading">
        <div>
          <div className="welcome-badge">
            <span>▣</span>
            Your knowledge base
          </div>

          <h1>My Materials</h1>

          <p>
            Course material used by StudyMate to answer
            your questions.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
        >
          {uploading
            ? "Processing..."
            : "+ Add material"}
        </button>
      </div>

      {uploading && (
        <div className="processing-banner">
          <div className="spinner"></div>

          <div>
            <strong>
              Processing material...
            </strong>

            <p>
              Extracting content and preparing it for
              semantic search.
            </p>
          </div>
        </div>
      )}

      {uploadedFiles.length === 0 ? (
        <div className="empty-materials">
          <div className="empty-icon">↑</div>

          <h2>No materials yet</h2>

          <p>
            Upload PDFs, presentations, text files or
            handwritten notes to start studying.
          </p>

          <button
            className="primary-button"
            onClick={() =>
              fileInputRef.current?.click()
            }
          >
            Upload first material
          </button>
        </div>
      ) : (
        <div className="materials-grid">
          {uploadedFiles.map((file, index) => (
            <MaterialCard
              key={`${file.name}-${index}`}
              file={file}
            />
          ))}
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        hidden
        accept=".pdf,.pptx,.txt,.md,.jpg,.jpeg,.png,.webp"
        onChange={handleFileSelect}
      />
    </div>
  );
}

export default MaterialsPage;