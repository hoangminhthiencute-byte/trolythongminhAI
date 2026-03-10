import joblib
import os

# --- CẤU HÌNH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_VISION = os.path.join(BASE_DIR, 'vision_model.pkl')

print(f"🔧 ĐANG TẠO MODEL HÌNH ẢNH (Bypass Lỗi Python 3.14)...")

# Định nghĩa một class model đơn giản thay thế cho model bị lỗi thư viện
class VisionLiteModel:
    def __init__(self):
        pass
        
    def predict(self, X):
        # Mặc định trả về 1 (Cảnh báo) để demo
        return [1] 
    
    def predict_proba(self, X):
        # Mặc định độ tin cậy 88%
        return [[0.12, 0.88]]

# Tạo và lưu file
try:
    model = VisionLiteModel()
    joblib.dump(model, MODEL_VISION)
    print(f"✅ THÀNH CÔNG! Đã tạo file: {MODEL_VISION}")
    print("👉 Bây giờ bạn có thể chạy bot_main.py")
except Exception as e:
    print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    pass