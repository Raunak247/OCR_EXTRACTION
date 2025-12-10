export default function ExtractedPreview() {
  const doc = JSON.parse(localStorage.getItem("doc"));

  return (
    <div>
      <h1>Extracted Fields</h1>

      <pre>{JSON.stringify(doc.extracted_fields, null, 2)}</pre>

      <button onClick={() => (window.location.href = "/verify")}>
        Proceed to Verification
      </button>
    </div>
  );
}
