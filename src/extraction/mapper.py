# src/extraction/mapper.py
"""
Map extractor output to standard MOSIP-like schema (example).
You can extend fields as per MOSIP schema.
"""

def map_to_mosip_schema(extracted: dict) -> dict:
    return {
        "fullName": extracted.get("name"),
        "dateOfBirth": extracted.get("dob"),
        "address": extracted.get("address"),
        "idNumber": extracted.get("id_number"),
        "rawTextSnippet": (extracted.get("raw_text") or "")[:100]
    }
