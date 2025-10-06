#!/usr/bin/env python3
"""
Complete Demo of Dynamic Persona Generator Flow
Goal → Clusters → Personas → Chat with Personas
"""

import requests
import json
import time

API_BASE = "https://dyn-personas-656907085987.asia-south1.run.app"

def demo_complete_flow():
    print("🎯 Dynamic Persona Generator - Complete Flow Demo")
    print("=" * 60)
    
    # Step 1: Define Goal
    goal = "increase bose headphone adoption among college students in tier-2 cities"
    print(f"\n📝 Step 1: Goal = '{goal}'")
    
    # Step 2: Generate Clusters
    print("\n�� Step 2: Generating clusters...")
    try:
        response = requests.post(f"{API_BASE}/clusters/generate", 
                               json={"goal": goal, "detailed_personas": True},
                               timeout=30)
        clusters_data = response.json()
        
        if clusters_data.get("clusters"):
            print(f"✅ Found {len(clusters_data['clusters'])} clusters")
            
            # Display clusters
            for i, cluster in enumerate(clusters_data["clusters"], 1):
                print(f"\n📊 Cluster {i}: {cluster['cluster_label']}")
                print(f"   Size: {cluster['cluster_size_pct']}% ({cluster['cluster_size']:,} users)")
                print(f"   Traits: {', '.join(cluster['top_traits'])}")
                print(f"   Description: {cluster['cluster_description']}")
            
            # Step 3: Select first cluster and get personas
            selected_cluster = clusters_data["clusters"][0]
            cluster_id = selected_cluster["cluster_id"]
            
            print(f"\n🔄 Step 3: Loading personas for Cluster {cluster_id}...")
            
            personas_response = requests.post(f"{API_BASE}/personas/{cluster_id}",
                                           json={"goal": goal, "detailed_personas": True},
                                           timeout=30)
            personas_data = personas_response.json()
            
            if personas_data.get("personas"):
                print(f"✅ Found {len(personas_data['personas'])} personas")
                
                # Display personas
                for i, persona in enumerate(personas_data["personas"], 1):
                    print(f"\n👤 Persona {i}: {persona['persona_name']}")
                    print(f"   Demographics: {persona['demographics']}")
                    print(f"   Cares about: {', '.join(persona['care_about_top2'])}")
                    print(f"   Main barrier: {persona['barriers_top1']}")
                    print(f"   Media preference: {persona['media_preference']}")
                    print(f"   Behavioral score: {persona['behavioral_score']}")
                
                # Step 4: Chat with first persona
                selected_persona = personas_data["personas"][0]
                persona_id = selected_persona["persona_id"]
                
                print(f"\n💬 Step 4: Chatting with {selected_persona['persona_name']}")
                print("-" * 40)
                
                # Sample conversation
                conversation_history = []
                test_messages = [
                    "Hi! I'm interested in Bose headphones. What do you think about them?",
                    "What's your main concern about the price?",
                    "Do you care about sound quality?",
                    "What about EMI options? Would that help?"
                ]
                
                for message in test_messages:
                    print(f"\n👤 You: {message}")
                    
                    chat_response = requests.post(f"{API_BASE}/personas/{persona_id}/chat",
                                               json={
                                                   "cluster_id": cluster_id,
                                                   "persona_id": persona_id,
                                                   "message": message,
                                                   "conversation_history": conversation_history
                                               },
                                               timeout=30)
                    
                    chat_data = chat_response.json()
                    persona_response = chat_data["response"]
                    conversation_history = chat_data["conversation_history"]
                    
                    print(f"🤖 {selected_persona['persona_name']}: {persona_response}")
                    
                    time.sleep(1)  # Pause between messages
                
                print(f"\n✅ Complete flow demonstrated successfully!")
                print(f"📊 Summary:")
                print(f"   - Goal: {goal}")
                print(f"   - Clusters found: {len(clusters_data['clusters'])}")
                print(f"   - Personas in selected cluster: {len(personas_data['personas'])}")
                print(f"   - Chat messages exchanged: {len(conversation_history)}")
                
            else:
                print("❌ No personas found")
        else:
            print("❌ No clusters found")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_individual_endpoints():
    """Test individual API endpoints"""
    print("\n🔧 Testing Individual Endpoints")
    print("=" * 40)
    
    # Test health endpoint
    try:
        health_response = requests.get(f"{API_BASE}/health", timeout=10)
        health_data = health_response.json()
        print(f"✅ Health check: {health_data}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test clusters endpoint
    try:
        clusters_response = requests.post(f"{API_BASE}/clusters/generate",
                                        json={"goal": "college students"},
                                        timeout=30)
        clusters_data = clusters_response.json()
        print(f"✅ Clusters endpoint: Found {len(clusters_data.get('clusters', []))} clusters")
    except Exception as e:
        print(f"❌ Clusters endpoint failed: {e}")

if __name__ == "__main__":
    print("Starting Dynamic Persona Generator Demo...")
    
    # Test individual endpoints first
    test_individual_endpoints()
    
    # Run complete flow demo
    demo_complete_flow()
    
    print("\n�� Demo completed!")
