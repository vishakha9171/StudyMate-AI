import QuizQuestion from "../components/QuizQuestion";

function QuizPage({
  quiz,
  quizLoading,
  handleGenerateQuiz,
}) {
  return (
    <div className="secondary-page">
      <div className="page-heading">
        <div>
          <div className="welcome-badge">
            <span>✎</span>
            Active recall
          </div>

          <h1>Practice Quiz</h1>

          <p>
            Test your understanding using only your
            uploaded course material.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={handleGenerateQuiz}
          disabled={quizLoading}
        >
          {quizLoading
            ? "Generating..."
            : "Generate Quiz"}
        </button>
      </div>

      {!quiz ? (
        <div className="quiz-empty">
          <div className="quiz-big-icon">✦</div>

          <h2>Ready to test yourself?</h2>

          <p>
            Generate practice questions from your
            uploaded course material.
          </p>

          <button
            className="primary-button"
            onClick={handleGenerateQuiz}
            disabled={quizLoading}
          >
            {quizLoading
              ? "Generating..."
              : "Generate 5 Questions"}
          </button>
        </div>
      ) : (
        <div className="quiz-container">
          {quiz.message && (
            <div className="error-card">
              <div className="error-icon">!</div>

              <div>
                <strong>Quiz unavailable</strong>

                <p>{quiz.message}</p>
              </div>
            </div>
          )}

          {quiz.questions?.map((item, index) => (
            <QuizQuestion
              key={index}
              item={item}
              index={index}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default QuizPage;