# Quick Start Guide

## Running the Application

### 1. Using Docker (Easiest)

```bash
docker build -t persona-generator .
docker run -p 8080:8080 persona-generator
```

Open http://localhost:8080

### 2. Using the Run Script

```bash
./run.sh
```

### 3. Manual Python Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```

Open http://localhost:8000

## Using the Web Interface

### Step 1: Enter Your Goal
Type a business goal or target audience description:
- "College students in tier-2 cities"
- "Budget-conscious tech enthusiasts"
- "Privacy-focused premium buyers"

Click **Generate Clusters**

### Step 2: Explore Clusters
- View 2-4 automatically generated customer segments
- Each shows demographics, traits, and audience size
- Click any cluster to explore personas

### Step 3: Select a Persona
- View 2-3 detailed personas per cluster
- Each has unique characteristics and behaviors
- Click a persona to start chatting

### Step 4: Chat with Persona
Ask questions like:
- "What do you think about the price?"
- "Are you concerned about privacy?"
- "What features matter most to you?"
- "Would you use EMI options?"

## Example Goals to Try

1. **Tech Product Launch**
   - "Increase Bose headphone adoption across India"
   - "Target college students in tier-2 cities"

2. **Budget Segment**
   - "Budget-conscious commuters"
   - "Price-sensitive young professionals"

3. **Privacy Focused**
   - "Privacy-conscious tech users"
   - "Users concerned about data collection"

4. **Premium Segment**
   - "Premium buyers willing to pay more"
   - "High-income tech enthusiasts"

## API Usage Examples

### Generate Clusters
```bash
curl -X POST http://localhost:8080/clusters/generate \
  -H "Content-Type: application/json" \
  -d '{"goal": "college students in tier-2 cities"}'
```

### Get Personas for Cluster
```bash
curl -X POST http://localhost:8080/personas/0 \
  -H "Content-Type: application/json" \
  -d '{"goal": "college students"}'
```

### Chat with Persona
```bash
curl -X POST http://localhost:8080/personas/dyn_0_0/chat \
  -H "Content-Type: application/json" \
  -d '{
    "cluster_id": 0,
    "persona_id": "dyn_0_0",
    "message": "What do you think about the price?"
  }'
```

## Troubleshooting

### Port Already in Use
```bash
# Change the port
uvicorn app.main:app --port 8001
# Or for Docker
docker run -p 8081:8080 persona-generator
```

### Data Files Missing
Make sure `data/users.parquet` and `data/feats.npy` exist. If not:
```bash
python scripts/generate_data.py
```

### Module Not Found
```bash
pip install -r requirements.txt
```

## Tips for Best Results

1. **Be Specific**: More specific goals generate better clusters
2. **Try Variations**: Test different goal descriptions
3. **Explore All Personas**: Each has unique characteristics
4. **Ask Follow-ups**: Build a conversation with personas
5. **Check Metadata**: Review silhouette scores and cluster sizes

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API at http://localhost:8080/docs
- Customize personas in `app/main.py`
- Modify the interface in `static/index.html`
