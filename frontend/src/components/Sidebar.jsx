function Sidebar({
  activePage,
  setActivePage,
  uploadedFiles,
  onAddMaterial,
  onNewChat,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">✦</div>

        <div>
          <div className="brand-name">StudyMate</div>
          <div className="brand-subtitle">
            AI Study Assistant
          </div>
        </div>
      </div>

      <div className="sidebar-section">
        <div className="sidebar-title">WORKSPACE</div>

        <button
          className={`sidebar-item ${
            activePage === "chat" ? "active" : ""
          }`}
          onClick={() => setActivePage("chat")}
        >
          <span className="sidebar-icon">⌘</span>
          <span>Study Chat</span>
        </button>

        <button
          className={`sidebar-item ${
            activePage === "materials" ? "active" : ""
          }`}
          onClick={() => setActivePage("materials")}
        >
          <span className="sidebar-icon">▣</span>
          <span>My Materials</span>

          {uploadedFiles.length > 0 && (
            <span className="sidebar-count">
              {uploadedFiles.length}
            </span>
          )}
        </button>

        <button
          className={`sidebar-item ${
            activePage === "quiz" ? "active" : ""
          }`}
          onClick={() => setActivePage("quiz")}
        >
          <span className="sidebar-icon">✎</span>
          <span>Practice Quiz</span>
        </button>
      </div>

      <div className="sidebar-section">
        <div className="sidebar-title">QUICK ACTIONS</div>

        <button
          className="sidebar-item"
          onClick={onAddMaterial}
        >
          <span className="sidebar-icon">＋</span>
          <span>Add Material</span>
        </button>

        <button
          className="sidebar-item"
          onClick={onNewChat}
        >
          <span className="sidebar-icon">↻</span>
          <span>New Chat</span>
        </button>
      </div>

      <div className="sidebar-bottom">
        <div className="grounded-card">
          <div className="grounded-icon">✓</div>

          <div>
            <strong>Material-grounded</strong>

            <p>
              Answers stay within your uploaded
              course materials.
            </p>
          </div>
        </div>

        <div className="sidebar-footer">
          StudyMate AI · v1.0
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;