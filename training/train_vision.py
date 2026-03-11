import os
import cv2
import numpy as np
import joblib
from skimage.feature import hog
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# --- CẤU HÌNH ---
DATA_DIR = 'dataset_ecg'
MODEL_FILE = 'vision_model.pkl'
IMG_SIZE = (128, 128) # Ảnh lớn hơn để nhìn rõ sóng

def get_hog(img):
    # Resize
    img = cv2.resize(img, IMG_SIZE)
    # Tính HOG (Đặc trưng hình dáng)
    features = hog(img, orientations=9, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), visualize=False, block_norm='L2-Hys')
    return features

def train():
    print("🚀 Đang xử lý ảnh (HOG)...")
    data = []
    labels = []
    classes = ['normal', 'abnormal'] # 0: Normal, 1: Abnormal

    for label_id, label_name in enumerate(classes):
        path = os.path.join(DATA_DIR, label_name)
        if not os.path.exists(path): continue
        
        for file in os.listdir(path):
            try:
                img_path = os.path.join(path, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    # Cắt giữa ảnh (Crop) để loại bỏ viền đen thừa
                    h, w = img.shape
                    img = img[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
                    
                    # Lấy đặc trưng HOG
                    feats = get_hog(img)
                    data.append(feats)
                    labels.append(label_id)
            except: pass

    if len(data) == 0:
        print("❌ Không có dữ liệu.")
        return

    print(f"✅ Tổng: {len(data)} ảnh.")
    
    # Chia tập dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(np.array(data), np.array(labels), test_size=0.2, random_state=42, stratify=labels)

    # TRAIN SVM (Kernel Linear thường tốt cho HOG)
    print("🧠 Đang train SVM Model...")
    # class_weight='balanced': Tự động phạt nặng nếu đoán sai lớp ít dữ liệu
    model = SVC(kernel='linear', probability=True, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)

    # Đánh giá
    print("\n📝 KẾT QUẢ:")
    preds = model.predict(X_test)
    print(classification_report(y_test, preds, target_names=classes))
    
    joblib.dump(model, MODEL_FILE)
    print(f"💾 Đã lưu model: {MODEL_FILE}")

if __name__ == "__main__":
    train()