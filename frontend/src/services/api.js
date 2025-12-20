const API_BASE_URL = "http://127.0.0.1:8000";

// ------------------ UPLOAD ------------------
export async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/process`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Upload failed");
    }

    return response.json();
}

// ------------------ NER ------------------
// (Not wired yet in backend – kept for future use)
export async function extractEntities(text) {
    const response = await fetch(`${API_BASE_URL}/ner`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });

    return response.json();
}

// ------------------ NARRATIVE ------------------
export async function generateNarrative(entities) {
    const response = await fetch(`${API_BASE_URL}/narrative`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entities }),
    });

    return response.json();
}

// ------------------ VALIDATION ------------------
export async function validateCase(entities) {
    const response = await fetch(`${API_BASE_URL}/validate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(entities),
    });

    return response.json();
}

// ------------------ SAVE CASE ------------------
export async function saveCase(entities, narrative) {
    const response = await fetch(`${API_BASE_URL}/save_case`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entities, narrative }),
    });

    return response.json();
}
