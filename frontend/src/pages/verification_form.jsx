import { useState } from "react";

export default function VerificationForm() {
  const doc = JSON.parse(localStorage.getItem("doc"));
  const [form, setForm] = useState({
    name: "",
    dob: "",
    address: "",
    id_number: ""
  });

  const next = () => {
    localStorage.setItem("userForm", JSON.stringify(form));
    window.location.href = "/live-check";
  };

  return (
    <div>
      <h1>Enter Your Details</h1>

      {Object.keys(form).map((key) => (
        <input
          key={key}
          placeholder={key}
          onChange={(e) =>
            setForm({ ...form, [key]: e.target.value })
          }
        />
      ))}

      <button onClick={next}>Next → Live Check</button>
    </div>
  );
}
