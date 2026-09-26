import streamlit as st
import urllib.parse

# ⚠️ ÎNLOCUIEȘTE AICI cu link-ul tău real generat din contul tău Stripe:
# (Mergi în Stripe -> Payment Links -> Creează un link de abonament lunar și lipește-l în loc la cel de jos)

LINK_PLATA_STRIPE = "https//stripe.com
# 1. Configurare servicii salvate în sesiune
if "servicii_salon" not in st.session_state:
    st.session_state.servicii_salon = {
        "Vopsit": 150,
        "Tunsoare Bărbați": 50,
        "Coafat": 80
    }

if "agenda_salariati" not in st.session_state:
    st.session_state.agenda_salariati = [
        {"id": 1, "ora": "09:00", "client": "Maria Georgescu", "telefon": "40712345678", "serviciu": "Vopsit"}
    ]

st.title("💇‍♀️ Beauty-IA: Agenda ta Inteligentă Pro")
st.subheader("📋 Carnetul tău Digital de Programări")

# --- VERIFICARE LIMITĂ PLATĂ (Maxim 3 programări în varianta gratuită) ---
numar_programari = len(st.session_state.agenda_salariati)

if numar_programari >= 3:
    # Blocăm complet interfața dacă s-a atins limita de 3 programări
    st.error("⚠️ Limita versiunii demo a fost atinsă (Maxim 3 programări active).")
    
    st.markdown(f"""
    <div style='background-color: #ffe6e6; padding: 20px; border-radius: 10px; border: 2px solid #ff4b4b; text-align: center; margin-bottom: 20px;'>
        <h3 style='color: #cc0000; margin-top: 0;'>🔒 Licență Expirată / Necesită Activare</h3>
        <p style='font-size: 16px; color: #333;'>Pentru a putea adăuga clienți noi și pentru a debloca complet agenda salonului tău, te rugăm să activezi abonamentul lunar.</p>
        <a href="{LINK_PLATA_STRIPE}" target="_blank">
            <button style='background-color: #635bff; color: white; border: none; padding: 12px 24px; font-size: 18px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; max-width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                💳 Plătește cu Cardul (via Stripe)
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Dezactivăm adăugarea de noi date, afișăm doar ce are deja introdus în mod citire
    st.warning("Dezactivează sau șterge din programările vechi pentru a elibera spațiu, sau cumpără licența.")

# --- SECȚIUNEA PROPRIETAR: ADAUGĂ/MODIFICĂ SERVICII ȘI PREȚURI ---
st.sidebar.header("⚙️ Configurare Salon")
with st.sidebar.expander("💰 Administrare Servicii și Prețuri", expanded=True):
    st.write("Adaugă sau modifică prețurile pentru servicii:")
    
    nou_serviciu = st.text_input("Nume serviciu nou (ex: Tunsoare):")
    nou_pret = st.number_input("Preț (lei):", min_value=0, value=30, step=5)
    
    # Permitem modificarea prețurilor doar dacă nu este blocat sau dacă vrea să le schimbe pe cele vechi
    if st.button("Adaugă / Actualizează Serviciu"):
        if nou_serviciu:
            st.session_state.servicii_salon[nou_serviciu] = nou_pret
            st.success(f"Adăugat: {nou_serviciu} - {nou_pret} lei")
            st.rerun()

    st.write("---")
    st.write("*Lista actuală de prețuri:*")
    for serv, pret in list(st.session_state.servicii_salon.items()):
        col_s1, col_s2 = st.columns([3, 1])
        col_s1.write(f"{serv}: {pret} lei")
        if col_s2.button("❌", key=f"del_serv_{serv}"):
            del st.session_state.servicii_salon[serv]
            st.rerun()

# --- FORMULAR PROGRAMARE NOUĂ (Se ascunde când se atinge limita) ---
if numar_programari < 3:
    st.write("---")
    st.write("### ➕ Adaugă o programare nouă")
    with st.form("form_programare"):
        col_f1, col_f2 = st.columns(2)
        ora_p = col_f1.text_input("Ora (ex: 10:30):")
        client_p = col_f2.text_input("Nume Client:")
        tel_p = col_f1.text_input("Telefon (format: 407xxxxxxxx):", value="407")
        
        servicii_disponibile = list(st.session_state.servicii_salon.keys())
        serviciu_p = col_f2.selectbox("Serviciu solicitat:", options=servicii_disponibile if servicii_disponibile else ["Niciun serviciu definit"])
        
        submit = st.form_submit_button("Salvează Programarea")
        if submit and client_p and ora_p:
            nou_id = max([p["id"] for p in st.session_state.agenda_salariati], default=0) + 1
            st.session_state.agenda_salariati.append({
                "id": nou_id, "ora": ora_p, "client": client_p, "telefon": tel_p, "serviciu": serviciu_p
            })
            st.success("Programare salvată cu succes!")
            st.rerun()

# --- AFIȘARE ÎNCASĂRI ȘI AGENDA ---
st.write("---")
total_incasari = sum([st.session_state.servicii_salon.get(prog["serviciu"], 0) for prog in st.session_state.agenda_salariati])
st.metric(label="💰 TOTAL ÎNCASĂRI ASTĂZI:", value=f"{total_incasari} lei")

st.write("### 📅 Programările de Azi:")
for prog in st.session_state.agenda_salariati:
    pret_serviciu = st.session_state.servicii_salon.get(prog["serviciu"], 0)
    
    with st.container():
        st.markdown(f"""
        <div style='background-color: #f9f9f9; padding: 10px; border-left: 5px solid #ff4b4b; border-radius: 5px; margin-bottom: 10px;'>
            <strong>🕒 {prog['ora']} - 👤 {prog['client']}</strong><br>
            💇‍♂️ {prog['serviciu']} — <span style='color: green; font-weight: bold;'>{pret_serviciu} lei</span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"📞 Tel: {prog['telefon']}")
        with col2:
            mesaj_standard = f"Bună {prog['client']}! 💅 Te confirmăm la Salon Elegance pentru {prog['serviciu']} la ora {prog['ora']}."
            mesaj_url = urllib.parse.quote(mesaj_standard)
            link_whatsapp = f"https://wa.me/{prog['telefon']}?text={mesaj_url}"
            st.markdown(f'<a href="{link_whatsapp}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer; width:100%;">🟢 WhatsApp</button></a>', unsafe_allow_html=True)
        with col3:
            if st.button("❌ Anulează", key=f"del_{prog['id']}"):
                st.session_state.agenda_salariati = [p for p in st.session_state.agenda_salariati if p["id"] != prog["id"]]
                st.rerun()
