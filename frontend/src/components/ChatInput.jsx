function ChatInput({
  question,
  setQuestion,
  handleAskQuestion,
  handleKeyDown,
  fileInputRef,
  loading,
  uploadedFiles,
}) {
  return (
    <div className="chat-input-wrapper">
      <div className="chat-input-box">
        <button
          className="attach-button"
          onClick={() => fileInputRef.current?.click()}
          title="Upload material"
        >
          ＋
        </button>

        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask anything about your course material..."
          rows={1}
        />

        <button
          className={`send-button ${
            question.trim() ? "ready" : ""
          }`}
          onClick={handleAskQuestion}
          disabled={!question.trim() || loading}
        >
          ↑
        </button>
      </div>

      <div className="input-footer">
        <span>Enter to send · Shift + Enter for new line</span>

        <span>
          {uploadedFiles.length > 0
            ? `${uploadedFiles.length} source${
                uploadedFiles.length !== 1 ? "s" : ""
              } connected`
            : "Upload material to begin"}
        </span>
      </div>
    </div>
  );
}

export default ChatInput;