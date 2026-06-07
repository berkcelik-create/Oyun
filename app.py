import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Oyun Hesap Yonetimi", page_icon="🎮", layout="wide")

DATA_FILE = 'accounts_v2.json'

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def load_all_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {"admin": "123456"}, "approved_accounts": [], "pending_accounts": []}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {"users": {"admin": "123456"}, "approved_accounts": [], "pending_accounts": []}
            return json.loads(content)
    except Exception:
        return {"users": {"admin": "123456"}, "approved_accounts": [], "pending_accounts": []}

def save_all_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Veri kayit hatasi: {e}")

# Oturum Durumlari
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

db = load_all_data()

# --- GIRIS VE KAYIT PANELI ---
if not st.session_state.logged_in:
    st.markdown("<br><h2 style='text-align: center;'>🔐 Oyun Hesap Yönetimi</h2>", unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["🚪 Giriş Yap", "📝 Kayıt Ol"])
    
    with tab_login:
        _, col_l, _ = st.columns([1, 1, 1])
        with col_l:
            with st.form("login_form"):
                l_user = st.text_input("Kullanıcı Adı").strip()
                l_pass = st.text_input("Şifre", type="password").strip()
                if st.form_submit_button("Giriş Yap", use_container_width=True):
                    if l_user in db["users"] and db["users"][l_user] == l_pass:
                        st.session_state.logged_in = True
                        st.session_state.username = l_user
                        st.success("Giriş başarılı!")
                        safe_rerun()
                    else:
                        st.error("Hatalı kullanıcı adı veya şifre!")
                        
    with tab_register:
        _, col_r, _ = st.columns([1, 1, 1])
        with col_r:
            with st.form("register_form"):
                r_user = st.text_input("Yeni Kullanıcı Adı").strip()
                r_pass = st.text_input("Yeni Şifre", type="password").strip()
                if st.form_submit_button("Hesap Oluştur", use_container_width=True):
                    if not r_user or not r_pass:
                        st.error("Alanlar boş bırakılamaz!")
                    elif r_user in db["users"]:
                        st.error("Bu kullanıcı adı zaten alınmış!")
                    elif r_user.lower() == "admin":
                        st.error("Bu kullanıcı adı yasaktır!")
                    else:
                        db["users"][r_user] = r_pass
                        save_all_data(db)
                        st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
    st.stop()

# --- ORTAK ÜST PANEL ---
top_col1, top_col2 = st.columns([9, 1])
with top_col2:
    if st.button("Çıkış 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        safe_rerun()

is_admin = (st.session_state.username == "admin")

with top_col1:
    if is_admin:
        st.title("🛡️ Yönetici Kontrol Paneli")
    else:
        st.title(f"🎮 Hoş geldin, {st.session_state.username}")

# --- ARAYÜZ GÖRÜNÜMLERİ ---
if is_admin:
    # --- ADMIN GÖRÜNÜMÜ ---
    tab_manage, tab_pending = st.tabs(["📋 Onaylı Hesaplar", "⏳ Onay Bekleyen Talepler"])
    
    with tab_manage:
        if not db
