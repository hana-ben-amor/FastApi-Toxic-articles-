from app.database import db, predictions_collection
from app.model import predict_toxicity
from datetime import datetime

def analyze_articles():
    articles = db["articles"].find()
    for art in articles:
        # Éviter de re-prédire si déjà en base
        if predictions_collection.find_one({"url": art["url"]}):
            continue
        
        text = art.get("title", "")
        if not text:
            continue

        prediction, score = predict_toxicity(text)

        record = {
            "text": text,
            "prediction": prediction,
            "score": score,
            "date": datetime.utcnow(),
            "url": art["url"],
            "source": art.get("source", "inconnu")
        }
        predictions_collection.insert_one(record)

    print("✅ Analyse terminée et stockée dans MongoDB.")

if __name__ == "__main__":
    analyze_articles()
