import streamlit as st
import json
import os

st.set_page_config(page_title="Hesaplar", page_icon="🎮", layout="wide")
DATA_FILE = 'accounts_v3.json'

def safe_rerun():
    if hasattr(st, "rerun"): st.rerun()
    elif hasattr(st, "experimental_rerun"): st.experimental_rerun()

def load_all_data():
    empty_db = {"users": {"admin": "123456"}, "approved_accounts": [], "pending_accounts": []}
    if not os.path.exists(DATA_FILE): return empty_db
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return json.loads(content) if content else empty_db
    except Exception: return empty_db

def save_all_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e: st.error(f"Hata: {e}")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""

db = load_all_data()

# --- GIRIS / KAYIT ---
if not st.session_state.logged_in:
    st.title("🎮 Oyun Hesap Sistemi")
    t_login, t_reg = st.tabs(["Giris Yap", "Kayit Ol"])
    with t_login:
        with st.form("l_form"):
            u = st.text_input("Kullanici Adi").strip()
            p = st.text_input("Sifre", type="password").strip()
            if st.form_submit_button("Giris", use_container_width=True):
                if u in db["users"] and db["users"][u] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    safe_rerun()
                else: st.error("Hatali bilgi!")
    with t_reg:
        with st.form("r_form"):
            ru = st.text_input("Yeni Kullanici Adi").strip()
            rp = st.text_input("Yeni Sifre", type="password").strip()
            if st.form_submit_button("Kayit Ol", use_container_width=True):
                if not ru or not rp: st.error("Bos birakmayiniz!")
                elif ru in db["users"] or ru.lower() == "admin": st.error("Bu isim yasak!")
                else:
                    db["users"][ru] = rp
                    save_all_data(db)
                    st.success("Kayit basarili!")
    st.stop()

# --- UST PANEL ---
c_t1, c_t2 = st.columns([9, 1])
with c_t2:
    if st.button("Cikis 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        safe_rerun()

is_admin = (st.session_state.username == "admin")
with c_t1:
    st.title("🛡️ Admin Panel" if is_admin else f"🎮 Hos geldin, {st.session_state.username}")

# --- GOVDE ---
if is_admin:
    t_on, t_bek, t_ek = st.tabs(["Onayli Hesaplar", "Onay Bekleyenler", "➕ Doğrudan Oyun Ekle"])
    with t_on:
        if not db["approved_accounts"]: st.info("Aktif hesap yok.")
        for idx, acc in enumerate(db["approved_accounts"]):
            with st.expander(f"{acc['platform']} - {acc['username']}"):
                st.write(f"**Oyunlar:** {acc['games']}")
                if st.checkbox("Sifreyi Goster", key=f"ap_sp_{idx}"): st.write(f"**Sifre:** `{acc['password']}`")
                b1, b2 = st.columns([1, 1])
                with b1: st.link_button("Koda Git ↗", acc['code_link'], use_container_width=True)
                with b2:
                    if st.button("Sil 🗑️", key=f"ap_del_{idx}", use_container_width=True):
                        db["approved_accounts"].pop(idx)
                        save_all_data(db)
                        safe_rerun()
    with t_bek:
        if not db["pending_accounts"]: st.info("Bekleyen istek yok.")
        for idx, acc in enumerate(db["pending_accounts"]):
            with st.expander(f"TALEP: {acc['platform']} ({acc['added_by']})"):
                st.write(f"**Oyunlar:** {acc['games']} | **Sifre:** `{acc['password']}`")
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
    with t_ek:
        with st.form("a_add"):
            ap = st.text_input("Platform")
            au = st.text_input("Kullanici Adi")
            asf = st.text_input("Sifre", type="password")
            ag = st.text_input("Oyunlar")
            al = st.text_input("Kod Linki")
            if st.form_submit_button("Direkt Ekle", use_container_width=True):
                if ap and au and asf and al:
                    db["approved_accounts"].append({"platform": ap, "username": au, "password": asf, "games": ag, "code_link": al, "added_by": "admin"})
                    save_all_data(db)
                    safe_rerun()
else:
    # NORMAL UYE EKRANI (Alt alta net gorunum)
    st.markdown("### ➕ Oyun Hesabi Oner / Ekle")
    with st.form("u_add_form", clear_on_submit=True):
        plat = st.text_input("Platform (Oren: Steam)")
        user = st.text_input("Kullanici Adi / E-posta")
        pas = st.text_input("Sifre", type="password")
        gms = st.text_input("Oyunlar")
        lnk = st.text_input("Kod Linki")
        if st.form_submit_button("Onaya Gonder", use_container_width=True):
            if plat and user and pas and lnk:
                db["pending_accounts"].append({"platform": plat, "username": user, "password": pas, "games": gms, "code_link": lnk, "added_by": st.session_state.username})
                save_all_data(db)
                st.success("Onaya gonderildi!")
                safe_rerun()
            else: st.error("Eksik alan birakmayiniz!")

    st.markdown("---")
    st.markdown("### 📋 Aktif Oyun Hesaplari")
    if not db["approved_accounts"]: st.info("Aktif hesap bulunmuyor.")
    for idx, acc in enumerate(db["approved_accounts"]):
        with st.expander(f"🎮 {acc['platform']} - ({acc['games']})"):
            st.write(f"**Kullanici Adi:** `{acc['username']}`")
            st.link_button("Koda Git ↗", acc['code_link'], type="primary")
