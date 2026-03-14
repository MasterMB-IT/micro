import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS DEFINITIVO: FAR WEST & CANYON STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    /* SFONDO FORZATO - CANYON & FAR WEST */
    .stApp { 
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6)), 
                    url('https://cdn.pixabay.com/photo/2016/11/29/09/49/adventure-1868817_1280.jpg');
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
        color: #ffffff; 
    }

    /* Titolo con colori tramonto */
    .train-title {
        font-family: 'Orbitron', sans-serif; font-weight: 900; text-align: center;
        color: #ff8c00; text-shadow: 2px 2px 15px rgba(255, 140, 0, 0.8);
        font-size: 3rem; margin-bottom: 20px; letter-spacing: 4px;
    }

    /* Pannelli semi-trasparenti per far vedere lo sfondo */
    .stExpander { 
        background-color: rgba(20, 10, 5, 0.8) !important; 
        border: 2px solid #ff8c00 !important; 
        border-radius: 15px !important;
        backdrop-filter: blur(8px);
    }

    /* Bottoni ad alto contrasto */
    .btn-genera button { background: linear-gradient(45deg, #ff8c00, #ffd700) !important; color: black !important; font-family: 'Orbitron'; font-weight: 900; height: 60px !important; width: 100%; border: none !important; box-shadow: 0 4px 15px rgba(255,140,0,0.4) !important; }
    .btn-resetta button { background: linear-gradient(45deg, #d63031, #ff7675) !important; color: white !important; font-family: 'Orbitron'; font-weight: 900; height: 60px !important; width: 100%; border: none !important; }
    .btn-verifica button { background: linear-gradient(45deg, #2d3436, #636e72) !important; color: #ff8c00 !important; font-family: 'Orbitron'; font-weight: 900; height: 60px !important; width: 100%; border: 1px solid #ff8c00 !important; margin-top: 20px; }

    /* Card Giorno con effetto Vetro */
    .summary-card {
        background: rgba(0, 0, 0, 0.7); 
        border: 1px solid #ff8c00; 
        padding: 20px; 
        border-radius: 15px; 
        position: relative;
        transition: 0.3s ease;
        backdrop-filter: blur(3px);
    }
    .summary-card:hover { 
        transform: translateY(-5px) scale(1.02); 
        box-shadow: 0 10px 30px rgba(255, 140, 0, 0.4);
        background: rgba(30, 15, 5, 0.9);
    }
    
    .day-label { color: #ffd700; font-family: 'Orbitron'; font-weight: bold; text-align: center; margin-bottom: 10px; font-size: 1.2rem; }
    .name-text { font-size: 1rem; font-weight: 800; text-align: center; text-transform: uppercase; margin: 3px 0; }

    /* Ingranaggio Ghost */
    .popover-container { position: absolute; top: 8px; right: 8px; z-index: 100; }
    div[data-testid="stPopover"] > button { background: transparent !important; border: none !important; color: rgba(255,215,0,0.5) !important; font-size: 1.3rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE INVARIATO ---
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
st.markdown('<div class="train-title">🌵 AOSR CANYON EXPRESS 🌵</div>', unsafe_allow_html=True)

# --- CONFIGURAZIONE ---
with st.expander("🛠️ CONFIGURAZIONE SPEDIZIONE", expanded=True):
    c1, c2, c3 = st.columns([1, 1.5, 1.5])
    st.session_state['sel_mese'] = c1.selectbox("Mese", MESI_ITA, index=MESI_ITA.index(st.session_state['sel_mese']))
    st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    m_r3, m_r2 = db[db['Grado'] == "R3"]['Nome'].tolist(), db[db['Grado'] == "R2"]['Nome'].tolist()
    sel_r3, sel_r2 = c2.multiselect("Filtra R3", m_r3), c3.multiselect("Filtra R2", m_r2)

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("🐎 GENERA CAROVANA"):
        pool = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
        random.shuffle(pool)
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
        st.session_state['master_cal'] = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11: c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
            else:
                c = pool[p_idx % len(pool)]; p = pool[(p_idx+1) % len(pool)]
                p_idx += 2
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
    if st.button("🗑️ RESETTA TUTTO"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h2 style='text-align: center; font-family: Orbitron; color: #ffd700;'>{st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h2>", unsafe_allow_html=True)
    cols = st.columns(6)
    for i, r in enumerate(st.session_state['master_cal']):
        with cols[i % 6]:
            g_c = db[db['Nome']==r['Capo']]['Grado'].values[0] if r['Capo'] in all_names else "R3"
            g_p = db[db['Nome']==r['Pass']]['Grado'].values[0] if r['Pass'] in all_names else "R3"
            c_col, p_col = ("#ff4757" if g == "R5/R4" else "#2ed573" for g in [g_c, g_p])
            
            st.markdown(f"""
            <div class="summary-card">
                <div class="day-label">GG {r['Giorno']}</div>
                <div class="name-text" style="color:{c_col};">{r['Capo']}</div>
                <div style="color:#aaa; font-size:0.65rem; text-align:center; margin: 5px 0; font-weight: bold;">TRAIN PASS</div>
                <div class="name-text" style="color:{p_col};">{r['Pass']}</div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="popover-container">', unsafe_allow_html=True)
            with st.popover("⚙️"):
                if st.button("🔄 Scambia Ruoli", key=f"sw_{i}"):
                    st.session_state['master_cal'][i]['Capo'], st.session_state['master_cal'][i]['Pass'] = r['Pass'], r['Capo']
                    st.rerun()
                nc = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"c_{i}")
                np = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"p_{i}")
                if st.button("💾 Salva", key=f"s_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np}); st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

    # --- VERIFICA ---
    st.markdown('<div class="btn-verifica">', unsafe_allow_html=True)
    if st.button("🛡️ VERIFICA INTEGRITÀ CAROVANA"):
        cal = st.session_state['master_cal']
        capi, pass_list = [d['Capo'] for d in cal], [d['Pass'] for d in cal]
        errori = []
        for d in cal:
            if d['Capo'] == d['Pass']: errori.append(f"GG {d['Giorno']}: **{d['Capo']}** ha doppio ruolo!")
        for n in set(capi):
            if capi.count(n) > 1: errori.append(f"Capo **{n}** compare {capi.count(n)} volte!")
        for n in set(pass_list):
            if pass_list.count(n) > 1: errori.append(f"Pass **{n}** compare {pass_list.count(n)} volte!")
        if errori:
            for err in errori: st.error(err)
        else:
            st.success("✅ INTEGRITÀ CONFERMATA!")
    st.markdown('</div>', unsafe_allow_html=True)
