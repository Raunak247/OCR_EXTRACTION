import { useState } from "react";
import { liveCheck } from "../api/api";

export default function LiveFieldCheck() {
  const doc = JSON.parse(localStorage.getItem("doc"));
  const form = JSON.parse(localStorage.getItem("userForm"));

  const [output, setOutput] = useState([]);

  const check = async () => {
    const fields = Object.keys(form);

    let results = [];

    for (let f of fields) {
      const res = await liveCheck(doc.document_id, f, form[f]);
      results.push({ field: f, ...res });
    }

    setOutput(results);
  };

  const next = () => (window.location.href = "/final-result");

  return (
    <div>
      <h1>Live Field Check</h1>

      <button onClick={check}>Run Comparison</button>

      <pre>{JSON.stringify(output, null, 2)}</pre>

      <button onClick={next}>Continue → Final</button>
    </div>
  );
}
