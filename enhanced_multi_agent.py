"""
Enhanced Multi-Agent System for Comprehensive 10K Dataset
Works with all ID Graph attributes and marketing segments
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import sqlite3
from llm_agent import generate_text, is_llm_enabled

@dataclass
class EnhancedGoalAnalysis:
    """Enhanced goal analysis with comprehensive attributes"""
    original_goal: str
    target_demographics: Dict[str, Any]
    behavioral_focus: List[str]
    psychographic_profile: Dict[str, Any]
    commerce_patterns: List[str]
    media_preferences: List[str]
    lifestyle_segments: List[str]
    intent: str
    confidence: float

class EnhancedMultiAgentSystem:
    """Enhanced multi-agent system for comprehensive dataset"""
    
    def __init__(self, db_path: str = "data/comprehensive_users.db"):
        self.db_path = db_path
        self.users_data = self._load_users_data()
        self.data_dictionary = self._load_data_dictionary()
        
        self.agents = {
            "enhanced_goal_analyzer": EnhancedGoalAnalyzerAgent(self.data_dictionary),
            "audience_filterer": AudienceFilteringAgent(self.users_data),
            "feature_engineer": EnhancedFeatureEngineerAgent(),
            "audience_clusterer": EnhancedClusteringAgent(),
            "persona_labeler": EnhancedPersonaLabelingAgent(),
            "strategy_generator": EnhancedStrategyGeneratorAgent()
        }
    
    def _load_users_data(self) -> pd.DataFrame:
        """Load comprehensive users data"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM users", conn)
        conn.close()
        return df
    
    def _load_data_dictionary(self) -> Dict:
        """Load data dictionary"""
        with open("data/data_dictionary.json", "r") as f:
            return json.load(f)
    
    def generate_enhanced_audiences(self, marketing_goal: str) -> Dict[str, Any]:
        """Generate enhanced audiences using comprehensive multi-agent pipeline"""
        
        print(f"🎯 Processing Enhanced Goal: '{marketing_goal}'")
        
        # Agent 1: Enhanced goal analysis
        goal_analysis = self.agents["enhanced_goal_analyzer"].analyze_enhanced_goal(marketing_goal)
        print(f"📊 Enhanced Analysis: {len(goal_analysis.behavioral_focus)} behavioral focuses, {goal_analysis.intent} intent")
        
        # Agent 2: Filter and segment audience
        filtered_audience = self.agents["audience_filterer"].filter_audience(goal_analysis)
        print(f"👥 Filtered Audience: {len(filtered_audience)} users")
        
        # Agent 3: Enhanced feature engineering
        engineered_data = self.agents["feature_engineer"].engineer_enhanced_features(
            filtered_audience, goal_analysis
        )
        print(f"⚙️ Enhanced Feature Engineering Complete")
        
        # Agent 4: Enhanced clustering
        clusters = self.agents["audience_clusterer"].cluster_enhanced_audience(
            engineered_data, goal_analysis
        )
        print(f"🎯 Generated {len(clusters['cluster_stats'])} enhanced clusters")
        
        # Agent 5: Enhanced persona labeling
        labeled_clusters = self.agents["persona_labeler"].label_enhanced_clusters(
            clusters, goal_analysis
        )
        print(f"🏷️ Enhanced Persona Labeling Complete")
        
        # Agent 6: Enhanced strategy generation
        strategies = self.agents["strategy_generator"].generate_enhanced_strategies(
            labeled_clusters, goal_analysis
        )
        print(f"📢 Generated {len(strategies)} enhanced strategies")
        
        return {
            "goal": marketing_goal,
            "goal_analysis": goal_analysis,
            "filtered_audience": filtered_audience,
            "enhanced_clusters": clusters,
            "enhanced_personas": labeled_clusters,
            "enhanced_strategies": strategies,
            "pipeline_success": True
        }

