const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";
const BASE = "http://localhost:8000/api";

export const uploadDocument = async (file) => {
    const form = new FormData();
    form.append("file", file);
    return axios.post(`${BASE}/extract`, form);
};

export const verifyFields = async (payload) =>
    axios.post(`${BASE}/verify`, payload);

export const issueVC = async (payload) =>
    axios.post(`${BASE}/vc/issue`, payload);

export async function uploadFile(file, templateHint=null){
  const fd = new FormData();
  fd.append("file", file);
  if(templateHint) fd.append("template_hint", templateHint);
  const res = await fetch(`${API_BASE}/extract`, {
    method: "POST",
    body: fd
  });
  return res.json();
}

export async function verifyDocument(document_id, user_values){
  const res = await fetch(`${API_BASE}/verify`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({document_id, user_values})
  });
  return res.json();
}

export async function issueVC(payload){
  const res = await fetch(`${API_BASE}/vc/issue`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });
  return res.json();
}
