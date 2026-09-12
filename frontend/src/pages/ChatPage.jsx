import ChatMessage from "../components/ChatMessage";
import ChatInput from "../components/ChatInput";
import UploadBox from "../components/UploadBox";
import LoadingSpinner from "../components/LoadingSpinner";

function ChatPage({
  messages,
  question,
  setQuestion,
  handleAskQuestion,
  handleKeyDown,
  fileInputRef,
  handleFileSelect,
  loading,
  uploading,
  uploadedFiles,
  clearChat,
}) {
  const hasMessages = messages.length > 0;

  return (
    <div className="chat-page">
      {!hasMessages ? (
        <div className="welcome-section">
          <div className="welcome-badge">
            <span>✦</span>
            Your personal course-material AI
          </div>

          <h1>
            Study smarter.
            <br />
            <span>Understand faster.</span>
          </h1>

          <p className="welcome-description">
            Ask questions from your lectures, PDFs,
            slides and handwritten notes. StudyMate
            answers only from your uploaded materials
            and shows exactly where the answer came from.
          </p>

          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">◈</div>

              <h3>Ask questions</h3>

              <p>
                Ask natural questions about your
                uploaded course material.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">◎</div>

              <h3>Precise citations</h3>

              <p>
                See the source file and exact page
                supporting the answer.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">✎</div>

              <h3>Handwritten notes</h3>

              <p>
                Upload handwritten notes and ask
                questions about them.
              </p>
            </div>
          </div>

          <div className="welcome-upload">
            <UploadBox
              fileInputRef={fileInputRef}
              handleFileSelect={handleFileSelect}
              uploading={uploading}
            />

            {uploading && (
              <div className="uploading-text">
                Processing your material with AI...
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="conversation-area">
          <div className="conversation-header">
            <div>
              <h2>Study Session</h2>

              <p>
                {uploadedFiles.length} material
                {uploadedFiles.length !== 1 ? "s" : ""}{" "}
                available
              </p>
            </div>

            <button
              className="clear-button"
              onClick={clearChat}
            >
              New chat
            </button>
          </div>

          <div className="messages-container">
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                message={message}
              />
            ))}

            {loading && (
              <LoadingSpinner />
            )}
          </div>
        </div>
      )}

      <ChatInput
        question={question}
        setQuestion={setQuestion}
        handleAskQuestion={handleAskQuestion}
        handleKeyDown={handleKeyDown}
        fileInputRef={fileInputRef}
        loading={loading}
        uploadedFiles={uploadedFiles}
      />

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

export default ChatPage;