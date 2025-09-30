from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import pandas as pd

from app.database import predictions_collection, db
from app.model import predict_toxicity

app = FastAPI(title="API Toxicité", version="1.0")

# Servir les images générées (graphiques)
app.mount("/static", StaticFiles(directory="."), name="static")

# Templates HTML
templates = Jinja2Templates(directory="templates")


# Modèle d’entrée
class TextInput(BaseModel):
    text: str
    url: str | None = None


# ---------- ENDPOINTS ---------- #

@app.post("/predict")
def predict(input_data: TextInput):
    try:
        prediction, score = predict_toxicity(input_data.text)

        # Sauvegarde MongoDB
        record = {
            "text": input_data.text,
            "prediction": prediction,
            "score": score,
            "date": datetime.utcnow(),
            "url": input_data.url
        }
        predictions_collection.insert_one(record)

        return {"prediction": prediction, "score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
def get_stats():
    stats = list(db["stats"].find({}, {"_id": 0}))
    return JSONResponse(content={"stats": stats})


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    stats = list(db["stats"].find({}, {"_id": 0}))

    if not stats:
        interpretation = "⚠️ Aucune statistique disponible."
        sites = []
    else:
        df = pd.DataFrame(stats)
        site_plus_toxique = df.loc[df["tres_toxique_pct"].idxmax()]["source"]

        interpretation = (
            f"Le site le plus toxique est <b>{site_plus_toxique}</b>, "
            f"avec un pourcentage élevé de contenus très toxiques."
        )
        sites = df["source"].tolist()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "sites": sites,
        "interpretation": interpretation
    })
