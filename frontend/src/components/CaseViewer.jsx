import React from "react";

export default function CaseViewer({ data }) {
  if (!data) return null;

  return (
    <div style={{ 
      padding: "15px",
      background: "#f8f8f8",
      border: "1px solid #ccc",
      borderRadius: "6px",
      marginTop: "10px"
    }}>
      <h3>Extracted Entities</h3>
      <pre style={{ whiteSpace: "pre-wrap" }}>
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}
