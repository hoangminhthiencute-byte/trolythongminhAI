# 🚀 Hướng Dẫn Cài Đặt Chi Tiết

## Bước 1: Kiểm Tra Python

Đảm bảo bạn có Python 3.10 trở lên:

```bash
python --version
```

Nếu chưa có, tải tại: https://www.python.org/downloads/

---

## Bước 2: Tạo Virtual Environment (Khuyến nghị)

### Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Bước 3: Cài Đặt Thư Viện

```bash
pip install -r requirements.txt
```

**Nếu gặp lỗi, cài từng package:**
```bash
pip install python-telegram-bot==20.7
pip install scikit-learn pandas numpy joblib
pip install opencv-python scikit-image Pillow
pip install requests
```

---

## Bước 4: Tải Dataset

### Dataset 1: Heart Disease (UCI)
1. Truy cập: https://www.kaggle.com/datasets/redwankarimsony/heart-disease-data
2. Tải file `heart_disease_uci.csv`
3. Đặt vào thư mục gốc `bottele/`

### Dataset 2: ECG Images
1. Tạo cấu trúc thư mục:
```
dataset_ecg/
├── Normal/
└── Abnormal/
```

2. Tải ảnh ECG từ các nguồn:
   - https://www.kaggle.com/datasets/shayanfazeli/heartbeat
   - https://physionet.org/content/ptbdb/1.0.0/

3. Phân loại ảnh:
   - Ảnh ECG bình thường → `dataset_ecg/Normal/`
   - Ảnh ECG bất thường → `dataset_ecg/Abnormal/`

**Lưu ý:** Cần ít nhất 50 ảnh mỗi loại để model hoạt động tốt.

---

## Bước 5: Lấy API Keys

### Telegram Bot Token:
1. Mở Telegram, tìm [@BotFather](https://t.me/BotFather)
2. Gửi: `/newbot`
3. Đặt tên bot (VD: "Cyber Heart AI")
4. Đặt username (VD: "cyber_heart_bot")
5. Copy token (dạng: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Groq API Key:
1. Truy cập: https://console.groq.com/
2. Đăng ký tài khoản (miễn phí)
3. Vào "API Keys" → "Create API Key"
4. Copy key (dạng: `gsk_...`)

---

## Bước 6: Cấu Hình Bot

Mở file `bot_main.py`, tìm dòng 19-20:

```python
TELEGRAM_TOKEN = "PASTE_YOUR_TOKEN_HERE"
GROQ_API_KEY = "PASTE_YOUR_GROQ_KEY_HERE"
```

Thay thế bằng keys của bạn.

---

## Bước 7: Chuẩn Bị Banner Image

Đặt file ảnh banner tên `hinhanhdev2.png` vào thư mục gốc.

Hoặc thay đổi tên trong `bot_main.py` (dòng 22):
```python
BANNER_FILENAME = "your_image.png"
```

---

## Bước 8: Huấn Luyện Models

### Option A: Train đầy đủ (Khuyến nghị)

```bash
# Train Agent 3 (Heart Disease)
python train_agent3.py

# Train Agent 2 (ECG Vision)
python train_vision.py
```

**Thời gian:** 1-5 phút tùy dataset

### Option B: Tạo model demo nhanh

```bash
python force_vision.py
```

**Lưu ý:** Model demo chỉ dùng để test, độ chính xác thấp.

---

## Bước 9: Kiểm Tra Hệ Thống

```bash
python check_full.py
```

Kết quả mong đợi:
```
✅ OK: opencv-python
✅ OK: python-telegram-bot
✅ OK: scikit-learn
✅ OK: heart_disease_uci.csv
✅ OK: train_agent3.py
✅ OK: Folder 'dataset_ecg' tồn tại
✅ OK: Có 100 ảnh Normal và 80 ảnh Abnormal.
🎉 MỌI THỨ ĐỀU ỔN! BẠN CÓ THỂ CHẠY BOT NGAY.
```

---

## Bước 10: Chạy Bot

```bash
python bot_main.py
```

Kết quả:
```
--- ⚡ SYSTEM BOOTING: CYBER HEART AI (PREMIUM UI) ---
✅ Local Models: ACTIVE
🚀 BOT READY (PREMIUM DESIGN)
```

---

## Bước 11: Test Bot

1. Mở Telegram
2. Tìm bot của bạn (VD: @cyber_heart_bot)
3. Gửi: `/start`
4. Thử các chức năng:
   - Nhập chỉ số: `55, 1, 130, 220, 150`
   - Upload ảnh ECG
   - Hỏi: "Triệu chứng đau ngực là gì?"

---

## ❗ Xử Lý Lỗi Thường Gặp

### Lỗi 1: ModuleNotFoundError
```bash
pip install <tên_module>
```

### Lỗi 2: FileNotFoundError: heart_disease_uci.csv
- Tải dataset từ Kaggle
- Đảm bảo file nằm đúng thư mục

### Lỗi 3: No models found
```bash
python train_agent3.py
python train_vision.py
```

### Lỗi 4: Telegram API error
- Kiểm tra token
- Kiểm tra kết nối internet

### Lỗi 5: Groq API error
- Kiểm tra API key
- Kiểm tra quota (free tier có giới hạn)

### Lỗi 6: Dataset folder empty
- Thêm ảnh vào `dataset_ecg/Normal/` và `dataset_ecg/Abnormal/`
- Mỗi folder cần ít nhất 10 ảnh

---

## 🎓 Tips

1. **Virtual Environment:** Luôn dùng venv để tránh conflict
2. **Dataset Quality:** Ảnh càng nhiều, model càng chính xác
3. **API Limits:** Groq free tier có giới hạn requests/phút
4. **Model Updates:** Re-train models khi có thêm dữ liệu mới

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Chạy `python check_full.py` để tự động kiểm tra
2. Đọc lỗi trong terminal
3. Google error message
4. Liên hệ tác giả

---

**Chúc bạn thành công! 🎉**