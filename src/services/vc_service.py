# src/services/vc_service.py
from src.vc.vc_payload_builder import VCPayloadBuilder
from src.vc.mosip_client import MOSIPVCClient
from src.utilis.file_manager import ensure_doc_folder

class VCService:
    def __init__(self):
        self.builder = VCPayloadBuilder()
        self.client = MOSIPVCClient()

    def create_and_issue_vc(self, doc_id: str, mapped_subject: dict, verification: dict, save_path_base: str = "files"):
        payload = self.builder.build_payload(doc_id, mapped_subject, verification)
        # attempt to call MOSIP
        resp = self.client.issue_vc(payload)
        # save VC to files/<doc_id>/report/vc.json (use file_manager in real code)
        report_dir = f"{save_path_base}/{doc_id}/report"
        ensure_doc_folder(report_dir)
        # simple write:
        import json, os
        with open(os.path.join(report_dir, "vc.json"), "w", encoding="utf8") as f:
            json.dump(resp, f, indent=2, ensure_ascii=False)
        return resp
