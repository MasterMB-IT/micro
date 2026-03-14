import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Train Manager Ultra Pro v3", layout="wide", page_icon="🚂")

# CSS Avanzato per look Gaming e visibilità
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

total_roster = leaders_list + r3_list

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configurazione")
mese_nome = st.sidebar.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
anno = st.sidebar.number_input("Anno", 2024, 2030, 2024)
mese_idx = list(calendar.month_name).index(mese_nome)
num_giorni = calendar.monthrange(anno, mese_idx)[1]

st.sidebar.markdown("---")
st.sidebar.subheader("🌟 Selezione Meritevoli")
meritevoli_scelti = st.sidebar.multiselect("Chi partecipa questo mese (R3)?", r3_list)

# --- HEADER ---
st.markdown(f"""<div class="month-header-box"><h1 style='color:#00c8ff; margin:0;'>{mese_nome.upper()} {anno}</h1></div>""", unsafe_allow_html=True)

# --- ANTE-GENERAZIONE: LEADER ---
with st.expander("🛠️ CONFIGURAZIONE ACCOPPIAMENTI R5/R4 (Giorni 1-11)", expanded=True):
    st.info("Impedisce automaticamente di selezionare la stessa persona per entrambi i ruoli.")
    custom_leaders = []
    cols = st.columns(3)
    for i in range(11):
        with cols[i % 3]:
            st.markdown(f"**Giorno {i+1:02d}**")
            capo = st.selectbox(f"Capotreno G{i+1}", leaders_list, index=i, key=f"c{i}")
            # Filtra la lista passeggeri per non includere il capotreno appena scelto
            pass_options = [n for n in leaders_list if n != capo]
            passeg = st.selectbox(f"Passeggero G{i+1}", pass_options, index=0, key=f"p{i}")
            custom_leaders.append({"capotreno": capo, "passeggero": passeg})

# --- GENERAZIONE ---
if st.button("🚀 GENERA CALENDARIO COMPLETO", use_container_width=True):
    
    # Randomizzazione R3 con controllo duplicati
    meritevoli_random = list(meritevoli_scelti)
    random.shuffle(meritevoli_random)
    
    giorni_info = []
    
    for giorno in range(1, num_giorni + 1):
        if giorno <= 11:
            config = custom_leaders[giorno-1]
            capotreno = config['capotreno']
            passeggero = config['passeggero']
        else:
            if len(meritevoli_random) >= 2:
                idx = (giorno - 12) % len(meritevoli_random)
                capotreno = meritevoli_random[idx]
                # Prende il successivo, se è lo stesso (lista corta), prende un altro
                pass_idx = (idx + 1) % len(meritevoli_random)
                passeggero = meritevoli_random[pass_idx]
            elif len(meritevoli_random) == 1:
                capotreno = meritevoli_random[0]
                passeggero = "Posto Vacante (Manca R3)"
            else:
                capotreno = "Nessun Meritevole"
                passeggero = "---"

        giorni_info.append({
            "Giorno": giorno,
            "Capotreno": capotreno,
            "Passeggero": passeggero
        })

    # Salviamo in session_state per permettere l'editing post-generazione
    st.session_state['data_cal'] = giorni_info

if 'data_cal' in st.session_state:
    # --- POST-GENERAZIONE: EDITING TOTALE ---
    st.subheader("📝 Modifica e Revisione Totale")
    df_edit = pd.DataFrame(st.session_state['data_cal'])
    
    # La tabella permette di cambiare TUTTO
    edited_df = st.data_editor(
        df_edit,
        column_config={
            "Capotreno": st.column_config.SelectboxColumn("Capotreno", options=total_roster, width="large"),
            "Passeggero": st.column_config.SelectboxColumn("Passeggero", options=total_roster, width="large")
        },
        disabled=["Giorno"],
        hide_index=True,
        use_container_width=True,
        key="main_editor"
    )
    
    # Aggiorniamo i dati visivi in base alla tabella
    giorni_visual = edited_df.to_dict('records')

    # --- RENDERING VISIVO ---
    st.markdown("---")
    st.subheader("🗓️ Visualizzazione Calendario")
    
    settimane = []
    settimana_corrente = []
    for i, d in enumerate(giorni_visual):
        settimana_corrente.append(d)
        wd = calendar.weekday(anno, mese_idx, d['Giorno'])
        if wd == 6 or i == len(giorni_visual) - 1:
            settimane.append(settimana_corrente)
            settimana_corrente = []

    for idx, sett in enumerate(settimane):
        st.markdown(f'<div class="week-block"><div class="week-title">Settimana {idx+1}</div>', unsafe_allow_html=True)
        for d in sett:
            capo_c = "leader-badge" if d['Capotreno'] in leaders_list else "merit-badge"
            pass_c = "leader-badge" if d['Passeggero'] in leaders_list else "merit-badge"
            st.markdown(f"""
                <div class="day-card">
                    <div style="color:#00c8ff; font-weight:700; width:60px;">{d['Giorno']:02d} {mese_nome[:3]}</div>
                    <div style="flex-grow:1; display:flex; gap:40px;">
                        <div><span class="role-label">Capotreno</span><br><span class="player-name {capo_c}">{d['Capotreno']}</span></div>
                        <div><span class="role-label">Passeggero</span><br><span class="player-name {pass_c}">{d['Passeggero']}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Export finale
    st.download_button("📥 Scarica Excel/CSV", edited_df.to_csv(index=False).encode('utf-8'), f"Treni_{mese_nome}.csv", "text/csv")
