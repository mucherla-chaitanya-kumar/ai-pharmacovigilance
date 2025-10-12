// frontend/src/services/api.js
const API_BASE_URL = "http://127.0.0.1:8000";  // FastAPI server URL

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData
  });

  return response.json();
}
