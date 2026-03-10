# 🏥 Cyber Heart AI - Trợ Lý Sức Khỏe Telegram Bot

**Dự án:** Hệ thống Multi-Agent AI cho chẩn đoán sức khỏe tim mạch  
**Tác giả:** Hoàng Minh Thiện  
**Đơn vị:** Lớp K17 - Ngành IoT - Đại học Gia Định  
**Năm:** 2025

---

## 📋 Mô Tả Dự Án

Cyber Heart AI là một chatbot Telegram thông minh sử dụng 5 agents AI để:
- 🔍 Phân tích điện tâm đồ (ECG) qua hình ảnh
- 📊 Đánh giá nguy cơ bệnh tim dựa trên chỉ số sinh tồn
- 💬 Tư vấn y tế thông qua Generative AI (Llama 3.3/4)
- 🍽️ Đề xuất thực đơn dinh dưỡng cá nhân hóa

---

## 🛠️ Công Nghệ Sử Dụng

### Core Technologies
- **Python 3.10+**
- **Telegram Bot API** (python-telegram-bot)
- **Groq API** (Llama 3.3 70B + Llama 4 Scout 17B)

### Machine Learning
- **scikit-learn** - Logistic Regression & SVM
- **Computer Vision** - OpenCV + HOG Feature Extraction
- **Data Processing** - Pandas, NumPy

### Models
- **Agent 2 (Vision):** SVM với HOG features cho phân loại ECG
- **Agent 3 (Data):** Logistic Regression cho dự đoán bệnh tim

---

## 📦 Cài Đặt

### 1. Clone Repository
```bash
git clone <repository-url>
cd bottele
```

### 2. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 3. Chuẩn Bị Dữ Liệu

#### Dataset Tim Mạch (Agent 3)
- Tải file `heart_disease_uci.csv` từ [Kaggle UCI Heart Disease](https://www.kaggle.com/datasets/redwankarimsony/heart-disease-data)
- Đặt vào thư mục gốc

#### Dataset ECG (Agent 2)
```
dataset_ecg/
├── Normal/       # Ảnh ECG bình thường
└── Abnormal/     # Ảnh ECG bất thường
```

### 4. Huấn Luyện Models

```bash
# Huấn luyện Agent 3 (Heart Disease Prediction)
python train_agent3.py

# Huấn luyện Agent 2 (ECG Vision)
python train_vision.py
```

Hoặc tạo model demo nhanh:
```bash
python force_vision.py
```

### 5. Cấu Hình Bot

Mở `bot_main.py` và cập nhật:
```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

### 6. Chạy Bot

```bash
python bot_main.py
```

---

## 🎯 Cách Sử Dụng

### Trên Telegram:

1. **Bắt đầu:** `/start`
2. **Chọn chức năng:**
   - 📝 **Nhập Chỉ Số:** Nhập 5 giá trị (tuổi, giới tính, huyết áp, cholesterol, nhịp tim)
     - Ví dụ: `55, 1, 130, 220, 150`
   - 📸 **Gửi Ảnh Y Tế:** Upload ảnh ECG hoặc X-quang
   - 💬 **Bác Sĩ Ảo:** Hỏi bất kỳ câu hỏi y tế nào

---

## 🧪 Kiểm Tra Hệ Thống

Chạy script kiểm tra tự động:
```bash
python check_full.py
```

Script này sẽ kiểm tra:
- ✅ Thư viện đã cài đặt
- ✅ Files cần thiết
- ✅ Dataset structure
- ✅ Models đã train

---

## 📁 Cấu Trúc Dự Án

```
bottele/
├── bot_main.py              # Main bot application
├── train_agent3.py          # Train heart disease model
├── train_vision.py          # Train ECG vision model
├── force_vision.py          # Create dummy vision model
├── check_full.py            # System validation script
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── heart_disease_uci.csv   # Heart disease dataset
├── hinhanhdev2.png         # Bot banner image
├── heart_model.pkl         # Trained heart model (generated)
├── vision_model.pkl        # Trained vision model (generated)
└── dataset_ecg/            # ECG image dataset
    ├── Normal/
    └── Abnormal/
```

---

## 🔧 Troubleshooting

### Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### Lỗi: No models found
```bash
python train_agent3.py
python train_vision.py
```

### Lỗi: Telegram token invalid
- Kiểm tra token tại [@BotFather](https://t.me/BotFather)
- Cập nhật `TELEGRAM_TOKEN` trong `bot_main.py`

### Lỗi: Groq API
- Đăng ký tại [Groq Console](https://console.groq.com/)
- Cập nhật `GROQ_API_KEY` trong `bot_main.py`

---

## 📊 Hiệu Suất Models

### Agent 3 (Heart Disease)
- **Model:** Logistic Regression
- **Features:** age, sex, trestbps, chol, thalch
- **Accuracy:** ~85-90% (tùy dataset)

### Agent 2 (ECG Vision)
- **Model:** SVM (Linear Kernel)
- **Features:** HOG (Histogram of Oriented Gradients)
- **Classes:** Normal / Abnormal
- **Accuracy:** ~80-85% (tùy dataset)

---

## 🚀 Tính Năng Nổi Bật

1. **Multi-Agent Architecture**
   - Agent 1: Orchestrator
   - Agent 2: Vision Analysis
   - Agent 3: Data Analysis
   - Agent 4: Medical Q&A
   - Agent 5: UI Generation

2. **AI-Powered**
   - Groq API với Llama 3.3 70B (text)
   - Llama 4 Scout 17B (vision)
   - Local ML models (offline capability)

3. **User-Friendly UI**
   - Inline keyboards
   - Rich markdown formatting
   - Progress indicators
   - Professional medical reports

---

## 📝 License

Dự án học tập - Đại học Gia Định © 2025

---

## 👨‍💻 Liên Hệ

**Hoàng Minh Thiện**  
Sinh viên K17 - IoT  
Đại học Gia Định

---

## 🙏 Credits

- **Telegram Bot API:** python-telegram-bot
- **Groq AI:** Llama models
- **UCI Heart Disease Dataset:** Kaggle
- **ECG Dataset:** Public medical datasets