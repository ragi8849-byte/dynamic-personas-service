#!/usr/bin/env node

/**
 * Test script for Bolt AI Integration
 * Run this to verify your persona generator works with Bolt AI
 */

const { BoltPersonaIntegration } = require('./bolt_integration_example.js');

async function testBoltIntegration() {
  console.log('🧪 Testing Bolt AI Integration');
  console.log('=' * 50);
  
  const personaGen = new BoltPersonaIntegration();
  
  // Test 1: Health Check
  console.log('\n1️⃣ Testing Health Check...');
  try {
    const response = await fetch('https://dyn-personas-656907085987.asia-south1.run.app/health');
    const data = await response.json();
    console.log(`✅ Health Check: ${data.ok ? 'PASS' : 'FAIL'}`);
    console.log(`   Users available: ${data.users}`);
  } catch (error) {
    console.log(`❌ Health Check: FAIL - ${error.message}`);
  }
  
  // Test 2: Generate Clusters
  console.log('\n2️⃣ Testing Cluster Generation...');
  const goal = "college students interested in headphones";
  const result = await personaGen.generatePersonas(goal);
  
  if (result.success) {
    console.log(`✅ Cluster Generation: PASS`);
    console.log(`   Generated ${result.clusters.length} clusters`);
    console.log(`   Generated ${result.personas.length} personas`);
    
    // Test 3: Chat with Persona
    if (result.personas.length > 0) {
      console.log('\n3️⃣ Testing Persona Chat...');
      const firstPersona = result.personas[0];
      const chatResult = await personaGen.chatWithPersona(
        firstPersona.persona_id, 
        "Hello! What do you think about Bose headphones?"
      );
      
      if (chatResult.success) {
        console.log(`✅ Persona Chat: PASS`);
        console.log(`   Persona: ${firstPersona.persona_name}`);
        console.log(`   Response: ${chatResult.response}`);
        console.log(`   Traits: ${JSON.stringify(chatResult.personaTraits, null, 2)}`);
      } else {
        console.log(`❌ Persona Chat: FAIL - ${chatResult.error}`);
      }
    }
    
    // Test 4: Format for Bolt AI
    console.log('\n4️⃣ Testing Bolt AI Formatting...');
    const formattedClusters = personaGen.formatClustersForBolt(result.clusters);
    const formattedPersonas = personaGen.formatPersonasForBolt(result.personas);
    
    console.log(`✅ Bolt AI Formatting: PASS`);
    console.log(`   Formatted ${formattedClusters.length} clusters`);
    console.log(`   Formatted ${formattedPersonas.length} personas`);
    
    // Test 5: LLM Traits
    console.log('\n5️⃣ Testing LLM Traits...');
    if (result.personas.length > 0) {
      const traits = personaGen.getPersonaTraitsForLLM(result.personas[0].persona_id);
      console.log(`✅ LLM Traits: PASS`);
      console.log(`   Traits structure: ${Object.keys(traits.traits).join(', ')}`);
    }
    
  } else {
    console.log(`❌ Cluster Generation: FAIL - ${result.error}`);
  }
  
  console.log('\n🎉 Bolt AI Integration Test Completed!');
}

// Run the test
testBoltIntegration().catch(console.error);
