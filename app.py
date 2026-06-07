import streamlit as st
import json
import os

st.set_page_config(
    page_title="Hesaplar",
    page_icon="🎮",
    layout="wide"
)

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
            if content:
                return json.loads(content)
            return empty_db
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

# --- GIRIS VE KAYIT ---
if not st.session_state.logged_in:
    st.title("🎮 Oyun Hesap Sistemi")
    t_login, t_reg = st.tabs(["Giris Yap", "Kayit Ol"])
    
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
                    st.success("Giris basarili!")
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
                    save_all_data(db)
                    st.success("Kayit basarili! Giris yapabilirsiniz.")
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
    if is_admin:
        st.title("🛡️ Admin Panel")
    else:
        st.title(f"🎮 Hos geldin, {st.session_state.username}")

# --- KONTROL AKISI ---
if is_admin:
    t_on, t_bek, t_ek = st.tabs(
        ["Onayli", "Bekleyenler", "➕ Oyun Ekle"]
    )
    
    with t_on:
        if not db["approved_accounts"]:
            st.info("Aktif hesap yok.")
        else:
            for idx, acc in enumerate(db["approved_accounts"]):
                t_str = f"{acc['platform']} - {acc['username']}"
                with st.expander(t_str):
                    st.write(f"**Oyunlar:** {acc['games']}")
                    st.write(f"**Kullanici:** `{acc['username']}`")
                    
                    chk_key = f"ap_sp_{idx}"
                    if st.checkbox("Sifreyi Goster", key=chk_key):
                        st.write(f"**Sifre:** `{acc['password']}`")
                    else:
                        st.write("**Sifre:** `••••••••`")
                        
                    b1, b2 = st.columns([1, 1])
                    with b1:
                        st.link_button(
                            "Koda Git ↗", 
                            acc['code_link'], 
                            use_container_width=True
                        )
                    with b2:
                        del_key = f"ap_del_{idx}"
                        btn_del = st.button(
                            "Sil 🗑️", 
                            key=del_key, 
                            use_container_width=True
                        )
                        if btn_del:
                            db["approved_accounts"].pop(idx)
                            save_all_data(db)
                            safe_rerun()

    with t_bek:
        if not db["pending_accounts"]:
            st.info("Bekleyen istek yok.")
        else:
            for idx, acc in enumerate(db["pending_accounts"]):
                p_str = f"TALEP: {acc['platform']} ({acc['added_by']})"
                with st.expander(p_str):
                    st.write(f"**Oyunlar:** {acc['games']}")
                    st.write(f"**Kullanici:** `{acc['username']}`")
                    st.write(f"**Sifre:** `{acc['password']}`")
                    st.write(f"**Link:** {acc['code_link']}")
                    
                    bo, br = st.columns([1, 1])
                    with bo:
                        ok_key
