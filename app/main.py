from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import pandas as pd, numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
FEATS = np.load("data/feats.npy")  # standardized feature matrix aligned to USERS rows

# OPTIMIZATION: Use smaller sample for faster API responses
SAMPLE_SIZE = 5000  # Much faster than 50K
if len(USERS) > SAMPLE_SIZE:
    logger.info(f"Using sample of {SAMPLE_SIZE} users for faster API responses")
    sample_indices = np.random.choice(len(USERS), SAMPLE_SIZE, replace=False)
    USERS = USERS.iloc[sample_indices].reset_index(drop=True)
    FEATS = FEATS[sample_indices]

# ---------- Models ----------
class DynamicReq(BaseModel):
    goal: str
    filters: Optional[Dict] = None
    k_min: int = 2  # Reduced from 3 for faster clustering
    k_max: int = 4  # Reduced from 6 for faster clustering
    min_cluster_pct: float = 0.03  # drop tiny clusters (<3% of subset)
    show_sub_personas: bool = True  # Show hierarchical personas

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
    if "bose" in g and "india" in g:
        f["brand_awareness_bose_min"] = 0.65 # Example heuristic
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
    if "brand_awareness_bose_min" in filters:
        mask &= (users.brand_awareness_bose >= filters["brand_awareness_bose_min"]).values
    return users[mask], feats[mask]

def choose_k(feats_sub: np.ndarray, k_min=2, k_max=4):
    best_k, best_score, best_model = None, -1, None
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        lab = km.fit_predict(feats_sub)
        sc = silhouette_score(feats_sub, lab) if len(set(lab)) > 1 else -1
        if sc > best_score:
            best_k, best_score, best_model = k, sc, km
    return best_k, best_score, best_model

def generate_sub_personas(grp: pd.DataFrame, cluster_id: int) -> List[Dict]:
    """Generate sub-personas within a cluster based on key traits"""
    sub_personas = []
    
    # Define sub-persona filters based on key traits
    sub_filters = [
        {"name": "Urban Tech Enthusiasts", "filters": {"city_tier": ["Tier-1"], "device_count_min": 3}},
        {"name": "Urban Tech Skeptics", "filters": {"city_tier": ["Tier-1"], "privacy_pref_min": 0.6}},
        {"name": "Budget-Conscious Users", "filters": {"price_sensitivity_min": 0.6}},
        {"name": "Brand-Aware Consumers", "filters": {"brand_awareness_bose_min": 0.7}},
        {"name": "Privacy-Focused Users", "filters": {"privacy_pref_min": 0.7}},
        {"name": "Multi-Device Users", "filters": {"device_count_min": 4}},
    ]
    
    for sub_filter in sub_filters:
        mask = np.ones(len(grp), dtype=bool)
        filters = sub_filter["filters"]
        
        if "city_tier" in filters:
            mask &= grp.city_tier.isin(filters["city_tier"]).values
        if "device_count_min" in filters:
            mask &= (grp.device_count >= filters["device_count_min"]).values
        if "privacy_pref_min" in filters:
            mask &= (grp.privacy_pref >= filters["privacy_pref_min"]).values
        if "price_sensitivity_min" in filters:
            mask &= (grp.price_sensitivity >= filters["price_sensitivity_min"]).values
        if "brand_awareness_bose_min" in filters:
            mask &= (grp.brand_awareness_bose >= filters["brand_awareness_bose_min"]).values
            
        sub_grp = grp[mask]
        
        if len(sub_grp) >= 10:  # Minimum size for sub-persona
            sub_persona = {
                "name": sub_filter["name"],
                "size": len(sub_grp),
                "size_pct": round(len(sub_grp)/len(grp)*100, 1),
                "traits": {
                    "avg_age": round(sub_grp["age"].mean(), 1),
                    "avg_device_count": round(sub_grp["device_count"].mean(), 1),
                    "avg_price_sensitivity": round(sub_grp["price_sensitivity"].mean(), 2),
                    "avg_privacy_pref": round(sub_grp["privacy_pref"].mean(), 2),
                    "avg_brand_awareness": round(sub_grp["brand_awareness_bose"].mean(), 2),
                    "top_income": sub_grp["income_band"].mode().iloc[0] if not sub_grp["income_band"].mode().empty else "Unknown",
                    "top_media": sub_grp["preferred_media"].mode().iloc[0] if not sub_grp["preferred_media"].mode().empty else "YouTube"
                }
            }
            sub_personas.append(sub_persona)
    
    return sub_personas

def summarize_cluster(grp: pd.DataFrame, show_sub_personas: bool = True):
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
    
    result = {
        "care_about": sorted(list(care_about)),
        "barriers": sorted(list(barriers)),
        "top_traits": top_traits,
        "priors": priors,
        "demographics": demographics
    }
    
    # Add sub-personas if requested
    if show_sub_personas:
        result["sub_personas"] = generate_sub_personas(grp, 0)  # cluster_id will be set later
    
    return result

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
    if n < 100:  # Reduced threshold for smaller dataset
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
            s = summarize_cluster(grp, req.show_sub_personas)
            # Update sub-personas with correct cluster_id
            if req.show_sub_personas and "sub_personas" in s:
                for sub_persona in s["sub_personas"]:
                    sub_persona["cluster_id"] = int(cid)
            
            personas.append({
                "id": f"dyn_{int(cid)}",
                "label": f"Dynamic Persona {int(cid)}",
                "size_pct": size_pct,
                "cluster_size": len(grp),
                **s
            })
        except Exception as e:
            logger.error(f"Error summarizing cluster {cid}: {e}")
            # Append a fallback persona with error info
            personas.append({
                "id": f"dyn_{int(cid)}",
                "label": f"Dynamic Persona {int(cid)} (Error)",
                "size_pct": size_pct,
                "cluster_size": len(grp),
                "care_about": [],
                "barriers": [f"summarization error: {e}"],
                "top_traits": [],
                "priors": {},
                "demographics": {},
                "sub_personas": []
            })

    personas = sorted(personas, key=lambda p: p["size_pct"], reverse=True)[:6]
    return {"personas": personas, "meta": {
        "subset_n": n, "k": best_k, "silhouette": round(float(best_score),3), "filters_applied": filters}
    }
