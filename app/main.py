from fastapi import FastAPI, HTTPException
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

# Allow CORS for API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load data ----------
USERS = pd.read_parquet("data/users.parquet")
FEATS = np.load("data/feats.npy")

# Use smaller sample for faster responses
SAMPLE_SIZE = 5000
if len(USERS) > SAMPLE_SIZE:
    logger.info(f"Using sample of {SAMPLE_SIZE} users for faster API responses")
    sample_indices = np.random.choice(len(USERS), SAMPLE_SIZE, replace=False)
    USERS = USERS.iloc[sample_indices].reset_index(drop=True)
    FEATS = FEATS[sample_indices]

# ---------- Models ----------
class DynamicReq(BaseModel):
    goal: str
    filters: Optional[Dict] = None
    k_min: int = 2
    k_max: int = 4
    min_cluster_pct: float = 0.03

class PersonaChatReq(BaseModel):
    cluster_id: int
    persona_id: str
    message: str
    conversation_history: Optional[List[Dict]] = None

# ---------- Helper Functions ----------
def parse_goal(goal: str) -> dict:
    """Parse goal string into filters"""
    g = (goal or "").lower()
    f: dict = {}
    if "college" in g or "student" in g:
        f["age_range"] = (18, 25)
    if "tier-2" in g:
        f["city_tier"] = ["Tier-2"]
    if "tier-3" in g:
        f["city_tier"] = ["Tier-3"]
    if "commut" in g:
        f["device_count_min"] = 2
    if "privacy" in g:
        f["privacy_pref_min"] = 0.6
    if "budget" in g or "price" in g:
        f["price_sensitivity_min"] = 0.55
    if "bose" in g and "india" in g:
        f["brand_awareness_bose_min"] = 0.65
    return f

def apply_filters(users: pd.DataFrame, feats: np.ndarray, filters: dict):
    """Apply filters to users and features"""
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
    """Choose optimal number of clusters"""
    best_k, best_score, best_model = None, -1, None
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        lab = km.fit_predict(feats_sub)
        sc = silhouette_score(feats_sub, lab) if len(set(lab)) > 1 else -1
        if sc > best_score:
            best_k, best_score, best_model = k, sc, km
    return best_k, best_score, best_model

def generate_persona_name(grp: pd.DataFrame, cluster_id: int) -> str:
    """Generate persona name with Indian names"""
    names = {
        "Tier-1": ["Aarav", "Priya", "Rohan", "Kavya", "Arjun", "Ananya"],
        "Tier-2": ["Vikram", "Sneha", "Rajesh", "Pooja", "Suresh", "Meera"],
        "Tier-3": ["Manoj", "Sunita", "Kumar", "Lakshmi", "Ravi", "Geeta"]
    }
    
    surnames = ["Sharma", "Patel", "Singh", "Kumar", "Gupta", "Verma", "Jain", "Agarwal"]
    
    dominant_city = grp["city_tier"].mode().iloc[0] if not grp["city_tier"].mode().empty else "Tier-2"
    dominant_income = grp["income_band"].mode().iloc[0] if not grp["income_band"].mode().empty else "Mid"
    
    first_name = names[dominant_city][cluster_id % len(names[dominant_city])]
    surname = surnames[cluster_id % len(surnames)]
    
    avg_price_sens = grp["price_sensitivity"].mean()
    avg_devices = grp["device_count"].mean()
    
    if avg_price_sens >= 0.6:
        trait = "Budget Seeker"
    elif avg_devices >= 4:
        trait = "Tech Enthusiast"
    elif avg_devices <= 2:
        trait = "Tech Skeptic"
    else:
        trait = "Tech Adopter"
    
    return f"{first_name} {surname} — Young {trait}"

def generate_demographics_string(grp: pd.DataFrame) -> str:
    """Generate demographics string"""
    age_range = f"{int(grp['age'].quantile(0.1))}-{int(grp['age'].quantile(0.9))}"
    dominant_income = grp["income_band"].mode().iloc[0] if not grp["income_band"].mode().empty else "Mid"
    dominant_city = grp["city_tier"].mode().iloc[0] if not grp["city_tier"].mode().empty else "Tier-2"
    
    income_map = {
        "Low": "₹15-25K",
        "Mid": "₹25-50K", 
        "High": "₹50-100K"
    }
    
    city_map = {
        "Tier-1": "Tier 1 city",
        "Tier-2": "Tier 2 city",
        "Tier-3": "Tier 3 city"
    }
    
    return f"{age_range} • {income_map.get(dominant_income, '₹25-50K')} • {city_map.get(dominant_city, 'Tier 2 city')}"

