import streamlit as st
import json
import os
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Admin - Oyun Hesap Yönetimi", page_icon="🔐", layout="wide")

# Sabit Dosya Yolları
DATA_FILE = 'accounts.json'
LOG_FILE = 'system_logs.json'

# --- YENİDEN YÜKLEME (RERUN) UYUMLULUK FONKSİYONU ---
def safe_rerun():
    """Her Streamlit sürümünde hatasız çalışacak rerun fonksiyonu"""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# --- VERİ TABANI (JSON) FONKSİYONLARI ---
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
        st.error(f"Veri kaydedilirken hata oluştu: {e}")

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

# --- OTURUM YÖNETİMİ ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Giriş Bilgileri
ADMIN_USER = "admin"
ADMIN_PASS = "123456"

# --- 1. GİRİŞ PANELİ ---
if not st.session_state.logged_in:
    st.markdown("<br><h2 style='text-align: center;'>🔐 Oyun Hesap Yönetimi - Giriş Paneli</h2>", unsafe_allow_html=True)
    
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        with st.form("login_form"):
            username = st.text_input("Kullanıcı Adı", key="login_username")
            password = st.text_input("Şifre", type="password", key="login_password")
            login_btn = st.form_submit_button("Giriş Yap", use_container_width=True)
            
            if login_btn:
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state.logged_in = True
                    add_log("Kullanıcı Girişi", "BAŞARILI", f"'{username}' giriş yaptı.")
                    st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                    safe_rerun()
                else:
                    add_log("Kullanıcı Girişi", "HATALI", f"'{username}' ile hatalı deneme.")
                    st.error("Hatalı kullanıcı adı veya şifre!")
    st.stop()

# --- 2. ADMIN PANELİ (Giriş Yapılınca Çalışacak Kısım) ---

# Çıkış Butonu
top_col1, top_col2 = st.columns([9, 1])
with top_col2:
    if st.button("Çıkış Yap 🚪", use_container_width=True):
        st.session_state.logged_in = False
        add_log("Kullanıcı Çıkışı", "BAŞARILI", "Oturum kapatıldı.")
        safe_rerun()

with top_col1:
    st.title("🛡️ Admin Kontrol Paneli")

tab_accounts, tab_logs = st.tabs(["🎮 Hesap Yönetimi", "📋 Sistem Logları"])
accounts = load_data(DATA_FILE)

# --- HESAP YÖNETİMİ SEKME ---
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
            
            submit_btn = st.form_submit_button("Hesabı Kaydet", use_container_width=True)
            
            if submit_btn:
                if platform and username and password and code_link:
                    new_account = {
                        "platform": platform,
                        "username": username,
                        "password": password,
                        "games": games,
                        "code_link": code_link
                    }
                    accounts.append(new_account)
                    save_data(DATA_FILE, accounts)
                    add_log("Hesap Ekleme", "BAŞARILI", f"{platform} - '{username}' eklendi.")
                    st.success("Hesap başarıyla kaydedildi!")
                    safe_rerun()
                else:
                    st.error("Lütfen tüm alanları doldurun!")

    with col2:
        st.subheader("📋 Kayıtlı Hesaplar")
        if not accounts:
            st.info("Henüz hiç hesap eklenmemiş.")
        else:
            for idx, acc in enumerate(accounts):
                with st.expander(f"🔑 {acc['platform']} - {acc['username']}"):
                    st.write(f"**Oyunlar:** {acc['games']}")
                    st.write(f"**Kullanıcı Adı:** `{acc['username']}`")
                    
                    # Şifre Göster/Gizle mekanizması
                    show_pass = st.checkbox("Şifreyi Göster
                
