# 🤖 LLM Integration Guide for Dynamic Persona Generator

## Current Status: Rule-Based Chat

**Your current chat system uses rule-based responses, not an actual LLM.**

### How Current Chat Works:

```python
# Rule-based responses based on keywords and persona traits
if "price" in message.lower():
    if persona_traits["price_sensitivity"] == "High":
        return "Honestly, price is a big concern for me..."
    else:
        return "Price matters, but I'm more focused on quality..."
```

## 🚀 Adding Real LLM Integration

### Option 1: OpenAI Integration

#### Step 1: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Set environment variable: `export OPENAI_API_KEY="your-key-here"`

#### Step 2: Update Your API
Replace `app/main.py` with `app/main_with_llm.py`:

```bash
cp app/main_with_llm.py app/main.py
```

#### Step 3: Test LLM Chat
```bash
curl -X POST "https://your-api-url/personas/dyn_1_0/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "cluster_id": 1,
    "persona_id": "dyn_1_0", 
    "message": "What do you think about Bose headphones?",
    "llm_provider": "openai"
  }'
```

### Option 2: Anthropic Claude Integration

#### Step 1: Get Anthropic API Key
1. Go to https://console.anthropic.com/
2. Create a new API key
3. Set environment variable: `export ANTHROPIC_API_KEY="your-key-here"`

#### Step 2: Test Claude Chat
```bash
curl -X POST "https://your-api-url/personas/dyn_1_0/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "cluster_id": 1,
    "persona_id": "dyn_1_0",
    "message": "What do you think about Bose headphones?", 
    "llm_provider": "anthropic"
  }'
```

### Option 3: Google Gemini Integration

#### Step 1: Get Google API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Set environment variable: `export GOOGLE_API_KEY="your-key-here"`

#### Step 2: Test Gemini Chat
```bash
curl -X POST "https://your-api-url/personas/dyn_1_0/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "cluster_id": 1,
    "persona_id": "dyn_1_0",
    "message": "What do you think about Bose headphones?",
    "llm_provider": "google"
  }'
```

## 🔧 LLM Integration Features

### Automatic Fallback
- If LLM API fails → Falls back to rule-based responses
- If no API key → Uses rule-based responses
- If timeout → Uses rule-based responses

### Persona Context
Each LLM call includes:
- **Persona Traits:** Age, tech savviness, price sensitivity, etc.
- **Personality:** Detailed personality description
- **Conversation History:** Previous messages for context
- **System Prompt:** Instructions for persona behavior

### Example LLM Prompt:
```
You are a persona in a market research study. Here are your characteristics:

{
  "age_group": "21 years old",
  "tech_savviness": "Medium", 
  "price_sensitivity": "High",
  "brand_awareness": "Low",
  "privacy_consciousness": "Medium",
  "city_tier": "Tier-2",
  "income_level": "Mid",
  "preferred_media": "YouTube",
  "device_count": "3.0 devices",
  "emi_usage_likelihood": "44.4%"
}

Your personality: You are a 21-year-old from a Tier-2 city with mid income. You're moderately tech-savvy and adopt technology when it makes sense. You're very price-conscious and always look for deals and EMI options. Respond naturally as this persona would, using casual language and expressing your genuine concerns and interests.

User message: What do you think about Bose headphones?

Response:
```

## 📊 Comparison: Rule-Based vs LLM

| Feature | Rule-Based | LLM |
|---------|------------|-----|
| **Response Quality** | Basic, predictable | Natural, contextual |
| **Cost** | Free | Pay per API call |
| **Speed** | Instant | 1-3 seconds |
| **Reliability** | Always works | Depends on API |
| **Customization** | Limited | Highly flexible |
| **Context Awareness** | Keyword-based | Full conversation |

## 🎯 Recommended Approach

### For Development/Testing:
- **Use rule-based responses** (current system)
- Fast, reliable, free
- Good for testing persona generation

### For Production:
- **Add LLM integration** with fallback
- Better user experience
- More natural conversations
- Automatic fallback ensures reliability

## 🚀 Quick Start with LLM

1. **Choose your LLM provider** (OpenAI, Anthropic, Google)
2. **Get API key** from provider
3. **Set environment variable** in your deployment
4. **Update API code** with LLM integration
5. **Test with `llm_provider` parameter**

### Example Deployment with OpenAI:

```bash
# Set API key in Cloud Run
gcloud run services update dyn-personas \
  --set-env-vars OPENAI_API_KEY="your-key-here"

# Test LLM chat
curl -X POST "https://dyn-personas-656907085987.asia-south1.run.app/personas/dyn_1_0/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "cluster_id": 1,
    "persona_id": "dyn_1_0",
    "message": "What do you think about Bose headphones?",
    "llm_provider": "openai"
  }'
```

## 💡 Pro Tips

1. **Start with rule-based** for development
2. **Add LLM for production** with fallback
3. **Monitor API costs** and usage
4. **Test different providers** for best results
5. **Use conversation history** for better context
6. **Set reasonable timeouts** (15 seconds)
7. **Implement rate limiting** for API calls

Your persona generator is ready for LLM integration! 🎉
