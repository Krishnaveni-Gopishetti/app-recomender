from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# LOAD DATA
df = pd.read_csv("Digital_Literacy_Final_Project_Professional.csv")
apps_df = pd.read_csv("apps_dataset_final.csv")

# ENCODING
le_edu = LabelEncoder()
le_dev = LabelEncoder()
le_target = LabelEncoder()

df["education_level"] = le_edu.fit_transform(df["education_level"])
df["device_type"] = le_dev.fit_transform(df["device_type"])
df["digital_literacy_level"] = le_target.fit_transform(df["digital_literacy_level"])

# MODEL
X = df[["age","education_level","internet_hours","device_type"]]
y = df["digital_literacy_level"]

model = RandomForestClassifier(n_estimators=120, max_depth=9)
model.fit(X, y)

levels = ["Beginner","Intermediate","Advanced"]

# 🔥 FAKE DETECTION
def check_app_authenticity(name, rating):
    if rating < 3:
        return "Fake ❌"
    elif "mod" in name.lower() or "hack" in name.lower():
        return "Suspicious ⚠️"
    else:
        return "Real ✅"

# FORMAT OUTPUT
def format_apps(df):
    result = []
    for _, row in df.iterrows():
        status = check_app_authenticity(row["app_name"], row["rating"])
        result.append({
            "name": row["app_name"],
            "rating": row["rating"],
            "link": row["app_link"],
            "status": status
        })
    return result

@app.route('/')
def home():
    return "ML API Running 🚀"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json

    age = int(data.get("age"))
    edu = data.get("education")
    internet = int(data.get("internet_hours"))
    device = data.get("device")
    category = data.get("category")

    edu_map = {"High School":0,"Bachelor":1,"Master":2}
    dev_map = {"Mobile":0,"Laptop":1,"Tablet":2}

    input_df = pd.DataFrame([{
        "age": age,
        "education_level": edu_map[edu],
        "internet_hours": internet,
        "device_type": dev_map[device]
    }])

    pred = model.predict(input_df)[0]
    level = levels[pred]

    apps_df2 = apps_df.drop_duplicates("app_name")

    # ⭐ Recommended
    recommended_apps = apps_df2.sample(n=min(5,len(apps_df2)))

    # 📂 Category
    filtered = apps_df2[apps_df2["category"].str.lower() == category.lower()]
    if len(filtered) == 0:
        filtered = apps_df2

    category_apps = filtered.sample(n=min(5,len(filtered)))

    return jsonify({
        "level": level,
        "recommended_apps": format_apps(recommended_apps),
        "category_apps": format_apps(category_apps)
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0', port=port)
