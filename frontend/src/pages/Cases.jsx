import React, { useEffect, useState } from "react";
import { getCases, getCaseById } from "../services/api";
import CaseViewer from "../components/CaseViewer";
import NarrativeBox from "../components/NarrativeBox";

export default function Cases() {
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);

  useEffect(() => {
    async function loadData() {
      const res = await getCases();
      if (res.status === "success") {
        setCases(res.cases);
      }
    }
    loadData();
  }, []);

  const loadCase = async (id) => {
    const res = await getCaseById(id);
    if (res.status === "success") {
      setSelectedCase(res.case);
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Case History 📁</h1>

      <div style={{ display: "flex", gap: "20px" }}>
        {/* LEFT: Case list */}
        <div style={{ width: "30%", borderRight: "1px solid #ccc" }}>
          <h2>Saved Cases</h2>
          {cases.map((item) => (
            <div
              key={item.id}
              onClick={() => loadCase(item.id)}
              style={{
                padding: "10px",
                marginBottom: "10px",
                border: "1px solid #ccc",
                cursor: "pointer",
                background: selectedCase?.id === item.id ? "#eef" : "#fafafa",
              }}
            >
              {item.title}
            </div>
          ))}
        </div>

        {/* RIGHT: Case details */}
        <div style={{ width: "70%", paddingLeft: "20px" }}>
          {selectedCase ? (
            <>
              <h2>{selectedCase.title}</h2>

              <CaseViewer data={selectedCase.entities} />

              <NarrativeBox text={selectedCase.narrative} />
            </>
          ) : (
            <p>Select a case from the list.</p>
          )}
        </div>
      </div>
    </div>
  );
}
