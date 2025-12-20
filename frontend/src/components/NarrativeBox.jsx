import React from "react";

export default function NarrativeBox({ text }) {
  if (!text) return null;

  return (
    <div style={{
      marginTop: "20px",
      padding: "15px",
      background: "#eef6ff",
      border: "1px solid #90caf9",
      borderRadius: "6px"
    }}>
      <h3>Narrative</h3>
      <p style={{ whiteSpace: "pre-wrap" }}>{text}</p>
    </div>
  );
}