class EnhancedGoalAnalyzerAgent:
    """Agent 1: Enhanced goal analysis with comprehensive attribute understanding"""
    
    def __init__(self, data_dictionary: Dict):
        self.data_dictionary = data_dictionary
        self._build_comprehensive_knowledge_base()
    
    def _build_comprehensive_knowledge_base(self):
        """Build comprehensive knowledge base"""
        
        # Demographics patterns
        self.demographic_patterns = {
            "age_groups": {
                "gen_z": ["gen z", "gen-z", "genz", "18-25", "young", "teen", "college"],
                "millennial": ["millennial", "millennials", "26-40", "young adult"],
                "gen_x": ["gen x", "gen-x", "41-55", "middle age"],
                "boomer": ["boomer", "baby boomer", "56+", "senior", "elderly"]
            },
            "income_levels": {
                "high_income": ["high income", "affluent", "wealthy", "premium", "luxury"],
                "middle_income": ["middle income", "middle class", "moderate"],
                "low_income": ["low income", "budget", "affordable", "value"]
            },
            "education": {
                "high_education": ["graduate", "postgraduate", "doctorate", "educated", "professional"],
                "medium_education": ["secondary", "high school", "diploma"],
                "basic_education": ["primary", "basic", "elementary"]
            }
        }
        
        # Behavioral patterns
        self.behavioral_patterns = {
            "shopping": ["shopping", "purchase", "buy", "retail", "ecommerce", "consumer"],
            "media": ["media", "entertainment", "content", "streaming", "social media"],
            "travel": ["travel", "tourism", "vacation", "trip", "journey"],
            "health": ["health", "fitness", "wellness", "medical", "pharma"],
            "finance": ["finance", "banking", "investment", "money", "wealth"],
            "technology": ["tech", "technology", "digital", "innovation", "gadgets"],
            "lifestyle": ["lifestyle", "luxury", "premium", "quality", "experience"]
        }
        
        # Psychographic patterns
        self.psychographic_patterns = {
            "innovators": ["innovator", "early adopter", "tech-savvy", "cutting edge"],
            "conservatives": ["conservative", "traditional", "conventional", "stable"],
            "socially_conscious": ["social", "environmental", "sustainable", "ethical"],
            "achievers": ["achiever", "successful", "ambitious", "career-focused"],
            "experiencers": ["experiencer", "adventurous", "spontaneous", "fun-loving"]
        }
        
        # Commerce patterns
        self.commerce_patterns = {
            "frequent_shoppers": ["frequent", "regular", "loyal", "repeat"],
            "bargain_hunters": ["bargain", "discount", "deal", "sale", "cheap"],
            "premium_buyers": ["premium", "luxury", "high-end", "quality"],
            "online_shoppers": ["online", "digital", "ecommerce", "internet"]
        }
    
    def analyze_enhanced_goal(self, goal: str) -> EnhancedGoalAnalysis:
        """Analyze goal with comprehensive understanding"""
        
        goal_lower = goal.lower()

        # Try LLM-assisted analysis first
        if is_llm_enabled():
            llm_analysis = self._analyze_goal_with_llm(goal)
            if llm_analysis:
                return llm_analysis
        
        # Fallback to rule-based analysis
        return self._analyze_goal_with_rules(goal_lower)
    
    def _analyze_goal_with_llm(self, goal: str) -> Optional[EnhancedGoalAnalysis]:
        """Analyze goal using LLM with structured output"""
        
        prompt = f"""
You are an expert marketing analyst. Analyze this goal and extract structured information in JSON format.

Goal: "{goal}"

Extract the following information:
1. Demographics: age groups (gen_z/millennial/gen_x/boomer), income levels (low_income/middle_income/high_income), education levels (basic_education/medium_education/high_education)
2. Behavioral focus: shopping, media, travel, health, finance, technology, lifestyle
3. Psychographics: innovators, conservatives, socially_conscious, achievers, experiencers
4. Commerce patterns: frequent_shoppers, bargain_hunters, premium_buyers, online_shoppers
5. Media preferences: social, video, streaming, content, entertainment, news
6. Lifestyle segments: luxury, premium, budget, family, single, professional
7. Intent: reach, engagement, conversion, retention
8. Confidence: 0.0 to 1.0 based on how clear the goal is

Return ONLY valid JSON in this exact format:
{{
    "demographics": {{
        "age_group": "millennial",
        "income_level": "high_income",
        "education_level": "high_education"
    }},
    "behavioral_focus": ["shopping", "technology"],
    "psychographics": {{"innovators": true}},
    "commerce_patterns": ["premium_buyers"],
    "media_preferences": ["social"],
    "lifestyle_segments": ["luxury"],
    "intent": "conversion",
    "confidence": 0.85
}}

Only include fields that are clearly present in the goal. Use null for missing fields.
"""
        
        llm_response = generate_text(prompt)
        if not llm_response:
            return None
        
        try:
            # Parse JSON response
            import json
            data = json.loads(llm_response.strip())
            
            # Convert to EnhancedGoalAnalysis format
            demographics = data.get("demographics", {})
            behavioral_focus = data.get("behavioral_focus", ["shopping"])
            psychographics = data.get("psychographics", {})
            commerce_patterns = data.get("commerce_patterns", [])
            media_preferences = data.get("media_preferences", [])
            lifestyle_segments = data.get("lifestyle_segments", [])
            intent = data.get("intent", "reach")
            confidence = data.get("confidence", 0.5)
            
            return EnhancedGoalAnalysis(
                original_goal=goal,
                target_demographics=demographics,
                behavioral_focus=behavioral_focus,
                psychographic_profile=psychographics,
                commerce_patterns=commerce_patterns,
                media_preferences=media_preferences,
                lifestyle_segments=lifestyle_segments,
                intent=intent,
                confidence=confidence
            )
            
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"LLM parsing error: {e}")
            return None
    
    def _analyze_goal_with_rules(self, goal_lower: str) -> EnhancedGoalAnalysis:
        """Fallback rule-based analysis"""
        
        # Analyze demographics
        target_demographics = self._analyze_demographics(goal_lower)
        
        # Analyze behavioral focus
        behavioral_focus = self._analyze_behavioral_focus(goal_lower)
        
        # Analyze psychographic profile
        psychographic_profile = self._analyze_psychographics(goal_lower)
        
        # Analyze commerce patterns
        commerce_patterns = self._analyze_commerce_patterns(goal_lower)
        
        # Analyze media preferences
        media_preferences = self._analyze_media_preferences(goal_lower)
        
        # Analyze lifestyle segments
        lifestyle_segments = self._analyze_lifestyle_segments(goal_lower)
        
        # Determine intent
        intent = self._determine_enhanced_intent(goal_lower)
        
        # Calculate confidence
        confidence = self._calculate_enhanced_confidence(
            target_demographics, behavioral_focus, psychographic_profile
        )
        
        return EnhancedGoalAnalysis(
            original_goal=goal_lower,
            target_demographics=target_demographics,
            behavioral_focus=behavioral_focus,
            psychographic_profile=psychographic_profile,
            commerce_patterns=commerce_patterns,
            media_preferences=media_preferences,
            lifestyle_segments=lifestyle_segments,
            intent=intent,
            confidence=confidence
        )
    
    def _analyze_demographics(self, goal: str) -> Dict[str, Any]:
        """Analyze demographic targeting"""
        demographics = {}
        
        # Age analysis
        for age_group, keywords in self.demographic_patterns["age_groups"].items():
            if any(keyword in goal for keyword in keywords):
                demographics["age_group"] = age_group
                break
        
        # Income analysis
        for income_level, keywords in self.demographic_patterns["income_levels"].items():
            if any(keyword in goal for keyword in keywords):
                demographics["income_level"] = income_level
                break
        
        # Education analysis
        for education_level, keywords in self.demographic_patterns["education"].items():
            if any(keyword in goal for keyword in keywords):
                demographics["education_level"] = education_level
                break
        
        return demographics
    
    def _analyze_behavioral_focus(self, goal: str) -> List[str]:
        """Analyze behavioral focus areas"""
        focus_areas = []
        for behavior, keywords in self.behavioral_patterns.items():
            if any(keyword in goal for keyword in keywords):
                focus_areas.append(behavior)
        return focus_areas if focus_areas else ["shopping"]
    
    def _analyze_psychographics(self, goal: str) -> Dict[str, Any]:
        """Analyze psychographic profile"""
        psychographics = {}
        for profile_type, keywords in self.psychographic_patterns.items():
            if any(keyword in goal for keyword in keywords):
                psychographics[profile_type] = True
        return psychographics
    
    def _analyze_commerce_patterns(self, goal: str) -> List[str]:
        """Analyze commerce patterns"""
        patterns = []
        for pattern_type, keywords in self.commerce_patterns.items():
            if any(keyword in goal for keyword in keywords):
                patterns.append(pattern_type)
        return patterns
    
    def _analyze_media_preferences(self, goal: str) -> List[str]:
        """Analyze media preferences"""
        preferences = []
        media_keywords = ["social", "video", "streaming", "content", "entertainment", "news"]
        for keyword in media_keywords:
            if keyword in goal:
                preferences.append(keyword)
        return preferences
    
    def _analyze_lifestyle_segments(self, goal: str) -> List[str]:
        """Analyze lifestyle segments"""
        segments = []
        lifestyle_keywords = ["luxury", "premium", "budget", "family", "single", "professional"]
        for keyword in lifestyle_keywords:
            if keyword in goal:
                segments.append(keyword)
        return segments
    
    def _determine_enhanced_intent(self, goal: str) -> str:
        """Determine enhanced intent"""
        if any(word in goal for word in ["reach", "awareness", "visibility"]):
            return "reach"
        elif any(word in goal for word in ["engagement", "interaction", "social"]):
            return "engagement"
        elif any(word in goal for word in ["conversion", "sales", "purchase"]):
            return "conversion"
        elif any(word in goal for word in ["retention", "loyalty", "repeat"]):
            return "retention"
        else:
            return "reach"
    
    def _calculate_enhanced_confidence(self, demographics: Dict, behavioral_focus: List[str], 
                                     psychographics: Dict) -> float:
        """Calculate enhanced confidence score"""
        confidence = 0.5  # Base confidence
        
        if demographics:
            confidence += 0.2
        if len(behavioral_focus) > 1:
            confidence += 0.2
        if psychographics:
            confidence += 0.1
        
        return min(confidence, 1.0)

