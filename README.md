# 🚀 Hybrid LLM+ML Multi-Agent System

A sophisticated persona generation system that combines the intelligence of Large Language Models (LLMs) with the reliability of Machine Learning (ML) algorithms.

## 🎯 What It Does

Takes a marketing goal like *"I want to introduce AI in my headphone brand, who could my customer be and how should I target them?"* and generates:

- **6 Customer Personas** with demographics, traits, and labels
- **Marketing Strategies** with campaigns, channels, and tactics
- **Targeting Recommendations** for your specific goal

## 🔧 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Data
```bash
python create_comprehensive_dataset.py
```

### 3. Test the System
```bash
python test_system.py
```

## 🤖 LLM Integration (Optional)

### With OpenAI API Key:
```bash
export ENABLE_LLM=1
export OPENAI_API_KEY=your_key_here
python test_system.py
```

### Without LLM (Rule-based Fallback):
```bash
# Just run without setting environment variables
python test_system.py
```

## 🎯 Test Your Own Goals

```python
from enhanced_multi_agent import EnhancedMultiAgentSystem

system = EnhancedMultiAgentSystem()
goal = "your marketing goal here"
analysis = system.agents['enhanced_goal_analyzer'].analyze_enhanced_goal(goal)
print(f"Intent: {analysis.intent}, Confidence: {analysis.confidence:.2f}")
```

## 🏗️ System Architecture

**6 Agents Working Together:**

1. **Enhanced Goal Analyzer** - Understands your marketing goal
2. **Audience Filterer** - Finds relevant users from 10K dataset
3. **Feature Engineer** - Creates 116+ marketing features
4. **Audience Clusterer** - Groups users into personas
5. **Persona Labeler** - Names and describes personas
6. **Strategy Generator** - Creates marketing strategies

## 🔄 Hybrid Approach

- **LLM Handles:** Decisions, labeling, creative suggestions
- **ML Handles:** Core computations, data processing, algorithms
- **Fallback:** System works perfectly without LLM

## 📊 Example Output

For your AI headphone brand goal, the system generates:

```
🎧 Persona 1: Mid-Age Female Audience • ₹5L-₹10L
   Size: 21.8% (218 users)
   Age: 32.9 years, Education: Graduate
   Digital Engagement: 0.79, Lifestyle Complexity: 1.22

🎧 Persona 2: Mid-Age Female Audience • ₹5L-₹10L
   Size: 21.3% (213 users)
   Age: 35.8 years, Education: Graduate
   Digital Engagement: 0.66, Lifestyle Complexity: 1.07
```

## 🚀 Key Features

- ✅ **101-feature comprehensive dataset**
- ✅ **LLM-assisted decision making**
- ✅ **Graceful fallback mechanisms**
- ✅ **Intent-aware clustering**
- ✅ **Marketing-focused persona generation**
- ✅ **End-to-end pipeline**

## 🔧 Troubleshooting

**Import Errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Data Errors:**
```bash
python create_comprehensive_dataset.py
```

**LLM Not Working:**
```bash
export ENABLE_LLM=1
export OPENAI_API_KEY=your_key_here
```

## 📁 Files

- `enhanced_multi_agent.py` - Main system with 6 agents
- `llm_agent.py` - LLM integration utilities
- `create_comprehensive_dataset.py` - Data generation
- `test_system.py` - Test script
- `requirements.txt` - Dependencies

## 🎯 Perfect For

- Marketing teams needing customer personas
- Product managers targeting specific audiences
- Data scientists building persona systems
- Anyone wanting to understand customer segments

---

**Ready to generate personas for your marketing goals?** 🚀

```bash
python test_system.py
```