import SourceCard from "./SourceCard";

function ChatMessage({ message }) {
  if (message.type === "user") {
    return (
      <div className="message-row user-row">
        <div className="user-message-card">
          {message.text}
        </div>

        <div className="user-avatar">V</div>
      </div>
    );
  }

  if (message.type === "system") {
    return (
      <div className="system-card">
        <div className="system-icon">✓</div>

        <div>
          <strong>Material processed</strong>

          <p>{message.text}</p>
        </div>
      </div>
    );
  }

  if (message.type === "error") {
    return (
      <div className="error-card">
        <div className="error-icon">!</div>

        <div>
          <strong>Something went wrong</strong>

          <p>{message.text}</p>
        </div>
      </div>
    );
  }

  if (message.type === "refusal") {
    return (
      <div className="message-row assistant-row">
        <div className="assistant-avatar">✦</div>

        <div className="refusal-card">
          <div className="refusal-header">
            <span className="refusal-icon">?</span>

            <strong>
              Not found in your materials
            </strong>
          </div>

          <p>{message.text}</p>

          <div className="refusal-note">
            StudyMate will not invent an answer when
            your uploaded material does not support it.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="message-row assistant-row">
      <div className="assistant-avatar">✦</div>

      <div className="assistant-content">
        <div className="answer-card">
          <div className="answer-header">
            <span>StudyMate AI</span>

            <span className="verified-badge">
              ✓ Material grounded
            </span>
          </div>

          <div className="answer-text">
            {message.text}
          </div>
        </div>

        {message.sources &&
          message.sources.length > 0 && (
            <div className="sources-section">
              <div className="sources-title">
                <span>⌕</span>
                Sources
              </div>

              <div className="source-grid">
                {message.sources.map((source, index) => (
                  <SourceCard
                    key={source.id || index}
                    source={source}
                  />
                ))}
              </div>
            </div>
          )}
      </div>
    </div>
  );
}

export default ChatMessage;