import { BrowserRouter, Routes, Route } from "react-router-dom";
import Upload from "/pages/Upload";
import ExtractedPreview from "./pages/ExtractedPreview";
import VerificationForm from "./pages/VerificationForm";
import LiveFieldCheck from "./pages/LiveFieldCheck";
import FinalResult from "./pages/FinalResult";
import IssueVC from "./pages/IssueVC";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/preview" element={<ExtractedPreview />} />
        <Route path="/verify" element={<VerificationForm />} />
        <Route path="/live-check" element={<LiveFieldCheck />} />
        <Route path="/final-result" element={<FinalResult />} />
        <Route path="/vc" element={<IssueVC />} />
      </Routes>
    </BrowserRouter>
  );
}
