# Dynamic Persona Generator

An AI-powered customer segmentation and persona chat system that uses machine learning clustering to generate detailed customer personas and enables interactive conversations with them.

## Features

- **Goal-Based Clustering**: Enter a business goal or target audience description and automatically generate relevant customer segments
- **Dynamic Persona Generation**: Create detailed, data-driven personas from clustered user data
- **Interactive Chat**: Chat with personas to understand their preferences, concerns, and behaviors
- **Modern Web Interface**: Clean, responsive UI with step-by-step workflow

## Architecture

- **Backend**: FastAPI (Python) with scikit-learn for ML clustering
- **Frontend**: Vanilla JavaScript with modern CSS
- **Data**: Pre-generated user dataset with 5,000 sample users
- **Clustering**: K-Means with silhouette scoring for optimal cluster selection

## Getting Started

### Option 1: Using Docker (Recommended)

```bash
# Build and run with Docker
docker build -t persona-generator .
docker run -p 8080:8080 persona-generator
```

Then open http://localhost:8080 in your browser.

### Option 2: Using run.sh Script

```bash
# Make the script executable (first time only)
chmod +x run.sh

# Run the application
./run.sh
```

The script will automatically use Docker if available, otherwise fallback to local Python.

### Option 3: Local Python Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open http://localhost:8000 in your browser.

## How to Use

### Step 1: Define Your Goal
Enter a business goal or target audience description. Examples:
- "Increase Bose headphone adoption among college students in tier-2 cities"
- "Target budget-conscious commuters who care about privacy"
- "Reach tech enthusiasts in tier-1 cities"

### Step 2: Select a Cluster
Review the automatically generated customer segments. Each cluster shows:
- Demographic profile
- Key traits and characteristics
- Size and percentage of audience
- Cohesion score

### Step 3: Choose a Persona
Select a specific persona within the cluster. Each persona includes:
- Name and demographics
- What they care about
- Key barriers to adoption
- Media preferences
- Behavioral score

### Step 4: Chat with Persona
Interact with the persona to understand:
- Pricing concerns
- Feature preferences
- Privacy considerations
- Tech savviness
- Purchase barriers

## API Endpoints

### `GET /`
Serves the web interface

### `GET /health`
Health check endpoint
```json
{
  "ok": true,
  "users": 5000
}
```

### `POST /clusters/generate`
Generate clusters from a goal
```json
{
  "goal": "college students in tier-2 cities",
  "k_min": 2,
  "k_max": 4,
  "detailed_personas": true
}
```

### `POST /personas/{cluster_id}`
Get personas for a specific cluster

### `POST /personas/{persona_id}/chat`
Chat with a specific persona

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── data/
│   ├── users.parquet        # User dataset
│   ├── feats.npy           # Feature matrix
│   └── encoders.pkl        # Label encoders
├── static/
│   └── index.html          # Web interface
├── scripts/
│   └── generate_data.py    # Data generation script
├── Dockerfile
├── requirements.txt
├── run.sh                  # Quick start script
└── README.md
```

## Data Schema

The user dataset includes:
- **Demographics**: age, city_tier, income_band
- **Behavior**: device_count, purchase_intent, emi_flag
- **Preferences**: privacy_pref, price_sensitivity, preferred_media
- **Brand Awareness**: brand_awareness_bose

## Technologies

- **FastAPI**: Modern Python web framework
- **scikit-learn**: Machine learning clustering
- **pandas/numpy**: Data manipulation
- **uvicorn**: ASGI server
- **Docker**: Containerization

## Development

### Adding New Features

1. Modify `app/main.py` for backend changes
2. Update `static/index.html` for frontend changes
3. Regenerate data if needed using `scripts/generate_data.py`

### Customizing Personas

Edit the persona generation functions in `app/main.py`:
- `generate_persona_name()`
- `generate_demographics_string()`
- `generate_personality_traits()`
- `generate_chat_personality()`

### Modifying Clustering

Adjust clustering parameters in the API request:
- `k_min`: Minimum number of clusters
- `k_max`: Maximum number of clusters
- `min_cluster_pct`: Minimum cluster size percentage

## Performance

- Uses optimized 5,000 user sample for fast responses
- Clustering typically completes in < 2 seconds
- Persona generation is near-instantaneous
- Chat responses use rule-based system (can be upgraded to LLM)

## Future Enhancements

- [ ] Integration with actual LLM for more natural conversations
- [ ] Real-time data updates from production systems
- [ ] Export personas to PDF/CSV
- [ ] Multi-language support
- [ ] A/B testing framework
- [ ] Advanced visualization and analytics

## License

This project is for demonstration purposes.
