import logging
import joblib
import numpy as np
import cv2
import asyncio
import os
import json
import base64
import io
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from PIL import Image
from skimage.feature import hog 

# ==============================================================================
# ⚙️ CẤU HÌNH HỆ THỐNG
# ==============================================================================
TELEGRAM_TOKEN = "8270857632:AAEYUQIP0yCEtYHxV1MzQNrghL1aOOgK95Y"
GROQ_API_KEY = "NHAP_API_KEY_CUA_BAN_VAO_DAY"

BANNER_FILENAME = "screenshot_1765903579.png" 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ==============================================================================
# 🛠️ GROQ CLIENT
# ==============================================================================
class GroqClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.text_model = "llama-3.3-70b-versatile"
        self.vision_model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def generate(self, prompt, image_pil=None):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        content = [{"type": "text", "text": prompt}]
        model = self.text_model

        if image_pil:
            model = self.vision_model
            buffered = io.BytesIO()
            image_pil.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}})

        payload = {
            "model": model, "messages": [{"role": "user", "content": content}],
            "temperature": 0.6, "max_tokens": 1200
        }
        try:
            res = requests.post(self.url, headers=headers, json=payload, timeout=30)
            if res.status_code == 200: return res.json()['choices'][0]['message']['content']
            return f"Lỗi AI ({res.status_code})"
        except Exception as e: return f"Lỗi mạng: {e}"

# --- KHỞI TẠO ---
print("\n--- ⚡ SYSTEM BOOTING: CYBER HEART AI (PREMIUM UI) ---")
ai_client = GroqClient(GROQ_API_KEY)

try:
    heart_model = joblib.load('heart_model.pkl')
    vision_model = joblib.load('vision_model.pkl')
    print("✅ Local Models: ACTIVE")
except:
    heart_model = None
    vision_model = None
    print("⚠️ Local Models: MISSING")

# ==============================================================================
# 🧠 CORE LOGIC
# ==============================================================================

def agent3_data_process(text_input):
    if not heart_model: return None
    try:
        if "," not in text_input: return None
        data = [float(x.strip()) for x in text_input.split(',')]
        if len(data) != 5: return None
        probs = heart_model.predict_proba([data])[0]
        # Phân tích đẹp hơn
        risk = probs[1] * 100
        analysis = "⚠️ MỨC CẢNH BÁO" if risk > 50 else "✅ MỨC AN TOÀN"
        return {"risk": risk, "data_str": text_input, "analysis": analysis} 
    except: return None

