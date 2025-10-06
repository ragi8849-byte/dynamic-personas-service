import numpy as np, pandas as pd, pickle, os
from sklearn.preprocessing import OneHotEncoder, StandardScaler

os.makedirs("data", exist_ok=True)
rng = np.random.default_rng(42)

# Adjust N if your machine is low on memory
N = 50_000

age = np.clip(rng.normal(34, 10, N), 18, 65).astype(int)
income_band = rng.choice(["Low","Mid","High"], size=N, p=[0.40,0.45,0.15])
city_tier = rng.choice(["Tier-1","Tier-2","Tier-3"], size=N, p=[0.50,0.30,0.20])
preferred_media = rng.choice(["YouTube","Instagram","TV","Twitter","Reddit"], size=N, p=[0.35,0.25,0.25,0.10,0.05])
owns_car = rng.choice([0,1], size=N, p=[0.60,0.40])
device_count = np.clip(rng.poisson(3, size=N), 0, 8)
emi_flag = rng.choice([0,1], size=N, p=[0.55,0.45])

brand_awareness_bose = np.clip(rng.normal(0.60, 0.20, N), 0, 1)
price_sensitivity   = np.clip(rng.normal(0.50, 0.20, N), 0, 1)
privacy_pref        = np.clip(rng.normal(0.40, 0.25, N), 0, 1)

users = pd.DataFrame({
    "age": age,
    "income_band": income_band,
    "city_tier": city_tier,
    "preferred_media": preferred_media,
    "owns_car": owns_car,
    "device_count": device_count,
    "emi_flag": emi_flag,
    "brand_awareness_bose": brand_awareness_bose,
    "price_sensitivity": price_sensitivity,
    "privacy_pref": privacy_pref,
})

# Save raw synthetic users
users.to_parquet("data/users.parquet", index=False)

# Create a standardized feature matrix for fast clustering later
cat = ["income_band","city_tier","preferred_media"]
num = ["age","owns_car","device_count","emi_flag","brand_awareness_bose","price_sensitivity","privacy_pref"]

enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_cat = enc.fit_transform(users[cat])
X_num = users[num].astype(float).values
X = np.hstack([X_num, X_cat])

scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X).astype("float32")

np.save("data/feats.npy", X_scaled)

with open("data/encoders.pkl", "wb") as f:
    pickle.dump({"encoder": enc, "scaler": scaler, "cat": cat, "num": num}, f)

print("Wrote:")
print(" - data/users.parquet")
print(" - data/feats.npy (shape:", X_scaled.shape, ")")
print(" - data/encoders.pkl")


