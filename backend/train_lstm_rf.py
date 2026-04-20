import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

# Load dataset
df = pd.read_csv('data/simulated_data.csv')

# Add timestamp if missing
if 'timestamp' not in df.columns:
    df['timestamp'] = pd.date_range(start='now', periods=len(df), freq='s')

# Sort by timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Feature and label selection
X = df[['temperature', 'humidity', 'nh3', 'weight', 'motion', 'age']]
y = df['health_status'].astype('category').cat.codes  # Healthy=0, Stressed=1, Sick=2

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(scaler, 'models/scaler.pkl')

# Reshape for LSTM (samples, timesteps, features)
X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y, test_size=0.2, random_state=42)

# Build LSTM model
lstm_model = Sequential()
lstm_model.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2])))
lstm_model.add(Dense(10, activation='relu'))

# Extract features from LSTM
lstm_features = lstm_model.predict(X_reshaped)

# Train Random Forest on LSTM features
rf_model = RandomForestClassifier(n_estimators=100)
rf_model.fit(lstm_features, y)

# Save trained model
joblib.dump(rf_model, 'models/lstm_rf_model.pkl')
print("✅ LSTM-RF model trained and saved!")

# Evaluate
preds = rf_model.predict(lstm_model.predict(X_test))
label_map = {0: "Healthy", 1: "Stressed", 2: "Sick"}
test_labels = [label_map[y] for y in y_test]
pred_labels = [label_map[p] for p in preds]

print("\nModel Evaluation:")
print(classification_report(test_labels, pred_labels))