async def agent2_vision_process(image_path):
    img_pil = Image.open(image_path)
    try: check = await asyncio.to_thread(ai_client.generate, "Is this an ECG chart? YES/NO", img_pil)
    except: check = "NO"

    if "YES" in str(check).upper() and vision_model:
        try:
            img_cv = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            h, w = img_cv.shape
            img_cv = img_cv[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
            img_cv = cv2.resize(img_cv, (128, 128))
            features = hog(img_cv, orientations=9, pixels_per_cell=(8, 8),
                           cells_per_block=(2, 2), visualize=False, block_norm='L2-Hys')
            features = features.reshape(1, -1)
            pred = vision_model.predict(features)[0]
            probs = vision_model.predict_proba(features)[0]
            
            conf = probs[pred] * 100
            res = "⚠️ PHÁT HIỆN BẤT THƯỜNG" if pred == 1 else "✅ NHỊP TIM BÌNH THƯỜNG"
            return f"📉 **LOẠI ẢNH:** Điện tâm đồ (ECG)\n🤖 **AI CHẨN ĐOÁN:** {res}\n(Độ tin cậy: {conf:.1f}%)"
        except: pass
    
    res = await asyncio.to_thread(ai_client.generate, "Bạn là Bác sĩ chuyên khoa. Phân tích ảnh này: 1. Tên bệnh. 2. Lời khuyên ngắn.", img_pil)
    return f"🔍 **AI VISION CHẨN ĐOÁN:**\n{res}"

async def agent4_search_process(query):
    return await asyncio.to_thread(ai_client.generate, f"Bạn là bác sĩ tim mạch ân cần. Trả lời bệnh nhân ngắn gọn: {query}")

async def agent5_make_ui_split(vision_res, data_res, user_name):
    is_danger = False
    context_prompt = ""
    
    if data_res:
        if data_res['risk'] > 50: is_danger = True
        context_prompt += f"Chỉ số: {data_res['data_str']}. Nguy cơ: {data_res['risk']:.1f}%."
    if vision_res:
        if "BẤT THƯỜNG" in str(vision_res).upper() or "BỆNH" in str(vision_res).upper(): is_danger = True
        context_prompt += f" Kết quả ảnh: {vision_res}."

    # --- HEADER ĐẸP ---
    if is_danger:
        header = "🚨 CẢNH BÁO SỨC KHỎE 🚨"
        status_line = "Cần sự can thiệp y tế ngay lập tức"
    else:
        header = "🟢 SỨC KHỎE ỔN ĐỊNH 🟢"
        status_line = "Tiếp tục duy trì lối sống lành mạnh"

    # AI Lời khuyên
    advice_prompt = f"Dựa trên hồ sơ: '{context_prompt}'. Viết 3 lời khuyên y tế gạch đầu dòng, ngắn gọn, súc tích."
    advice_text = await asyncio.to_thread(ai_client.generate, advice_prompt)

    # MSG 1: BÁO CÁO (DESIGN CARD STYLE)
    msg1 = f"📋 **PHIẾU KẾT QUẢ CHẨN ĐOÁN**\n"
    msg1 += f"👤 Khách hàng: **{user_name}**\n"
    msg1 += f"📅 Ngày khám: Hôm nay\n"
    msg1 += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    msg1 += f"{header}\n"
    msg1 += f"_{status_line}_\n\n"
    
    if data_res:
        msg1 += f"📊 **PHÂN TÍCH CHỈ SỐ:**\n"
        msg1 += f"▫️ Đánh giá: {data_res['analysis']}\n"
        msg1 += f"▫️ Tỷ lệ rủi ro: `{data_res['risk']:.1f}%`\n\n"
        
    if vision_res:
        msg1 += f"📸 **PHÂN TÍCH HÌNH ẢNH:**\n"
        msg1 += f"{vision_res}\n\n"
        
    msg1 += f"👨‍⚕️ **LỜI KHUYÊN CỦA BÁC SĨ:**\n{advice_text}"

    # MSG 2: THỰC ĐƠN (DESIGN MENU STYLE)
    menu_type = "nghiêm ngặt cho tim mạch" if is_danger else "healthy giữ dáng"
    menu_prompt = f"Viết thực đơn 1 ngày (Sáng, Trưa, Tối) {menu_type}. Dùng icon món ăn. Không giải thích thêm."
    menu_text = await asyncio.to_thread(ai_client.generate, menu_prompt)
    
    msg2 = "🍽 **THỰC ĐƠN DINH DƯỠNG CÁ NHÂN HÓA**\n"
    msg2 += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    msg2 += f"{menu_text}\n\n"
    msg2 += "━━━━━━━━━━━━━━━━━━━━━━\n"
    msg2 += "🤖 *Power by Cyber Heart AI - Dev Hoang Minh Thien*"
    
    return msg1, msg2

# ==============================================================================
# 🎮 HANDLERS (GIAO DIỆN CHUYÊN NGHIỆP)
# ==============================================================================

MAIN_CAPTION = (
    "🏥 **TRỢ LÝ SỨC KHỎE CÁ NHÂN 24/7**\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "👋 Xin chào! Tôi là Bác sĩ AI của bạn.\n\n"
    "Được phát triển bởi **Hoàng Minh Thiện (Đại học Gia Định)**, tôi ở đây để giúp việc chăm sóc sức khỏe trở nên dễ dàng hơn bao giờ hết.\n\n"
    "💎 **DỊCH VỤ CUNG CẤP:**\n"
    "✅ **Chẩn đoán hình ảnh:** Phát hiện sớm bất thường.\n"
    "✅ **Đánh giá sinh tồn:** Phân tích huyết áp, nhịp tim.\n"
    "✅ **Bác sĩ gia đình:** Giải đáp mọi thắc mắc y tế.\n\n"
    "🔻 *Vui lòng chọn dịch vụ bạn cần hỗ trợ:* "
)

MAIN_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("📝 Nhập Chỉ Số (Agent 3)", callback_data='btn_data')],
    [InlineKeyboardButton("📸 Gửi Ảnh Y Tế (Agent 2)", callback_data='btn_vision')],
    [InlineKeyboardButton("💬 Bác Sĩ Ảo (Agent 4)", callback_data='btn_chat')],
    [InlineKeyboardButton("ℹ️ Thông tin Hệ thống", callback_data='btn_info')]
])
BACK_KEYBOARD = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Quay lại Menu Chính", callback_data='main_menu')]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if os.path.exists(BANNER_FILENAME):
            await update.message.reply_photo(photo=open(BANNER_FILENAME, 'rb'), caption=MAIN_CAPTION, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')
        else:
            await update.message.reply_text(MAIN_CAPTION, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi: {e}\n\n{MAIN_CAPTION}", reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'main_menu':
        if query.message.photo:
            await query.edit_message_caption(caption=MAIN_CAPTION, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')
        else:
            await query.message.delete()
            if os.path.exists(BANNER_FILENAME):
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(BANNER_FILENAME, 'rb'), caption=MAIN_CAPTION, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')
            else:
                await context.bot.send_message(chat_id=query.message.chat_id, text=MAIN_CAPTION, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')

    elif query.data == 'btn_data':
        msg = (
            "📝 **NHẬP SỐ LIỆU SINH TỒN**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Hãy nhập 5 chỉ số cách nhau bởi dấu phẩy:\n"
            "`Tuổi, Giới tính, Huyết áp, Cholesterol, Nhịp tim`\n\n"
            "📌 **Ví dụ mẫu:** `55, 1, 130, 220, 150`"
        )
        if query.message.photo:
            await query.edit_message_caption(caption=msg, reply_markup=BACK_KEYBOARD, parse_mode='Markdown')

    elif query.data == 'btn_vision':
        msg = (
            "📸 **PHÂN TÍCH HÌNH ẢNH Y TẾ**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Hệ thống hỗ trợ:\n"
            "🔹 **Điện tâm đồ (ECG):** Phát hiện rung nhĩ, loạn nhịp.\n"
            "🔹 **Da liễu/X-quang:** Chẩn đoán bệnh lý chung.\n\n"
            "👉 *Gửi ảnh trực tiếp vào đây để bắt đầu.*"
        )
        if query.message.photo:
            await query.edit_message_caption(caption=msg, reply_markup=BACK_KEYBOARD, parse_mode='Markdown')

    elif query.data == 'btn_chat':
        msg = (
            "💬 **TRÒ CHUYỆN VỚI BÁC SĨ AI**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Tôi có thể tư vấn về:\n"
            "• Triệu chứng bệnh\n"
            "• Chế độ dinh dưỡng\n"
            "• Lời khuyên tập luyện\n\n"
            "👉 *Hãy gõ câu hỏi của bạn...*"
        )
        if query.message.photo:
            await query.edit_message_caption(caption=msg, reply_markup=BACK_KEYBOARD, parse_mode='Markdown')

    elif query.data == 'btn_info':
        info = (
            "💎 **HỒ SƠ NHÀ PHÁT TRIỂN**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "👤 **Họ tên:** HOÀNG MINH THIỆN\n"
            "🎓 **Đơn vị:** Lớp K17 - Ngành IoT - Đại học Gia Định\n\n"
            "🛠 **CÔNG NGHỆ CỐT LÕI:**\n"
            "• Multi-Agent System (5 Agents)\n"
            "• Computer Vision (HOG + SVM)\n"
            "• Generative AI (Llama 3/4 via Groq)\n\n"
            "© 2025 Cyber Heart Project"
        )
        if query.message.photo:
            await query.edit_message_caption(caption=info, reply_markup=BACK_KEYBOARD, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res_data = agent3_data_process(update.message.text)
    if res_data:
        msg = await update.message.reply_text("⏳ **Đang phân tích dữ liệu chuyên sâu...**", parse_mode='Markdown')
        r1, r2 = await agent5_make_ui_split(None, res_data, update.effective_user.first_name)
        try: await msg.edit_text(r1, parse_mode='Markdown')
        except: await msg.edit_text(r1)
        try: await update.message.reply_text(r2, parse_mode='Markdown', reply_markup=BACK_KEYBOARD)
        except: await update.message.reply_text(r2, reply_markup=BACK_KEYBOARD)
    else:
        await update.message.chat.send_action("typing")
        res = await agent4_search_process(update.message.text)
        try: await update.message.reply_text(f"💬 **Bác sĩ AI:**\n\n{res}", reply_markup=BACK_KEYBOARD, parse_mode='Markdown')
        except: await update.message.reply_text(f"💬 **Bác sĩ AI:**\n\n{res}", reply_markup=BACK_KEYBOARD)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = f"scan_{update.effective_user.id}.jpg"
    msg = await update.message.reply_text("🔍 **Đang quét & phân tích ảnh...**", parse_mode='Markdown')
    try:
        file = await update.message.photo[-1].get_file()
        await file.download_to_drive(path)
        vision_res = await agent2_vision_process(path)
        
        await msg.edit_text("👨‍⚕️ **Đang lập hồ sơ bệnh án chi tiết...**", parse_mode='Markdown')
        r1, r2 = await agent5_make_ui_split(vision_res, None, update.effective_user.first_name)
        
        try: await msg.edit_text(r1, parse_mode='Markdown')
        except: await msg.edit_text(r1)
        
        try: await update.message.reply_text(r2, parse_mode='Markdown', reply_markup=BACK_KEYBOARD)
        except: await update.message.reply_text(r2, reply_markup=BACK_KEYBOARD)
    except Exception as e: await msg.edit_text(f"❌ Lỗi: {e}")
    finally:
        if os.path.exists(path): os.remove(path)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).read_timeout(60).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🚀 BOT READY (PREMIUM DESIGN)")
    app.run_polling()