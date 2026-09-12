import { useRef, useState } from "react";

import { uploadFile, askQuestion, generateQuiz } from "./api";

import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import ChatPage from "./pages/ChatPage";
import MaterialsPage from "./pages/MaterialsPage";
import QuizPage from "./pages/QuizPage";

import "./App.css";

function App() {
  const [activePage, setActivePage] = useState("chat");

  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");

  const [uploadedFiles, setUploadedFiles] = useState([]);

  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const [quizLoading, setQuizLoading] = useState(false);
  const [quiz, setQuiz] = useState(null);

  const fileInputRef = useRef(null);

  const handleFileSelect = async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setUploading(true);

    try {
      const result = await uploadFile(file);

      setUploadedFiles((previous) => [
        ...previous,
        {
          name: result.filename,
          chunks: result.chunks_created,
        },
      ]);

      setMessages((previous) => [
        ...previous,
        {
          type: "system",
          text: `${file.name} is ready. You can now ask questions about it.`,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          type: "error",
          text: error.message || "File upload failed.",
        },
      ]);
    } finally {
      setUploading(false);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleAskQuestion = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    const userMessage = {
      type: "user",
      text: trimmedQuestion,
    };

    const previousMessages = messages;

    setMessages((previous) => [...previous, userMessage]);
    setQuestion("");
    setLoading(true);

    const history = previousMessages
      .filter(
        (message) =>
          message.type === "user" ||
          message.type === "assistant"
      )
      .map((message) => ({
        role: message.type === "user" ? "user" : "assistant",
        content: message.text,
      }));

    try {
      const result = await askQuestion(
        trimmedQuestion,
        history
      );

      setMessages((previous) => [
        ...previous,
        {
          type: result.refused ? "refusal" : "assistant",
          text: result.answer,
          sources: result.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          type: "error",
          text: error.message || "Something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAskQuestion();
    }
  };

  const handleGenerateQuiz = async () => {
    if (quizLoading) {
      return;
    }

    setQuizLoading(true);
    setQuiz(null);

    try {
      const result = await generateQuiz(
        "course material and important concepts"
      );

      setQuiz(result);
    } catch (error) {
      setQuiz({
        questions: [],
        message: error.message || "Quiz generation failed.",
      });
    } finally {
      setQuizLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setQuestion("");
  };

  return (
    <div className="app-shell">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
        uploadedFiles={uploadedFiles}
        onAddMaterial={() => fileInputRef.current?.click()}
        onNewChat={clearChat}
      />

      <main className="main-content">
        <Navbar activePage={activePage} />

        <div className="page-content">
          {activePage === "chat" && (
            <ChatPage
              messages={messages}
              question={question}
              setQuestion={setQuestion}
              handleAskQuestion={handleAskQuestion}
              handleKeyDown={handleKeyDown}
              fileInputRef={fileInputRef}
              handleFileSelect={handleFileSelect}
              loading={loading}
              uploading={uploading}
              uploadedFiles={uploadedFiles}
              clearChat={clearChat}
            />
          )}

          {activePage === "materials" && (
            <MaterialsPage
              uploadedFiles={uploadedFiles}
              uploading={uploading}
              fileInputRef={fileInputRef}
              handleFileSelect={handleFileSelect}
            />
          )}

          {activePage === "quiz" && (
            <QuizPage
              quiz={quiz}
              quizLoading={quizLoading}
              handleGenerateQuiz={handleGenerateQuiz}
            />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;