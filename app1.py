from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# ✅ LOAD DATASETS (upload these files in GitHub)
df = pd.read_csv("Digital_Literacy_Final_Project_Professional.csv")
apps_df = pd.read_csv("apps_dataset_final.csv")

# ✅ ENCODING
le_edu = LabelEncoder()
le_dev = LabelEncoder()
le_target = LabelEncoder()

df["education_level"] = le_edu.fit_transform(df["education_level"])
df["device_type"] = le_dev.fit_transform(df["device_type"])
df["digital_literacy_level"] = le_target.fit_transform(df["digital_literacy_level"])

# ✅ TRAIN MODEL
X = df[["age","education_level","internet_hours","device_type"]]
y = df["digital_literacy_level"]

model = RandomForestClassifier(n_estimators=120, max_depth=9, random_state=42)
model.fit(X, y)

levels = ["Beginner","Intermediate","Advanced"]

# ✅ API
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

    # FILTER APPS
    apps_df2 = apps_df.drop_duplicates("app_name")

    cat_apps = apps_df2.sample(n=min(5,len(apps_df2)))

    pers = apps_df2.copy()
    pers = pers.sample(n=min(10,len(pers)))

    return jsonify({
        "level": level,
        "category_apps": cat_apps["app_name"].tolist(),
        "personalized_apps": pers["app_name"].tolist()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