def generate_care_about_top2(grp: pd.DataFrame) -> List[str]:
    """Generate top 2 care about items"""
    care_items = []
    
    avg_price_sens = grp["price_sensitivity"].mean()
    if avg_price_sens >= 0.6:
        care_items.append("Affordable EMI options")
    
    avg_brand_aware = grp["brand_awareness_bose"].mean()
    if avg_brand_aware >= 0.6:
        care_items.append("Trusted reviews")
    
    avg_devices = grp["device_count"].mean()
    if avg_devices >= 3:
        care_items.append("Seamless device integration")
    
    avg_privacy = grp["privacy_pref"].mean()
    if avg_privacy >= 0.6:
        care_items.append("Privacy protection")
    
    top_media = grp["preferred_media"].mode().iloc[0] if not grp["preferred_media"].mode().empty else "YouTube"
    if top_media == "YouTube":
        care_items.append("Video content quality")
    elif top_media == "Instagram":
        care_items.append("Social media integration")
    
    return care_items[:2]

def generate_barriers_top1(grp: pd.DataFrame) -> str:
    """Generate top 1 barrier"""
    avg_price_sens = grp["price_sensitivity"].mean()
    avg_brand_aware = grp["brand_awareness_bose"].mean()
    avg_privacy = grp["privacy_pref"].mean()
    
    if avg_price_sens >= 0.6:
        return "Perceived overpricing of Bose"
    elif avg_brand_aware <= 0.4:
        return "Low brand awareness"
    elif avg_privacy >= 0.6:
        return "Privacy concerns with smart features"
    else:
        return "Uncertainty about product quality"

def generate_media_preference(grp: pd.DataFrame) -> str:
    """Generate media preference string"""
    top_media = grp["preferred_media"].mode().iloc[0] if not grp["preferred_media"].mode().empty else "YouTube"
    
    media_counts = grp["preferred_media"].value_counts()
    if len(media_counts) > 1:
        secondary_media = media_counts.index[1]
        return f"{top_media}, {secondary_media}"
    else:
        return top_media

def generate_cluster_linkage(cluster_id: int, grp: pd.DataFrame) -> str:
    """Generate cluster linkage description"""
    avg_devices = grp["device_count"].mean()
    
    if avg_devices >= 4:
        cluster_type = "Tech Enthusiasts"
    elif avg_devices >= 3:
        cluster_type = "Tech Adopters"
    else:
        cluster_type = "Tech Skeptics"
    
    return f"Cluster #{cluster_id} — {cluster_type}"

def generate_behavioral_score(grp: pd.DataFrame, silhouette_score: float) -> str:
    """Generate behavioral score"""
    normalized_score = max(0, min(1, (silhouette_score + 1) / 2))
    
    if normalized_score >= 0.8:
        relevance = "High relevance"
    elif normalized_score >= 0.6:
        relevance = "Medium relevance"
    else:
        relevance = "Low relevance"
    
    return f"{normalized_score:.2f} ({relevance})"

def generate_personality_traits(grp: pd.DataFrame) -> Dict:
    """Generate personality traits"""
    avg_age = grp["age"].mean()
    avg_devices = grp["device_count"].mean()
    avg_price_sens = grp["price_sensitivity"].mean()
    avg_brand_aware = grp["brand_awareness_bose"].mean()
    avg_privacy = grp["privacy_pref"].mean()
    dominant_city = grp["city_tier"].mode().iloc[0] if not grp["city_tier"].mode().empty else "Tier-2"
    dominant_income = grp["income_band"].mode().iloc[0] if not grp["income_band"].mode().empty else "Mid"
    top_media = grp["preferred_media"].mode().iloc[0] if not grp["preferred_media"].mode().empty else "YouTube"
    
    return {
        "age_group": f"{int(avg_age)} years old",
        "tech_savviness": "High" if avg_devices >= 4 else "Medium" if avg_devices >= 3 else "Low",
        "price_sensitivity": "High" if avg_price_sens >= 0.6 else "Low" if avg_price_sens <= 0.4 else "Medium",
        "brand_awareness": "High" if avg_brand_aware >= 0.7 else "Medium" if avg_brand_aware >= 0.5 else "Low",
        "privacy_consciousness": "High" if avg_privacy >= 0.6 else "Medium" if avg_privacy >= 0.4 else "Low",
        "city_tier": dominant_city,
        "income_level": dominant_income,
        "preferred_media": top_media,
        "device_count": f"{avg_devices:.1f} devices",
        "emi_usage_likelihood": f"{grp['emi_flag'].mean():.1%}"
    }