class AudienceFilteringAgent:
    """Agent 2: Filters audience based on enhanced goal analysis"""
    
    def __init__(self, users_data: pd.DataFrame):
        self.users_data = users_data
    
    def filter_audience(self, goal_analysis: EnhancedGoalAnalysis) -> pd.DataFrame:
        """Filter audience based on enhanced goal analysis with LLM-assisted SQL generation"""
        
        # Try LLM-assisted SQL generation first
        if is_llm_enabled():
            llm_sql = self._generate_llm_sql_query(goal_analysis)
            if llm_sql:
                try:
                    # Execute LLM-generated SQL (simulated)
                    filtered_data = self._execute_llm_sql_query(llm_sql, goal_analysis)
                    if len(filtered_data) >= 100:
                        return filtered_data
                except Exception as e:
                    print(f"LLM SQL execution failed: {e}, falling back to rule-based")
        
        # Fallback to rule-based filtering
        return self._filter_audience_rules(goal_analysis)
    
    def _generate_llm_sql_query(self, goal_analysis: EnhancedGoalAnalysis) -> Optional[str]:
        """Generate SQL query using LLM assistance"""
        
        # Get available columns for context
        available_columns = list(self.users_data.columns)[:30]  # First 30 columns
        
        prompt = f"""
You are a data analyst expert in SQL. Generate a SQL query to filter users based on marketing goal analysis.

Available columns: {available_columns}

Goal Analysis:
- Demographics: {goal_analysis.target_demographics}
- Behavioral Focus: {goal_analysis.behavioral_focus}
- Psychographics: {goal_analysis.psychographic_profile}
- Commerce Patterns: {goal_analysis.commerce_patterns}
- Media Preferences: {goal_analysis.media_preferences}
- Lifestyle Segments: {goal_analysis.lifestyle_segments}
- Intent: {goal_analysis.intent}

Generate a SQL query that:
1. Filters users based on the analysis above
2. Uses appropriate WHERE conditions
3. Ensures at least 100 users are returned
4. Uses column names exactly as provided
5. Handles missing/null values appropriately

Return ONLY the SQL query, no explanations. Use 'users' as the table name.

Example format:
SELECT * FROM users WHERE age >= 26 AND age <= 40 AND annual_hhi IN ('₹5L-₹10L') AND tech_adoption_score > 0.6
"""
        
        llm_response = generate_text(prompt)
        if not llm_response:
            return None
        
        # Clean and validate SQL
        sql_query = llm_response.strip()
        if sql_query.upper().startswith('SELECT'):
            return sql_query
        
        return None
    
    def _execute_llm_sql_query(self, sql_query: str, goal_analysis: EnhancedGoalAnalysis) -> pd.DataFrame:
        """Execute LLM-generated SQL query (simulated with pandas)"""
        
        # For demo purposes, we'll simulate SQL execution using pandas filtering
        # In production, you'd connect to a real database and execute the SQL
        
        filtered_data = self.users_data.copy()
        
        # Parse basic SQL conditions (simplified parser for demo)
        if 'WHERE' in sql_query.upper():
            where_clause = sql_query.split('WHERE')[1].strip()
            
            # Apply filters based on goal analysis (simulating SQL execution)
            filtered_data = self._apply_demographic_filters(filtered_data, goal_analysis.target_demographics)
            filtered_data = self._apply_behavioral_filters(filtered_data, goal_analysis.behavioral_focus)
            filtered_data = self._apply_psychographic_filters(filtered_data, goal_analysis.psychographic_profile)
            filtered_data = self._apply_commerce_filters(filtered_data, goal_analysis.commerce_patterns)
        
        return filtered_data
    
    def _filter_audience_rules(self, goal_analysis: EnhancedGoalAnalysis) -> pd.DataFrame:
        """Fallback rule-based audience filtering"""
        
        filtered_data = self.users_data.copy()
        
        # Apply demographic filters
        filtered_data = self._apply_demographic_filters(filtered_data, goal_analysis.target_demographics)
        
        # Apply behavioral filters
        filtered_data = self._apply_behavioral_filters(filtered_data, goal_analysis.behavioral_focus)
        
        # Apply psychographic filters
        filtered_data = self._apply_psychographic_filters(filtered_data, goal_analysis.psychographic_profile)
        
        # Apply commerce filters
        filtered_data = self._apply_commerce_filters(filtered_data, goal_analysis.commerce_patterns)
        
        # Sample if too large
        if len(filtered_data) > 2000:
            filtered_data = filtered_data.sample(n=2000, random_state=42)
        
        # Fallback if empty after strict filters: relax and select a reasonable cohort
        if len(filtered_data) == 0:
            # Prefer high propensity to buy if available, else use digital engagement
            df = self.users_data.copy()
            if "propensity_to_buy" in df.columns:
                filtered_data = df.sort_values("propensity_to_buy", ascending=False).head(1000)
            elif "tech_adoption_score" in df.columns:
                filtered_data = df.sort_values("tech_adoption_score", ascending=False).head(1000)
            else:
                filtered_data = df.sample(n=min(1000, len(df)), random_state=42)
        
        return filtered_data
    
    def _apply_demographic_filters(self, data: pd.DataFrame, demographics: Dict[str, Any]) -> pd.DataFrame:
        """Apply demographic filters"""
        
        if "age_group" in demographics:
            age_group = demographics["age_group"]
            if age_group == "gen_z":
                data = data[data["age"].between(18, 25)]
            elif age_group == "millennial":
                data = data[data["age"].between(26, 40)]
            elif age_group == "gen_x":
                data = data[data["age"].between(41, 55)]
            elif age_group == "boomer":
                data = data[data["age"] >= 56]
        
        if "income_level" in demographics:
            income_level = demographics["income_level"]
            if income_level == "high_income":
                data = data[data["annual_hhi"].isin(["₹10L-₹20L", "₹20L-₹50L", "₹50L+"])]
            elif income_level == "middle_income":
                data = data[data["annual_hhi"].isin(["₹2L-₹5L", "₹5L-₹10L"])]
            elif income_level == "low_income":
                data = data[data["annual_hhi"] == "Under ₹2L"]
        
        if "education_level" in demographics:
            education_level = demographics["education_level"]
            if education_level == "high_education":
                data = data[data["education_level"].isin(["Graduate", "Postgraduate", "Doctorate"])]
            elif education_level == "medium_education":
                data = data[data["education_level"] == "Secondary"]
            elif education_level == "basic_education":
                data = data[data["education_level"] == "Primary"]
        
        return data
    
    def _apply_behavioral_filters(self, data: pd.DataFrame, behavioral_focus: List[str]) -> pd.DataFrame:
        """Apply behavioral filters"""
        
        if "shopping" in behavioral_focus:
            data = data[data["grocery_spend"] > data["grocery_spend"].quantile(0.3)]
        
        if "media" in behavioral_focus:
            data = data[data["social_media_usage"] > 0.5]
        
        if "travel" in behavioral_focus:
            data = data[data["travel_frequency"].isin(["Occasionally", "Frequently"])]
        
        if "health" in behavioral_focus:
            data = data[data["fitness_interest"] > 0.5]
        
        if "finance" in behavioral_focus:
            data = data[data["investment_interest"] > 0.5]
        
        if "technology" in behavioral_focus:
            data = data[data["tech_adoption_score"] > 0.6]
        
        return data
    
    def _apply_psychographic_filters(self, data: pd.DataFrame, psychographics: Dict[str, Any]) -> pd.DataFrame:
        """Apply psychographic filters"""
        
        if "innovators" in psychographics:
            data = data[data["innovation_preference"] > 0.6]
        
        if "conservatives" in psychographics:
            data = data[data["conscientiousness"] > 0.6]
        
        if "socially_conscious" in psychographics:
            data = data[data["environmental_consciousness"] > 0.6]
        
        if "achievers" in psychographics:
            data = data[data["conscientiousness"] > 0.6]
        
        if "experiencers" in psychographics:
            data = data[data["extraversion"] > 0.6]
        
        return data
    
    def _apply_commerce_filters(self, data: pd.DataFrame, commerce_patterns: List[str]) -> pd.DataFrame:
        """Apply commerce pattern filters"""
        
        if "frequent_shoppers" in commerce_patterns:
            data = data[data["grocery_frequency"].isin(["Daily", "Weekly"])]
        
        if "premium_buyers" in commerce_patterns:
            data = data[data["beauty_spend"] > data["beauty_spend"].quantile(0.7)]
        
        if "online_shoppers" in commerce_patterns:
            data = data[data["tech_adoption_score"] > 0.6]
        
        return data

