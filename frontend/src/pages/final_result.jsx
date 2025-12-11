import { verifyAll } from "../api/api";

export default function FinalResult() {
  const doc = JSON.parse(localStorage.getItem("doc"));
  const form = JSON.parse(localStorage.getItem("userForm"));

  const finish = async () => {
    const payload = {
      document_id: doc.document_id,
      user_fields: form
    };

    const res = await verifyAll(payload);
    localStorage.setItem("final", JSON.stringify(res));
    window.location.href = "/vc";
  };

  return (
    <div>
      <h1>Final Verification</h1>

      <button onClick={finish}>Verify</button>
    </div>
  );
}
