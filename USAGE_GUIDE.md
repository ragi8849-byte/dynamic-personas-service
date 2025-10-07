# 🚀 Clean Persona API - Usage Guide

## 📋 Core Files (Cleaned Up)

```
📁 Core Files:
├── enhanced_multi_agent.py    # Main multi-agent system
├── llm_agent.py              # LLM integration utilities  
├── persona_api.py            # Clean API interface
├── create_comprehensive_dataset.py  # Data generation
├── test_system.py            # Test script
└── requirements.txt          # Dependencies
```

## 🎯 API Endpoints

### **Endpoint 1: `analyze_goal(goal)`**
Analyzes a marketing goal and returns structured analysis.

**Usage:**
```python
from persona_api import PersonaAPI
api = PersonaAPI()

result = api.analyze_goal("Increase apple watch adoption among fitness enthusiasts")
print(result)
```

**Output:**
```json
{
  "goal": "Increase apple watch adoption among fitness enthusiasts",
  "intent": "reach",
  "confidence": 0.50,
  "demographics": {},
  "behavioral_focus": ["health"],
  "psychographics": {},
  "commerce_patterns": [],
  "media_preferences": [],
  "lifestyle_segments": []
}
```

### **Endpoint 2: `generate_personas(goal)`**
Generates complete personas for a marketing goal (full E2E pipeline).

**Usage:**
```python
from persona_api import PersonaAPI
api = PersonaAPI()

result = api.generate_personas("Increase apple watch adoption among fitness enthusiasts")
print(result)
```

**Output:**
```json
{
  "goal": "Increase apple watch adoption among fitness enthusiasts",
  "goal_analysis": {
    "intent": "reach",
    "confidence": 0.50,
    "demographics": {},
    "behavioral_focus": ["health"]
  },
  "audience_filtering": {
    "filtered_users": 2000,
    "total_features": 117
  },
  "clustering": {
    "optimal_clusters": 3,
    "algorithm": "kmeans"
  },
  "personas": [
    {
      "id": 0,
      "name": "Mid-Age Female Audience • ₹2L-₹5L",
      "size_percentage": 29.9,
      "size_users": 598,
      "demographics": {
        "avg_age": 35.6,
        "dominant_gender": "Female",
        "dominant_income": "₹2L-₹5L",
        "dominant_education": "Secondary"
      },
      "behavioral_scores": {
        "spending_power": 1.08,
        "digital_engagement": 0.64,
        "lifestyle_complexity": 1.29
      }
    }
  ],
  "system_info": {
    "llm_enabled": true,
    "total_personas": 3
  }
}
```

## 🚀 Quick Usage Examples

### **1. Quick Goal Analysis**
```bash
python -c "
from persona_api import PersonaAPI
api = PersonaAPI()
result = api.analyze_goal('target tech professionals for B2B software')
print(f'Intent: {result[\"intent\"]}, Confidence: {result[\"confidence\"]:.2f}')
"
```

### **2. Complete Persona Generation**
```bash
python -c "
from persona_api import PersonaAPI
api = PersonaAPI()
result = api.generate_personas('target tech professionals for B2B software')
print(f'Generated {result[\"system_info\"][\"total_personas\"]} personas')
for persona in result['personas']:
    print(f'- {persona[\"name\"]} ({persona[\"size_percentage\"]:.1f}%)')
"
```

### **3. Test Multiple Goals**
```bash
python -c "
from persona_api import PersonaAPI
api = PersonaAPI()

goals = [
    'engage fitness enthusiasts for health app',
    'convert high-income consumers for luxury brand sales',
    'retain millennial parents for family products'
]

for goal in goals:
    result = api.analyze_goal(goal)
    print(f'{goal}: {result[\"intent\"]} (confidence: {result[\"confidence\"]:.2f})')
"
```

## 🤖 LLM Integration

### **Enable LLM:**
```bash
export ENABLE_LLM=1
export OPENAI_API_KEY=your_key_here
```

### **Disable LLM (Rule-based fallback):**
```bash
unset ENABLE_LLM
unset OPENAI_API_KEY
```

## 📊 System Capabilities

- ✅ **101-feature comprehensive dataset**
- ✅ **6-agent multi-agent system**
- ✅ **LLM-assisted decision making**
- ✅ **Graceful fallback mechanisms**
- ✅ **Intent-aware clustering**
- ✅ **Marketing-focused persona generation**
- ✅ **End-to-end pipeline**

## 🎯 Perfect For

- Marketing teams needing customer personas
- Product managers targeting specific audiences
- Data scientists building persona systems
- Anyone wanting to understand customer segments

## 🔧 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Generate data (if needed)
python create_comprehensive_dataset.py

# Test the system
python test_system.py
```

---

**Ready to generate personas? Use the clean API endpoints above!** 🚀
