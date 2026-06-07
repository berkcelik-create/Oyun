import streamlit as st
import json
import os

# Sayfa ayarlarını yapalım (Geniş ekran ve koyu tema uyumu için)
st.set_page_config(page_title="Oyun Hesap Yönetimi", page_icon="🎮", layout="wide")

DATA_FILE = 'accounts.json'

# Verileri yükleme fonksiyonu
def load_accounts():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# Verileri kaydetme fonksiyonu
def save_accounts(accounts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, indent=4, ensure_ascii=False)

# Başlık
st.title("🎮 Oyun Hesap Yönetimi")
st.write("Hesaplarını güvenli bir şekilde sakla ve tek tıkla kod sayfasına git.")

accounts = load_accounts()

# İki sütunlu düzen: Sol tarafta hesap ekleme, sağ tarafta liste
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("➕ Yeni Hesap Ekle")
    with st.form("add_account_form", clear_on_submit=True):
        platform = st.text_input("Platform", placeholder="Örn: Riot Games, Steam")
        username = st.text_input("Kullanıcı Adı / E-posta")
        password = st.text_input("Şifre", type="password") # Şifreyi yazarken gizler
        games = st.text_input("İçindeki Oyunlar", placeholder="Örn: Valorant, LoL")
        code_link = st.text_input("Kod Alınacak Sitenin Linki", placeholder="https://...")
        
        submit_btn = st.form_submit_button("Hesabı Kaydet")
        
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
                save_accounts(accounts)
                st.success("Hesap başarıyla kaydedildi!")
                st.rerun()
            else:
                st.error("Lütfen gerekli alanları doldurun!")

with col2:
    st.subheader("📋 Kayıtlı Hesaplar")
    
    if not accounts:
        st.info("Henüz hiç hesap eklenmemiş.")
    else:
        # Her hesabı şık birer kart (expander) içinde gösterelim
        for idx, acc in enumerate(accounts):
            with st.expander(f"🔑 {acc['platform']} - {acc['username']}"):
                st.write(f"**İçindeki Oyunlar:** {acc['games']}")
                st.write(f"**Kullanıcı Adı:** `{acc['username']}`")
                st.write(f"**Şifre:** `{acc['password']}`")
                
                # Kod sayfasına giden buton
                st.link_button("Koda Git ↗", acc['code_link'], type="primary")
                
                # Hesap Silme Butonu
                if st.button("Bu Hesabı Sil", key=f"del_{idx}"):
                    accounts.pop(idx)
                    save_accounts(accounts)
                    st.success("Hesap silindi!")
                    st.rerun()
