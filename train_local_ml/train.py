import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# Giả sử bạn đã có dữ liệu CSV
DATA_PATH = "data.csv"
MODEL_PATH = "model.joblib"

def train_model():
    # Load dữ liệu
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["y"])
    y = df["y"]

    # Huấn luyện model
    model = LinearRegression()
    model.fit(X, y)

    # Đánh giá model
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    print(f"Model trained. MSE: {mse}")

    # Lưu model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
