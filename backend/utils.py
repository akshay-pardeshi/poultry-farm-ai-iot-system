
import random
import pandas as pd
from datetime import datetime

def generate_sensor_data():
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": round(random.uniform(25, 35), 1),
        "humidity": round(random.uniform(60, 80), 1),
        "nh3": round(random.uniform(5, 10), 1),
        "weight": round(random.uniform(1.2, 2.5), 2),
        "motion": random.choice([0, 1]),
        "sound": random.choice(["Normal", "Sneezing", "Distress"]),
        "age": random.randint(20, 50),
        "health_status": random.choice(["Healthy", "Stressed", "Sick"]),
        "disease_type": random.choice(["--", "Respiratory Infection"])
    }

    df = pd.DataFrame([data])

    # Ensure header is written only once
    file_exists = pd.io.common.file_exists("data/simulated_data.csv")
    
    df.to_csv("data/simulated_data.csv", mode='a', index=False, header=not file_exists)
    
    return data