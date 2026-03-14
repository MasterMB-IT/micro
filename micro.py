import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Train Manager Global Edition", layout="wide", page_icon="🚂")

# CSS Gaming Style
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
    .r2-r1-badge { color: #a29bfe; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE INIZIALE (Session State per permettere modifiche) ---
if 'players_db' not in st.session_state:
    # Popoliamo il database iniziale con i nomi che abbiamo
    db = []
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: db.append({"Nome": n, "Grado": "R5/R4"})
    
    r3_init = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_init: db.append({"Nome": n, "Grado": "R3"})
    
    # Aggiungiamo slot vuoti per R2 ed R1 che l'utente può riempire
    for i in range(1, 6): db.append({"Nome": f"Player R2_{i}", "Grado": "R2"})
    for i in range(1, 6): db.append({"Nome": f"Player R1_{i}", "Grado": "R1"})
    
    st.session_state['players_db'] = pd.DataFrame(db)

# --- SIDEBAR: GESTIONE ROSTER ---
st.sidebar.title("👥 Gestione Alleanza")
with st.sidebar.expander("Modifica Gradi / Nomi"):
    # Tabella editabile per cambiare gradi o nomi al volo
    edited_db = st.data_editor(st.session_state['players_db'], hide_index=True, use_container_width=True)
    st.session_state['players_db'] = edited_db

st.sidebar.markdown("---")
st.sidebar.subheader("📅 Periodo")
mese_nome = st.sidebar.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
anno = st.sidebar.number_input("Anno", 2024, 2030, 2024)
num_giorni = calendar.monthrange(anno, list(calendar.month_name).index(mese_nome))[1]

# --- SELEZIONE MERITEVOLI (Da tutto il database) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🌟 Selezione Meritevoli")
# Permette di scegliere chiunque tranne i Leader (che sono fissi)
potential_merits = st.session_state['players_db'][st.session_state['players_db']['Grado'] != "R5/R4"]['Nome'].tolist()
meritevoli_scelti = st.sidebar.multiselect("Chi partecipa ai treni?", options=potential_merits)

# --- MAIN ---
st.markdown(f'<div class="month-header-box"><h1 style="color:#00c8ff; margin:0;">{mese_nome.upper()} {anno}</h1></div>', unsafe_allow_html=True)

# --- CONFIGURAZIONE LEADER ---
leaders_list = st.session_state['players_db'][st.session_state['players_db']['Grado'] == "R5/R4"]['Nome'].tolist()

with st.expander("🛠️ ACCOPPIAMENTI LEADER (Giorno 1-11)", expanded=True):
    custom_leaders = []
    cols = st.columns(3)
    for i in range(11):
        with cols[i % 3]:
            st.markdown(f"**Giorno {i+1:02d}**")
            capo = st.selectbox(f"Capo G{i+1}", leaders_list, index=i % len(leaders_list), key=f"c{i}")
            pass_opt = [n for n in leaders_list if n != capo]
            passeg = st.selectbox(f"Pass G{i+1}", pass_opt, index=0, key=f"p{i}")
            custom_leaders.append({"Capotreno": capo, "Passeggero": passeg})

# --- GENERAZIONE ---
if st.button("🚀 GENERA CALENDARIO", use_container_width=True):
    pool = list(meritevoli_scelti)
    random.shuffle(pool)
    giorni = []
    for g in range(1, num_giorni + 1):
        if g <= 11:
            c, p = custom_leaders[g-1]['Capotreno'], custom_leaders[g-1]['Passeggero']
        else:
            if len(pool) >= 2: c, p = pool.pop(0), pool.pop(0)
            elif len(pool) == 1: c, p = pool.pop(0), "DA ASSEGNARE"
            else: c, p = "DA ASSEGNARE", "DA ASSEGNARE"
        giorni.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
    st.session_state['data_cal'] = giorni

# --- OUTPUT E MODIFICA ---
if 'data_cal' in st.session_state:
    edit_mode = st.checkbox("🛠️ MODALITÀ MODIFICA POST-GENERAZIONE")
    
    if edit_mode:
        all_names = st.session_state['players_db']['Nome'].tolist()
        df_edit = pd.DataFrame(st.session_state['data_cal'])
        res = st.data_editor(df_edit, column_config={
            "Capotreno": st.column_config.SelectboxColumn("Capotreno", options=all_names, width="large"),
            "Passeggero": st.column_config.SelectboxColumn("Passeggero", options=all_names, width="large")
        }, disabled=["Giorno"], hide_index=True, use_container_width=True)
        st.session_state['data_cal'] = res.to_dict('records')

    # Rendering grafico
    for i, d in enumerate(st.session_state['data_cal']):
        if i % 7 == 0: st.markdown(f'<div class="week-title">Settimana {(i//7)+1}</div>', unsafe_allow_html=True)
        
        # Colore dinamico in base al grado nel DB
        grado_capo = st.session_state['players_db'][st.session_state['players_db']['Nome'] == d['Capotreno']]['Grado'].values
        grado_pass = st.session_state['players_db'][st.session_state['players_db']['Nome'] == d['Passeggero']]['Grado'].values
        
        c_cls = "leader-badge" if "R5/R4" in grado_capo else "merit-badge" if "R3" in grado_capo else "r2-r1-badge"
        p_cls = "leader-badge" if "R5/R4" in grado_pass else "merit-badge" if "R3" in grado_pass else "r2-r1-badge"
        
        st.markdown(f"""
            <div class="day-card">
                <div style="color:#00c8ff; font-weight:700; width:50px;">{d['Giorno']:02d}</div>
                <div style="flex-grow:1; display:flex; gap:30px;">
                    <div><span style="font-size:0.7rem; color:#888;">CAPO</span><br><span class="{c_cls}">{d['Capotreno']}</span></div>
                    <div><span style="font-size:0.7rem; color:#888;">PASS</span><br><span class="{p_cls}">{d['Passeggero']}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.download_button("📥 Scarica CSV", pd.DataFrame(st.session_state['data_cal']).to_csv(index=False).encode('utf-8'), "Treni.csv")
