from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import pandas as pd, numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ---------- App ----------
app = FastAPI(title="Dynamic Persona Generator", version="0.1")

# Allow local dev from Bolt / Vercel previews
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load data created in Step 1 ----------
USERS = pd.read_parquet("data/users.parquet")
# OPTIMIZATION: Use smaller sample for faster API responses
SAMPLE_SIZE = 5000  # Much faster than 50K
if len(USERS) > SAMPLE_SIZE:
    print(f"Using sample of {SAMPLE_SIZE} users for faster API responses")
    sample_indices = np.random.choice(len(USERS), SAMPLE_SIZE, replace=False)
    USERS = USERS.iloc[sample_indices].reset_index(drop=True)
    FEATS = FEATS[sample_indices]
FEATS = np.load("data/feats.npy")  # standardized feature matrix aligned to USERS rows

# ---------- Models ----------
class DynamicReq(BaseModel):
    goal: str
    filters: Optional[Dict] = None
    k_min: int = 2
    k_max: int = 4
    min_cluster_pct: float = 0.03  # drop tiny clusters (<3% of subset)

# ---------- Helpers ----------
def parse_goal(goal: str) -> dict:
    """Very simple rules to get started. Extend later."""
    g = (goal or "").lower()
    f: dict = {}
    if "college" in g or "student" in g:
        f["age_range"] = (18, 25)
    if "tier-2" in g:
        f["city_tier"] = ["Tier-2"]
    if "tier-3" in g:
        f["city_tier"] = ["Tier-3"]
    if "commut" in g:  # commute/commuters
        f["device_count_min"] = 2
    if "privacy" in g:
        f["privacy_pref_min"] = 0.6
    if "budget" in g or "price" in g:
        f["price_sensitivity_min"] = 0.55
    return f

def apply_filters(users: pd.DataFrame, feats: np.ndarray, filters: dict):
    mask = np.ones(len(users), dtype=bool)
    if "age_range" in filters:
        lo, hi = filters["age_range"]
        mask &= users.age.between(lo, hi).values
    if "city_tier" in filters:
        mask &= users.city_tier.isin(filters["city_tier"]).values
    if "device_count_min" in filters:
        mask &= (users.device_count >= filters["device_count_min"]).values
    if "privacy_pref_min" in filters:
        mask &= (users.privacy_pref >= filters["privacy_pref_min"]).values
    if "price_sensitivity_min" in filters:
        mask &= (users.price_sensitivity >= filters["price_sensitivity_min"]).values
    return users[mask], feats[mask]

def choose_k(feats_sub: np.ndarray, k_min=3, k_max=6):
    best_k, best_score, best_model = None, -1, None
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        lab = km.fit_predict(feats_sub)
        sc = silhouette_score(feats_sub, lab) if len(set(lab)) > 1 else -1
        if sc > best_score:
            best_k, best_score, best_model = k, sc, km
    return best_k, best_score, best_model

def summarize_cluster(grp: pd.DataFrame):
    care_about, barriers, top_traits = set(), set(), []
    # Heuristics from synthetic signals
    if grp["brand_awareness_bose"].mean() > 0.65:
        care_about.add("brand reputation")
    if grp["price_sensitivity"].mean() > 0.55:
        barriers.add("price premium"); care_about.add("discounts")
    if grp["privacy_pref"].mean() > 0.55:
        barriers.add("always-on mics"); care_about.add("local control")
    if grp["device_count"].mean() >= 3:
        care_about.add("seamless casting"); top_traits.append("multi-device")
    if grp["price_sensitivity"].mean() < 0.45:
        top_traits.append("low price sensitivity")
    if grp["brand_awareness_bose"].mean() >= 0.7:
        top_traits.append("brand aware")

    top_media = grp["preferred_media"].mode().iloc[0] if not grp["preferred_media"].mode().empty else "YouTube"
    demographics = {
        "age_range": f"{int(grp['age'].quantile(0.1))}-{int(grp['age'].quantile(0.9))}",
        "income_band": grp["income_band"].mode().iloc[0],
        "geo": grp["city_tier"].mode().iloc[0]
    }
    priors = {
        "emi_usage": round(float(grp["emi_flag"].mean()), 2),
        "brand_awareness_bose": round(float(grp["brand_awareness_bose"].mean()), 2),
        "top_media": [top_media]
    }
    return {
        "care_about": sorted(list(care_about)),
        "barriers": sorted(list(barriers)),
        "top_traits": top_traits,
        "priors": priors,
        "demographics": demographics
    }

# ---------- Routes ----------
@app.get("/health")
def health():
    return {"ok": True, "users": int(len(USERS))}

@app.post("/personas/dynamic")
def dynamic_personas(req: DynamicReq):
    goal = req.goal or ""
    filters = req.filters or parse_goal(goal)

    users_sub, feats_sub = apply_filters(USERS, FEATS, filters)
    n = len(users_sub)
    if n < 500:
        return {"personas": [], "meta": {"subset_n": n, "filters_applied": filters, "warning": "too few users"}}

    best_k, best_score, best_model = choose_k(feats_sub, req.k_min, req.k_max)
    labels = best_model.predict(feats_sub)

    users_sub = users_sub.copy()
    users_sub["cid"] = labels

    personas = []
    for cid, grp in users_sub.groupby("cid"):
        size_pct = round(len(grp)/n*100.0, 1)
        if size_pct < (req.min_cluster_pct * 100):
            continue  # drop tiny clusters
        try:
            s = summarize_cluster(grp)
        except Exception as e:  # defensive: never drop a cluster silently
            s = {
                "care_about": [],
                "barriers": [],
                "top_traits": [],
                "priors": {
                    "emi_usage": round(float(grp["emi_flag"].mean()), 2),
                    "brand_awareness_bose": round(float(grp["brand_awareness_bose"].mean()), 2),
                    "top_media": [str(grp.get("preferred_media", pd.Series(["YouTube"])) .mode().iloc[0]) if not grp.get("preferred_media", pd.Series()).mode().empty else "YouTube"]
                },
                "demographics": {
                    "age_range": f"{int(grp['age'].min())}-{int(grp['age'].max())}",
                    "income_band": str(grp.get("income_band", pd.Series(["Mid"])) .mode().iloc[0]),
                    "geo": str(grp.get("city_tier", pd.Series(["Tier-1"])) .mode().iloc[0])
                }
            }
        personas.append({
            "id": f"dyn_{int(cid)}",
            "label": f"Dynamic Persona {int(cid)}",
            "size_pct": size_pct,
            **s
        })

    personas = sorted(personas, key=lambda p: p["size_pct"], reverse=True)[:6]
    return {"personas": personas, "meta": {
        "subset_n": n, "k": best_k, "silhouette": round(float(best_score),3), "filters_applied": filters}
    }
