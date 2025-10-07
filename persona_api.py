#!/usr/bin/env python3
"""
Clean API Interface for Hybrid LLM+ML Multi-Agent System
Simple endpoints for persona generation
"""

from enhanced_multi_agent import EnhancedMultiAgentSystem
from llm_agent import is_llm_enabled
import json

class PersonaAPI:
    """Clean API interface for persona generation"""
    
    def __init__(self):
        self.system = EnhancedMultiAgentSystem()
    
    def analyze_goal(self, goal: str) -> dict:
        """Analyze marketing goal and return structured analysis"""
        analysis = self.system.agents['enhanced_goal_analyzer'].analyze_enhanced_goal(goal)
        return {
            "goal": goal,
            "intent": analysis.intent,
            "confidence": analysis.confidence,
            "demographics": analysis.target_demographics,
            "behavioral_focus": analysis.behavioral_focus,
            "psychographics": analysis.psychographic_profile,
            "commerce_patterns": analysis.commerce_patterns,
            "media_preferences": analysis.media_preferences,
            "lifestyle_segments": analysis.lifestyle_segments
        }
    
    def generate_personas(self, goal: str) -> dict:
        """Generate complete personas for a marketing goal"""
        
        # Step 1: Goal Analysis
        analysis = self.system.agents['enhanced_goal_analyzer'].analyze_enhanced_goal(goal)
        
        # Step 2: Audience Filtering
        filtered_audience = self.system.agents['audience_filterer'].filter_audience(analysis)
        
        # Step 3: Feature Engineering
        engineered_features = self.system.agents['feature_engineer'].engineer_enhanced_features(filtered_audience, analysis)
        
        # Step 4: Clustering
        clusters = self.system.agents['audience_clusterer'].cluster_enhanced_audience(engineered_features, analysis)
        
        # Step 5: Persona Labeling
        personas = self.system.agents['persona_labeler'].label_enhanced_clusters(clusters, analysis)
        
        # Step 6: Strategy Generation
        strategies = self.system.agents['strategy_generator'].generate_enhanced_strategies(personas, analysis)
        
        return {
            "goal": goal,
            "goal_analysis": {
                "intent": analysis.intent,
                "confidence": analysis.confidence,
                "demographics": analysis.target_demographics,
                "behavioral_focus": analysis.behavioral_focus
            },
            "audience_filtering": {
                "filtered_users": len(filtered_audience),
                "total_features": engineered_features.shape[1]
            },
            "clustering": {
                "optimal_clusters": clusters["optimal_k"],
                "algorithm": clusters.get("clustering_params", {}).get("algorithm", "kmeans") if clusters.get("clustering_params") else "kmeans"
            },
            "personas": self._format_personas(personas),
            "strategies": strategies,
            "system_info": {
                "llm_enabled": is_llm_enabled(),
                "total_personas": len(personas["cluster_stats"])
            }
        }
    
    def _format_personas(self, personas: dict) -> list:
        """Format personas for clean output with enhanced fields"""
        formatted_personas = []
        cluster_stats = personas["cluster_stats"]
        cluster_labels = personas.get("cluster_labels", {})
        
        for cluster_id, stats in cluster_stats.items():
            label = cluster_labels.get(cluster_id, f"Cluster {cluster_id}")
            
            # Calculate adoption likelihood
            adoption_likelihood = self._calculate_adoption_likelihood(stats)
            
            # Generate Care About and Barriers
            care_about, barriers = self._generate_care_about_barriers(stats)
            
            formatted_personas.append({
                "id": cluster_id,
                "name": label,
                "size_percentage": stats["size_pct"],
                "size_users": stats["size"],
                "adoption_likelihood": adoption_likelihood,
                "demographics": {
                    "avg_age": stats["avg_age"],
                    "dominant_gender": stats["dominant_gender"],
                    "dominant_income": stats["dominant_income"],
                    "dominant_education": stats["dominant_education"]
                },
                "behavioral_scores": {
                    "spending_power": stats["avg_spending_power"],
                    "digital_engagement": stats["avg_digital_engagement"],
                    "lifestyle_complexity": stats["avg_lifestyle_complexity"]
                },
                "care_about": care_about,
                "barriers": barriers,
                "tech_adoption_score": self._calculate_tech_adoption_score(stats)
            })
        
        return formatted_personas
    
    def _calculate_adoption_likelihood(self, stats: dict) -> str:
        """Calculate adoption likelihood based on persona characteristics"""
        age = stats["avg_age"]
        spending_power = stats["avg_spending_power"]
        digital_engagement = stats["avg_digital_engagement"]
        lifestyle_complexity = stats["avg_lifestyle_complexity"]
        
        # Scoring logic
        score = 0
        
        # Age factor (22-55 is optimal)
        if 22 <= age <= 35:
            score += 3
        elif 36 <= age <= 45:
            score += 2
        elif 46 <= age <= 55:
            score += 1
        
        # Spending power
        if spending_power > 0.8:
            score += 2
        elif spending_power > 0.6:
            score += 1
        
        # Digital engagement
        if digital_engagement > 0.7:
            score += 2
        elif digital_engagement > 0.5:
            score += 1
        
        # Lifestyle complexity
        if lifestyle_complexity > 0.7:
            score += 1
        
        # Convert to likelihood
        if score >= 6:
            return "High"
        elif score >= 4:
            return "Medium-high"
        elif score >= 2:
            return "Medium"
        else:
            return "Low"
    
    def _generate_care_about_barriers(self, stats: dict) -> tuple:
        """Generate Care About and Barriers based on persona characteristics"""
        age = stats["avg_age"]
        spending_power = stats["avg_spending_power"]
        digital_engagement = stats["avg_digital_engagement"]
        income = stats["dominant_income"]
        
        care_about = []
        barriers = []
        
        # Care About logic
        if spending_power > 0.7:
            care_about.append("Premium quality")
            care_about.append("Brand reputation")
        else:
            care_about.append("Value for money")
            care_about.append("Affordable options")
        
        if digital_engagement > 0.6:
            care_about.append("Smart features")
            care_about.append("Easy integration")
        else:
            care_about.append("Simple setup")
            care_about.append("Reliability")
        
        if age < 35:
            care_about.append("Modern design")
            care_about.append("Social features")
        else:
            care_about.append("Durability")
            care_about.append("Customer support")
        
        # Barriers logic
        if spending_power < 0.5:
            barriers.append("Price sensitivity")
        
        if digital_engagement < 0.4:
            barriers.append("Tech complexity")
        
        if age > 50:
            barriers.append("Learning curve")
        
        if income in ["₹0-₹2L", "₹2L-₹5L"]:
            barriers.append("Budget constraints")
        
        return care_about[:3], barriers[:2]  # Top 3 care about, top 2 barriers
    
    def _calculate_tech_adoption_score(self, stats: dict) -> float:
        """Calculate technology adoption score"""
        digital_engagement = stats["avg_digital_engagement"]
        age = stats["avg_age"]
        
        # Base score from digital engagement
        score = digital_engagement
        
        # Age adjustment
        if age < 30:
            score += 0.2
        elif age < 40:
            score += 0.1
        elif age > 50:
            score -= 0.1
        
        return min(1.0, max(0.0, score))
    
    def analyze_competitors(self, goal: str) -> dict:
        """Analyze competitors mentioned in the goal (optional API)"""
        
        # Detect competitors in goal
        competitors = self._detect_competitors(goal)
        
        if not competitors:
            return {"competitors_detected": False, "message": "No competitors mentioned in goal"}
        
        # Analyze each competitor
        competitor_analysis = {}
        for competitor in competitors:
            competitor_analysis[competitor] = self._analyze_competitor(competitor, goal)
        
        return {
            "competitors_detected": True,
            "competitors": competitors,
            "analysis": competitor_analysis,
            "recommendations": self._generate_competitor_recommendations(competitor_analysis)
        }
    
    def _detect_competitors(self, goal: str) -> list:
        """Detect competitors mentioned in the goal"""
        goal_lower = goal.lower()
        competitors = []
        
        # Common competitor brands
        brand_keywords = {
            "sonos": ["sonos"],
            "apple": ["apple", "homepod", "siri"],
            "jbl": ["jbl"],
            "bose": ["bose"],
            "amazon": ["amazon", "echo", "alexa"],
            "google": ["google", "nest", "assistant"],
            "samsung": ["samsung", "galaxy"],
            "sony": ["sony"],
            "bowers": ["bowers", "wilkins"]
        }
        
        for brand, keywords in brand_keywords.items():
            if any(keyword in goal_lower for keyword in keywords):
                competitors.append(brand.title())
        
        return competitors
    
    def _analyze_competitor(self, competitor: str, goal: str) -> dict:
        """Analyze a specific competitor"""
        
        # Competitor characteristics (simplified)
        competitor_profiles = {
            "Sonos": {
                "strengths": ["Premium sound quality", "Multi-room audio", "Design"],
                "weaknesses": ["High price", "Limited smart features", "Setup complexity"],
                "target_demographics": ["High-income", "Audiophiles", "Tech-savvy"],
                "price_position": "Premium"
            },
            "Apple": {
                "strengths": ["Ecosystem integration", "Siri", "Design", "Brand loyalty"],
                "weaknesses": ["Limited compatibility", "High price", "Limited features"],
                "target_demographics": ["Apple users", "Premium segment", "Tech enthusiasts"],
                "price_position": "Premium"
            },
            "Jbl": {
                "strengths": ["Portable", "Affordable", "Good sound", "Brand recognition"],
                "weaknesses": ["Limited smart features", "Build quality", "Ecosystem"],
                "target_demographics": ["Budget-conscious", "Young adults", "Casual users"],
                "price_position": "Budget"
            },
            "Bose": {
                "strengths": ["Sound quality", "Noise cancellation", "Brand reputation"],
                "weaknesses": ["Price", "Limited smart features", "Ecosystem"],
                "target_demographics": ["Professionals", "Audiophiles", "Premium segment"],
                "price_position": "Premium"
            }
        }
        
        return competitor_profiles.get(competitor, {
            "strengths": ["Brand recognition"],
            "weaknesses": ["Unknown"],
            "target_demographics": ["General market"],
            "price_position": "Unknown"
        })
    
    def _generate_competitor_recommendations(self, competitor_analysis: dict) -> list:
        """Generate recommendations based on competitor analysis"""
        recommendations = []
        
        for competitor, analysis in competitor_analysis.items():
            if analysis["price_position"] == "Premium":
                recommendations.append(f"Focus on value proposition vs {competitor}")
            elif analysis["price_position"] == "Budget":
                recommendations.append(f"Emphasize premium quality vs {competitor}")
            
            if "Limited smart features" in analysis["weaknesses"]:
                recommendations.append(f"Highlight smart features vs {competitor}")
        
        return recommendations[:3]  # Top 3 recommendations

