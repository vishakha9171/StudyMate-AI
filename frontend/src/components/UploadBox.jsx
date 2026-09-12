function UploadBox({
  fileInputRef,
  handleFileSelect,
  uploading,
}) {
  return (
    <>
      <button
        className="upload-large-button"
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
      >
        <span className="upload-large-icon">↑</span>

        <span>
          <strong>
            {uploading
              ? "Processing material..."
              : "Upload course material"}
          </strong>

          <small>
            PDF, PPTX, TXT, MD or handwritten images
          </small>
        </span>
      </button>

      <input
        ref={fileInputRef}
        type="file"
        hidden
        accept=".pdf,.pptx,.txt,.md,.jpg,.jpeg,.png,.webp"
        onChange={handleFileSelect}
      />
    </>
  );
}

export default UploadBox;