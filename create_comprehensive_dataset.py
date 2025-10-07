"""
Create comprehensive 10K synthetic dataset with all ID Graph attributes
Based on the marketing segments data dictionary
"""

import pandas as pd
import numpy as np
import sqlite3
from sklearn.preprocessing import LabelEncoder
import json

def create_comprehensive_dataset():
    """Create comprehensive 10K synthetic dataset with all attributes"""
    
    np.random.seed(42)
    n_users = 10000
    
    print("🚀 Creating comprehensive 10K synthetic dataset...")
    
    # User IDs
    user_ids = range(1, n_users + 1)
    
    # ==================== DEMOGRAPHICS ====================
    print("📊 Generating Demographics...")
    
    # Age (18-75)
    age = np.random.normal(35, 12, n_users)
    age = np.clip(age, 18, 75).astype(int)
    
    # Gender
    gender = np.random.choice(["Male", "Female", "Other"], n_users, p=[0.48, 0.50, 0.02])
    
    # Income (Annual Household Income)
    income_ranges = ["Under ₹2L", "₹2L-₹5L", "₹5L-₹10L", "₹10L-₹20L", "₹20L-₹50L", "₹50L+"]
    income_weights = [0.15, 0.25, 0.30, 0.20, 0.08, 0.02]
    annual_hhi = np.random.choice(income_ranges, n_users, p=income_weights)
    
    # Education
    education_levels = ["Primary", "Secondary", "Graduate", "Postgraduate", "Doctorate"]
    education_weights = [0.20, 0.30, 0.35, 0.13, 0.02]
    education_level = np.random.choice(education_levels, n_users, p=education_weights)
    
    # Location
    regions = ["North", "South", "East", "West", "Central"]
    region_weights = [0.25, 0.25, 0.20, 0.20, 0.10]
    region = np.random.choice(regions, n_users, p=region_weights)
    
    city_tiers = ["Tier-1", "Tier-2", "Tier-3", "Rural"]
    city_tier_weights = [0.30, 0.35, 0.25, 0.10]
    city_tier = np.random.choice(city_tiers, n_users, p=city_tier_weights)
    
    # ==================== HOUSEHOLD COMPOSITION ====================
    print("🏠 Generating Household Composition...")
    
    # Marital Status
    marital_status = np.random.choice(["Single", "Married", "Divorced", "Widowed"], 
                                    n_users, p=[0.35, 0.55, 0.08, 0.02])
    
    # Number of Adults
    num_adults = np.random.choice([1, 2, 3, 4], n_users, p=[0.25, 0.60, 0.12, 0.03])
    
    # Number of Children
    num_children = np.random.choice([0, 1, 2, 3, 4], n_users, p=[0.30, 0.25, 0.25, 0.15, 0.05])
    
    # Youngest Child Age
    youngest_child_age = np.where(num_children > 0, 
                                np.random.choice(["0-2", "3-5", "6-12", "13-17", "18+"], n_users, 
                                               p=[0.20, 0.20, 0.30, 0.20, 0.10]), 
                                "None")
    
    # Home Ownership
    home_ownership = np.random.choice(["Own", "Rent", "Other"], n_users, p=[0.60, 0.35, 0.05])
    
    # Dwelling Type
    dwelling_type = np.random.choice(["Apartment", "House", "Villa", "Other"], 
                                   n_users, p=[0.40, 0.45, 0.10, 0.05])
    
    # Dwelling Unit Size
    dwelling_size = np.random.choice(["1BHK", "2BHK", "3BHK", "4BHK+"], 
                                   n_users, p=[0.15, 0.35, 0.35, 0.15])
    
    # ==================== COMMERCE & SHOPPING ====================
    print("🛒 Generating Commerce & Shopping Behavior...")
    
    # Grocery Shopping
    grocery_frequency = np.random.choice(["Daily", "Weekly", "Bi-weekly", "Monthly"], 
                                       n_users, p=[0.15, 0.50, 0.25, 0.10])
    
    grocery_spend = np.random.normal(8000, 3000, n_users)
    grocery_spend = np.clip(grocery_spend, 2000, 25000)
    
    # Electronics Shopping
    electronics_interest = np.random.beta(2, 3, n_users)  # 0-1 score
    electronics_frequency = np.random.choice(["Never", "Rarely", "Occasionally", "Frequently"], 
                                           n_users, p=[0.20, 0.30, 0.35, 0.15])
    
    # Beauty and Personal Care
    beauty_interest = np.random.beta(3, 2, n_users)  # Higher for females
    beauty_interest = np.where(gender == "Female", beauty_interest * 1.3, beauty_interest * 0.7)
    beauty_interest = np.clip(beauty_interest, 0, 1)
    
    beauty_spend = beauty_interest * np.random.normal(2000, 1000, n_users)
    beauty_spend = np.clip(beauty_spend, 0, 10000)
    
    # Household Products
    household_spend = np.random.normal(5000, 2000, n_users)
    household_spend = np.clip(household_spend, 1000, 15000)
    
    # Auto Shopping
    auto_interest = np.random.beta(2, 4, n_users)
    auto_budget = np.where(auto_interest > 0.5, 
                          np.random.normal(500000, 200000, n_users),
                          np.random.normal(200000, 100000, n_users))
    auto_budget = np.clip(auto_budget, 50000, 2000000)
    
    # ==================== MEDIA & CONTENT INTERESTS ====================
    print("📱 Generating Media & Content Interests...")
    
    # Social Media Usage
    social_media_usage = np.random.beta(3, 2, n_users)
    social_platforms = ["Facebook", "Instagram", "Twitter", "LinkedIn", "TikTok", "YouTube"]
    
    # Content Preferences
    content_preferences = {
        "Entertainment": np.random.beta(3, 2, n_users),
        "News": np.random.beta(2, 3, n_users),
        "Sports": np.random.beta(2, 3, n_users),
        "Technology": np.random.beta(2, 3, n_users),
        "Fashion": np.random.beta(2, 3, n_users),
        "Health": np.random.beta(3, 2, n_users),
        "Travel": np.random.beta(2, 3, n_users),
        "Food": np.random.beta(3, 2, n_users)
    }
    
    # Streaming Services
    streaming_services = np.random.choice(["Netflix", "Amazon Prime", "Disney+", "Hotstar", "None"], 
                                        n_users, p=[0.30, 0.25, 0.15, 0.20, 0.10])
    
    # ==================== TRAVEL ====================
    print("✈️ Generating Travel Behavior...")
    
    # Travel Frequency
    travel_frequency = np.random.choice(["Never", "Rarely", "Occasionally", "Frequently"], 
                                      n_users, p=[0.10, 0.30, 0.45, 0.15])
    
    # Travel Budget
    travel_budget = np.where(travel_frequency == "Frequently", 
                           np.random.normal(100000, 50000, n_users),
                           np.random.normal(50000, 25000, n_users))
    travel_budget = np.clip(travel_budget, 10000, 500000)
    
    # Travel Preferences
    travel_preferences = np.random.choice(["Domestic", "International", "Both"], 
                                        n_users, p=[0.40, 0.30, 0.30])
    
    # ==================== HEALTH & FITNESS ====================
    print("💪 Generating Health & Fitness...")
    
    # Fitness Interest
    fitness_interest = np.random.beta(2, 3, n_users)
    fitness_frequency = np.random.choice(["Never", "Rarely", "Weekly", "Daily"], 
                                       n_users, p=[0.20, 0.30, 0.35, 0.15])
    
    # Health Products
    health_product_interest = np.random.beta(3, 2, n_users)
    health_spend = health_product_interest * np.random.normal(3000, 1500, n_users)
    health_spend = np.clip(health_spend, 0, 15000)
    
    # ==================== INVESTMENTS & FINANCE ====================
    print("💰 Generating Investment & Finance...")
    
    # Investment Interest
    investment_interest = np.random.beta(2, 3, n_users)
    investment_amount = np.where(investment_interest > 0.5, 
                               np.random.normal(100000, 50000, n_users),
                               np.random.normal(25000, 15000, n_users))
    investment_amount = np.clip(investment_amount, 5000, 1000000)
    
    # Investment Types
    investment_types = np.random.choice(["Stocks", "Mutual Funds", "FD", "Gold", "Real Estate", "None"], 
                                      n_users, p=[0.15, 0.25, 0.30, 0.15, 0.10, 0.05])
    
    # ==================== ALCOHOL & LIFESTYLE ====================
    print("🍷 Generating Alcohol & Lifestyle...")
    
    # Alcohol Consumption
    alcohol_consumption = np.random.choice(["Never", "Rarely", "Occasionally", "Frequently"], 
                                         n_users, p=[0.40, 0.30, 0.25, 0.05])
    
    alcohol_spend = np.where(alcohol_consumption == "Frequently", 
                           np.random.normal(5000, 2000, n_users),
                           np.random.normal(2000, 1000, n_users))
    alcohol_spend = np.clip(alcohol_spend, 0, 15000)
    
    # ==================== BUSINESS & PROFESSIONAL ====================
    print("💼 Generating Business & Professional...")
    
    # Company Size (for employed users)
    company_size = np.random.choice(["1-10", "11-50", "51-200", "201-500", "500+"], 
                                  n_users, p=[0.20, 0.25, 0.25, 0.20, 0.10])
    
    # Industry
    industries = ["IT", "Finance", "Healthcare", "Education", "Manufacturing", "Retail", "Other"]
    industry_weights = [0.20, 0.15, 0.15, 0.15, 0.15, 0.10, 0.10]
    industry = np.random.choice(industries, n_users, p=industry_weights)
    
    # Job Level
    job_level = np.random.choice(["Entry", "Mid", "Senior", "Executive"], 
                               n_users, p=[0.30, 0.40, 0.25, 0.05])
    
    # ==================== DEVICE & TECHNOLOGY ====================
    print("📱 Generating Device & Technology...")
    
    # Device Ownership
    smartphone_ownership = np.random.choice([0, 1], n_users, p=[0.05, 0.95])
    laptop_ownership = np.random.choice([0, 1], n_users, p=[0.20, 0.80])
    tablet_ownership = np.random.choice([0, 1], n_users, p=[0.60, 0.40])
    
    # Technology Adoption
    tech_adoption_score = np.random.beta(3, 2, n_users)
    
    # ==================== PSYCHOGRAPHICS ====================
    print("🧠 Generating Psychographics...")
    
    # Personality Traits (Big 5)
    openness = np.random.normal(0.5, 0.2, n_users)
    conscientiousness = np.random.normal(0.5, 0.2, n_users)
    extraversion = np.random.normal(0.5, 0.2, n_users)
    agreeableness = np.random.normal(0.5, 0.2, n_users)
    neuroticism = np.random.normal(0.5, 0.2, n_users)
    
    # Clip to 0-1 range
    openness = np.clip(openness, 0, 1)
    conscientiousness = np.clip(conscientiousness, 0, 1)
    extraversion = np.clip(extraversion, 0, 1)
    agreeableness = np.clip(agreeableness, 0, 1)
    neuroticism = np.clip(neuroticism, 0, 1)
    
    # Values
    environmental_consciousness = np.random.beta(3, 2, n_users)
    social_responsibility = np.random.beta(2, 3, n_users)
    innovation_preference = np.random.beta(2, 3, n_users)
    
    # ==================== ADDITIONAL MARKETING SIGNALS ====================
    print("📈 Generating Additional Marketing Signals...")
    
    # Social platform usage (binary)
    fb_usage = np.random.choice([0, 1], n_users, p=[0.4, 0.6])
    ig_usage = np.random.choice([0, 1], n_users, p=[0.5, 0.5])
    yt_usage = np.random.choice([0, 1], n_users, p=[0.35, 0.65])
    tt_usage = np.random.choice([0, 1], n_users, p=[0.7, 0.3])
    li_usage = np.random.choice([0, 1], n_users, p=[0.6, 0.4])
    
    # Ad engagement metrics (0-1)
    ctr_score = np.random.beta(2, 5, n_users)
    vtr_score = np.random.beta(3, 4, n_users)
    dwell_time_score = np.random.beta(3, 3, n_users)
    
    # Payment preferences
    payment_method = np.random.choice(["UPI", "Credit Card", "Debit Card", "COD", "Wallet"], n_users, p=[0.45, 0.20, 0.20, 0.05, 0.10])
    emi_preference = np.random.choice([0, 1], n_users, p=[0.75, 0.25])
    
    # E-commerce behavior
    cart_abandon_rate = np.random.beta(3, 3, n_users)
    purchase_frequency = np.random.choice(["Low", "Medium", "High"], n_users, p=[0.5, 0.35, 0.15])
    avg_order_value = np.random.normal(2500, 1200, n_users)
    avg_order_value = np.clip(avg_order_value, 200, 15000)
    
    # App category usage (0-1)
    gaming_app_use = np.random.beta(2, 4, n_users)
    finance_app_use = np.random.beta(2, 3, n_users)
    shopping_app_use = np.random.beta(3, 2, n_users)
    food_delivery_use = np.random.beta(3, 2, n_users)
    ride_hailing_use = np.random.beta(2, 3, n_users)
    
    # Device specs
    device_os = np.random.choice(["Android", "iOS", "Other"], n_users, p=[0.7, 0.28, 0.02])
    device_ram_gb = np.random.choice([2, 3, 4, 6, 8, 12], n_users, p=[0.05, 0.10, 0.30, 0.25, 0.20, 0.10])
    device_storage_gb = np.random.choice([32, 64, 128, 256, 512], n_users, p=[0.10, 0.30, 0.35, 0.20, 0.05])
    
    # Time-of-day and weekend activity
    active_morning = np.random.beta(2, 3, n_users)
    active_evening = np.random.beta(3, 2, n_users)
    weekend_activity = np.random.beta(2, 3, n_users)
    
    # Email engagement
    email_open_rate = np.random.beta(2, 4, n_users)
    email_click_rate = np.random.beta(2, 6, n_users)
    unsubscribed = np.random.choice([0, 1], n_users, p=[0.95, 0.05])
    
    # Loyalty and coupons
    loyalty_tier = np.random.choice(["None", "Bronze", "Silver", "Gold", "Platinum"], n_users, p=[0.50, 0.20, 0.20, 0.08, 0.02])
    coupon_usage_rate = np.random.beta(2, 3, n_users)
    referral_tendency = np.random.beta(2, 3, n_users)
    
    # Satisfaction and NPS
    csat_score = np.random.beta(4, 2, n_users)
    nps_score = np.random.normal(0.2, 0.2, n_users)
    nps_score = np.clip(nps_score, 0, 1)
    
    # Churn and propensity
    churn_risk = np.random.beta(2, 3, n_users)
    propensity_to_buy = np.random.beta(3, 2, n_users)
    
    # Languages and geo granularity
    language_pref = np.random.choice(["English", "Hindi", "Tamil", "Telugu", "Kannada", "Bengali", "Marathi", "Gujarati", "Other"], n_users, p=[0.35, 0.25, 0.06, 0.06, 0.05, 0.07, 0.07, 0.05, 0.04])
    zipcode_cluster = np.random.choice([f"Z{z:03d}" for z in range(1, 101)], n_users)
    
    # Brand affinities (0-1)
    brand_bose_affinity = np.random.beta(2, 3, n_users)
    brand_apple_affinity = np.random.beta(2, 3, n_users)
    brand_samsung_affinity = np.random.beta(2, 3, n_users)
    brand_nike_affinity = np.random.beta(2, 3, n_users)
    brand_amazon_affinity = np.random.beta(3, 2, n_users)
    
    # ==================== CREATE DATAFRAME ====================
    print("📊 Creating comprehensive DataFrame...")
    
    # Create main DataFrame
    df = pd.DataFrame({
        # Demographics
        "user_id": user_ids,
        "age": age,
        "gender": gender,
        "annual_hhi": annual_hhi,
        "education_level": education_level,
        "region": region,
        "city_tier": city_tier,
        
        # Household Composition
        "marital_status": marital_status,
        "num_adults": num_adults,
        "num_children": num_children,
        "youngest_child_age": youngest_child_age,
        "home_ownership": home_ownership,
        "dwelling_type": dwelling_type,
        "dwelling_size": dwelling_size,
        
        # Commerce & Shopping
        "grocery_frequency": grocery_frequency,
        "grocery_spend": grocery_spend,
        "electronics_interest": electronics_interest,
        "electronics_frequency": electronics_frequency,
        "beauty_interest": beauty_interest,
        "beauty_spend": beauty_spend,
        "household_spend": household_spend,
        "auto_interest": auto_interest,
        "auto_budget": auto_budget,
        
        # Media & Content
        "social_media_usage": social_media_usage,
        "streaming_services": streaming_services,
        "entertainment_interest": content_preferences["Entertainment"],
        "news_interest": content_preferences["News"],
        "sports_interest": content_preferences["Sports"],
        "technology_interest": content_preferences["Technology"],
        "fashion_interest": content_preferences["Fashion"],
        "health_interest": content_preferences["Health"],
        "travel_interest": content_preferences["Travel"],
        "food_interest": content_preferences["Food"],
        
        # Travel
        "travel_frequency": travel_frequency,
        "travel_budget": travel_budget,
        "travel_preferences": travel_preferences,
        
        # Health & Fitness
        "fitness_interest": fitness_interest,
        "fitness_frequency": fitness_frequency,
        "health_product_interest": health_product_interest,
        "health_spend": health_spend,
        
        # Investments & Finance
        "investment_interest": investment_interest,
        "investment_amount": investment_amount,
        "investment_types": investment_types,
        
        # Alcohol & Lifestyle
        "alcohol_consumption": alcohol_consumption,
        "alcohol_spend": alcohol_spend,
        
        # Business & Professional
        "company_size": company_size,
        "industry": industry,
        "job_level": job_level,
        
        # Device & Technology
        "smartphone_ownership": smartphone_ownership,
        "laptop_ownership": laptop_ownership,
        "tablet_ownership": tablet_ownership,
        "tech_adoption_score": tech_adoption_score,
        
        # Psychographics
        "openness": openness,
        "conscientiousness": conscientiousness,
        "extraversion": extraversion,
        "agreeableness": agreeableness,
        "neuroticism": neuroticism,
        "environmental_consciousness": environmental_consciousness,
        "social_responsibility": social_responsibility,
        "innovation_preference": innovation_preference
        ,
        # Additional Marketing Signals
        "fb_usage": fb_usage,
        "ig_usage": ig_usage,
        "yt_usage": yt_usage,
        "tt_usage": tt_usage,
        "li_usage": li_usage,
        "ctr_score": ctr_score,
        "vtr_score": vtr_score,
        "dwell_time_score": dwell_time_score,
        "payment_method": payment_method,
        "emi_preference": emi_preference,
        "cart_abandon_rate": cart_abandon_rate,
        "purchase_frequency": purchase_frequency,
        "avg_order_value": avg_order_value,
        "gaming_app_use": gaming_app_use,
        "finance_app_use": finance_app_use,
        "shopping_app_use": shopping_app_use,
        "food_delivery_use": food_delivery_use,
        "ride_hailing_use": ride_hailing_use,
        "device_os": device_os,
        "device_ram_gb": device_ram_gb,
        "device_storage_gb": device_storage_gb,
        "active_morning": active_morning,
        "active_evening": active_evening,
        "weekend_activity": weekend_activity,
        "email_open_rate": email_open_rate,
        "email_click_rate": email_click_rate,
        "unsubscribed": unsubscribed,
        "loyalty_tier": loyalty_tier,
        "coupon_usage_rate": coupon_usage_rate,
        "referral_tendency": referral_tendency,
        "csat_score": csat_score,
        "nps_score": nps_score,
        "churn_risk": churn_risk,
        "propensity_to_buy": propensity_to_buy,
        "language_pref": language_pref,
        "zipcode_cluster": zipcode_cluster,
        "brand_bose_affinity": brand_bose_affinity,
        "brand_apple_affinity": brand_apple_affinity,
        "brand_samsung_affinity": brand_samsung_affinity,
        "brand_nike_affinity": brand_nike_affinity,
        "brand_amazon_affinity": brand_amazon_affinity
    })
    
    # ==================== ADD CORRELATIONS ====================
    print("🔗 Adding realistic correlations...")
    
    # Age correlations
    df.loc[df["age"] > 50, "investment_interest"] *= 1.3
    df.loc[df["age"] < 30, "tech_adoption_score"] *= 1.2
    
    # Income correlations
    high_income_mask = df["annual_hhi"].isin(["₹10L-₹20L", "₹20L-₹50L", "₹50L+"])
    df.loc[high_income_mask, "travel_frequency"] = np.random.choice(["Occasionally", "Frequently"], 
                                                                  len(df[high_income_mask]), p=[0.6, 0.4])
    df.loc[high_income_mask, "investment_interest"] *= 1.4
    
    # Gender correlations
    df.loc[df["gender"] == "Female", "beauty_interest"] *= 1.5
    df.loc[df["gender"] == "Male", "sports_interest"] *= 1.3
    
    # Family correlations
    has_children_mask = df["num_children"] > 0
    df.loc[has_children_mask, "grocery_spend"] *= 1.3
    df.loc[has_children_mask, "household_spend"] *= 1.2
    
    # Education correlations
    high_education_mask = df["education_level"].isin(["Postgraduate", "Doctorate"])
    df.loc[high_education_mask, "investment_interest"] *= 1.2
    df.loc[high_education_mask, "tech_adoption_score"] *= 1.1
    
    # Clip all numerical values to valid ranges
    for col in df.columns:
        if df[col].dtype in ['float64'] and col not in ['user_id', 'num_adults', 'num_children', 'avg_order_value']:
            df[col] = np.clip(df[col], 0, 1)
    
    return df