# Initialize API
api = PersonaAPI()

def main():
    """Demo the clean API endpoints"""
    
    print("🚀 CLEAN PERSONA API ENDPOINTS")
    print("=" * 50)
    print()
    
    # Test goal
    goal = "Increase apple watch adoption among fitness enthusiasts"
    
    print("📋 ENDPOINT 1: analyze_goal(goal)")
    print("-" * 30)
    result = api.analyze_goal(goal)
    print(f"Goal: {result['goal']}")
    print(f"Intent: {result['intent']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Demographics: {result['demographics']}")
    print(f"Behavioral Focus: {result['behavioral_focus']}")
    print()
    
    print("📋 ENDPOINT 2: generate_personas(goal)")
    print("-" * 30)
    result = api.generate_personas(goal)
    print(f"Goal: {result['goal']}")
    print(f"Intent: {result['goal_analysis']['intent']}")
    print(f"Confidence: {result['goal_analysis']['confidence']:.2f}")
    print(f"Filtered Users: {result['audience_filtering']['filtered_users']}")
    print(f"Features: {result['audience_filtering']['total_features']}")
    print(f"Clusters: {result['clustering']['optimal_clusters']}")
    print(f"Algorithm: {result['clustering']['algorithm']}")
    print(f"Personas: {result['system_info']['total_personas']}")
    print(f"LLM Enabled: {result['system_info']['llm_enabled']}")
    print()
    
    print("🎯 GENERATED PERSONAS:")
    for persona in result['personas']:
        print(f"  {persona['name']}")
        print(f"    Size: {persona['size_percentage']:.1f}% ({persona['size_users']} users)")
        print(f"    Age: {persona['demographics']['avg_age']:.1f} years")
        print(f"    Gender: {persona['demographics']['dominant_gender']}")
        print(f"    Income: {persona['demographics']['dominant_income']}")
        print(f"    Education: {persona['demographics']['dominant_education']}")
        print()

if __name__ == "__main__":
    main()
