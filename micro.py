import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Train Manager Pro", layout="wide")

# CSS Personalizzato per estetica e spaziatura
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stHeader { font-family: 'Segoe UI', sans-serif; color: #1E1E1E; }
    .month-box { 
        padding: 20px; 
        border-radius: 10px; 
        background-color: #ffffff; 
        border: 2px solid #007bff;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE NOMI ---
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

# --- SIDEBAR: CONTROLLI ANTE-GENERAZIONE ---
st.sidebar.image("https://img.icons8.com/fluency/96/train.png", width=80)
st.sidebar.title("Configurazione")

# 1. Scelta Mese e Anno
st.sidebar.subheader("📅 Periodo")
col_m, col_a = st.sidebar.columns(2)
mese_nome = col_m.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
anno = col_a.number_input("Anno", min_value=2024, max_value=2030, value=2024)

mese_idx = list(calendar.month_name).index(mese_nome)
num_giorni = calendar.monthrange(anno, mese_idx)[1]

# 2. Selezione Meritevoli (Multi-select spazioso)
st.sidebar.subheader("🌟 Sezione Meritevoli")
meritevoli_scelti = st.sidebar.multiselect(
    "Seleziona i membri R3/Meritevoli per questo mese:",
    options=r3_list,
    help="Puoi cercare i nomi scrivendo"
)

# --- MAIN INTERFACE ---
st.markdown(f"""
    <div class="month-box">
        <h1 style='margin:0; color:#007bff;'>CALENDARIO TRENI - {mese_nome.upper()} {anno}</h1>
        <p style='margin:0; color:#555;'>Assegnazione Capotreni e Passeggeri</p>
    </div>
    """, unsafe_allow_html=True)

# Pulsante di Generazione
if st.button("🚀 GENERA CALENDARIO AUTOMATICO", use_container_width=True):
    
    data_list = []
    
    # Algoritmo di riempimento
    for giorno in range(1, num_giorni + 1):
        # Logica Leader (primi 11 giorni)
        if giorno <= 11:
            capotreno = leaders[giorno-1]
            # Il passeggero potrebbe essere il leader successivo o un meritevole
            passeggero = leaders[giorno] if giorno < 11 else (meritevoli_scelti[0] if meritevoli_scelti else "Da assegnare")
        else:
            # Logica Meritevoli (dal giorno 12 in poi)
            if meritevoli_scelti:
                idx = (giorno - 12) % len(meritevoli_scelti)
                capotreno = meritevoli_scelti[idx]
                passeggero = meritevoli_scelti[(idx + 1) % len(meritevoli_scelti)]
            else:
                capotreno = "Nessun Meritevole"
                passeggero = "---"

        data_list.append({
            "Data": f"{giorno:02d} {mese_nome}",
            "Ruolo: CAPOTRENO": capotreno,
            "Ruolo: PASSEGGERO": passeggero,
            "Note": ""
        })

    # Creazione DataFrame
    df = pd.DataFrame(data_list)
    
    # --- POST GENERAZIONE: EDITING TOTALE ---
    st.subheader("📝 Revisione Post-Generazione")
    st.info("Puoi modificare qualsiasi cella qui sotto cliccandoci sopra. I cambiamenti sono immediati.")
    
    # Tabella interattiva avanzata
    edited_df = st.data_editor(
        df,
        column_config={
            "Ruolo: CAPOTRENO": st.column_config.SelectboxColumn(
                "Capotreno",
                options=leaders + r3_list,
                width="large"
            ),
            "Ruolo: PASSEGGERO": st.column_config.SelectboxColumn(
                "Passeggero",
                options=leaders + r3_list,
                width="large"
            )
        },
        disabled=["Data"],
        hide_index=True,
        num_rows="dynamic",
        use_container_width=True
    )

    # Esportazione
    st.download_button(
        label="📥 Scarica Calendario in Excel",
        data=edited_df.to_csv(index=False).encode('utf-8'),
        file_name=f'Calendario_Treni_{mese_nome}_{anno}.csv',
        mime='text/csv',
    )
else:
    st.warning("Seleziona i meritevoli nella colonna di sinistra e clicca su 'Genera' per iniziare.")
