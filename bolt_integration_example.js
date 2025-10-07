/**
 * Bolt AI Integration Example for Dynamic Persona Generator
 * 
 * This example shows how to integrate your persona generator with Bolt AI
 * using the deployed API endpoints.
 */

class BoltPersonaIntegration {
  constructor() {
    this.apiBase = 'https://dyn-personas-656907085987.asia-south1.run.app';
    this.conversationHistory = new Map(); // Store conversation history per persona
  }

  /**
   * Generate personas for a business goal
   * @param {string} goal - Business goal or target audience
   * @returns {Promise<Object>} Generated clusters and personas
   */
  async generatePersonas(goal) {
    try {
      console.log(`🎯 Generating personas for goal: "${goal}"`);
      
      // Step 1: Generate clusters
      const clustersResponse = await fetch(`${this.apiBase}/clusters/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          goal: goal,
          detailed_personas: true
        })
      });

      if (!clustersResponse.ok) {
        throw new Error(`Clusters API failed: ${clustersResponse.status}`);
      }

      const clustersData = await clustersResponse.json();
      console.log(`✅ Generated ${clustersData.clusters.length} clusters`);

      // Step 2: Get personas for the first cluster (most relevant)
      const firstCluster = clustersData.clusters[0];
      const personasResponse = await fetch(`${this.apiBase}/personas/${firstCluster.cluster_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          goal: goal,
          detailed_personas: true
        })
      });

      if (!personasResponse.ok) {
        throw new Error(`Personas API failed: ${personasResponse.status}`);
      }

      const personasData = await personasResponse.json();
      console.log(`✅ Generated ${personasData.personas.length} personas`);

