import streamlit as st
import urllib.parse

st.set_page_config(page_title="Beauty-IA Agenda Pro", page_icon="💅", layout="centered")

st.markdown("""
    <style>
    .reportview-container { background: #111116; }
    h1 { color: #FF4B4B !important; text-shadow: 2px 2px 4px #000000; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 10px; }
    .stButton>button:hover { background-color: #FF2E2E; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("💅 Beauty-IA: Agenda ta Inteligentă Pro")

if "agenda_salariati" not in st.session_state:
    st.session_state.agenda_salariati = [
        {"id": 0, "ora": "09:00", "client": "Maria Georgescu", "telefon": "0722111222", "serviciu": "Vopsit", "pret": 150},
        {"id": 1, "ora": "10:30", "client": "Elena Ionescu", "telefon": "0733444555", "serviciu": "Manichiură", "pret": 90}
    ]
if "next_id" not in st.session_state:
    st.session_state.next_id = 2

total_incasari = sum(prog["pret"] for prog in st.session_state.agenda_salariati)

st.markdown("### 📓 Carnetul tău Digital de Programări")
st.metric(label="💰 TOTAL ÎNCASĂRI ASTĂZI:", value=f"{total_incasari} lei")
st.write("---")

for prog in st.session_state.agenda_salariati:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"⏰ *{prog['ora']}* — 👤 *{prog['client']}*")
        st.write(f"✂️ {prog['serviciu']} — *{prog['pret']} lei*")
        st.write(f"📞 Tel: {prog['telefon']}")
    
    with col2:
        mesaj_standard = f"Bună {prog['client']}! 😊 Te confirmăm la Salon Elegance pentru {prog['serviciu']} la ora {prog['ora']}. Te așteptăm! ✨"
        mesaj_url = urllib.parse.quote(mesaj_standard)
        link_whatsapp = f"https://wa.me/{prog['telefon'][1:]}?text={mesaj_url}"
        st.markdown(f'<a href="{link_whatsapp}" target="_blank"><button style="background-color:#25D366; color:white; border:none; border-radius:5px; padding:5px 10px; cursor:pointer; width:100%;">💬 WhatsApp</button></a>', unsafe_allow_html=True)
    
    with col3:
        if st.button("❌ Anulează", key=f"del_{prog['id']}"):
            st.session_state.agenda_salariati = [p for p in st.session_state.agenda_salariati if p["id"] != prog["id"]]
            st.rerun()
    st.write(" ")

st.markdown("---")
st.markdown("### 🤖 Simulare Mesaj Nou de la un Client")

nume_nou = st.text_input("Nume client nou:", "Andrei Popescu")
tel_nou = st.text_input("Număr de telefon client:", "0744666777")
mesaj_client = st.text_input("Ce scrie clientul pe WhatsApp?", value="Vreau să mă tund la ora 13 sau unu.. aș putea să vin?")

if st.button("🚀 Procesează Mesajul și Salvează în Agendă"):
    txt = mesaj_client.lower()
    pret_total = 0
    serviciu_detectat = "Serviciu nespecificat"
    
    if "tund" in txt or "tuns" in txt:
        pret_total = 60
        serviciu_detectat = "Tuns"
    elif "vopsit" in txt:
        pret_total = 150
        serviciu_detectat = "Vopsit"
        
    ora_detectata = "13:00"
    if "13" in txt or "unu" in txt:
        ora_detectata = "13:00"

    ora_ocupata = any(p["ora"] == ora_detectata for p in st.session_state.agenda_salariati)
    
    if ora_ocupata:
        st.warning(f"⚠️ Ora 13:00 ocupată!")
    else:
        noua_programare = {
            "id": st.session_state.next_id, 
            "ora": ora_detectata, 
            "client": nume_nou, 
            "telefon": tel_nou,
            "serviciu": serviciu_detectat, 
            "pret": pret_total
        }
        st.session_state.agenda_salariati.append(noua_programare)
        st.session_state.next_id += 1
        st.rerun()