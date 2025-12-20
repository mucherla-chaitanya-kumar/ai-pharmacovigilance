import React, { useState } from "react";
import { uploadFile } from "../services/api";

export default function UploadForm({ onUploadComplete }) {
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file!");
      return;
    }

    try {
      const res = await uploadFile(file);
      console.log("UPLOAD RESPONSE:", res);

      // NO assumptions, NO status checks
      onUploadComplete(res);

    } catch (err) {
      console.error("UPLOAD ERROR:", err);
      alert("Something went wrong.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}
