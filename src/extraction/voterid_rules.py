# src/extraction/voterid_rules.py
import re
# Voter ID often alpha-numeric length ~10
VOTER_RE = re.compile(r"\b([A-Z0-9]{8,12})\b")

def find_voterid(text: str):
    # naive, try find 'EPIC' or similar around
    if "EPIC" in text or "E P I C" in text:
        m = VOTER_RE.search(text)
        if m:
            return m.group(1)
    return None
