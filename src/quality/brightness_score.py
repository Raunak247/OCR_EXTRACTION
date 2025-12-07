# src/quality/brightness_score.py
def brightness_score(image):
    avg = image.mean()
    return max(0, min(1, (avg - 50) / 150))
