# �� Integrating Dynamic Persona Generator with Bolt AI

## Overview
Your Dynamic Persona Generator can be integrated with Bolt AI in multiple ways:

1. **Direct API Integration** - Bolt calls your API endpoints
2. **Bolt Plugin/Extension** - Create a Bolt-specific integration
3. **Webhook Integration** - Real-time persona updates
4. **Embedded Widget** - Direct UI integration

## Method 1: Direct API Integration (Recommended)

### Step 1: API Endpoints for Bolt
Your service provides these endpoints:

```bash
# Base URL
https://dyn-personas-656907085987.asia-south1.run.app

# Endpoints
POST /clusters/generate     # Generate clusters from goal
POST /personas/{cluster_id} # Get personas for cluster
POST /personas/{persona_id}/chat # Chat with persona
GET  /health                # Health check
```

### Step 2: Bolt AI Integration Code

```javascript
// Bolt AI Integration Example
class PersonaGeneratorIntegration {
  constructor() {
    this.apiBase = 'https://dyn-personas-656907085987.asia-south1.run.app';
  }

  async generatePersonasForGoal(goal) {
    try {
      // Step 1: Generate clusters
      const clustersResponse = await fetch(`${this.apiBase}/clusters/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal, detailed_personas: true })
      });
      
      const clusters = await clustersResponse.json();
      
      // Step 2: Get personas for first cluster
      const firstCluster = clusters.clusters[0];
      const personasResponse = await fetch(`${this.apiBase}/personas/${firstCluster.cluster_id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal, detailed_personas: true })
      });
      
      const personas = await personasResponse.json();
      
      return {
        clusters: clusters.clusters,
        personas: personas.personas,
        selectedCluster: firstCluster
      };
    } catch (error) {
      console.error('Persona generation failed:', error);
      throw error;
    }
  }

  async chatWithPersona(personaId, message, conversationHistory = []) {
    try {
      const response = await fetch(`${this.apiBase}/personas/${personaId}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cluster_id: this.extractClusterId(personaId),
          persona_id: personaId,
          message,
          conversation_history: conversationHistory
        })
      });
      
      return await response.json();
    } catch (error) {
      console.error('Chat failed:', error);
      throw error;
    }
  }

  extractClusterId(personaId) {
    return parseInt(personaId.split('_')[1]);
  }
}

// Usage in Bolt AI
const personaGen = new PersonaGeneratorIntegration();

// Generate personas for a business goal
const result = await personaGen.generatePersonasForGoal(
  "increase bose headphone adoption among college students"
);

console.log('Generated clusters:', result.clusters);
console.log('Generated personas:', result.personas);
```

## Method 2: Bolt Plugin/Extension

### Step 1: Create Bolt Plugin Structure

```javascript
// bolt-persona-plugin.js
class PersonaPlugin {
  constructor(bolt) {
    this.bolt = bolt;
    this.apiBase = 'https://dyn-personas-656907085987.asia-south1.run.app';
  }

  async initialize() {
    // Register persona generation command
    this.bolt.registerCommand('generate-personas', this.generatePersonas.bind(this));
    this.bolt.registerCommand('chat-persona', this.chatPersona.bind(this));
  }

  async generatePersonas(goal) {
    const response = await fetch(`${this.apiBase}/clusters/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal, detailed_personas: true })
    });
    
    const data = await response.json();
    
    // Format for Bolt AI display
    return {
      type: 'persona-clusters',
      clusters: data.clusters.map(cluster => ({
        id: cluster.cluster_id,
        title: cluster.cluster_label,
        description: cluster.cluster_description,
        size: `${cluster.cluster_size_pct}% (${cluster.cluster_size} users)`,
        traits: cluster.top_traits,
        icon: cluster.representative_icon
      }))
    };
  }

  async chatPersona(personaId, message) {
    const response = await fetch(`${this.apiBase}/personas/${personaId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        cluster_id: parseInt(personaId.split('_')[1]),
        persona_id: personaId,
        message,
        conversation_history: []
      })
    });
    
    const data = await response.json();
    
    return {
      type: 'persona-response',
      personaId,
      response: data.response,
      traits: data.persona_traits
    };
  }
}

