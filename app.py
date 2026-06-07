import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Oyun Hesaplari", page_icon="🎮", layout="wide")

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
            return json.loads(content) if content else []
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
    logs.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "status": status,
        "details": details
    })
    save_data(LOG_FILE, logs)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Giriş Bilgileri
ADMIN_USER, ADMIN_PASS = "admin", "123456"
USER_USER, USER_PASS = "uye", "123"

# --- GIRIS PANELI ---
if not st.session_state.logged_in:
    st.markdown("<br><h2 style='text-align: center;'>🔐 Giriş Paneli</h2>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        with st.form("login_form"):
            username = st.text_input("Kullanici Adi")
            password = st.text_input("Sifre", type="password")
            if st.form_submit_button("Giris Yap", use_container_width=True):
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    add_log("Giris", "BASARILI", "Admin girdi.")
                    safe_rerun()
                elif username == USER_USER and password == USER_PASS:
                    st.session_state.logged_in = True
                    st.session_state.is_admin = False
                    add_log("Giris", "BASARILI", "Uye girdi.")
                    safe_rerun()
                else:
                    st.error("Hatali kullanici adi veya sifre!")
    st.stop()

# --- PANEL BAŞLIĞI VE ÇIKIŞ ---
top_col1, top_col2 = st.columns([9, 1])
with top_col2:
    if st.button("Cikis 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        safe_rerun()

with top_col1:
    st.title("🛡️ Admin Paneli" if st.session_state.is_admin else "🎮 Oyun Hesaplari")

accounts = load_data(DATA_FILE)

# --- PANEL GORUNUMLERI ---
if st.session_state.is_admin:
    tab_accounts, tab_logs = st.tabs(["🎮 Hesaplar", "📋 Loglar"])
    
    with tab_accounts:
        col
