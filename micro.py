import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Wild West", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS STILE FAR WEST CALDO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&display=swap');

    .stApp { 
        background: linear-gradient(rgba(46, 34, 21, 0.6), rgba(20, 15, 10, 0.8)), 
                    url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop');
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    .train-title {
        font-family: 'Special Elite', cursive;
        text-align: center; color: #ffcc66;
        text-shadow: 3px 3px 0px #4b2e1b;
        font-size: 2.5rem; margin-bottom: 10px; width: 100%;
    }

    .summary-card {
        background: #f4e4bc; border: 2px solid #8b5a2b; 
        padding: 10px 5px; border-radius: 2px; 
        position: relative; box-shadow: 3px 3px 10px rgba(0,0,0,0.5);
        color: #2b1d0e; margin-bottom: 10px; min-height: 140px;
    }

    .diapo-card {
        background: #f4e4bc; border: 2px solid #8b5a2b; 
        padding: 8px 4px; border-radius: 4px; 
        text-align: center; box-shadow: 4px 4px 8px rgba(0,0,0,0.4);
        margin-bottom: 8px; min-height: 85px; 
        display: flex; flex-direction: column; justify-content: center;
    }

    .diapo-day { 
        color: #8b0000; font-family: 'Special Elite'; font-weight: bold; 
        font-size: 0.8rem; margin-bottom: 4px; border-bottom: 1px solid rgba(139, 90, 43, 0.4);
    }
    
    .diapo-name { 
        font-family: 'Special Elite'; font-size: 0.7rem; font-weight: 800; 
        margin: 2px 0; line-height: 1.2; text-transform: uppercase;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }

    .day-label { color: #8b0000; font-family: 'Special Elite'; font-weight: bold; font-size: 0.9rem; border-bottom: 1px dashed #8b5a2b; }
    .name-text { font-family: 'Special Elite'; font-size: 0.85rem; font-weight: 800; text-align: center; text-transform: uppercase; margin: 2px 0; }
    .role-label { color: #8b5a2b; font-size: 0.6rem; text-align: center; font-family: 'Special Elite'; text-transform: uppercase; }

    .btn-genera button { background: #d4a373 !important; color: #2b1d0e !important; font-family: 'Special Elite'; font-weight: bold; border: 2px solid #4b3621 !important; height: 45px !important; }
    .btn-resetta button { background: #a44a3f !important; color: #f1e5ac !important; font-family: 'Special Elite'; border: 2px solid #4b1d1d !important; height: 45px !important; }
    
    /* Stile Pulsante Controllo */
    .btn-controllo button { 
        background: #5d4037 !important; color: #ffcc66 !important; 
        font-family: 'Special Elite'; border: 2px solid #ffcc66 !important;
        width: 100%; margin-top: 20px; font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    data = [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + [{"Nome": n, "Grado": "R3"} for n in r3] + [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state:
    st.session_state['players_db'] = init_db()
    st.session_state['sel_mese'] = MESI_ITA[datetime.now().month - 1]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- TITOLO ---
st.markdown('<div class="train-title">🚂 AOSR EXPRESS</div>', unsafe_allow_html=True)

# --- CONFIGURAZIONE ---
with st.expander("📜 REGISTRO DEL CAPOTRENO", expanded=True):
    c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
    st.session_state['sel_mese'] = c1.selectbox("Periodo", MESI_ITA, index=MESI_ITA.index(st.session_state['sel_mese']))
    st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    
    m_leaders = db[db['Grado'] == "R5/R4"]['Nome'].tolist()
    m_r3 = db[db['Grado'] == "R3"]['Nome'].tolist()
    m_r2 = db[db['Grado'] == "R2"]['Nome'].tolist()
    
    sel_leaders = c2.multiselect("Sceriffi R5/R4", m_leaders)
    sel_r3 = c3.multiselect("Banditi R3", m_r3)
    sel_r2 = c4.multiselect("Fuorilegge R2", m_r2)

col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("⚒️ GENERA"):
        pool_leaders = sel_leaders if sel_leaders else m_leaders
        pool_others = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
        random.shuffle(pool_others)
        num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
        st.session_state['master_cal'] = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11: 
                c = pool_leaders[(g-1)%len(pool_leaders)]
                p = pool_leaders[g%len(pool_leaders)]
            else:
                c = pool_others[p_idx % len(pool_others)]
                p = pool_others[(p_idx+1) % len(pool_others)]
                p_idx += 2
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
    if st.button("🏜️ RESET"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_b3:
    modo_diapositiva = st.toggle("🎞️ DIAPOSITIVA (Vista Totale)", value=False)

# --- CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h3 style='text-align: center; font-family: Special Elite; color: #ffcc66; margin-bottom: 5px;'>📅 {st.session_state['sel_mese'].upper()}</h3>", unsafe_allow_html=True)
    
    if modo_diapositiva:
        cols = st.columns(8)
        for i, r in enumerate(st.session_state['master_cal']):
            with cols[i % 8]:
                c_col = "#8b0000" if any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                p_col = "#8b0000" if any(db[(db['Nome'] == r['Pass']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                st.markdown(f"""
                <div class="diapo-card">
                    <div class="diapo-day">GG {r['Giorno']}</div>
                    <div class="diapo-name" style="color:{c_col};">C: {r['Capo']}</div>
                    <div class="diapo-name" style="color:{p_col};">P: {r['Pass']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        cols = st.columns(7)
        for i, r in enumerate(st.session_state['master_cal']):
            with cols[i % 7]:
                c_col = "#8b0000" if any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                p_col = "#8b0000" if any(db[(db['Nome'] == r['Pass']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                st.markdown(f"""
                <div class="summary-card">
                    <div class="day-label">GG {r['Giorno']}</div>
                    <div class="role-label">CAPO</div>
                    <div class="name-text" style="color:{c_col};">🤠 {r['Capo']}</div>
                    <div class="role-label">PASS</div>
                    <div class="name-text" style="color:{p_col};">🐎 {r['Pass']}</div>
                """, unsafe_allow_html=True)
                with st.popover("⚙️"):
                    nc = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"c_{i}")
                    np = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"p_{i}")
                    if st.button("💾 Salva", key=f"s_{i}"):
                        st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np}); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # --- NUOVO PULSANTE DI CONTROLLO FINALE ---
    st.markdown("---")
    st.markdown('<div class="btn-controllo">', unsafe_allow_html=True)
    if st.button("🔍 ISPEZIONE INTEGRITÀ CARICO"):
        cal = st.session_state['master_cal']
        capi = [d['Capo'] for d in cal]
        passy = [d['Pass'] for d in cal]
        
        # Trova duplicati
        dup_capi = list(set([x for x in capi if capi.count(x) > 1]))
        dup_pass = list(set([x for x in passy if passy.count(x) > 1]))
        
        if not dup_capi and not dup_pass:
            st.success("✅ NESSUN DUPLICATO! Il convoglio è bilanciato alla perfezione.")
        else:
            if dup_capi:
                st.error(f"⚠️ CAPITRENO DOPPI: {', '.join(dup_capi)}")
            if dup_pass:
                st.warning(f"⚠️ PASSEGGERI DOPPI: {', '.join(dup_pass)}")
    st.markdown('</div>', unsafe_allow_html=True)