      return {
        success: true,
        goal: goal,
        clusters: clustersData.clusters,
        personas: personasData.personas,
        selectedCluster: firstCluster,
        meta: clustersData.meta
      };

    } catch (error) {
      console.error('❌ Persona generation failed:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Chat with a specific persona
   * @param {string} personaId - Persona ID (e.g., "dyn_1_0")
   * @param {string} message - User message
   * @returns {Promise<Object>} Persona response and traits
   */
  async chatWithPersona(personaId, message) {
    try {
      console.log(`💬 Chatting with persona ${personaId}: "${message}"`);
      
      // Get conversation history for this persona
      const history = this.conversationHistory.get(personaId) || [];
      
      // Extract cluster ID from persona ID
      const clusterId = parseInt(personaId.split('_')[1]);
      
      const response = await fetch(`${this.apiBase}/personas/${personaId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cluster_id: clusterId,
          persona_id: personaId,
          message: message,
          conversation_history: history
        })
      });

      if (!response.ok) {
        throw new Error(`Chat API failed: ${response.status}`);
      }

      const chatData = await response.json();
      
      // Update conversation history
      this.conversationHistory.set(personaId, chatData.conversation_history);
      
      console.log(`✅ Persona responded: "${chatData.response}"`);
      
      return {
        success: true,
        personaId: personaId,
        response: chatData.response,
        personaTraits: chatData.persona_traits,
        conversationHistory: chatData.conversation_history
      };

    } catch (error) {
      console.error('❌ Chat failed:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get persona traits for LLM consumption
   * @param {string} personaId - Persona ID
   * @returns {Object} Persona traits formatted for LLM
   */
  getPersonaTraitsForLLM(personaId) {
    // This would typically fetch from your stored persona data
    // For now, return a template structure
    return {
      personaId: personaId,
      traits: {
        age_group: "21 years old",
        tech_savviness: "Medium",
        price_sensitivity: "Medium",
        brand_awareness: "Medium",
        privacy_consciousness: "Low",
        city_tier: "Tier-1",
        income_level: "Mid",
        preferred_media: "YouTube",
        device_count: "3.0 devices",
        emi_usage_likelihood: "44.4%"
      },
      personality: "You are a 21-year-old from a Tier-1 city with mid income. You're moderately tech-savvy and adopt technology when it makes sense. You balance price and quality, looking for good value. Respond naturally as this persona would, using casual language and expressing your genuine concerns and interests."
    };
  }

  /**
   * Format clusters for Bolt AI display
   * @param {Array} clusters - Array of cluster objects
   * @returns {Array} Formatted clusters for UI
   */
  formatClustersForBolt(clusters) {
    return clusters.map(cluster => ({
      id: cluster.cluster_id,
      title: cluster.cluster_label,
      description: cluster.cluster_description,
      size: `${cluster.cluster_size_pct}% of audience`,
      userCount: cluster.cluster_size.toLocaleString(),
      traits: cluster.top_traits,
      icon: cluster.representative_icon,
      demographics: cluster.demographics_summary,
      engagement: cluster.engagement_score
    }));
  }

  /**
   * Format personas for Bolt AI display
   * @param {Array} personas - Array of persona objects
   * @returns {Array} Formatted personas for UI
   */
  formatPersonasForBolt(personas) {
    return personas.map(persona => ({
      id: persona.persona_id,
      name: persona.persona_name,
      demographics: persona.demographics,
      caresAbout: persona.care_about_top2,
      barriers: persona.barriers_top1,
      mediaPreference: persona.media_preference,
      behavioralScore: persona.behavioral_score,
      clusterLinkage: persona.cluster_linkage,
      traits: persona.personality_traits,
      chatPersonality: persona.chat_personality
    }));
  }
}

// Example usage for Bolt AI
async function boltPersonaExample() {
  const personaGen = new BoltPersonaIntegration();
  
  // Example 1: Generate personas for a business goal
  console.log('🚀 Starting Bolt AI Persona Integration Example');
  console.log('=' * 60);
  
  const goal = "increase bose headphone adoption among college students in tier-2 cities";
  const result = await personaGen.generatePersonas(goal);
  
  if (result.success) {
    console.log('\n�� Generated Clusters:');
    const formattedClusters = personaGen.formatClustersForBolt(result.clusters);
    formattedClusters.forEach((cluster, index) => {
      console.log(`${index + 1}. ${cluster.title}`);
      console.log(`   Size: ${cluster.size} (${cluster.userCount} users)`);
      console.log(`   Traits: ${cluster.traits.join(', ')}`);
      console.log(`   Description: ${cluster.description}`);
      console.log('');
    });
    
    console.log('\n👤 Generated Personas:');
    const formattedPersonas = personaGen.formatPersonasForBolt(result.personas);
    formattedPersonas.forEach((persona, index) => {
      console.log(`${index + 1}. ${persona.name}`);
      console.log(`   Demographics: ${persona.demographics}`);
      console.log(`   Cares about: ${persona.caresAbout.join(', ')}`);
      console.log(`   Main barrier: ${persona.barriers}`);
      console.log(`   Media preference: ${persona.mediaPreference}`);
      console.log(`   Behavioral score: ${persona.behavioralScore}`);
      console.log('');
    });
    
    // Example 2: Chat with the first persona
    if (result.personas.length > 0) {
      const firstPersona = result.personas[0];
      console.log(`\n💬 Chatting with ${firstPersona.persona_name}:`);
      console.log('-'.repeat(40));
      
      const testMessages = [
        "Hi! I'm interested in Bose headphones. What do you think about them?",
        "What's your main concern about the price?",
        "Do you care about sound quality?",
        "What about EMI options? Would that help?"
      ];
      
      for (const message of testMessages) {
        console.log(`\n👤 You: ${message}`);
        
        const chatResult = await personaGen.chatWithPersona(firstPersona.persona_id, message);
        
        if (chatResult.success) {
          console.log(`🤖 ${firstPersona.persona_name}: ${chatResult.response}`);
          
          // Show persona traits for LLM consumption
          console.log(`📋 Persona Traits:`, chatResult.personaTraits);
        } else {
          console.log(`❌ Chat failed: ${chatResult.error}`);
        }
        
        // Small delay between messages
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    console.log('\n✅ Bolt AI Integration Example Completed Successfully!');
    
  } else {
    console.log(`❌ Persona generation failed: ${result.error}`);
  }
}

// Export for use in Bolt AI
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    BoltPersonaIntegration,
    boltPersonaExample
  };
}

// Run example if executed directly
if (typeof window === 'undefined' && require.main === module) {
  boltPersonaExample().catch(console.error);
}
