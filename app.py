import streamlit as st
import json
import os
from datetime import datetime

# Sayfa Ayarlari
st.set_page_config(
    page_title="Admin - Oyun Hesap Yonetimi", 
    page_icon="🔐", 
    layout="wide"
)

DATA_FILE = 'accounts.json'
LOG_FILE = 'system_logs.json'

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception:
        return []

def save_data(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Hata: {e}")

def add_log(action, status, details=""):
    logs = load_data(LOG_FILE)
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "status": status,
        "details": details
    }
    logs.insert(0, log_entry)
    save_data(LOG_FILE, logs)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

ADMIN_USER = "admin"
ADMIN_PASS = "123456"

# --- GIRIS PANELI ---
if not st.session_state.logged_in:
    st.markdown("<br><h2 style='text-align: center;'>🔐 Giriş Paneli</h2>", unsafe_allow_html=True)
    
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        with st.form("login_form"):
            username = st.text_input("Kullanici Adi", key="l_user")
            password = st.text_input("Sifre", type="password", key="l_pass")
            login_btn = st.form_submit_button("Giris Yap", use_container_width=True)
            
            if login_btn:
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state.logged_in = True
                    add_log("Giris", "BASARILI", f"'{username}' girdi.")
                    st.success("Giris basarili!")
                    safe_rerun()
                else:
                    add_log("Giris", "HATALI", f"'{username}' hatali deneme.")
                    st.error("Hatali kullanici adi veya sifre!")
    st.stop()

# --- ADMIN PANELİ ---
top_col1, top_col2 = st.columns([9, 1])
with top_col2:
    if st.button("Cikis 🚪", use_container_width=True):
        st.session_state.logged_in = False
        add_log("Cikis", "BASARILI", "Oturum kapatildi.")
        safe_rerun()

with top_col1:
    st.title("🛡️ Kontrol Paneli")

tab_accounts, tab_logs = st.tabs(["🎮 Hesaplar", "📋 Loglar"])
accounts = load_data(DATA_FILE)

# --- HESAPLAR ---
with tab_accounts:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("➕ Yeni Hesap Ekle")
        with st.form("add_form", clear_on_submit=True):
            platform = st.text_input("Platform")
            username = st.text_input("Kullanici Adi")
            password = st.text_input("Sifre", type="password")
            games = st.text_input("Oyunlar")
            code_link = st.text_input("Kod Linki")
            
            submit_btn = st.form_submit_button("Kaydet", use_container_width=True)
            
            if submit_btn:
                if platform and username and password and code_link:
                 if platform and username and password and code_link:
                    new_acc = {
                        "platform": platform,
                        "username": username,
                        "password": password,
                        "games": games,
                        "code_link": code_link
                    }
                    accounts.append(new_acc)
                    save_data(DATA_FILE, accounts)
                    add_log("Ekleme", "BASARILI", f"{platform} eklendi.")
                    st.success("Kaydedildi!")
                    safe_rerun()
                else:
                    st.error("Eksik alan birakmayin!")
                 
             
                        "platform": platform,
                        "username": username,
                        "password": password,
                        "games": games,
