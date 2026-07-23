import streamlit as st
import os
import json
from datetime import datetime

DATA_DIR = "stored_prompts"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)
CATEGORIES = ["政治", "生活", "社會", "地方", "國際", "娛樂", "高雄", "台中"]

def load_data():
    json_path = os.path.join(DATA_DIR, "data.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    json_path = os.path.join(DATA_DIR, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="新聞部 AI 提示詞圖書館", layout="wide")
st.title("📸 新聞部 AI 提示詞圖書館")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📤 分享我的得意之作")
    author = st.text_input("您的名字 / 職稱", placeholder="例如：政治線記者 小明")
    category = st.selectbox("選擇新聞組別", CATEGORIES)
    prompt_input = st.text_area("您使用的 AI 提示詞")
    uploaded_file = st.file_uploader("上傳您生成的圖片或影片", type=["jpg", "png", "jpeg", "mp4"])

    if st.button("🚀 發布到圖書館", use_container_width=True):
        if not author or not prompt_input or not uploaded_file:
            st.error("❌ 請填寫所有欄位並上傳檔案喔！")
        else:
            file_ext = os.path.splitext(uploaded_file.name)[1]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(IMAGE_DIR, f"{timestamp}{file_ext}")
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            current_data = load_data()
            current_data.insert(0, {
                "author": author, "category": category, "prompt": prompt_input,
                "file_path": file_path, "file_type": "video" if file_ext.lower() == ".mp4" else "image",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_data(current_data)
            st.success(f"🎉 分享成功！已歸類至【{category}】組！")
            st.balloons()

with col2:
    st.header("✨ 大家的作品與提示詞")
    selected_tab = st.radio("🔍 篩選組別：", ["全部"] + CATEGORIES, horizontal=True)
    posts = load_data()
    filtered_posts = [p for p in posts if p.get("category") == selected_tab] if selected_tab != "全部" else posts
    st.divider()

    if not filtered_posts:
        st.info("💡 目前還沒有人分享作品，快上傳第一個作品吧！")
    else:
        for post in filtered_posts:
            with st.container():
                st.markdown(f"🏷️ **【{post.get('category', '未分類')}】** ｜ 👤 {post['author']} ｜ 📅 {post['time']}")
                if post["file_type"] == "video":
                    st.video(post["file_path"])
                else:
                    st.image(post["file_path"], use_container_width=True)
                st.write("📝 **使用的提示詞（點擊右上方可複製）：**")
                st.code(post["prompt"], language="text")
                st.divider()
