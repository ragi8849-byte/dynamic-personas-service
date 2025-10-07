# 🚀 UI Integration - Quick Setup

## Your UI + Our API Integration

**Your UI shows:**
- Chat interface for user goals
- Audience segments with adoption likelihood  
- Persona cards with "Care About" and "Barriers"
- Canvas panel for project overview

**Our API provides:**
- `analyze_goal(goal)` - Quick goal analysis
- `generate_personas(goal)` - Complete E2E persona generation

## Quick Integration

### 1. Backend API Endpoint
```python
from persona_api import PersonaAPI
from flask import Flask, request, jsonify

app = Flask(__name__)
api = PersonaAPI()

@app.route('/api/analyze-goal', methods=['POST'])
def analyze_goal():
    goal = request.json['goal']
    result = api.analyze_goal(goal)
    return jsonify(result)

@app.route('/api/generate-personas', methods=['POST'])
def generate_personas():
    goal = request.json['goal']
    result = api.generate_personas(goal)
    return jsonify(result)
```

### 2. Frontend Integration
```javascript
// When user submits goal in chat
async function analyzeGoal(goal) {
    const response = await fetch('/api/analyze-goal', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({goal: goal})
    });
    return await response.json();
}

// Generate personas for canvas
async function generatePersonas(goal) {
    const response = await fetch('/api/generate-personas', {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({goal: goal})
    });
    return await response.json();
}
```

### 3. Map to Your UI Components

**Chat Interface:**
- User goal → `analyze_goal(goal)` → Intent, confidence, demographics

**Audience Segments:**
- `generate_personas(goal)` → Persona cards with adoption likelihood

**Canvas Panel:**
- Project goal → Complete persona analysis
- Competitors → Behavioral focus analysis

## Quick Test
```bash
python -c "
from persona_api import PersonaAPI
api = PersonaAPI()
goal = 'Bose wants to sell 9M smart speakers in 2026, competing with Sonos, Apple, JBL'
result = api.generate_personas(goal)
print(f'Generated {result[\"system_info\"][\"total_personas\"]} personas')
for persona in result['personas']:
    print(f'- {persona[\"name\"]} ({persona[\"size_percentage\"]:.1f}%)')
"
```

**Ready to integrate!** 🚀
