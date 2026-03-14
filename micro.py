import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Arcade Train Manager", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS ARCADE WESTERN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Press+Start+2P&display=swap');

    /* SFONDO PIXEL ART ARCADE FAR WEST */
    .stApp { 
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)), 
                    url('https://img.freepik.com/premium-photo/pixel-art-desert-landscape-with-cacti-mountains-sunset_1020495-200.jpg');
        background-size: cover !important;
        background-position: bottom center !important;
        background-attachment: fixed !important;
        color: #ffffff; 
    }

    .train-title {
        font-family: 'Press Start 2P', cursive;
        text-align: center;
        color: #ffcc00;
        text-shadow: 4px 4px #cc3300;
        font-size: 1.8rem;
        margin-bottom: 30px;
        line-height: 1.6;
    }

    /* Pannelli stile cabinato */
    .stExpander { 
        background-color: rgba(40, 20, 0, 0.85) !important; 
        border: 3px solid #ffcc00 !important; 
        border-radius: 5px !important;
        backdrop-filter: blur(5px);
    }

    /* Bottoni Arcade */
    .btn-genera button { background: #2ecc71 !important; border-bottom: 5px solid #27ae60 !important; color: white !important; font-family: 'Press Start 2P'; font-size: 0.8rem !important; height: 70px !important; width: 100%; border-radius: 5px !important; }
    .btn-resetta button { background: #e74c3c !important; border-bottom: 5px solid #c0392b !important; color: white !important; font-family: 'Press Start 2P'; font-size: 0.8rem !important; height: 70px !important; width: 100%; border-radius: 5px !important; }
    .btn-verifica button { background: #f1c40f !important; border-bottom: 5px solid #f39c12 !important; color: black !important; font-family: 'Press Start 2P'; font-size: 0.8rem !important; height: 70px !important; width: 100%; border-radius: 5px !important; margin-top: 20px; }

    /* Card Giorno Arcade */
    .summary-card {
        background: rgba(0, 0, 0, 0.85); 
        border: 2px solid #555; 
        padding: 15px; 
        border-radius: 0px; 
        position: relative; 
        border-left: 5px solid #ffcc00;
        transition: 0.2s;
    }
    .summary-card:hover { transform: translateY(-5px); border-color: #ffcc00; box-shadow: 0 5px 15px rgba(255, 204, 0, 0.3); }
    
    .day-label { color: #ffcc00; font-family: 'Press Start 2P'; font-size: 0.7rem; text-align: center; margin-bottom: 10px; }
    .name-text { font-family: 'Orbitron'; font-size: 0.9rem; font-weight: 800; text-align: center; text-transform: uppercase; margin: 3px 0; }

    /* Popover */
    div[data-testid="stPopover"] > button { background: rgba(255,255,255,0.1) !important; border: 1px solid #555 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE DATABASE ---
if 'players_data' not in st.session_state:
    st.session_state['players_data'] = {
        "R5/R4": "Hool (R5), MASTER (R4), Le 12 Scimmie (R4), Sagittarius A1 (R4), Starbetty (R4), PEPPE (R4), Ricky Around (R4), uncle g (R4), 09ALEX24 (R4), ShinyPasta (R4), Wall 7 (R4)",
        "R3": "G Erry, Uncle g brother, Cane Avvoltoio, Ghandal, Aryron, Tricheco, Maメツ, NOVEMBERGENZ, Lalla 96, Whale Panda, GennaroM, EchoZero, EDDward, AMY, Resilienza, Ana Bunny, Giuseppec84, Benito Muschiolini, Pandino19, xFlotchy, MX63, holdfast, Ghost, BadBigBoss, Stefano00000, PakII, BANDOLERO26, BlOOdyBlade, Whale hunter Levve, Aresxxx, KingGruffalo, Hulkspakka, Joseone, ImAde, Nysbie, LeFada13, Skifetto, SPio24, TomEnergy, Markus Defender, Sho0t3r, Wolf006, Zokra, perseusxxx, Bendico, Obbyy, ArLes, Fatz87, cruel neve, Trivellatore, Osgh00, Slowfia ABOH, Pontatinatore, 27Francesco, MissDrinks, krompir, MaledettO",
        "R2": "teomadh, Bossnico, Valecit, FarmerHool, camiiiii 08, Doctor team, Yass081, Nuorifleming, Vergabrio, Frenk70, Comandante Maveric, Thor9000, MrBolly, BustaMaki, Ritardato, StUnTmArK, MONKEY D LUFFY 20, CineSalentino, Danylo98, Ezechielefabianino, BRNcommando, LEONIDA, elchicogyot, erer1000, Pupisnic, Backfire1, AnarchyBG, Fabrizio1987, JurdanS, WiseR9, Infinity8080"
    }

# --- GESTIONE NOMI (EDITOR) ---
with st.expander("👥 GESTIONE EQUIPAGGIO (Modifica Nomi)", expanded=False):
    st.info("Separa i nomi con una virgola. Le modifiche influenzeranno il prossimo calendario generato.")
    col_ed1, col_ed2, col_ed3 = st.columns(3)
    
    new_r4 = col_ed1.text_area("Capitani (R5/R4)", st.session_state['players_data']["R5/R4"], height=150)
    new_r3 = col_ed2.text_area("Passeggeri R3", st.session_state['players_data']["R3"], height=150)
    new_r2 = col_ed3.text_area("Passeggeri R2", st.session_state['players_data']["R2"], height=150)
    
    if st.button("💾 SALVA MODIFICHE EQUIPAGGIO"):
        st.session_state['players_data']["R5/R4"] = new_r4
        st.session_state['players_data']["R3"] = new_r3
        st.session_state['players_data']["R2"] = new_r2
        st.success("Equipaggio aggiornato!")
        st.rerun()

# Creazione liste nomi pulite
def get_list(key):
    return [n.strip() for n in st.session_state['players_data'][key].split(",") if n.strip()]

list_r4 = get_list("R5/R4")
list_r3 = get_list("R3")
list_r2 = get_list("R2")
all_names_list = sorted(list_r4 + list_r3 + list_r2)

# --- UI GENERALE ---
st.markdown('<div class="train-title">AOSR CANYON RUNNER<br>ARCADE EDITION</div>', unsafe_allow_html=True)

with st.expander("🛠️ CONFIGURAZIONE TRENO", expanded=True):
    c1, c2, c3 = st.columns([1, 1.5, 1.5])
    sel_mese = c1.selectbox("Mese", MESI_ITA, index=datetime.now().month - 1)
    sel_anno = c1.number_input("Anno", 2024, 2030, 2026)
    sel_r3 = c2.multiselect("Filtra R3", list_r3)
    sel_r2 = c3.multiselect("Filtra R2", list_r2)

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("🕹️ START GENERATION"):
        pool = (sel_r3 if sel_r3 else list_r3) + (sel_r2 if sel_r2 else list_r2)
        random.shuffle(pool)
        num_gg = (pd.Timestamp(year=sel_anno, month=MESI_ITA.index(sel_mese)+1, day=1) + pd.offsets.MonthEnd(0)).day
        st.session_state['master_cal'] = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11: 
                c = list_r4[(g-1)%len(list_r4)]
                p = list_r4[g%len(list_r4)]
            else:
                c = pool[p_idx % len(pool)]; p = pool[(p_idx+1) % len(pool)]
                p_idx += 2
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
    if st.button("🛑 RESET SYSTEM"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- DISPLAY CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h3 style='text-align: center; font-family: Press Start 2P; color: #ffcc00; font-size: 1rem;'>{sel_mese.upper()} {sel_anno}</h3>", unsafe_allow_html=True)
    cols = st.columns(6)
    for i, r in enumerate(st.session_state['master_cal']):
        with cols[i % 6]:
            c_col = "#ff4757" if r['Capo'] in list_r4 else "#2ed573"
            p_col = "#ff4757" if r['Pass'] in list_r4 else "#2ed573"
            
            st.markdown(f"""
            <div class="summary-card">
                <div class="day-label">DAY {r['Giorno']}</div>
                <div class="name-text" style="color:{c_col};">{r['Capo']}</div>
                <div style="color:#666; font-size:0.5rem; text-align:center; font-family:'Press Start 2P'; margin: 5px 0;">PASS</div>
                <div class="name-text" style="color:{p_col};">{r['Pass']}</div>
            """, unsafe_allow_html=True)
            
            with st.popover("⚙️"):
                nc = st.selectbox("Capo", all_names_list, index=all_names_list.index(r['Capo']), key=f"c_{i}")
                np = st.selectbox("Pass", all_names_list, index=all_names_list.index(r['Pass']), key=f"p_{i}")
                if st.button("UPDATE", key=f"s_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np}); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- VERIFICA ---
    st.markdown('<div class="btn-verifica">', unsafe_allow_html=True)
    if st.button("🛡️ INTEGRITY CHECK (VERIFICA)"):
        cal = st.session_state['master_cal']
        capi = [d['Capo'] for d in cal]
        pass_list = [d['Pass'] for d in cal]
        errori = []
        for d in cal:
            if d['Capo'] == d['Pass']: errori.append(f"Giorno {d['Giorno']}: **{d['Capo']}** doppio ruolo!")
        for n in set(capi):
            if capi.count(n) > 1: errori.append(f"Capo **{n}** compare {capi.count(n)} volte!")
        for n in set(pass_list):
            if pass_list.count(n) > 1: errori.append(f"Pass **{n}** compare {pass_list.count(n)} volte!")
        
        if errori:
            for err in errori: st.error(err)
        else:
            st.success("✅ GAME CLEAR: Nessun conflitto trovato!")
    st.markdown('</div>', unsafe_allow_html=True)
