import streamlit as st
import json
import os
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Admin - Oyun Hesap Yönetimi", page_icon="🔐", layout="wide")

# Sabit Dosya Yolları
DATA_FILE = 'accounts.json'
LOG_FILE = 'system_logs.json'

# --- YARDIMCI FONKSİYONLAR ---
def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_log(action, status, details=""):
    logs = load_data(LOG_FILE)
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "status": status,
        "details": details
    }
    logs.insert(0, log_entry)  # En yeni logu en üste ekle
    save_data(LOG_FILE, logs)

# --- OTURUM KONTROLÜ (Giriş Paneli) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Belirlemek istediğin Admin Giriş Bilgileri
# NOT: GitHub'a yükleyeceksen bu şifreyi kimseyle paylaşma!
ADMIN_USER = "admin"
ADMIN_PASS = "123456" # Burayı dilediğin gibi değiştir

if not st.session_state.logged_in:
    # Giriş Ekranı Arayüzü
    st.markdown("<h2 style='text-align: center;'>🔐 Oyun Hesap Yönetimi - Giriş Paneli</h2>", unsafe_allow_html=True)
    
    col_space1, col_login, col_space2 = st.columns([1, 1, 1])
    with col_login:
        with st.form("login_form"):
            username = st.text_input("Kullanıcı Adı")
            password = st.text_input("Şifre", type="password")
            login_btn = st.form_submit_button("Giriş Yap", use_container_width=True)
            
            if login_btn:
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state.logged_in = True
                    add_log("Kullanıcı Girişi", "BAŞARILI", f"'{username}' başarıyla giriş yaptı.")
                    st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                    st.rerun()
                else:
                    add_log("Kullanıcı Girişi", "HATALI", f"'{username}' kullanıcı adı ile hatalı deneme yapıldı.")
                    st.error("Hatalı kullanıcı adı veya şifre!")
    st.stop() # Kullanıcı giriş yapmadıysa sayfanın geri kalanını yükleme

# --- ADMIN PANELİ (Giriş Yapıldıktan Sonra) ---

# Çıkış Butonu (Sağ Üst Köşe)
top_col1, top_col2 = st.columns([9, 1])
with top_col2:
    if st.button("Çıkış Yap 🚪", use_container_width=True):
        st.session_state.logged_in = False
        add_log("Kullanıcı Çıkışı", "BAŞARILI", "Oturum sonlandırıldı.")
        st.rerun()

with top_col1:
    st.title("🛡️ Admin Kontrol Paneli")

# Sekmeli Menü Yapısı (Hesaplar ve Loglar için)
tab_accounts, tab_logs = st.tabs(["🎮 Hesap Yönetimi", "📋 Sistem Logları"])

accounts = load_data(DATA_FILE)

# --- 1. SEKME: HESAP YÖNETİMİ ---
with tab_accounts:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("➕ Yeni Hesap Ekle")
        with st.form("add_account_form", clear_on_submit=True):
            platform = st.text_input("Platform", placeholder="Örn: Riot Games, Steam")
            username = st.text_input("Hesap Kullanıcı Adı / E-posta")
            password = st.text_input("Şifre", type="password")
            games = st.text_input("İçindeki Oyunlar", placeholder="Örn: Valorant, LoL")
            code_link = st.text_input("Kod Alınacak Sitenin Linki", placeholder="https://...")
            
            submit_btn = st.form_submit_button("Hes
