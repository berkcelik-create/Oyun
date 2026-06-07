import streamlit as st
import json
import os

st.set_page_config(page_title="Hesaplar", page_icon="🎮", layout="wide")

DATA_FILE = 'accounts_v3.json'

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def load_all_data():
    empty_db = {
        "users": {"admin": "123456"},
        "approved_accounts": [],
        "pending_accounts": []
    }
    if not os.path.exists(DATA_FILE):
        return empty_db
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return json.loads(content) if content else empty_db
    except Exception:
        return empty_db

def save_all_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Hata: {e}")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

db = load_all_data()

# --- GİRİŞ VE KAYIT EKRANI ---
if not st.session_state.logged_in:
    st.title("🎮 Oyun Hesap Sistemi")
    t_login, t_reg = st.tabs(["Giriş Yap", "Kayıt Ol"])
    
    with t_login:
        with st.form("l_form"):
            u = st.text_input("Kullanıcı Adı").strip()
            p = st.text_input("Şifre", type="password").strip()
            if st.form_submit_button("Giriş", use_container_width=True):
                if u in db["users"] and db["users"][u] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.success("Giriş başarılı!")
                    safe_rerun()
                else:
                    st.error("Hatalı kullanıcı adı veya şifre!")
                    
    with t_reg:
        with st.form("r_form"):
            ru = st.text_input("Yeni Kullanıcı Adı").strip()
            rp = st.text_input("Yeni Şifre", type="password").strip()
            if st.form_submit_button("Kayıt Ol", use_container_width=True):
                if not ru or not rp:
                    st.error("Boş bırakmayınız!")
                elif ru in db["users"] or ru.lower() == "admin":
                    st.error("Bu isim yasak veya zaten alınmış!")
                else:
                    db["users"][ru] = rp
                    save_all_data(db)
                    st.success("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
    st.stop()

# --- ÜST PANEL (ÇIKIŞ BUTONU) ---
c_t1, c_t2 = st.columns([9, 1])
with c_t2:
    if st.button("Çıkış 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        safe_rerun()

is_admin = (st.session_state.username == "admin")
with c_t1:
    if is_admin:
        st.title("🛡️ Admin Panel")
    else:
        st.title(f"🎮 Hoş geldin, {st.session_state.username}")

# --- KONTROL AKIŞI (YÖNETİCİ VS ÜYE) ---
if is_admin:
    # --- ADMIN GÖRÜNÜMÜ ---
    t_onayli, t_bekleyen, t_admin_ekle = st.tabs(["Onaylı Hesaplar", "Onay Bekleyenler", "➕ Doğrudan Oyun Ekle"])
    
    with t_onayli:
        if not db["approved_accounts"]:
            st.info("Sistemde aktif hesap yok.")
        else:
            for idx, acc in enumerate(db["approved_accounts"]):
                with st.expander(f"{acc['platform']} - {acc['username']}"):
                    st.write(f"**Oyunlar:** {acc['games']}")
                    st.write(f"**Kullanıcı:** `{acc['username']}`")
                    if st.checkbox("Şifreyi Göster", key=f"ap_sp_{idx}"):
                        st.write(f"**Şifre:** `{acc['password']}`")
                    else:
                        st.write("**Şifre:** `••••••••`")
                    st.markdown("<br>", unsafe_allow_html=True)
                    b1, b2 = st.columns([1, 1])
                    with b1:
                        st.link_button("Koda Git ↗", acc['code_link'], use_container_width=True)
                    with b2:
                        if st.button("Sil 🗑️", key=f"ap_del_{idx}", use_container_width=True):
                            db["approved_accounts"].pop(idx)
                            save_all_data(db)
                            safe_rerun()

    with t_bekleyen:
        if not db["pending_accounts"]:
            st.info("Onay bekleyen istek yok.")
        else:
            for idx, acc in enumerate(db["pending_accounts"]):
                with st.expander(f"TALEP: {acc['platform']} ({acc['added_by']})"):
                    st.write(f"**Oyunlar:** {acc['games']}")
                    st.write(f"**Kullanıcı:** `{acc['username']}`")
                    st.write(f"**Şifre:** `{acc['password']}`")
                    st.write(f"**Link:** {acc['code_link']}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    bo, br = st.columns([1, 1])
                    with bo:
                        if st.button("Onayla 🟢", key=f"ok_{idx}", use_container_width=True):
                            item = db["pending_accounts"].pop(idx)
                            db["approved_accounts"].append(item)
                            save_all_data(db)
                            safe_rerun()
                    with br:
                        if st.button("Reddet 🔴", key=f"no_{idx}", use_container_width=True):
                            db["pending_accounts"].pop(idx)
                            save_all_data(db)
                            safe_rerun()

    with t_admin_ekle:
        st.subheader("🛠️ Onay Gerektirmeden Hesap Ekle")
        with st.form("admin_add_form", clear_on_submit=True):
            a_plat = st.text_input("Platform")
            a_user = st.text_input("Kullanıcı Adı / E-posta")
            a_pas = st.text_input("
