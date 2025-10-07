# Dynamic Persona Generator API

A FastAPI service that generates dynamic personas from business goals using machine learning clustering.

## Features

- **Goal-based clustering**: Generate user clusters from business goals
- **Dynamic personas**: Create detailed personas with Indian names and demographics
- **Rule-based chat**: Chat with personas using contextual responses
- **Optimized performance**: Uses 5K user sample for fast responses
- **RESTful API**: Clean endpoints for integration

## API Endpoints

### Health Check
```bash
GET /health
```

### Generate Clusters
```bash
POST /clusters/generate
Content-Type: application/json

{
  "goal": "college students interested in headphones",
  "k_min": 2,
  "k_max": 4,
  "min_cluster_pct": 0.03
}
```

### Get Personas for Cluster
```bash
POST /personas/{cluster_id}
Content-Type: application/json

{
  "goal": "college students interested in headphones"
}
```

### Chat with Persona
```bash
POST /personas/{persona_id}/chat
Content-Type: application/json

{
  "cluster_id": 1,
  "persona_id": "dyn_1_0",
  "message": "What do you think about Bose headphones?",
  "conversation_history": []
}
```

### Legacy Endpoint
```bash
POST /personas/dynamic
Content-Type: application/json

{
  "goal": "college students interested in headphones"
}
```

## Response Format

### Cluster Response
```json
{
  "clusters": [
    {
      "cluster_id": 1,
      "cluster_label": "Tech Adopters • Tier-1 • Value Conscious",
      "cluster_size": 390,
      "cluster_size_pct": 37.2,
      "cluster_description": "This cluster represents mid income users in Tier-1 cities...",
      "top_traits": ["High YouTube Usage"],
      "representative_icon": "🧑‍💻 💰 📱",
      "engagement_score": "Cohesion 0.12 • Low Separation",
      "demographics_summary": "18-25 years • Mid income • Tier-1 cities",
      "personas_count": 3
    }
  ],
  "meta": {
    "subset_n": 1048,
    "k": 4,
    "silhouette": 0.122,
    "filters_applied": {"age_range": [18, 25]}
  }
}
```

### Persona Response
```json
{
  "personas": [
    {
      "persona_id": "dyn_1_0",
      "persona_name": "Priya Patel — Young Tech Adopter",
      "demographics": "18-24 • ₹25-50K • Tier 1 city",
      "care_about_top2": ["Seamless device integration", "Video content quality"],
      "barriers_top1": "Uncertainty about product quality",
      "media_preference": "YouTube, Instagram",
      "cluster_linkage": "Cluster #1 — Tech Adopters",
      "behavioral_score": "0.58 (Low relevance)",
      "personality_traits": {
        "age_group": "21 years old",
        "tech_savviness": "Medium",
        "price_sensitivity": "Medium",
        "brand_awareness": "Medium",
        "privacy_consciousness": "Low",
        "city_tier": "Tier-1",
        "income_level": "Mid",
        "preferred_media": "YouTube",
        "device_count": "3.0 devices",
        "emi_usage_likelihood": "44.4%"
      },
      "chat_personality": "You are a 21-year-old from a Tier-1 city..."
    }
  ],
  "cluster_info": {
    "cluster_id": 1,
    "cluster_size": 390,
    "cluster_label": "Cluster #1"
  }
}
```

### Chat Response
```json
{
  "persona_id": "dyn_1_0",
  "response": "Sounds interesting! Tell me more about what makes these headphones special and why I should consider them.",
  "persona_traits": {
    "age_group": "21 years old",
    "tech_savviness": "Medium",
    "price_sensitivity": "Medium",
    "brand_awareness": "Medium",
    "privacy_consciousness": "Low",
    "city_tier": "Tier-1",
    "income_level": "Mid",
    "preferred_media": "YouTube",
    "device_count": "3.0 devices",
    "emi_usage_likelihood": "44.4%"
  },
  "conversation_history": [
    {"role": "user", "message": "What do you think about Bose headphones?"},
    {"role": "persona", "message": "Sounds interesting! Tell me more..."}
  ]
}
```

## Local Development

### Setup
```bash
# Clone repository
git clone <repository-url>
cd synthetic-personas/dyn-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate data
cd scripts
python generate_data.py
cd ..

# Run API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Test API
```bash
# Health check
curl http://localhost:8000/health

# Generate clusters
curl -X POST http://localhost:8000/clusters/generate \
  -H "Content-Type: application/json" \
  -d '{"goal": "college students"}'

# Chat with persona
curl -X POST http://localhost:8000/personas/dyn_1_0/chat \
  -H "Content-Type: application/json" \
  -d '{"cluster_id": 1, "persona_id": "dyn_1_0", "message": "Hello!"}'
```

## Docker Deployment

### Build and Run
```bash
# Build image
docker build -t dynamic-personas .

# Run container
docker run -p 8080:8080 dynamic-personas
```

### Test Docker
```bash
curl http://localhost:8080/health
```

## Production Deployment

The API is deployed on Google Cloud Run:
- **URL**: `https://dyn-personas-656907085987.asia-south1.run.app`
- **Health**: `https://dyn-personas-656907085987.asia-south1.run.app/health`

## Chat System

The chat system uses **rule-based responses** based on:
- Keywords in messages (`price`, `quality`, `tech`, `privacy`)
- Persona traits (price sensitivity, tech savviness, brand awareness)
- Pre-written contextual responses

### Example Chat Flow
1. User: "What about the price?"
2. Persona: "Honestly, price is a big concern for me. I need to know about EMI options..."

## Data

- **Dataset**: 5,000 synthetic users (sampled from 50,000)
- **Features**: Age, income, city tier, media preferences, device usage, etc.
- **Clustering**: K-means with silhouette score optimization
- **Personas**: 2-3 personas per cluster with detailed traits

## Performance

- **Response time**: < 30 seconds for cluster generation
- **Chat response**: Instant (rule-based)
- **Memory usage**: Optimized for 5K users
- **Scalability**: Ready for horizontal scaling

## License

MIT License
