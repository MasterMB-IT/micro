import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA E TEMA ---
st.set_page_config(page_title="Train Manager Ultra", layout="wide", page_icon="🚂")

# CSS Avanzato per un look Gaming/Professional, spaziatura e pulizia
st.markdown("""
    <style>
    /* Sfondo scuro e font globale */
    .stApp {
        background-color: #121418;
        color: #e0e0e0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Header Mese Grande e Accattivante */
    .month-header-box {
        background: linear-gradient(135deg, #1e2229 0%, #121418 100%);
        padding: 30px;
        border-radius: 15px;
        border-left: 5px solid #00c8ff;
        box-shadow: 0 4px 15px rgba(0,200,255,0.2);
        text-align: center;
        margin-bottom: 35px;
    }
    .month-header-title {
        margin: 0;
        color: #00c8ff;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1px;
        text-transform: uppercase;
    }
    .month-header-subtitle {
        margin: 5px 0 0 0;
        color: #a0a0a0;
        font-size: 1.2rem;
        font-weight: 400;
    }

    /* Stile per i blocchi Settimanali */
    .week-block {
        background-color: #1e2229;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        border: 1px solid #2a3039;
    }
    .week-title {
        color: #ff9f43; /* Colore accento per la settimana */
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 2px solid #ff9f43;
        padding-bottom: 5px;
        display: inline-block;
    }

    /* Stile per le card giornaliere all'interno della settimana */
    .day-card {
        background-color: #252a33;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #333945;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .day-date {
        color: #00c8ff;
        font-weight: 700;
        font-size: 1.1rem;
        width: 80px;
    }
    .role-info {
        flex-grow: 1;
        display: flex;
        gap: 20px;
        justify-content: flex-start;
    }
    .role-block {
        display: flex;
        flex-direction: column;
    }
    .role-label {
        color: #808080;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .player-name {
        color: #ffffff;
        font-weight: 600;
        font-size: 1rem;
    }
    .leader-badge {
        color: #ff4757; /* Colore per i Leader */
        font-weight: 700;
    }
    .merit-badge {
        color: #2ed573; /* Colore per i Meritevoli */
        font-weight: 700;
    }

    /* Bottoni e Input Sidebar */
    .stButton>button {
        background-color: #00c8ff;
        color: #121418;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 12px 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0099cc;
        box-shadow: 0 0 10px rgba(0,200,255,0.5);
    }
    .stMultiSelect div[data-baseweb="select"] {
        background-color: #1e2229;
        border-color: #333945;
        color: #ffffff;
    }

    /* Nascondi header streamlit standard */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE NOMI (Invariato) ---
leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", 
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

# --- SIDEBAR: CONTROLLI (Invariato nella logica, stilizzato via CSS) ---
st.sidebar.markdown("<h1 style='color:#00c8ff; text-align:center;'>TRAIN PANEL</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.subheader("📅 Periodo")
col_m, col_a = st.sidebar.columns(2)
mese_nome = col_m.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
anno = col_a.number_input("Anno", min_value=2024, max_value=2030, value=2024)

mese_idx = list(calendar.month_name).index(mese_nome)
num_giorni = calendar.monthrange(anno, mese_idx)[1]

st.sidebar.markdown("---")
st.sidebar.subheader("🌟 Sezione Meritevoli")
meritevoli_scelti = st.sidebar.multiselect(
    "Seleziona R3/Meritevoli:",
    options=r3_list,
    help="Cerca o seleziona i nomi"
)

st.sidebar.markdown("---")

# --- MAIN INTERFACE: HEADER ---
st.markdown(f"""
    <div class="month-header-box">
        <h1 class="month-header-title">{mese_nome} {anno}</h1>
        <p class="month-header-subtitle">Programma Ufficiale Assegnazione Treni Alleanza</p>
    </div>
    """, unsafe_allow_html=True)

# --- LOGICA DI GENERAZIONE E RANDOMIZZAZIONE ---
if st.button("🚀 GENERA / RIGENERA CALENDARIO", use_container_width=True):
    
    # 1. Randomizzazione vera degli R3
    # Creiamo una copia per non alterare la lista originale e la mescoliamo
    meritevoli_random = list(meritevoli_scelti)
    random.shuffle(meritevoli_random)
    
    # 2. Struttura dati per il calendario
    giorni_info = []
    
    for giorno in range(1, num_giorni + 1):
        # Logica Leader (primi 11 giorni) - Sequenziale tra leader, come richiesto
        if giorno <= 11:
            capotreno = leaders[giorno-1]
            # Il passeggero potrebbe essere un altro leader o il primo R3 random
            if giorno < 11:
                passeggero = leaders[giorno]
            else:
                passeggero = meritevoli_random[0] if meritevoli_random else "Da assegnare"
            is_leader = True
        else:
            # Logica Meritevoli (dal giorno 12 in poi) - Random
            if meritevoli_random:
                # Usiamo l'operatore modulo per ciclare sulla lista RANDOMIZZATA
                idx = (giorno - 12) % len(meritevoli_random)
                capotreno = meritevoli_random[idx]
                # Accoppiamento casuale: il passeggero è il successivo nella lista random
                passeggero = meritevoli_random[(idx + 1) % len(meritevoli_random)]
            else:
                capotreno = "Nessun Meritevole"
                passeggero = "---"
            is_leader = False

        giorni_info.append({
            "giorno": giorno,
            "capotreno": capotreno,
            "passeggero": passeggero,
            "is_leader": is_leader
        })

    # --- RENDERING ORDINATO PER SETTIMANE ---
    st.subheader("🗓️ Calendario Dettagliato")
    
    # Organizziamo i giorni in settimane
    settimane = []
    settimana_corrente = []
    
    for i, info in enumerate(giorni_info):
        settimana_corrente.append(info)
        # Se è domenica (o l'ultimo giorno del mese), chiudiamo la settimana
        # calendar.weekday restituisce 0=Lunedì, ..., 6=Domenica
        wd = calendar.weekday(anno, mese_idx, info['giorno'])
        if wd == 6 or i == len(giorni_info) - 1:
            settimane.append(settimana_corrente)
            settimana_corrente = []

    # Rendering visivo delle settimane
    for i, settimana in enumerate(settimane):
        st.markdown(f"""<div class="week-block"><div class="week-title">Settimana {i+1}</div>""", unsafe_allow_html=True)
        
        for d in settimana:
            # Scegliamo il badge corretto in base al ruolo
            capo_class = "leader-badge" if d['is_leader'] else "merit-badge"
            # Il passeggero del giorno 11 è un R3, quindi badge verde
            pass_class = "leader-badge" if d['is_leader'] and d['giorno'] < 11 else "merit-badge"
            
            # Rendering della card giornaliera con HTML pulito
            st.markdown(f"""
                <div class="day-card">
                    <div class="day-date">{d['giorno']:02d} {mese_nome[:3]}</div>
                    <div class="role-info">
                        <div class="role-block">
                            <span class="role-label">Capotreno</span>
                            <span class="player-name {capo_class}">{d['capotreno']}</span>
                        </div>
                        <div class="role-block">
                            <span class="role-label">Passeggero</span>
                            <span class="player-name {pass_class}">{d['passeggero']}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True) # Chiude week-block

    # --- POST GENERAZIONE: EDITING E EXPORT (Spostato sotto il rendering visivo) ---
    st.markdown("---")
    st.subheader("📝 Revisione e Modifica Rapida (Tabella)")
    st.info("Usa questa tabella per scambi veloci dell'ultimo minuto. Le modifiche qui non influenzano la visualizzazione a schede sopra.")
    
    # Creiamo un DataFrame pulito per l'editor
    df_editor = pd.DataFrame([{
        "Data": f"{d['giorno']:02d} {mese_nome}",
        "Capotreno": d['capotreno'],
        "Passeggero": d['passeggero']
    } for d in giorni_info])
    
    edited_df = st.data_editor(
        df_editor,
        column_config={
            "Capotreno": st.column_config.SelectboxColumn("Capotreno", options=leaders + r3_list, width="large"),
            "Passeggero": st.column_config.SelectboxColumn("Passeggero", options=leaders + r3_list, width="large")
        },
        disabled=["Data"],
        hide_index=True,
        use_container_width=True
    )

    # Esportazione
    st.download_button(
        label="📥 Scarica Calendario Finale (CSV)",
        data=edited_df.to_csv(index=False).encode('utf-8'),
        file_name=f'Calendario_Treni_{mese_nome}_{anno}.csv',
        mime='text/csv',
    )
else:
    # Stato iniziale arioso
    st.markdown("---")
    st.warning("👈 Configura il periodo e seleziona i meritevoli nella colonna di sinistra, poi clicca su 'Genera' per visualizzare il programma.")
