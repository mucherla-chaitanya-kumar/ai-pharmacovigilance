import React, { useState } from "react";
import UploadForm from "../components/UploadForm";

export default function Home() {
  const [caseData, setCaseData] = useState(null);
  const [validation, setValidation] = useState(null);
  const [narrative, setNarrative] = useState("");

  const handleUploadComplete = (res) => {
    setCaseData(res.case);
    setValidation(res.validation);
    setNarrative("");
  };

  const generateNarrative = async () => {
    const response = await fetch("http://127.0.0.1:8000/narrative", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(caseData),
    });

    const data = await response.json();
    setNarrative(data.narrative);
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <h1>AI Pharmacovigilance System </h1>
        <p className="subtitle">
          Automated adverse event extraction, validation, and narrative generation
        </p>
      </header>

      {/* Upload */}
      <section className="card">
        <h2>Upload Literature</h2>
        <UploadForm onUploadComplete={handleUploadComplete} />
      </section>

      {/* Extracted Case */}
      {caseData && (
        <section className="card">
          <h2>Extracted Case</h2>
          <pre className="code-block">
            {JSON.stringify(caseData, null, 2)}
          </pre>

          <button className="primary-btn" onClick={generateNarrative}>
            Generate Narrative
          </button>
        </section>
      )}

      {/* Narrative */}
      {narrative && (
        <section className="card">
          <h2>Generated Narrative</h2>
          <div className="info-box">{narrative}</div>
        </section>
      )}

      {/* Validation */}
      {validation && (
        <section className="card">
          <h2>Validation Result</h2>
          <div
            className={
              validation.semantic_valid ? "success-box" : "error-box"
            }
          >
            {validation.semantic_valid
              ? "Case is semantically valid"
              : validation.errors.join(", ")}
          </div>
        </section>
      )}
    </div>
  );
}
