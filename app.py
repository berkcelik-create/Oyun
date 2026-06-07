import streamlit as st
import json
import os

st.set_page_config(
    page_title="Oyunlar",
    page_icon="🎮",
    layout="wide"
)

DATA_FILE = 'games_v2.json'

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def load_data():
    empty_db = {
        "users": {
            "admin": "123456"
        },
        "games": []
    }
    if not os.path.exists(DATA_FILE):
        return empty_db
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            return empty_db
    except Exception:
        return empty_db

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(
                data, 
                f, 
                indent=4, 
                ensure_ascii=False
            )
    except Exception as e:
        st.error(f"Hata: {e}")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

db = load_data()

# --- GIRIS VE KAYIT ---
if not st.session_state.logged_in:
    st.title("🎮 Oyun Oneri Platformu")
    t_login, t_reg = st.tabs(
        ["Giris Yap", "Kayit Ol"]
    )
    
    with t_login:
        with st.form("l_form"):
            u = st.text_input("Kullanici Adi").strip()
            p = st.text_input("Sifre", type="password").strip()
            btn_l = st.form_submit_button(
                "Giris", 
                use_container_width=True
            )
            if btn_l:
                if u in db["users"] and db["users"][u] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    safe_rerun()
                else:
                    st.error("Hatali bilgi!")
                    
    with t_reg:
        with st.form("r_form"):
            ru = st.text_input("Yeni Kullanici Adi").strip()
            rp = st.text_input("Yeni Sifre", type="password").strip()
            btn_r = st.form_submit_button(
                "Kayit Ol", 
                use_container_width=True
            )
            if btn_r:
                if not ru or not rp:
                    st.error("Bos birakmayiniz!")
                elif ru in db["users"] or ru.lower() == "admin":
                    st.error("Bu isim yasak veya alinmis!")
                else:
                    db["users"][ru] = rp
                    save_data(db)
                    st.success("Kayit basarili!")
    st.stop()

# --- UST PANEL ---
c_t1, c_t2 = st.columns([9, 1])
with c_t2:
    btn_out = st.button(
        "Cikis 🚪", 
        use_container_width=True
    )
    if btn_out:
        st.session_state.logged_in = False
        st.session_state.username = ""
        safe_rerun()

is_admin = (st.session_state.username == "admin")
with c_t1:
    st.title(f"🎮 Hos geldin, {st.session_state.username}")

# --- ANA GOVDE ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("➕ Yeni Oyun Oner")
    with st.form("add_game_form", clear_on_submit=True):
        g_name = st.text_input("Oyun Adi")