class EnhancedFeatureEngineerAgent:
    """Agent 3: Enhanced feature engineering"""
    
    def engineer_enhanced_features(self, data: pd.DataFrame, goal_analysis: EnhancedGoalAnalysis) -> pd.DataFrame:
        """Engineer enhanced features with LLM-assisted feature selection"""
        
        df = data.copy()
        
        # Try LLM-assisted feature engineering first
        if is_llm_enabled():
            llm_features = self._generate_llm_feature_recommendations(df, goal_analysis)
            if llm_features:
                df = self._apply_llm_feature_engineering(df, llm_features, goal_analysis)
        
        # Always apply core feature engineering
        df = self._create_composite_features(df)
        df = self._create_behavioral_scores(df, goal_analysis)
        df = self._create_psychographic_profiles(df)
        df = self._create_lifestyle_indicators(df)
        df = self._create_engagement_loyalty_signals(df)
        
        return df
    
    def _generate_llm_feature_recommendations(self, df: pd.DataFrame, goal_analysis: EnhancedGoalAnalysis) -> Optional[Dict]:
        """Generate feature engineering recommendations using LLM"""
        
        available_features = list(df.columns)[:20]  # First 20 features
        
        prompt = f"""
You are a data scientist expert in feature engineering for marketing analytics. Recommend feature engineering strategies based on the goal analysis.

Available features: {available_features}

Goal Analysis:
- Demographics: {goal_analysis.target_demographics}
- Behavioral Focus: {goal_analysis.behavioral_focus}
- Psychographics: {goal_analysis.psychographic_profile}
- Commerce Patterns: {goal_analysis.commerce_patterns}
- Media Preferences: {goal_analysis.media_preferences}
- Lifestyle Segments: {goal_analysis.lifestyle_segments}
- Intent: {goal_analysis.intent}

Recommend:
1. Which existing features to prioritize for clustering
2. New composite features to create
3. Feature transformations to apply
4. Feature interactions to consider

Return JSON format:
{{
    "priority_features": ["feature1", "feature2"],
    "composite_features": [
        {{"name": "feature_name", "formula": "feature1 * 0.5 + feature2 * 0.5"}}
    ],
    "transformations": [
        {{"feature": "feature_name", "transform": "log", "reason": "normalize distribution"}}
    ],
    "interactions": [
        {{"features": ["feature1", "feature2"], "reason": "capture synergy"}}
    ]
}}
"""
        
        llm_response = generate_text(prompt)
        if not llm_response:
            return None
        
        try:
            import json
            return json.loads(llm_response.strip())
        except json.JSONDecodeError:
            return None
    
    def _apply_llm_feature_engineering(self, df: pd.DataFrame, llm_features: Dict, goal_analysis: EnhancedGoalAnalysis) -> pd.DataFrame:
        """Apply LLM-recommended feature engineering"""
        
        # Apply composite features
        if "composite_features" in llm_features:
            for comp_feature in llm_features["composite_features"]:
                try:
                    name = comp_feature["name"]
                    formula = comp_feature["formula"]
                    # Simple formula evaluation (in production, use safer methods)
                    df[name] = eval(formula.replace("feature1", "df['feature1']").replace("feature2", "df['feature2']"))
                except:
                    pass  # Skip invalid formulas
        
        # Apply transformations
        if "transformations" in llm_features:
            for transform in llm_features["transformations"]:
                try:
                    feature = transform["feature"]
                    transform_type = transform["transform"]
                    if transform_type == "log" and feature in df.columns:
                        df[f"{feature}_log"] = np.log1p(df[feature])
                    elif transform_type == "sqrt" and feature in df.columns:
                        df[f"{feature}_sqrt"] = np.sqrt(df[feature])
                except:
                    pass  # Skip invalid transformations
        
        return df
    
    def _create_composite_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create composite features"""
        
        # Spending power
        df["spending_power"] = (
            df["grocery_spend"] * 0.3 +
            df["beauty_spend"] * 0.2 +
            df["household_spend"] * 0.3 +
            df["health_spend"] * 0.2 +
            (df["avg_order_value"] / max(1.0, float(df["avg_order_value"].max()))) * 0.2
        )
        
        # Digital engagement
        df["digital_engagement"] = (
            df["social_media_usage"] * 0.4 +
            df["tech_adoption_score"] * 0.3 +
            df["streaming_services"].apply(lambda x: 1 if x != "None" else 0) * 0.2 +
            (df.get("fb_usage", 0) + df.get("ig_usage", 0) + df.get("yt_usage", 0) + df.get("tt_usage", 0)) / 4 * 0.1
        )
        
        # Lifestyle complexity
        df["lifestyle_complexity"] = (
            df["travel_frequency"].apply(lambda x: {"Never": 0, "Rarely": 1, "Occasionally": 2, "Frequently": 3}[x]) * 0.3 +
            df["fitness_frequency"].apply(lambda x: {"Never": 0, "Rarely": 1, "Weekly": 2, "Daily": 3}[x]) * 0.3 +
            df["investment_interest"] * 0.4
        )
        
        return df
    
    def _create_behavioral_scores(self, df: pd.DataFrame, goal_analysis: EnhancedGoalAnalysis) -> pd.DataFrame:
        """Create behavioral scores"""
        
        # Shopping behavior score
        df["shopping_behavior_score"] = (
            df["grocery_spend"] / df["grocery_spend"].max() * 0.3 +
            df["beauty_spend"] / df["beauty_spend"].max() * 0.2 +
            df["electronics_interest"] * 0.3 +
            df["auto_interest"] * 0.2 +
            (df.get("shopping_app_use", 0) * 0.2) +
            (1 - df.get("cart_abandon_rate", 0)) * 0.2 +
            (df.get("propensity_to_buy", 0) * 0.4)
        )
        
        # Media consumption score
        df["media_consumption_score"] = (
            df["social_media_usage"] * 0.3 +
            df["entertainment_interest"] * 0.2 +
            df["news_interest"] * 0.2 +
            df["technology_interest"] * 0.2 +
            (df.get("email_open_rate", 0) * 0.05 + df.get("email_click_rate", 0) * 0.05)
        )
        
        # Health consciousness score
        df["health_consciousness_score"] = (
            df["fitness_interest"] * 0.4 +
            df["health_product_interest"] * 0.3 +
            df["health_interest"] * 0.3
        )
        
        return df
    
    def _create_psychographic_profiles(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create psychographic profiles"""
        
        # Innovation profile
        df["innovation_profile"] = (
            df["innovation_preference"] * 0.4 +
            df["tech_adoption_score"] * 0.3 +
            df["openness"] * 0.3
        )
        
        # Social responsibility profile
        df["social_responsibility_profile"] = (
            df["social_responsibility"] * 0.4 +
            df["environmental_consciousness"] * 0.3 +
            df["agreeableness"] * 0.3
        )
        
        # Achievement orientation
        df["achievement_orientation"] = (
            df["conscientiousness"] * 0.4 +
            df["investment_interest"] * 0.3 +
            df["extraversion"] * 0.3
        )
        
        return df
    
    def _create_lifestyle_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create lifestyle indicators"""
        
        # Family orientation
        df["family_orientation"] = (
            df["num_children"].apply(lambda x: min(x, 4) / 4) * 0.4 +
            df["marital_status"].apply(lambda x: 1 if x == "Married" else 0) * 0.3 +
            df["grocery_spend"] / df["grocery_spend"].max() * 0.3
        )
        
        # Urban sophistication
        df["urban_sophistication"] = (
            df["city_tier"].apply(lambda x: {"Tier-1": 1, "Tier-2": 0.7, "Tier-3": 0.4, "Rural": 0.1}[x]) * 0.4 +
            df["education_level"].apply(lambda x: {"Primary": 0.2, "Secondary": 0.4, "Graduate": 0.7, "Postgraduate": 0.9, "Doctorate": 1.0}[x]) * 0.3 +
            df["tech_adoption_score"] * 0.3
        )
        
        return df

    def _create_engagement_loyalty_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create engagement and loyalty signals from expanded feature set"""
        # Loyalty score from tier and coupon/referral behavior
        tier_weight = df.get("loyalty_tier", "None").map({"None": 0.0, "Bronze": 0.25, "Silver": 0.5, "Gold": 0.75, "Platinum": 1.0}) if "loyalty_tier" in df else 0
        df["loyalty_score"] = (
            (tier_weight if isinstance(tier_weight, pd.Series) else 0) * 0.5 +
            df.get("coupon_usage_rate", 0) * 0.25 +
            df.get("referral_tendency", 0) * 0.25
        )
        
        # Brand affinity composite
        df["brand_affinity_score"] = (
            df.get("brand_bose_affinity", 0) * 0.2 +
            df.get("brand_apple_affinity", 0) * 0.2 +
            df.get("brand_samsung_affinity", 0) * 0.2 +
            df.get("brand_nike_affinity", 0) * 0.2 +
            df.get("brand_amazon_affinity", 0) * 0.2
        )
        
        # Risk and opportunity indices
        df["retention_risk_index"] = (
            df.get("churn_risk", 0) * 0.6 + (1 - df.get("loyalty_score", 0)) * 0.4
        )
        df["conversion_opportunity_index"] = (
            df.get("propensity_to_buy", 0) * 0.6 + df.get("digital_engagement", 0) * 0.4
        )
        return df