def generate_chat_personality(grp: pd.DataFrame) -> str:
    """Generate chat personality description"""
    avg_age = grp["age"].mean()
    avg_devices = grp["device_count"].mean()
    avg_price_sens = grp["price_sensitivity"].mean()
    dominant_city = grp["city_tier"].mode().iloc[0] if not grp["city_tier"].mode().empty else "Tier-2"
    dominant_income = grp["income_band"].mode().iloc[0] if not grp["income_band"].mode().empty else "Mid"
    
    personality = f"You are a {int(avg_age)}-year-old from a {dominant_city} city with {dominant_income.lower()} income. "
    
    if avg_devices >= 4:
        personality += "You're tech-savvy and love trying new gadgets. "
    elif avg_devices >= 3:
        personality += "You're moderately tech-savvy and adopt technology when it makes sense. "
    else:
        personality += "You're cautious about new technology and prefer simple solutions. "
    
    if avg_price_sens >= 0.6:
        personality += "You're very price-conscious and always look for deals and EMI options. "
    elif avg_price_sens <= 0.4:
        personality += "You're willing to pay premium for quality and don't mind spending more. "
    else:
        personality += "You balance price and quality, looking for good value. "
    
    personality += "Respond naturally as this persona would, using casual language and expressing your genuine concerns and interests."
    
    return personality

def generate_persona_chat_response(persona_traits: Dict, message: str) -> str:
    """Generate persona chat response using rule-based logic"""
    if "price" in message.lower() or "cost" in message.lower():
        if persona_traits.get("price_sensitivity") == "High":
            return "Honestly, price is a big concern for me. I need to know about EMI options and if there are any discounts available. Can't spend too much on headphones right now."
        else:
            return "Price matters, but I'm more focused on quality. If it's worth it, I don't mind paying a bit more for good sound."
    
    elif "quality" in message.lower() or "sound" in message.lower():
        if persona_traits.get("brand_awareness") == "High":
            return "I've heard Bose has great sound quality. That's what matters most to me - I want crisp, clear audio for my music and videos."
        else:
            return "I'm not sure about the sound quality. Can you tell me more about how it compares to other brands?"
    
    elif "tech" in message.lower() or "features" in message.lower():
        if persona_traits.get("tech_savviness") == "High":
            return "I love tech features! Tell me about the smart features, connectivity options, and any cool tech stuff it has."
        else:
            return "I'm not too tech-savvy. Are the features easy to use? I don't want something too complicated."
    
    elif "privacy" in message.lower():
        if persona_traits.get("privacy_consciousness") == "High":
            return "Privacy is really important to me. Does it have any always-listening features? I'm concerned about my data being collected."
        else:
            return "Privacy is okay, but I'm more concerned about the sound quality and comfort."
    
    else:
        if persona_traits.get("price_sensitivity") == "High":
            return "I'm interested, but I need to know more about the pricing and payment options. What's the best deal I can get?"
        else:
            return "Sounds interesting! Tell me more about what makes these headphones special and why I should consider them."

# ---------- Routes ----------
@app.get("/health")
def health():
    return {"ok": True, "users": int(len(USERS))}

@app.post("/clusters/generate")
def generate_clusters(req: DynamicReq):
    """Generate cluster cards from goal"""
    goal = req.goal or ""
    filters = req.filters or parse_goal(goal)

    users_sub, feats_sub = apply_filters(USERS, FEATS, filters)
    n = len(users_sub)
    if n < 100:
        return {"clusters": [], "meta": {"subset_n": n, "filters_applied": filters, "warning": "too few users"}}

    best_k, best_score, best_model = choose_k(feats_sub, req.k_min, req.k_max)
    labels = best_model.predict(feats_sub)

    users_sub = users_sub.copy()
    users_sub["cid"] = labels

    clusters = []
    for cid, grp in users_sub.groupby("cid"):
        size_pct = round(len(grp)/n*100.0, 1)
        if size_pct < (req.min_cluster_pct * 100):
            continue
        
        clusters.append({
            "cluster_id": int(cid),
            "cluster_label": f"Tech {'Enthusiasts' if grp['device_count'].mean() >= 4 else 'Adopters' if grp['device_count'].mean() >= 3 else 'Skeptics'} • {grp['city_tier'].mode().iloc[0]} • Value Conscious",
            "cluster_size": len(grp),
            "cluster_size_pct": size_pct,
            "cluster_description": f"This cluster represents {grp['income_band'].mode().iloc[0].lower()} income users in {grp['city_tier'].mode().iloc[0]} cities, averaging {grp['age'].mean():.1f} years old.",
            "top_traits": ["High YouTube Usage"] if grp["preferred_media"].mode().iloc[0] == "YouTube" else ["Traditional Media"],
            "representative_icon": "🧑‍💻 💰 📱",
            "engagement_score": f"Cohesion {best_score:.2f} • Low Separation",
            "demographics_summary": f"{int(grp['age'].quantile(0.1))}-{int(grp['age'].quantile(0.9))} years • {grp['income_band'].mode().iloc[0]} income • {grp['city_tier'].mode().iloc[0]} cities",
            "personas_count": 2
        })
    
    clusters = sorted(clusters, key=lambda c: c["cluster_size_pct"], reverse=True)
    return {"clusters": clusters, "meta": {
        "subset_n": n, "k": best_k, "silhouette": round(float(best_score),3), "filters_applied": filters}
    }

