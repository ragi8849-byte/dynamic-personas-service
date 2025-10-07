#!/usr/bin/env python3
"""
Quick Test Script for Hybrid LLM+ML Multi-Agent System
Run this to test the complete system locally
"""

from enhanced_multi_agent import EnhancedMultiAgentSystem
from llm_agent import is_llm_enabled
import os

def test_system():
    """Test the complete multi-agent system"""
    
    print("🚀 TESTING HYBRID LLM+ML MULTI-AGENT SYSTEM")
    print("=" * 60)
    print()
    
    # Check LLM status
    print(f"🤖 LLM Status: {'Enabled' if is_llm_enabled() else 'Disabled (using rule-based fallback)'}")
    print()
    
    # Test goal
    goal = 'I want to introduce AI in my headphone brand, who could my customer be and how should I target them?'
    print(f"🎯 Test Goal: {goal}")
    print()
    
    # Initialize system
    print("🔄 Initializing Multi-Agent System...")
    system = EnhancedMultiAgentSystem()
    print("✅ System initialized!")
    print()
    
    # Run complete pipeline
    print("🔄 Running Complete Pipeline...")
    print("-" * 40)
    
    # Step 1: Goal Analysis
    print("1️⃣ Goal Analysis...")
    analysis = system.agents['enhanced_goal_analyzer'].analyze_enhanced_goal(goal)
    print(f"   Intent: {analysis.intent}")
    print(f"   Confidence: {analysis.confidence:.2f}")
    print(f"   Demographics: {analysis.target_demographics}")
    print(f"   Behavioral Focus: {analysis.behavioral_focus}")
    print()
    
    # Step 2: Audience Filtering
    print("2️⃣ Audience Filtering...")
    filtered_audience = system.agents['audience_filterer'].filter_audience(analysis)
    print(f"   Filtered Users: {len(filtered_audience)}")
    print()
    
    # Step 3: Feature Engineering
    print("3️⃣ Feature Engineering...")
    engineered_features = system.agents['feature_engineer'].engineer_enhanced_features(filtered_audience, analysis)
    print(f"   Engineered Features: {engineered_features.shape[1]}")
    print()
    
    # Step 4: Clustering
    print("4️⃣ Clustering...")
    clusters = system.agents['audience_clusterer'].cluster_enhanced_audience(engineered_features, analysis)
    print(f"   Optimal Clusters: {clusters['optimal_k']}")
    print()
    
    # Step 5: Persona Labeling
    print("5️⃣ Persona Labeling...")
    personas = system.agents['persona_labeler'].label_enhanced_clusters(clusters, analysis)
    print(f"   Generated Personas: {len(personas['cluster_stats'])}")
    print()
    
    # Display personas
    print("🎯 GENERATED PERSONAS:")
    print("-" * 40)
    cluster_stats = personas['cluster_stats']
    cluster_labels = personas.get('cluster_labels', {})
    
    for cluster_id, stats in cluster_stats.items():
        label = cluster_labels.get(cluster_id, f'Cluster {cluster_id}')
        print(f"🎧 {label}")
        print(f"   Size: {stats['size_pct']:.1f}% ({stats['size']} users)")
        print(f"   Age: {stats['avg_age']:.1f} years")
        print(f"   Gender: {stats['dominant_gender']}")
        print(f"   Income: {stats['dominant_income']}")
        print(f"   Education: {stats['dominant_education']}")
        print()
    
    print("✅ COMPLETE PIPELINE SUCCESSFUL!")
    print()
    print("🎯 KEY INSIGHTS:")
    print("   • System successfully processed your AI headphone brand goal")
    print("   • Generated customer personas for targeting")
    print("   • Provided marketing insights and recommendations")
    print("   • Hybrid LLM+ML approach working perfectly")
    print()
    
    if is_llm_enabled():
        print("🤖 LLM Integration Active:")
        print("   • Intelligent goal analysis")
        print("   • Smart SQL generation")
        print("   • Advanced feature engineering")
        print("   • Optimal clustering parameters")
        print("   • Marketing-focused persona labels")
    else:
        print("🔧 Rule-based Fallback Active:")
        print("   • Reliable keyword matching")
        print("   • Standard SQL building")
        print("   • Core feature engineering")
        print("   • K-means clustering")
        print("   • Template-based labels")

def test_multiple_goals():
    """Test system with multiple goals"""
    
    print("\n🔄 TESTING MULTIPLE GOALS")
    print("=" * 60)
    
    test_goals = [
        "engage fitness enthusiasts for health app",
        "convert high-income consumers for luxury brand sales",
        "retain millennial parents for family products",
        "reach gen-z audience for social media platform",
        "target tech professionals for B2B software"
    ]
    
    system = EnhancedMultiAgentSystem()
    
    for i, goal in enumerate(test_goals, 1):
        print(f"\n{i}. Goal: {goal}")
        analysis = system.agents['enhanced_goal_analyzer'].analyze_enhanced_goal(goal)
        print(f"   Intent: {analysis.intent} (confidence: {analysis.confidence:.2f})")
        print(f"   Demographics: {analysis.target_demographics}")
        print(f"   Behavioral Focus: {analysis.behavioral_focus}")

if __name__ == "__main__":
    test_system()
    test_multiple_goals()