def save_comprehensive_dataset(df, db_path="data/comprehensive_users.db", csv_path="data/comprehensive_users.csv"):
    """Save comprehensive dataset to multiple formats"""
    
    import os
    os.makedirs("data", exist_ok=True)
    
    # Save to SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql("users", conn, if_exists="replace", index=False)
    conn.close()
    
    # Save to CSV
    df.to_csv(csv_path, index=False)
    
    # Save data dictionary
    data_dict = {
        "dataset_info": {
            "total_users": len(df),
            "total_features": len(df.columns),
            "created_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "feature_categories": {
            "demographics": ["age", "gender", "annual_hhi", "education_level", "region", "city_tier"],
            "household": ["marital_status", "num_adults", "num_children", "youngest_child_age", "home_ownership", "dwelling_type", "dwelling_size"],
            "commerce": ["grocery_frequency", "grocery_spend", "electronics_interest", "beauty_interest", "beauty_spend", "household_spend", "auto_interest", "auto_budget"],
            "media": ["social_media_usage", "streaming_services", "entertainment_interest", "news_interest", "sports_interest", "technology_interest", "fashion_interest", "health_interest", "travel_interest", "food_interest"],
            "lifestyle": ["travel_frequency", "travel_budget", "travel_preferences", "fitness_interest", "fitness_frequency", "health_product_interest", "health_spend"],
            "finance": ["investment_interest", "investment_amount", "investment_types"],
            "consumption": ["alcohol_consumption", "alcohol_spend"],
            "professional": ["company_size", "industry", "job_level"],
            "technology": ["smartphone_ownership", "laptop_ownership", "tablet_ownership", "tech_adoption_score"],
            "psychographics": ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism", "environmental_consciousness", "social_responsibility", "innovation_preference"]
        }
    }
    
    with open("data/data_dictionary.json", "w") as f:
        json.dump(data_dict, f, indent=2)
    
    print(f"✅ Saved comprehensive dataset:")
    print(f"📊 SQLite: {db_path}")
    print(f"📄 CSV: {csv_path}")
    print(f"📚 Data Dictionary: data/data_dictionary.json")
    print(f"�� Total Users: {len(df):,}")
    print(f"🔢 Total Features: {len(df.columns)}")
    
    return data_dict

if __name__ == "__main__":
    # Create comprehensive dataset
    print("🚀 Creating comprehensive 10K synthetic dataset...")
    df = create_comprehensive_dataset()
    
    # Save dataset
    data_dict = save_comprehensive_dataset(df)
    
    # Show sample data
    print("\n📋 Sample data:")
    print(df.head())
    
    print("\n📈 Dataset statistics:")
    print(df.describe())
    
    print("\n🎯 Feature distribution:")
    for category, features in data_dict["feature_categories"].items():
        print(f"{category.title()}: {len(features)} features")
