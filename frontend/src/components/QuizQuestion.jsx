function QuizQuestion({ item, index }) {
  return (
    <div className="quiz-question-card">
      <div className="quiz-question-top">
        <span className="question-number">
          {String(index + 1).padStart(2, "0")}
        </span>

        <span className="question-source">
          {item.source} · Page {item.page}
        </span>
      </div>

      <h2>{item.question}</h2>

      <div className="quiz-options">
        {item.options?.map((option, optionIndex) => (
          <div
            className="quiz-option"
            key={optionIndex}
          >
            <span>
              {String.fromCharCode(65 + optionIndex)}
            </span>

            {option}
          </div>
        ))}
      </div>

      <div className="quiz-answer">
        <strong>Answer:</strong> {item.answer}
      </div>
    </div>
  );
}

export default QuizQuestion;