import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS ELITE CON SFONDO TRENO STILIZZATO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    /* SFONDO TRENO FAR WEST STILIZZATO */
    .stApp { 
        background-color: #0b0e14;
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.7)), 
                          url('https://images.unsplash.com/photo-1535970854227-28f4df670860?q=80&w=1920&auto=format&fit=crop');
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        color: #ffffff; 
    }

    .train-title {
        font-family: 'Orbitron', sans-serif; font-weight: 900; text-align: center;
        color: #00c8ff; text-shadow: 0 0 20px rgba(0, 200, 255, 0.6);
        font-size: 3rem; margin-bottom: 30px; letter-spacing: 5px;
    }

    /* Expander per Gestione Nomi e Configurazione */
    .stExpander { 
        background-color: rgba(17, 21, 30, 0.9) !important; 
        border: 1px solid #00c8ff !important; 
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
    }

    /* Bottoni */
    .btn-genera button { background: linear-gradient(45deg, #2ed573, #7bed9f) !important; color: black !important; font-family: 'Orbitron'; font-weight: 900; height: 65px !important; width: 100%; border: none !important; box-shadow: 0 4px 15px rgba(46,213,115,0.4) !important; }
    .btn-resetta button { background: linear-gradient(45deg, #ff4757, #ff6b81) !important; color: white !important; font-family: 'Orbitron'; font-weight: 900; height: 65px !important; width: 100%; border: none !important; }
    .btn-verifica button { background: linear-gradient(45deg, #00c8ff, #005f73) !important; color: white !important; font-family: 'Orbitron'; font-weight: 900; height: 60px !important; width: 100%; border: none !important; margin-top: 20px; }

    /* Card Giorno */
    .summary-card {
        background: rgba(10, 10, 10, 0.85); border: 1px solid #333; padding: 20px; 
        border-radius: 15px; position: relative; border-top: 3px solid #00c8ff;
        transition: 0.3s ease;
        backdrop-filter: blur(5px);
    }
    .summary-card:hover { transform: scale(1.05); border-color: #00c8ff; box-shadow: 0 10px 40px rgba(0, 200, 255, 0.5); }
    
    .day-label { color: #00c8ff; font-family: 'Orbitron'; font-weight: bold; text-align: center; margin-bottom: 12px; font-size: 1.1rem; }
    .name-text { font-size: 1rem; font-weight: 800; text-align: center; text-transform: uppercase; margin: 4px 0; }

    /* Popover Ingranaggio */
    .popover-container { position: absolute; top: 10px; right: 10px; z-index: 100; }
    div[data-testid="stPopover"] > button { background: transparent !important; border: none !important; color: rgba(255,255,255,0.3) !important; font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE DINAMICO (SESSION STATE) ---
if 'players_data' not in st.session_state:
    st.session_state['players_data'] = {
        "R5/R4": "Hool (R5), MASTER (R4), Le 12 Scimmie (R4), Sagittarius A1 (R4), Starbetty (R4), PEPPE (R4), Ricky Around (R4), uncle g (R4), 09ALEX24 (R4), ShinyPasta (R4), Wall 7 (R4)",
        "R3": "G Erry, Uncle g brother, Cane Avvoltoio, Ghandal, Aryron, Tricheco, Maメツ, NOVEMBERGENZ, Lalla 96, Whale Panda, GennaroM, EchoZero, EDDward, AMY, Resilienza, Ana Bunny, Giuseppec84, Benito Muschiolini, Pandino19, xFlotchy, MX63, holdfast, Ghost, BadBigBoss, Stefano00000, PakII, BANDOLERO26, BlOOdyBlade, Whale hunter Levve, Aresxxx, KingGruffalo, Hulkspakka, Joseone, ImAde, Nysbie, LeFada13, Skifetto, SPio24, TomEnergy, Markus Defender, Sho0t3r, Wolf006, Zokra, perseusxxx, Bendico, Obbyy, ArLes, Fatz87, cruel neve, Trivellatore, Osgh00, Slowfia ABOH, Pontatinatore, 27Francesco, MissDrinks, krompir, MaledettO",
        "R2": "teomadh, Bossnico, Valecit, FarmerHool, camiiiii 08, Doctor team, Yass081, Nuorifleming, Vergabrio, Frenk70, Comandante Maveric, Thor9000, MrBolly, BustaMaki, Ritardato, StUnTmArK, MONKEY D LUFFY 20, CineSalentino, Danylo98, Ezechielefabianino, BRNcommando, LEONIDA, elchicogyot, erer1000, Pupisnic, Backfire1, AnarchyBG, Fabrizio1987, JurdanS, WiseR9, Infinity8080"
    }

# --- SEZIONE GESTIONE NOMI ---
with st.expander("👥 GESTIONE EQUIPAGGIO (Modifica i nomi)", expanded=False):
    st.write("Modifica le liste qui sotto separando i nomi con una virgola.")
    col_ed1, col_ed2, col_ed3 = st.columns(3)
    
    new_r4 = col_ed1.text_area("Capitani (R5/R4)", st.session_state['players_data']["R5/R4"], height=150)
    new_r3 = col_ed2.text_area("Passeggeri R3", st.session_state['players_data']["R3"], height=150)
    new_r2 = col_ed3.text_area("Passeggeri R2", st.session_state['players_data']["R2"], height=150)
    
    if st.button("💾 SALVA MODIFICHE"):
        st.session_state['players_data']["R5/R4"] = new_r4
        st.session_state['players_data']["R3"] = new_r3
        st.session_state['players_data']["R2"] = new_r2
        st.rerun()

# Funzioni per pulire le liste
def get_clean_list(key):
    return [n.strip() for n in st.session_state['players_data'][key].split(",") if n.strip()]

list_r4 = get_clean_list("R5/R4")
list_r3 = get_clean_list("R3")
list_r2 = get_clean_list("R2")
all_names = sorted(list_r4 + list_r3 + list_r2)

# --- UI PRINCIPALE ---
st.markdown('<div class="train-title">🚄 AOSR EXPRESS ELITE</div>', unsafe_allow_html=True)

with st.expander("🛠️ CONFIGURAZIONE TRENO", expanded=True):
    c1, c2, c3 = st.columns([1, 1.5, 1.5])
    sel_mese = c1.selectbox("Seleziona Mese", MESI_ITA, index=datetime.now().month - 1)
    sel_anno = c1.number_input("Anno", 2024, 2030, 2026)
    sel_r3 = c2.multiselect("Filtra R3", list_r3)
    sel_r2 = c3.multiselect("Filtra R2", list_r2)

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("🚀 GENERA NUOVO CALENDARIO"):
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
    if st.button("🗑️ RESETTA SISTEMA"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h2 style='text-align: center; font-family: Orbitron; color: white;'>{sel_mese.upper()} {sel_anno}</h2>", unsafe_allow_html=True)
    cols = st.columns(6)
    for i, r in enumerate(st.session_state['master_cal']):
        with cols[i % 6]:
            c_col = "#ff4757" if r['Capo'] in list_r4 else "#2ed573"
            p_col = "#ff4757" if r['Pass'] in list_r4 else "#2ed573"
            
            st.markdown(f"""
            <div class="summary-card">
                <div class="day-label">GG {r['Giorno']}</div>
                <div class="name-text" style="color:{c_col};">{r['Capo']}</div>
                <div style="color:#666; font-size:0.65rem; text-align:center; margin: 5px 0; font-weight: bold;">TRAIN PASS</div>
                <div class="name-text" style="color:{p_col};">{r['Pass']}</div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="popover-container">', unsafe_allow_html=True)
            with st.popover("⚙️"):
                nc = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"c_{i}")
                np = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"p_{i}")
                if st.button("💾 Salva", key=f"s_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np}); st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

    # --- VERIFICA ---
    st.markdown('<div class="btn-verifica">', unsafe_allow_html=True)
    if st.button("🛡️ VERIFICA INTEGRITÀ TRENO"):
        cal = st.session_state['master_cal']
        capi = [d['Capo'] for d in cal]
        pass_list = [d['Pass'] for d in cal]
        errori = []
        for d in cal:
            if d['Capo'] == d['Pass']: errori.append(f"GG {d['Giorno']}: **{d['Capo']}** è in doppio ruolo!")
        for n in set(capi):
            if capi.count(n) > 1: errori.append(f"Capo **{n}** compare {capi.count(n)} volte!")
        for n in set(pass_list):
            if pass_list.count(n) > 1: errori.append(f"Pass **{n}** compare {pass_list.count(n)} volte!")
        
        if errori:
            for err in errori: st.error(err)
        else:
            st.success("✅ INTEGRITÀ CONFERMATA!")
    st.markdown('</div>', unsafe_allow_html=True)
