import pandas as pd
from app.database import predictions_collection, db

def compute_stats():
    data = list(predictions_collection.find({}, {"source": 1, "prediction": 1, "score": 1}))
    df = pd.DataFrame(data)

    if df.empty:
        print("⚠️ Aucune donnée trouvée dans predictions")
        return None

    # Classifier selon le score
    def classify(row):
        if row["prediction"] == "toxique":
            return "légèrement toxique" if row["score"] < 0.5 else "très toxique"
        return "non toxique"

    df["toxic_level"] = df.apply(classify, axis=1)

    # Stats par source
    resultats = df.groupby(["source", "toxic_level"]).size().unstack(fill_value=0)
    resultats_pct = resultats.div(resultats.sum(axis=1), axis=0) * 100

    # Sauvegarde dans MongoDB
    stats_collection = db["stats"]
    stats_collection.delete_many({})  # reset
    for site, row in resultats_pct.iterrows():
        stats_collection.insert_one({
            "source": site,
            "non_toxique_pct": row.get("non toxique", 0),
            "legerement_toxique_pct": row.get("légèrement toxique", 0),
            "tres_toxique_pct": row.get("très toxique", 0)
        })

    print("✅ Statistiques enregistrées dans MongoDB.")
    return resultats_pct

if __name__ == "__main__":
    stats = compute_stats()
    print(stats)
