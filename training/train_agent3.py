import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score

# --- CẤU HÌNH ---
DATA_FILE = 'heart_disease_uci.csv'
MODEL_FILE = 'heart_model.pkl'

def train():
    print("⏳ Agent 3 đang đọc dữ liệu từ CSV...")
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print(f"❌ Lỗi: Không thấy file '{DATA_FILE}'")
        return

    # 1. Chọn các cột quan trọng (tương thích file UCI của bạn)
    # age, sex, trestbps (huyết áp), chol (cholesterol), thalch (nhịp tim)
    feature_cols = ['age', 'sex', 'trestbps', 'chol', 'thalch']
    target_col = 'num' # 0: Khỏe, 1-4: Bệnh

    # 2. Xử lý dữ liệu
    print("   ... Đang làm sạch dữ liệu ...")
    
    # Chuyển đổi giới tính: Male->1, Female->0
    df['sex'] = df['sex'].map({'Male': 1, 'Female': 0})
    
    # Tạo cột Target (0 là khỏe, >0 là bệnh -> chuyển thành 1)
    df['target'] = (df[target_col] > 0).astype(int)
    
    X = df[feature_cols]
    y = df['target']

    # Xử lý các ô trống (NaN) bằng cách điền giá trị trung bình
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)

    # 3. Chia tập train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Huấn luyện (Logistic Regression)
    print("🔄 Đang huấn luyện mô hình...")
    model = LogisticRegression(max_iter=3000)
    model.fit(X_train, y_train)

    # 5. Đánh giá
    acc = model.score(X_test, y_test)
    print(f"✅ Agent 3 đã học xong! Độ chính xác: {acc*100:.2f}%")

    # 6. Lưu model
    joblib.dump(model, MODEL_FILE)
    print(f"💾 Đã lưu file model: {MODEL_FILE}")

if __name__ == "__main__":
    train()