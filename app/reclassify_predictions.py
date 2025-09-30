from app.database import predictions_collection
from app.model import predict_toxicity
from datetime import datetime

def reclassify_predictions():
    docs = predictions_collection.find()

    updated = 0
    for doc in docs:
        text = doc.get("text", "")
        if not text:
            continue

        # Reclasser avec ton modèle corrigé
        prediction, score = predict_toxicity(text)

        # Mettre à jour uniquement si la prédiction change
        if doc.get("prediction") != prediction or doc.get("score") != score:
            predictions_collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {
                    "prediction": prediction,
                    "score": score,
                    "updated_at": datetime.utcnow()
                }}
            )
            updated += 1

    print(f"✅ Reclassification terminée. {updated} documents mis à jour.")

if __name__ == "__main__":
    reclassify_predictions()