class EnhancedClusteringAgent:
    """Agent 4: Enhanced clustering with comprehensive features"""
    
    def cluster_enhanced_audience(self, data: pd.DataFrame, goal_analysis: EnhancedGoalAnalysis) -> Dict[str, Any]:
        """Cluster enhanced audience with LLM-assisted parameter selection"""
        
        # Select features for clustering
        feature_columns = self._select_enhanced_features(data, goal_analysis)
        X = data[feature_columns].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Try LLM-assisted clustering parameter selection
        clustering_params = None
        if is_llm_enabled():
            clustering_params = self._generate_llm_clustering_params(X_scaled, goal_analysis)
        
        # Determine optimal number of clusters
        if clustering_params and "optimal_k" in clustering_params:
            optimal_k = clustering_params["optimal_k"]
        else:
            optimal_k = self._find_enhanced_optimal_k(X_scaled, goal_analysis)
        
        # Perform clustering with LLM-recommended parameters
        if clustering_params and "algorithm" in clustering_params:
            cluster_labels = self._apply_llm_clustering_algorithm(X_scaled, optimal_k, clustering_params)
        else:
            # Default KMeans clustering
            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init="auto")
            cluster_labels = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels
        data["cluster_id"] = cluster_labels
        
        # Calculate cluster statistics
        cluster_stats = self._calculate_enhanced_cluster_stats(data, feature_columns)
        
        return {
            "clusters": data,
            "cluster_stats": cluster_stats,
            "optimal_k": optimal_k,
            "feature_columns": feature_columns,
            "scaler": scaler,
            "clustering_params": clustering_params
        }
    
    def _generate_llm_clustering_params(self, X_scaled: np.ndarray, goal_analysis: EnhancedGoalAnalysis) -> Optional[Dict]:
        """Generate clustering parameters using LLM assistance"""
        
        n_samples, n_features = X_scaled.shape
        
        prompt = f"""
You are a data scientist expert in clustering algorithms for marketing analytics. Recommend clustering parameters based on the data and goal analysis.

Data Info:
- Samples: {n_samples}
- Features: {n_features}
- Goal Analysis: {goal_analysis.intent}
- Demographics: {goal_analysis.target_demographics}
- Behavioral Focus: {goal_analysis.behavioral_focus}

Recommend:
1. Optimal number of clusters (k)
2. Best clustering algorithm for this use case
3. Any specific parameters for the algorithm

Return JSON format:
{{
    "optimal_k": 6,
    "algorithm": "kmeans",
    "reasoning": "K-means works well for marketing segments",
    "parameters": {{
        "random_state": 42,
        "n_init": "auto"
    }}
}}

Available algorithms: kmeans, hdbscan, dbscan, gaussian_mixture
"""
        
        llm_response = generate_text(prompt)
        if not llm_response:
            return None
        
        try:
            import json
            return json.loads(llm_response.strip())
        except json.JSONDecodeError:
            return None
    
    def _apply_llm_clustering_algorithm(self, X_scaled: np.ndarray, optimal_k: int, clustering_params: Dict) -> np.ndarray:
        """Apply LLM-recommended clustering algorithm"""
        
        algorithm = clustering_params.get("algorithm", "kmeans")
        
        if algorithm == "kmeans":
            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init="auto")
            return kmeans.fit_predict(X_scaled)
        
        elif algorithm == "hdbscan":
            from sklearn.cluster import HDBSCAN
            hdbscan = HDBSCAN(min_cluster_size=max(10, optimal_k), min_samples=5)
            labels = hdbscan.fit_predict(X_scaled)
            # Convert HDBSCAN labels to 0-based cluster IDs
            unique_labels = np.unique(labels)
            label_map = {label: i for i, label in enumerate(unique_labels)}
            return np.array([label_map[label] for label in labels])
        
        elif algorithm == "dbscan":
            from sklearn.cluster import DBSCAN
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            labels = dbscan.fit_predict(X_scaled)
            # Convert DBSCAN labels to 0-based cluster IDs
            unique_labels = np.unique(labels)
            label_map = {label: i for i, label in enumerate(unique_labels)}
            return np.array([label_map[label] for label in labels])
        
        elif algorithm == "gaussian_mixture":
            from sklearn.mixture import GaussianMixture
            gmm = GaussianMixture(n_components=optimal_k, random_state=42)
            return gmm.fit_predict(X_scaled)
        
        else:
            # Fallback to KMeans
            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init="auto")
            return kmeans.fit_predict(X_scaled)
    
    def _select_enhanced_features(self, data: pd.DataFrame, goal_analysis: EnhancedGoalAnalysis) -> List[str]:
        """Select enhanced features for clustering"""
        
        base_features = [
            "spending_power", "digital_engagement", "lifestyle_complexity",
            "shopping_behavior_score", "media_consumption_score", "health_consciousness_score",
            "innovation_profile", "social_responsibility_profile", "achievement_orientation",
            "family_orientation", "urban_sophistication",
            # Newly added signals
            "loyalty_score", "brand_affinity_score", "retention_risk_index", "conversion_opportunity_index"
        ]
        
        # Intent-specific features
        if goal_analysis.intent == "conversion":
            base_features.extend(["electronics_interest", "auto_interest", "beauty_interest", "propensity_to_buy", "avg_order_value"])
        elif goal_analysis.intent == "engagement":
            base_features.extend(["social_media_usage", "entertainment_interest", "fitness_interest", "email_open_rate", "email_click_rate"])
        elif goal_analysis.intent == "retention":
            base_features.extend(["investment_interest", "travel_frequency", "lifestyle_complexity", "loyalty_score", "churn_risk"])
        
        # Filter available features
        available_features = [f for f in base_features if f in data.columns]
        
        return available_features
    
    def _find_enhanced_optimal_k(self, X: np.ndarray, goal_analysis: EnhancedGoalAnalysis) -> int:
        """Find optimal number of clusters for enhanced data"""
        
        # Intent-specific k ranges
        k_ranges = {
            "reach": (3, 6),
            "engagement": (2, 5),
            "conversion": (2, 4),
            "retention": (2, 4)
        }
        
        k_min, k_max = k_ranges.get(goal_analysis.intent, (2, 5))
        
        best_k = 2
        best_score = -1
        
        for k in range(k_min, k_max + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
            labels = kmeans.fit_predict(X)
            score = silhouette_score(X, labels)
            
            if score > best_score:
                best_score = score
                best_k = k
        
        return best_k
    
    def _calculate_enhanced_cluster_stats(self, data: pd.DataFrame, feature_columns: List[str]) -> Dict[int, Dict]:
        """Calculate enhanced cluster statistics"""
        cluster_stats = {}
        
        for cluster_id in data["cluster_id"].unique():
            cluster_data = data[data["cluster_id"] == cluster_id]
            
            stats = {
                "size": len(cluster_data),
                "size_pct": len(cluster_data) / len(data) * 100,
                "avg_age": cluster_data["age"].mean(),
                "dominant_gender": cluster_data["gender"].mode().iloc[0] if not cluster_data["gender"].mode().empty else "Unknown",
                "dominant_income": cluster_data["annual_hhi"].mode().iloc[0] if not cluster_data["annual_hhi"].mode().empty else "Unknown",
                "dominant_education": cluster_data["education_level"].mode().iloc[0] if not cluster_data["education_level"].mode().empty else "Unknown",
                "avg_spending_power": cluster_data["spending_power"].mean(),
                "avg_digital_engagement": cluster_data["digital_engagement"].mean(),
                "avg_lifestyle_complexity": cluster_data["lifestyle_complexity"].mean()
            }
            
            cluster_stats[cluster_id] = stats
        
        return cluster_stats

class EnhancedPersonaLabelingAgent:
    """Agent 5: Enhanced persona labeling"""
    
    def label_enhanced_clusters(self, clusters: Dict[str, Any], goal_analysis: EnhancedGoalAnalysis) -> Dict[str, Any]:
        """Label enhanced clusters"""
        
        labeled_clusters = clusters.copy()
        cluster_stats = clusters["cluster_stats"]
        intent = goal_analysis.intent
        
        cluster_labels = {}
        
        for cluster_id, stats in cluster_stats.items():
            label = self._generate_enhanced_cluster_label(cluster_id, stats, intent)
            cluster_labels[cluster_id] = label
        
        labeled_clusters["cluster_labels"] = cluster_labels
        
        return labeled_clusters
    
    def _generate_enhanced_cluster_label(self, cluster_id: int, stats: Dict[str, Any], intent: str) -> str:
        """Generate enhanced cluster label with LLM assistance"""
        
        # Prepare cluster characteristics for LLM
        cluster_summary = self._prepare_cluster_summary(stats, intent)
        
        # Try LLM-assisted labeling first
        if is_llm_enabled():
            llm_label = self._generate_llm_cluster_label(cluster_summary, intent)
            if llm_label:
                return llm_label.strip()[:120]
        
        # Fallback to rule-based labeling
        return self._generate_rule_based_label(stats, intent)
    
    def _prepare_cluster_summary(self, stats: Dict[str, Any], intent: str) -> str:
        """Prepare cluster summary for LLM"""
        
        # Key characteristics
        age = stats["avg_age"]
        gender = stats["dominant_gender"]
        income = stats["dominant_income"]
        education = stats["dominant_education"]
        
        # Behavioral scores
        spending_power = stats["avg_spending_power"]
        digital_engagement = stats["avg_digital_engagement"]
        lifestyle_complexity = stats["avg_lifestyle_complexity"]
        
        # Additional metrics if available
        size_pct = stats["size_pct"]
        
        summary = f"""
Cluster Characteristics:
- Demographics: {gender}, Age {age:.1f}, {income}, {education}
- Size: {size_pct:.1f}% of audience
- Spending Power: {spending_power:.2f} (0-1 scale)
- Digital Engagement: {digital_engagement:.2f} (0-1 scale)
- Lifestyle Complexity: {lifestyle_complexity:.2f} (0-1 scale)
- Marketing Intent: {intent}
"""
        return summary
    
    def _generate_llm_cluster_label(self, cluster_summary: str, intent: str) -> Optional[str]:
        """Generate cluster label using LLM"""
        
        prompt = f"""
You are a marketing analyst creating audience segment labels. Based on these cluster characteristics, create a concise, descriptive label (max 80 characters) that captures the key traits and marketing potential.

{cluster_summary}

Guidelines:
- Include key demographic info (age group, gender, income level)
- Add behavioral descriptor (e.g., "Tech-Savvy", "Budget-Conscious", "Premium")
- Consider the marketing intent: {intent}
- Be specific but concise
- Use format: "[Behavioral Trait] [Demographic] • [Income/Context]"

Examples:
- "Tech-Savvy Young Professionals • ₹5L-₹10L"
- "Budget-Conscious Millennial Parents • ₹2L-₹5L"
- "Premium Urban Sophisticates • ₹10L+"

Label:"""
        
        return generate_text(prompt)
    
    def _generate_rule_based_label(self, stats: Dict[str, Any], intent: str) -> str:
        """Fallback rule-based labeling"""
        
        age = stats["avg_age"]
        spending_power = stats["avg_spending_power"]
        digital_engagement = stats["avg_digital_engagement"]
        lifestyle_complexity = stats["avg_lifestyle_complexity"]
        gender = stats["dominant_gender"]
        income = stats["dominant_income"]
        
        # Intent-specific labeling
        if intent == "conversion":
            if spending_power > 0.7:
                label = f"High-Value {gender} Shoppers • {income}"
            elif digital_engagement > 0.7:
                label = f"Digital-First {gender} Buyers • {income}"
            else:
                label = f"Traditional {gender} Consumers • {income}"
        
        elif intent == "engagement":
            if digital_engagement > 0.7:
                label = f"Highly Engaged {gender} Users • {income}"
            elif lifestyle_complexity > 0.7:
                label = f"Active Lifestyle {gender} Users • {income}"
            else:
                label = f"Moderate {gender} Engagers • {income}"
        
        elif intent == "retention":
            if lifestyle_complexity > 0.7:
                label = f"Complex Lifestyle {gender} Users • {income}"
            elif spending_power > 0.7:
                label = f"Premium {gender} Customers • {income}"
            else:
                label = f"Standard {gender} Users • {income}"
        
        else:  # reach
            if age < 30:
                label = f"Young {gender} Audience • {income}"
            elif age > 50:
                label = f"Mature {gender} Audience • {income}"
            else:
                label = f"Mid-Age {gender} Audience • {income}"
        
        return label

class EnhancedStrategyGeneratorAgent:
    """Agent 6: Enhanced strategy generation"""
    
    def generate_enhanced_strategies(self, labeled_clusters: Dict[str, Any], 
                                   goal_analysis: EnhancedGoalAnalysis) -> List[Dict[str, Any]]:
        """Generate enhanced strategies"""
        
        strategies = []
        cluster_stats = labeled_clusters["cluster_stats"]
        cluster_labels = labeled_clusters["cluster_labels"]
        
        for cluster_id in cluster_stats.keys():
            strategy = self._generate_enhanced_strategy(
                cluster_id, cluster_stats[cluster_id], 
                cluster_labels[cluster_id], goal_analysis
            )
            strategies.append(strategy)
        
        return strategies
    
    def _generate_enhanced_strategy(self, cluster_id: int, stats: Dict[str, Any], 
                                  label: str, goal_analysis: EnhancedGoalAnalysis) -> Dict[str, Any]:
        """Generate enhanced strategy"""
        
        # Generate strategy based on intent and cluster characteristics
        if goal_analysis.intent == "conversion":
            strategy = self._generate_conversion_strategy(stats, label)
        elif goal_analysis.intent == "engagement":
            strategy = self._generate_engagement_strategy(stats, label)
        elif goal_analysis.intent == "retention":
            strategy = self._generate_retention_strategy(stats, label)
        else:
            strategy = self._generate_reach_strategy(stats, label)
        
        return {
            "cluster_id": cluster_id,
            "audience_label": label,
            "strategy": strategy,
            "budget_recommendation": self._calculate_enhanced_budget(stats),
            "channel_recommendation": self._recommend_enhanced_channels(stats, goal_analysis),
            "timeline": self._suggest_enhanced_timeline(stats, goal_analysis),
            "success_metrics": self._define_success_metrics(goal_analysis.intent)
        }
    
    def _generate_conversion_strategy(self, stats: Dict[str, Any], label: str) -> Dict[str, Any]:
        """Generate conversion strategy"""
        base = {
            "objective": "Drive conversions and sales",
            "tactics": [
                "Retargeting campaigns for high-intent users",
                "Dynamic product ads based on behavior",
                "Personalized messaging and offers",
                "Conversion-optimized landing pages",
                "Cross-selling and upselling strategies"
            ],
            "focus_areas": ["Purchase funnel optimization", "Cart abandonment recovery", "Product recommendations"]
        }
        # Optional LLM enrichment
        if is_llm_enabled():
            draft = generate_text(
                f"Suggest 3 channel-specific tactics for the audience '{label}' focusing on conversion.")
            if draft:
                base["llm_suggestions"] = draft
        return base
    
    def _generate_engagement_strategy(self, stats: Dict[str, Any], label: str) -> Dict[str, Any]:
        """Generate engagement strategy"""
        base = {
            "objective": "Increase audience engagement and interaction",
            "tactics": [
                "Interactive content campaigns",
                "Social media engagement programs",
                "User-generated content initiatives",
                "Community building activities",
                "Gamification elements"
            ],
            "focus_areas": ["Social media presence", "Content marketing", "Community engagement"]
        }
        if is_llm_enabled():
            draft = generate_text(
                f"Suggest 3 engaging content ideas for '{label}' audience with hooks/calls-to-action.")
            if draft:
                base["llm_suggestions"] = draft
        return base
    
    def _generate_retention_strategy(self, stats: Dict[str, Any], label: str) -> Dict[str, Any]:
        """Generate retention strategy"""
        base = {
            "objective": "Build customer loyalty and retention",
            "tactics": [
                "Loyalty program development",
                "Personalized retention campaigns",
                "Customer feedback and improvement",
                "Exclusive offers for existing customers",
                "Long-term relationship building"
            ],
            "focus_areas": ["Customer lifetime value", "Repeat purchase behavior", "Brand loyalty"]
        }
        if is_llm_enabled():
            draft = generate_text(
                f"Propose 3 retention campaign ideas for '{label}' audience with personalization angles.")
            if draft:
                base["llm_suggestions"] = draft
        return base
    
    def _generate_reach_strategy(self, stats: Dict[str, Any], label: str) -> Dict[str, Any]:
        """Generate reach strategy"""
        base = {
            "objective": "Maximize audience reach and brand visibility",
            "tactics": [
                "Broad targeting across multiple platforms",
                "High-frequency ad placements",
                "Video content for maximum engagement",
                "Cross-platform campaign coordination",
                "Brand awareness campaigns"
            ],
            "focus_areas": ["Brand visibility", "Market penetration", "Awareness building"]
        }
        if is_llm_enabled():
            draft = generate_text(
                f"Suggest 3 high-reach channel tactics for '{label}' audience with creative angles.")
            if draft:
                base["llm_suggestions"] = draft
        return base
    
    def _calculate_enhanced_budget(self, stats: Dict[str, Any]) -> str:
        """Calculate enhanced budget recommendation"""
        spending_power = stats["avg_spending_power"]
        size_pct = stats["size_pct"]
        
        if spending_power > 0.7 and size_pct > 20:
            return "High Budget (₹100K-₹500K)"
        elif spending_power > 0.5 and size_pct > 15:
            return "Medium Budget (₹50K-₹100K)"
        else:
            return "Low Budget (₹10K-₹50K)"
    
    def _recommend_enhanced_channels(self, stats: Dict[str, Any], goal_analysis: EnhancedGoalAnalysis) -> List[str]:
        """Recommend enhanced channels"""
        digital_engagement = stats["avg_digital_engagement"]
        
        if digital_engagement > 0.7:
            channels = ["Instagram", "TikTok", "YouTube", "Facebook", "Google Display"]
        elif digital_engagement > 0.4:
            channels = ["Facebook", "Instagram", "Google Search", "YouTube"]
        else:
            channels = ["Google Search", "Facebook", "Traditional Media"]
        
        return channels
    
    def _suggest_enhanced_timeline(self, stats: Dict[str, Any], goal_analysis: EnhancedGoalAnalysis) -> str:
        """Suggest enhanced timeline"""
        if goal_analysis.intent == "conversion":
            return "2-4 weeks (short-term)"
        elif goal_analysis.intent == "engagement":
            return "4-8 weeks (medium-term)"
        elif goal_analysis.intent == "retention":
            return "8-12 weeks (long-term)"
        else:
            return "6-10 weeks (medium-term)"
    
    def _define_success_metrics(self, intent: str) -> List[str]:
        """Define success metrics"""
        metrics = {
            "reach": ["Impressions", "Reach", "Frequency", "Brand Awareness"],
            "engagement": ["Engagement Rate", "Click-through Rate", "Time on Site", "Social Shares"],
            "conversion": ["Conversions", "ROAS", "CPA", "Revenue"],
            "retention": ["Retention Rate", "Customer Lifetime Value", "Repeat Purchase Rate", "Churn Rate"]
        }
        return metrics.get(intent, ["Impressions", "Engagement Rate", "Conversions"])

# Example usage
if __name__ == "__main__":
    # Initialize enhanced multi-agent system
    enhanced_system = EnhancedMultiAgentSystem()
    
    # Test with comprehensive goals
    test_goals = [
        "reach young professionals for tech product awareness",
        "convert high-income consumers for luxury brand sales",
        "engage fitness enthusiasts for health app",
        "retain millennial parents for family products",
        "target tech-savvy entrepreneurs for B2B software"
    ]
    
    for goal in test_goals:
        print(f"\n🎯 Testing Enhanced Goal: '{goal}'")
        result = enhanced_system.generate_enhanced_audiences(goal)
        print(f"✅ Generated {len(result['enhanced_clusters']['cluster_stats'])} enhanced clusters")
        print(f"📢 Generated {len(result['enhanced_strategies'])} enhanced strategies")
        
        for strategy in result['enhanced_strategies']:
            print(f"  - {strategy['audience_label']}: {strategy['strategy']['objective']}")
