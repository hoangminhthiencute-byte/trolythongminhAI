import os
import sys
import importlib.util

print("\n" + "="*40)
print("   CHƯƠNG TRÌNH KIỂM TRA LỖI (DEBUG)   ")
print("="*40 + "\n")

# 1. KIỂM TRA THƯ VIỆN
libraries = {
    "cv2": "opencv-python",
    "telegram": "python-telegram-bot",
    "sklearn": "scikit-learn",
    "joblib": "joblib",
    "pandas": "pandas",
    "numpy": "numpy"
}

print("1. KIỂM TRA THƯ VIỆN CÀI ĐẶT:")
all_libs_ok = True
for lib_name, install_name in libraries.items():
    if importlib.util.find_spec(lib_name) is None:
        print(f"   ❌ THIẾU: {install_name} (Cần cài đặt)")
        all_libs_ok = False
    else:
        print(f"   ✅ OK: {install_name}")

if not all_libs_ok:
    print("\n   👉 LỆNH SỬA LỖI (Copy và chạy dòng này):")
    print(f"   & {sys.executable} -m pip install opencv-python python-telegram-bot scikit-learn joblib pandas numpy")
    print("\n" + "-"*40)

# 2. KIỂM TRA DỮ LIỆU
print("\n2. KIỂM TRA FILE VÀ THƯ MỤC:")

files_to_check = {
    "heart_disease_uci.csv": "File dữ liệu tim mạch (Tải từ Kaggle)",
    "train_agent3.py": "Code huấn luyện Agent 3",
    "train_vision.py": "Code huấn luyện Agent 2",
    "bot_main.py": "Code chính của Bot",
    "hinhanhdev2.png": "Banner image cho bot"
}

all_files_ok = True
for filename, desc in files_to_check.items():
    if os.path.exists(filename):
        print(f"   ✅ OK: {filename}")
    else:
        print(f"   ❌ THIẾU: {filename} ({desc})")
        all_files_ok = False

# 3. KIỂM TRA FOLDER ẢNH (Cho Agent 2)
print("\n3. KIỂM TRA FOLDER ẢNH (Agent 2):")
if os.path.exists("dataset_ecg"):
    print("   ✅ OK: Folder 'dataset_ecg' tồn tại")
    
    # Check folder con
    if os.path.exists("dataset_ecg/Normal") and os.path.exists("dataset_ecg/Abnormal"):
         # Đếm số ảnh
        n_normal = len(os.listdir("dataset_ecg/Normal"))
        n_abnormal = len(os.listdir("dataset_ecg/Abnormal"))
        if n_normal > 0 and n_abnormal > 0:
            print(f"   ✅ OK: Có {n_normal} ảnh Normal và {n_abnormal} ảnh Abnormal.")
        else:
            print("   ❌ LỖI: Folder Normal hoặc Abnormal đang trống (Không có ảnh).")
    else:
        print("   ❌ LỖI: Thiếu folder con 'Normal' hoặc 'Abnormal' bên trong dataset_ecg.")
else:
    print("   ❌ THIẾU: Folder 'dataset_ecg'.")
    all_files_ok = False

print("\n" + "="*40)
if all_libs_ok and all_files_ok:
    print("🎉 MỌI THỨ ĐỀU ỔN! BẠN CÓ THỂ CHẠY BOT NGAY.")
else:
    print("⚠️ HỆ THỐNG CÒN LỖI. HÃY KHẮC PHỤC CÁC DÒNG CÓ DẤU ❌ Ở TRÊN.")
print("="*40 + "\n")