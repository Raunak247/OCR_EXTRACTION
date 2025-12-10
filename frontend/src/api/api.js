import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

// Upload File
export const uploadDocument = async (file) => {
  const form = new FormData();
  form.append("file", file);

  const res = await API.post("/extract", form, {
    headers: { "Content-Type": "multipart/form-data" }
  });

  return res.data;
};

// Live field verification
export const liveCheck = async (document_id, field_name, user_value) => {
  const res = await API.post("/verify/live", {
    document_id,
    field_name,
    user_value
  });

  return res.data;
};

// Full verification
export const verifyAll = async (payload) => {
  const res = await API.post("/verify", payload);
  return res.data;
};

// VC Issue
export const issueVC = async (payload) => {
  const res = await API.post("/vc/issue", payload);
  return res.data;
};
