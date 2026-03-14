import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Train Manager Ultra Pro", layout="wide", page_icon="🚂")

# CSS Avanzato (Mantenuto e migliorato per i menu a tendina)
st.markdown("""
    <style>
    .stApp { background-color: #121418; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
    .month-header-box {
        background: linear-gradient(135deg, #1e2229 0%, #121418 100%);
        padding: 25px; border-radius: 15px; border-left: 5px solid #00c8ff;
        text-align: center; margin-bottom: 30px;
    }
    .week-block { background-color: #1e2229; border-radius: 12px; padding: 20px; margin-bottom: 25px; border: 1px solid #2a3039; }
    .week-title { color: #ff9f43; font-size: 1.5rem; font-weight: 700; border-bottom: 2px solid #ff9f43; padding-bottom: 5px; margin-bottom: 15px; display: inline-block; }
    .day-card { background-color: #252a33; border-radius: 8px; padding: 12px; margin-bottom: 8px; border: 1px solid #333945; display: flex; justify-content: space-between; align-items: center; }
    .leader-badge { color: #ff4757; font-weight: 700; }
    .merit-badge { color: #2ed573; font-weight: 700; }
    .role-label { color: #808080; font-size: 0.75rem; text-transform: uppercase; }
    .player-name { color: #ffffff; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE NOMI ---
leaders_list = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", 
                "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", 
                "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]

r3_list = sorted(["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", 
           "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", 
           "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", 
           "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", 
           "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", 
           "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", 
           "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", 
           "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", 
           "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"])

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configurazione")
mese_nome = st.sidebar.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
anno = st.sidebar.number_input("Anno", 2024, 2030, 2024)
mese_idx = list(calendar.month_name).index(mese_nome)
num_giorni = calendar.monthrange(anno, mese_idx)[1]

st.sidebar.markdown("---")
st.sidebar.subheader("🌟 Selezione Meritevoli")
meritevoli_scelti = st.sidebar.multiselect("Chi partecipa (R3)?", r3_list)

# --- SEZIONE SPECIALE: ACCOPPIAMENTO LEADER (R5/R4) ---
st.markdown(f"""<div class="month-header-box"><h1 style='color:#00c8ff; margin:0;'>{mese_nome.upper()} {anno}</h1></div>""", unsafe_allow_html=True)

with st.expander("🛠️ CONFIGURAZIONE ACCOPPIAMENTI R5/R4 (Primi 11 Giorni)", expanded=True):
    st.write("Personalizza chi fa il passeggero con quale leader per i primi 11 giorni:")
    custom_leaders = []
    
    cols = st.columns(3)
    for i in range(11):
        with cols[i % 3]:
            st.markdown(f"**Giorno {i+1:02d}**")
            capo = st.selectbox(f"Capotreno G{i+1}", leaders_list, index=i, key=f"c{i}")
            # Di default suggeriamo il leader successivo come passeggero, ma l'utente può cambiare
            pass_default = (i + 1) % len(leaders_list)
            passeg = st.selectbox(f"Passeggero G{i+1}", leaders_list, index=pass_default, key=f"p{i}")
            custom_leaders.append({"capotreno": capo, "passeggero": passeg})

# --- GENERAZIONE ---
if st.button("🚀 GENERA CALENDARIO COMPLETO", use_container_width=True):
    
    # Randomizzazione R3
    meritevoli_random = list(meritevoli_scelti)
    random.shuffle(meritevoli_random)
    
    giorni_info = []
    
    for giorno in range(1, num_giorni + 1):
        if giorno <= 11:
            # Usa gli accoppiamenti scelti manualmente nell'expander
            config = custom_leaders[giorno-1]
            capotreno = config['capotreno']
            passeggero = config['passeggero']
            is_leader = True
        else:
            # Logica Random per R3
            if meritevoli_random:
                idx = (giorno - 12) % len(meritevoli_random)
                capotreno = meritevoli_random[idx]
                passeggero = meritevoli_random[(idx + 1) % len(meritevoli_random)]
            else:
                capotreno = "Nessun Meritevole"
                passeggero = "---"
            is_leader = False

        giorni_info.append({"giorno": giorno, "capotreno": capotreno, "passeggero": passeggero, "is_leader": is_leader})

    # --- RENDERING A SETTIMANE ---
    settimane = []
    settimana_corrente = []
    for i, info in enumerate(giorni_info):
        settimana_corrente.append(info)
        wd = calendar.weekday(anno, mese_idx, info['giorno'])
        if wd == 6 or i == len(giorni_info) - 1:
            settimane.append(settimana_corrente)
            settimana_corrente = []

    for i, settimana in enumerate(settimane):
        st.markdown(f"""<div class="week-block"><div class="week-title">Settimana {i+1}</div>""", unsafe_allow_html=True)
        for d in settimana:
            capo_c = "leader-badge" if d['capotreno'] in leaders_list else "merit-badge"
            pass_c = "leader-badge" if d['passeggero'] in leaders_list else "merit-badge"
            st.markdown(f"""
                <div class="day-card">
                    <div style="color:#00c8ff; font-weight:700; width:60px;">{d['giorno']:02d}</div>
                    <div style="flex-grow:1; display:flex; gap:30px;">
                        <div><span class="role-label">Capotreno:</span><br><span class="{capo_c}">{d['capotreno']}</span></div>
                        <div><span class="role-label">Passeggero:</span><br><span class="{pass_c}">{d['passeggero']}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Export
    df_export = pd.DataFrame(giorni_info)[['giorno', 'capotreno', 'passeggero']]
    st.download_button("📥 Scarica in CSV", df_export.to_csv(index=False).encode('utf-8'), f"Treni_{mese_nome}.csv", "text/csv")
