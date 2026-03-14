import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Train Manager Pro - 100 Players Edition", layout="wide")

# CSS per pulizia visiva e colori gradi
st.markdown("""
    <style>
    .stApp { background-color: #121418; color: #e0e0e0; }
    .month-header { background: linear-gradient(90deg, #1e2229, #121418); padding: 20px; border-radius: 10px; border-bottom: 4px solid #00c8ff; text-align: center; }
    .week-container { background-color: #1e2229; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #333; }
    .r5-r4 { color: #ff4757; font-weight: bold; }
    .r3 { color: #2ed573; font-weight: bold; }
    .r2-r1 { color: #a29bfe; font-weight: bold; }
    .day-box { background-color: #252a33; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE DATABASE (100 Giocatori) ---
if 'players_df' not in st.session_state:
    data = []
    # R5 e R4 (11)
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    
    # R3 (57 nomi estratti)
    r3_names = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_names: data.append({"Nome": n, "Grado": "R3"})
    
    # R2 e R1 (Riempimento fino a 100)
    for i in range(1, 17): data.append({"Nome": f"Player_R2_{i}", "Grado": "R2"})
    for i in range(1, 16): data.append({"Nome": f"Player_R1_{i}", "Grado": "R1"})
    
    st.session_state['players_df'] = pd.DataFrame(data)

# --- SIDEBAR: GESTIONE CATEGORIE E SPOSTAMENTI ---
st.sidebar.title("👥 Gestione Roster (100)")

with st.sidebar.expander("🔄 SPOSTA GIOCATORI TRA GRADI"):
    st.write("Modifica il grado per spostare il giocatore in un'altra categoria.")
    # Editor per cambiare gradi
    temp_df = st.data_editor(st.session_state['players_df'], 
                              column_config={"Grado": st.column_config.SelectboxColumn("Grado", options=["R5/R4", "R3", "R2", "R1"])},
                              hide_index=True, use_container_width=True)
    st.session_state['players_df'] = temp_df

st.sidebar.markdown("---")

# --- SELEZIONE MERITEVOLI DIVISA ---
st.sidebar.subheader("🌟 Selezione Meritevoli")
# Creiamo liste filtrate per la selezione
pool_r3 = st.session_state['players_df'][st.session_state['players_df']['Grado'] == "R3"]['Nome'].tolist()
pool_r2 = st.session_state['players_df'][st.session_state['players_df']['Grado'] == "R2"]['Nome'].tolist()
pool_r1 = st.session_state['players_df'][st.session_state['players_df']['Grado'] == "R1"]['Nome'].tolist()

sel_r3 = st.sidebar.multiselect("Seleziona da R3", pool_r3)
sel_r2 = st.sidebar.multiselect("Seleziona da R2", pool_r2)
sel_r1 = st.sidebar.multiselect("Seleziona da R1", pool_r1)

meritevoli_totali = sel_r3 + sel_r2 + sel_r1

# --- CALCOLO GIORNI ---
mese_nome = st.sidebar.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
anno = st.sidebar.number_input("Anno", 2024, 2030, 2024)
mese_idx = list(calendar.month_name).index(mese_nome)
num_giorni = calendar.monthrange(anno, mese_idx)[1]

# --- HEADER ---
st.markdown(f'<div class="month-header"><h1>{mese_nome.upper()} {anno}</h1></div>', unsafe_allow_html=True)

# --- LEADER (1-11) ---
leaders_final = st.session_state['players_df'][st.session_state['players_df']['Grado'] == "R5/R4"]['Nome'].tolist()
with st.expander("🛠️ CONFIGURAZIONE LEADER (Giorno 1-11)"):
    config_l = []
    c1, c2, c3 = st.columns(3)
    for i in range(11):
        target_col = [c1, c2, c3][i % 3]
        with target_col:
            capo = st.selectbox(f"Capo G{i+1}", leaders_final, index=i % len(leaders_final), key=f"cap{i}")
            pass_opt = [n for n in leaders_final if n != capo]
            passg = st.selectbox(f"Pass G{i+1}", pass_opt, index=0, key=f"pas{i}")
            config_l.append({"Giorno": i+1, "Capotreno": capo, "Passeggero": passg})

# --- GENERAZIONE ---
if st.button("🚀 GENERA PROGRAMMA TRENI", use_container_width=True):
    random.shuffle(meritevoli_totali)
    pool = list(meritevoli_totali)
    
    final_cal = []
    for g in range(1, num_giorni + 1):
        if g <= 11:
            final_cal.append(config_l[g-1])
        else:
            if len(pool) >= 2:
                final_cal.append({"Giorno": g, "Capotreno": pool.pop(0), "Passeggero": pool.pop(0)})
            elif len(pool) == 1:
                final_cal.append({"Giorno": g, "Capotreno": pool.pop(0), "Passeggero": "VUOTO"})
            else:
                final_cal.append({"Giorno": g, "Capotreno": "VUOTO", "Passeggero": "VUOTO"})
    st.session_state['current_cal'] = final_cal

# --- OUTPUT E MODIFICA ---
if 'current_cal' in st.session_state:
    if st.checkbox("🛠️ MODIFICA POST-GENERAZIONE"):
        all_players = st.session_state['players_df']['Nome'].tolist()
        df_edit = pd.DataFrame(st.session_state['current_cal'])
        edited = st.data_editor(df_edit, column_config={
            "Capotreno": st.column_config.SelectboxColumn("Capotreno", options=all_players),
            "Passeggero": st.column_config.SelectboxColumn("Passeggero", options=all_players)
        }, hide_index=True, use_container_width=True)
        st.session_state['current_cal'] = edited.to_dict('records')

    # Visualizzazione
    data_vis = st.session_state['current_cal']
    for i, d in enumerate(data_vis):
        if i % 7 == 0: st.markdown(f'<h3 class="week-title">Settimana {(i//7)+1}</h3>', unsafe_allow_html=True)
        
        # Identificazione Grado per colori
        row_c = st.session_state['players_df'][st.session_state['players_df']['Nome'] == d['Capotreno']]
        row_p = st.session_state['players_df'][st.session_state['players_df']['Nome'] == d['Passeggero']]
        
        g_c = row_c['Grado'].values[0] if not row_c.empty else "N/A"
        g_p = row_p['Grado'].values[0] if not row_p.empty else "N/A"
        
        c_style = "r5-r4" if g_c == "R5/R4" else "r3" if g_c == "R3" else "r2-r1"
        p_style = "r5-r4" if g_p == "R5/R4" else "r3" if g_p == "R3" else "r2-r1"

        st.markdown(f"""
            <div class="day-box">
                <strong>Giorno {d['Giorno']:02d}</strong> | 
                Capotreno: <span class="{c_style}">{d['Capotreno']}</span> ({g_c}) — 
                Passeggero: <span class="{p_style}">{d['Passeggero']}</span> ({g_p})
            </div>
        """, unsafe_allow_html=True)
