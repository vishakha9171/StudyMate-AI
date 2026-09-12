function Navbar({ activePage }) {
  const pageName =
    activePage === "chat"
      ? "Study Chat"
      : activePage === "materials"
      ? "My Materials"
      : "Practice Quiz";

  return (
    <header className="navbar">
      <div className="breadcrumb">
        <span>StudyMate</span>
        <span className="breadcrumb-slash">/</span>
        <strong>{pageName}</strong>
      </div>

      <div className="navbar-right">
        <div className="ai-status">
          <span className="status-dot"></span>
          AI Ready
        </div>

        <div className="user-avatar">V</div>
      </div>
    </header>
  );
}

export default Navbar;