import streamlit as st
import json
import os
from datetime import datetime

# Sayfa Ayarlari
st.set_page_config(
    page_title="Oyun Hesap Yonetimi", 
    page_icon="🎮", 
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

# Oturum Durumlari
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Sabit Giris Bilgileri
ADMIN_USER = "admin"
ADMIN_PASS = "123456"

USER_USER = "uye"
USER_PASS = "123"

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
                    st.session_state.is_admin = True
                    add_log("Giris", "BASARILI", "Admin girisi yapti.")
                    st.success("Admin olarak giris yapildi!")
                    safe_rerun()
                elif username == USER_USER and password == USER_PASS:
                    st.session_state.logged_in = True
                    st.session_state.is_admin = False
                    add_log("Giris", "BASARILI", "Normal kullanici girisi yapti.")
                    st.success("Kullanici olarak giris yapildi!")
                    safe_rerun()
                else:
                    add_log("Giris", "HATALI", f"'{username}' ile hatali deneme.")
                    st.error("Hatali kullanici adi veya sifre!")
    st.stop()

# --- ORTAK UST PANEL (Cikis Butonu) ---
top_col1, top_col2 = st.columns([9, 1])
with top_col2:
    if st.button("Cikis 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        add_log("Cikis", "BASARILI", "Oturum kapatildi.")
        safe_rerun()

with top_col1:
    if st.session_state.is_admin:
        st.title("🛡️ Admin Kontrol Paneli")
    else:
        st.title("🎮 Kayitli Oyun Hesaplari")

accounts = load_data(DATA_FILE)

# --- PANEL GORUNUMLERI ---
if st.session_state.is_admin:
    # --- ADMIN SEKMELI GORUNUM ---
    tab_accounts, tab_logs = st.tabs(["🎮 Hesaplar", "📋 Loglar"])
    
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

        with col2:
            st.subheader("📋 Kayitli Hesaplar (Admin Gorunumu)")
            if not accounts:
                st.info("Henuz hesap yok.")
            else:
                for idx, acc in enumerate(accounts):
                    with st.expander(f"🔑 {acc['platform']} - {acc['username']}"):
                        st.write(f"**Oyunlar:** {acc['games']}")
                        st.write(f"**Kullanici:** `{acc['username']}`")
                        
                        show_pass = st.checkbox("Sifreyi Goster", key=f"sp_{idx}")
                        if show_pass:
                            st.write(f"**Sifre:** `{acc['password']}`")
                        else:
                            st.write("**Sifre:** `••••••••`")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        btn_col1, btn_col2 = st.columns([1, 1])
                        with btn_col1:
                            st.link_button("Koda Git ↗", acc['code_link'], type="primary", use_container_width=True)
                        with btn_col2:
                            if st.button("Sil 🗑️", key=f"del_{idx}", use_container_width=True):
                                accounts.pop(idx)
                                save_data(DATA_FILE, accounts)
                                add_log("Silme", "BASARILI", f"{acc['platform']} silindi.")
                                st.success("Silindi!")
                                safe_rerun()

    with tab_logs:
        st.subheader("🚨 Sistem Hareketleri")
        logs = load_data(LOG_FILE)
        if st.button("Temizle 🧼"):
            save_data(LOG_FILE, [])
            add_log("Temizleme", "BASARILI", "Loglar sifirlandi.")
            st.success("Temizlendi!")
            safe_rerun()
            
        st.markdown("---")
        if not logs:
            st.info("Log yok.")
        else:
            for log in logs:
                color = "🟢" if log.get('status') == "BASARILI" else "🔴"
                st.markdown(f"**{log.get('timestamp')}** | {color} **[{log.get('action')}]** - {log.get('details')}")

else:
    # --- NORMAL KULLANICI GORUNUMU ---
    st.subheader("📋 Kullanima Hazir Hesaplar")
    st.write("Hesap bilgilerini inceleyebilir ve 'Koda Git' butonu ile giris kodunuzu alabilirsiniz.")
    st.markdown("---")
    
    if not accounts:
        st.info("Sistemde su an gosterilecek hesap bulunmuyor.")
    else:
        # Normal kullanicilar icin yan yana kartlar halinde şık bir listeleme yapalim
        for idx, acc in enumerate(accounts):
            with st.expander(f"🎮 {acc['platform']} - ({acc['games']})"):
                st.
