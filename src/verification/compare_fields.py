# src/verification/compare_fields.py

from rapidfuzz import fuzz

class FieldComparator:
    """
    Compares extracted OCR fields with user-submitted data.
    Returns match score, match status, and reason for mismatch.
    """

    def compare(self, extracted_data: dict, submitted_data: dict) -> dict:
        results = {}

        for field, extracted_value in extracted_data.items():
            submitted_value = submitted_data.get(field, "")

            # Normalize (None → empty string)
            extracted_value = extracted_value or ""
            submitted_value = submitted_value or ""

            # Calculate string similarity score
            similarity_score = fuzz.ratio(extracted_value.lower(), submitted_value.lower()) / 100

            # Determine match status
            if similarity_score >= 0.85:
                status = "match"
                reason = "Values are highly similar"
            elif 0.60 <= similarity_score < 0.85:
                status = "partial_match"
                reason = "Values are similar but not exact"
            else:
                status = "mismatch"
                reason = "Values differ significantly"

            # Save result
            results[field] = {
                "extracted_value": extracted_value,
                "submitted_value": submitted_value,
                "score": round(similarity_score, 2),
                "status": status,
                "reason": reason,
            }

        return results
