import React, { useState } from "react";
import { uploadFile } from "../services/api";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    try {
      const res = await uploadFile(file);

      if (res.status === "success") {
        setResponse(res.files); // array of uploaded files with text previews
      } else {
        setResponse([]);
        alert("Upload failed!");
      }
    } catch (err) {
      console.error(err);
      alert("Error uploading file.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Upload Literature</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit">Upload</button>
      </form>

      {response.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h3>Uploaded Files & Text Preview</h3>
          {response.map((fileItem, idx) => (
            <div key={idx} style={{ marginBottom: "15px", padding: "10px", border: "1px solid #ccc" }}>
              <strong>{fileItem.filename}</strong>
              <p style={{ whiteSpace: "pre-wrap" }}>{fileItem.text_preview}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
