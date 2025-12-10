import { issueVC } from "../api/api";

export default function IssueVC() {
  const final = JSON.parse(localStorage.getItem("final"));

  const generate = async () => {
    const data = await issueVC(final);
    localStorage.setItem("vc", JSON.stringify(data));
    alert("VC Issued. QR Code ready.");
  };

  return (
    <div>
      <h1>Issue Verifiable Credential</h1>

      <button onClick={generate}>Generate VC</button>
    </div>
  );
}
