from transformers import pipeline

# Charger modèle Hugging Face
classifier = pipeline("text-classification", model="unitary/toxic-bert", truncation=True)

def predict_toxicity(text: str):
    result = classifier(text[:512])[0]
    label = result["label"]
    score = result["score"]

    # Nouveau seuil
    if "toxic" in label.lower() and score >= 0.5:
        prediction = "toxique"
    elif "toxic" in label.lower() and score >= 0.2:
        prediction = "légèrement toxique"
    else:
        prediction = "non-toxique"

    return prediction, round(score, 2)