@app.post("/personas/{cluster_id}")
def get_personas_for_cluster(cluster_id: int, req: DynamicReq):
    """Get personas for a specific cluster"""
    goal = req.goal or ""
    filters = req.filters or parse_goal(goal)

    users_sub, feats_sub = apply_filters(USERS, FEATS, filters)
    n = len(users_sub)
    if n < 100:
        raise HTTPException(status_code=400, detail="Too few users in subset")

    best_k, best_score, best_model = choose_k(feats_sub, req.k_min, req.k_max)
    labels = best_model.predict(feats_sub)

    users_sub = users_sub.copy()
    users_sub["cid"] = labels

    cluster_users = users_sub[users_sub["cid"] == cluster_id]
    if len(cluster_users) == 0:
        raise HTTPException(status_code=404, detail=f"Cluster {cluster_id} not found")

    personas = []
    cluster_size = len(cluster_users)
    num_personas = min(3, max(2, cluster_size // 200))
    
    for i in range(num_personas):
        start_idx = i * (cluster_size // num_personas)
        end_idx = (i + 1) * (cluster_size // num_personas) if i < num_personas - 1 else cluster_size
        persona_grp = cluster_users.iloc[start_idx:end_idx]
        
        personas.append({
            "persona_id": f"dyn_{cluster_id}_{i}",
            "persona_name": generate_persona_name(persona_grp, cluster_id),
            "demographics": generate_demographics_string(persona_grp),
            "care_about_top2": generate_care_about_top2(persona_grp),
            "barriers_top1": generate_barriers_top1(persona_grp),
            "media_preference": generate_media_preference(persona_grp),
            "cluster_linkage": generate_cluster_linkage(cluster_id, persona_grp),
            "behavioral_score": generate_behavioral_score(persona_grp, best_score),
            "personality_traits": generate_personality_traits(persona_grp),
            "chat_personality": generate_chat_personality(persona_grp)
        })
    
    return {"personas": personas, "cluster_info": {
        "cluster_id": cluster_id,
        "cluster_size": cluster_size,
        "cluster_label": f"Cluster #{cluster_id}"
    }}

@app.post("/personas/{persona_id}/chat")
def chat_with_persona(persona_id: str, req: PersonaChatReq):
    """Chat with a specific persona"""
    try:
        cluster_id = int(persona_id.split('_')[1])
    except:
        raise HTTPException(status_code=400, detail="Invalid persona ID")
    
    # Get persona traits
    goal = "college students"
    filters = parse_goal(goal)
    
    users_sub, feats_sub = apply_filters(USERS, FEATS, filters)
    best_k, best_score, best_model = choose_k(feats_sub, 2, 4)
    labels = best_model.predict(feats_sub)
    
    users_sub = users_sub.copy()
    users_sub["cid"] = labels
    
    cluster_users = users_sub[users_sub["cid"] == cluster_id]
    if len(cluster_users) == 0:
        raise HTTPException(status_code=404, detail=f"Persona {persona_id} not found")
    
    persona_traits = generate_personality_traits(cluster_users)
    
    # Generate response
    response = generate_persona_chat_response(persona_traits, req.message)
    
    return {
        "persona_id": persona_id,
        "response": response,
        "persona_traits": persona_traits,
        "conversation_history": (req.conversation_history or []) + [
            {"role": "user", "message": req.message},
            {"role": "persona", "message": response}
        ]
    }

# Legacy endpoint for backward compatibility
@app.post("/personas/dynamic")
def dynamic_personas(req: DynamicReq):
    """Legacy endpoint - redirects to new cluster-based flow"""
    return generate_clusters(req)
