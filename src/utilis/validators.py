# src/utils/validators.py
def is_valid_docid(doc_id: str) -> bool:
    if not doc_id:
        return False
    # simple length check — adapt as per your doc-id scheme
    return len(doc_id) >= 6
