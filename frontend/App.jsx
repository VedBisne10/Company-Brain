import { useState } from "react";
import { askQuestion } from "./services/api";

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    try { setAnswer(await askQuestion(question)); } finally { setLoading(false); }
  }

  return <main style={{ maxWidth: 800, margin: "4rem auto", fontFamily: "system-ui", padding: 24 }}>
    <p style={{ color: "#667085" }}>Company Brain</p>
    <h1>Ask your company knowledge</h1>
    <form onSubmit={submit} style={{ display: "flex", gap: 12 }}>
      <input value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Why did the team choose OAuth?" style={{ flex: 1, padding: 12 }} />
      <button disabled={loading} type="submit">{loading ? "Searching…" : "Ask"}</button>
    </form>
    {answer && <section style={{ marginTop: 32, whiteSpace: "pre-wrap" }}><h2>Answer</h2><p>{answer.answer}</p><h3>Sources</h3>{answer.citations.map((citation) => <p key={citation.id}><a href={citation.url || "#"}>{citation.title}</a></p>)}</section>}
  </main>;
}