// Export for Bolt AI
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PersonaPlugin;
}
```

## Method 3: Webhook Integration

### Step 1: Create Webhook Endpoint

```python
# webhook_handler.py
from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/webhook/bolt-persona-update")
async def handle_bolt_webhook(request: Request):
    data = await request.json()
    
    # Process Bolt AI request
    goal = data.get('goal')
    action = data.get('action')
    
    if action == 'generate_clusters':
        # Generate clusters and send back to Bolt
        response = requests.post(
            'https://dyn-personas-656907085987.asia-south1.run.app/clusters/generate',
            json={'goal': goal, detailed_personas: True}
        )
        
        return {
            'status': 'success',
            'clusters': response.json()['clusters']
        }
    
    elif action == 'chat_persona':
        # Handle persona chat
        persona_id = data.get('persona_id')
        message = data.get('message')
        
        response = requests.post(
            f'https://dyn-personas-656907085987.asia-south1.run.app/personas/{persona_id}/chat',
            json={
                'cluster_id': data.get('cluster_id'),
                'persona_id': persona_id,
                'message': message,
                'conversation_history': data.get('conversation_history', [])
            }
        )
        
        return {
            'status': 'success',
            'response': response.json()['response']
        }
```

## Method 4: Embedded Widget Integration

### Step 1: Create Embeddable Widget

```html
<!-- persona-widget.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Persona Generator Widget</title>
    <style>
        .persona-widget {
            width: 100%;
            max-width: 600px;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        .persona-card {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 15px;
            margin: 10px 0;
        }
        .chat-container {
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 15px;
            margin-top: 15px;
        }
        .chat-messages {
            height: 200px;
            overflow-y: auto;
            border: 1px solid #eee;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="persona-widget">
        <h3>🎯 Dynamic Persona Generator</h3>
        
        <!-- Goal Input -->
        <div>
            <label>Business Goal:</label>
            <input type="text" id="goal-input" placeholder="Enter your business goal...">
            <button onclick="generatePersonas()">Generate Personas</button>
        </div>
        
        <!-- Clusters Display -->
        <div id="clusters-container" style="display: none;">
            <h4>Generated Clusters:</h4>
            <div id="clusters-list"></div>
        </div>
        
        <!-- Personas Display -->
        <div id="personas-container" style="display: none;">
            <h4>Personas:</h4>
            <div id="personas-list"></div>
        </div>
        
        <!-- Chat Interface -->
        <div id="chat-container" class="chat-container" style="display: none;">
            <h4>Chat with Persona:</h4>
            <div id="chat-messages" class="chat-messages"></div>
            <input type="text" id="chat-input" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const API_BASE = 'https://dyn-personas-656907085987.asia-south1.run.app';
        let currentPersonas = [];
        let selectedPersonaId = null;

        async function generatePersonas() {
            const goal = document.getElementById('goal-input').value;
            if (!goal) return;

            try {
                const response = await fetch(`${API_BASE}/clusters/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ goal, detailed_personas: true })
                });

                const data = await response.json();
                displayClusters(data.clusters);
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function displayClusters(clusters) {
            const container = document.getElementById('clusters-container');
            const list = document.getElementById('clusters-list');
            
            list.innerHTML = clusters.map(cluster => `
                <div class="persona-card" onclick="loadPersonas(${cluster.cluster_id})">
                    <strong>${cluster.cluster_label}</strong><br>
                    ${cluster.cluster_size_pct}% of audience (${cluster.cluster_size} users)<br>
                    <small>${cluster.cluster_description}</small>
                </div>
            `).join('');
            
            container.style.display = 'block';
        }

        async function loadPersonas(clusterId) {
            try {
                const response = await fetch(`${API_BASE}/personas/${clusterId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ goal: document.getElementById('goal-input').value, detailed_personas: true })
                });

                const data = await response.json();
                displayPersonas(data.personas);
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function displayPersonas(personas) {
            const container = document.getElementById('personas-container');
            const list = document.getElementById('personas-list');
            
            list.innerHTML = personas.map(persona => `
                <div class="persona-card" onclick="startChat('${persona.persona_id}')">
                    <strong>${persona.persona_name}</strong><br>
                    ${persona.demographics}<br>
                    <small>Cares about: ${persona.care_about_top2.join(', ')}</small>
                </div>
            `).join('');
            
            container.style.display = 'block';
            currentPersonas = personas;
        }

        function startChat(personaId) {
            selectedPersonaId = personaId;
            document.getElementById('chat-container').style.display = 'block';
            
            // Add welcome message
            const messages = document.getElementById('chat-messages');
            messages.innerHTML = '<div>Hello! I\'m ready to chat about your product.</div>';
        }

        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message || !selectedPersonaId) return;

            // Add user message
            addMessage('You', message);
            input.value = '';

            try {
                const response = await fetch(`${API_BASE}/personas/${selectedPersonaId}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        cluster_id: parseInt(selectedPersonaId.split('_')[1]),
                        persona_id: selectedPersonaId,
                        message,
                        conversation_history: []
                    })
                });

                const data = await response.json();
                addMessage('Persona', data.response);
            } catch (error) {
                console.error('Error:', error);
                addMessage('Persona', 'Sorry, I encountered an error.');
            }
        }

        function addMessage(sender, message) {
            const messages = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
```

## Method 5: Bolt AI Specific Integration

### Step 1: Bolt AI Configuration

```yaml
# bolt-config.yaml
integrations:
  persona_generator:
    api_base: "https://dyn-personas-656907085987.asia-south1.run.app"
    endpoints:
      clusters: "/clusters/generate"
      personas: "/personas/{cluster_id}"
      chat: "/personas/{persona_id}/chat"
    timeout: 30
    retry_attempts: 3

commands:
  generate_personas:
    description: "Generate personas for a business goal"
    parameters:
      goal:
        type: string
        required: true
        description: "Business goal or target audience"
    handler: "persona_generator.generatePersonas"
  
  chat_persona:
    description: "Chat with a specific persona"
    parameters:
      persona_id:
        type: string
        required: true
      message:
        type: string
        required: true
    handler: "persona_generator.chatPersona"
```

### Step 2: Bolt AI Handler

```python
# bolt_handlers.py
import requests
from typing import Dict, Any

class PersonaGeneratorHandler:
    def __init__(self, config: Dict[str, Any]):
        self.api_base = config['integrations']['persona_generator']['api_base']
        self.timeout = config['integrations']['persona_generator']['timeout']
    
    async def generate_personas(self, goal: str) -> Dict[str, Any]:
        """Generate personas for a business goal"""
        try:
            response = requests.post(
                f"{self.api_base}/clusters/generate",
                json={"goal": goal, "detailed_personas": True},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "clusters": data.get("clusters", []),
                    "meta": data.get("meta", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def chat_persona(self, persona_id: str, message: str) -> Dict[str, Any]:
        """Chat with a specific persona"""
        try:
            cluster_id = int(persona_id.split('_')[1])
            
            response = requests.post(
                f"{self.api_base}/personas/{persona_id}/chat",
                json={
                    "cluster_id": cluster_id,
                    "persona_id": persona_id,
                    "message": message,
                    "conversation_history": []
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "response": data.get("response", ""),
                    "persona_traits": data.get("persona_traits", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

## Testing Your Integration

### Step 1: Test API Endpoints

```bash
# Test health
curl https://dyn-personas-656907085987.asia-south1.run.app/health

# Test cluster generation
curl -X POST https://dyn-personas-656907085987.asia-south1.run.app/clusters/generate \
  -H "Content-Type: application/json" \
  -d '{"goal": "college students"}'

# Test persona chat
curl -X POST https://dyn-personas-656907085987.asia-south1.run.app/personas/dyn_1_0/chat \
  -H "Content-Type: application/json" \
  -d '{"cluster_id": 1, "persona_id": "dyn_1_0", "message": "Hello!"}'
```

### Step 2: Integration Checklist

- [ ] API endpoints are accessible
- [ ] CORS headers are properly set
- [ ] Error handling is implemented
- [ ] Rate limiting is considered
- [ ] Authentication (if needed) is configured
- [ ] Response format matches Bolt AI expectations
- [ ] Timeout settings are appropriate
- [ ] Retry logic is implemented

## Best Practices for Bolt AI Integration

1. **Error Handling**: Always handle API failures gracefully
2. **Caching**: Cache persona data to reduce API calls
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Authentication**: Add API keys if needed for production
5. **Monitoring**: Add logging and monitoring for API calls
6. **Documentation**: Document all endpoints and parameters
7. **Testing**: Test all integration scenarios thoroughly

## Production Considerations

1. **Scalability**: Your API can handle multiple concurrent requests
2. **Reliability**: Implement retry logic and fallback mechanisms
3. **Security**: Add authentication and input validation
4. **Monitoring**: Monitor API performance and usage
5. **Backup**: Have backup strategies for API failures

Your Dynamic Persona Generator is ready for Bolt AI integration! 🚀
