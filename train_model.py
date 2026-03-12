import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Load dataset
data = pd.read_csv("car_price_dataset.csv")

# Remove unnecessary columns
data = data.drop(["Car ID", "Model"], axis=1)

# Convert text columns to numbers
data = pd.get_dummies(data, drop_first=True)

# Features and target
X = data.drop("Price", axis=1)
y = data["Price"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predict
pred = model.predict(X_test)

# Accuracy
print("Model Accuracy:", r2_score(y_test, pred))