import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS ELITE CON SFONDO FAR WEST/CANYON E ANIMAZIONI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    /* SFONDO FAR WEST/CANYON DEFINITIVO */
    .stApp { 
        background-color: #0b0e14;
        background-image: linear-gradient(rgba(11, 14, 20, 0.5), rgba(11, 14, 20, 0.7)), 
                          url('https://images.unsplash.com/photo-1533161358997-7c0934983b54?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff; 
    }

    .train-title {
        font-family: 'Orbitron', sans-serif; font-weight: 900; text-align: center;
        color: #ff9f43; /* Colore ambra/tramonto per contrasto Western */
        text-shadow: 0 0 20px rgba(255, 159, 67, 0.6);
        font-size: 2.8rem; margin-bottom: 30px; letter-spacing: 5px;
    }

    /* Expander e Input con overlay per leggibilità */
    .stExpander { 
        background-color: rgba(26, 31, 44, 0.85) !important; 
        border: 1px solid #ff9f43 !important; 
        border-radius: 15px !important;
        backdrop-filter: blur(5px); /* Sfocatura sfondo per leggibilità */
    }

    /* Bottoni Fluo Western-Style */
    .btn-genera button { background: linear-gradient(45deg, #2ed573, #7bed9f) !important; color: black !important; font-family: 'Orbitron'; font-weight: 900; height: 65px !important; width: 100%; border: none !important; box-shadow: 0 4px 15px rgba(46,213,115,0.4) !important; }
    .btn-resetta button { background: linear-gradient(45deg, #ff4757, #ff6b81) !important; color: white !important; font-family: 'Orbitron'; font-weight: 900; height: 65px !important; width: 100%; border: none !important; box-shadow: 0 4px 15px rgba(255,71,87,0.4) !important; }
    .btn-verifica button { background: linear-gradient(45deg, #ff9f43, #ff6b81) !important; color: white !important; font-family: 'Orbitron'; font-weight: 900; height: 65px !important; width: 100%; border: none !important; margin-top: 30px; box-shadow: 0 0 20px rgba(255,159,67,0.5) !important; }

    /* Card Animata con overlay per leggibilità */
    .summary-card {
        background: rgba(10, 10, 10, 0.75); border: 1px solid #444; padding: 20px; 
        border-radius: 15px; position: relative; border-top: 3px solid #ff9f43;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(5px); /* Sfocatura sfondo per leggibilità */
    }
    .summary-card:hover { transform: scale(1.05); border-color: #ff9f43; box-shadow: 0 10px 40px rgba(255, 159, 67, 0.5); background: rgba(20, 20, 20, 0.9); }
    
    .day-label { color: #ff9f43; font-family: 'Orbitron'; font-weight: bold; text-align: center; margin-bottom: 12px; font-size: 1.1rem; }
    .name-text { font-size: 1rem; font-weight: 800; text-align: center; text-transform: uppercase; margin: 4px 0; letter-spacing: 1px; }

    /* Ingranaggio Ghost */
    .popover-container { position: absolute; top: 10px; right: 10px; z-index: 100; }
    div[data-testid="stPopover"] > button { background: transparent !important; border: none !important; color: rgba(255,255,255,0.4) !important; font-size: 1.2rem !important; }
    div[data-testid="stPopover"] > button:hover { color: #ff9f43 !important; transform: rotate(90deg); transition: 0.3s; }
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

# --- UI ---
st.markdown('<div class="train-title">🚄 AOSR EXPRESS ELITE</div>', unsafe_allow_html=True)

with st.expander("🛠️ CONFIGURAZIONE TRENO", expanded=True):
    c1, c2, c3 = st.columns([1, 1.5, 1.5])
    st.session_state['sel_mese'] = c1.selectbox("Seleziona Mese", MESI_ITA, index=MESI_ITA.index(st.session_state['sel_mese']))
    st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    m_r3, m_r2 = db[db['Grado'] == "R3"]['Nome'].tolist(), db[db['Grado'] == "R2"]['Nome'].tolist()
    sel_r3, sel_r2 = c2.multiselect("Filtra R3", m_r3), c3.multiselect("Filtra R2", m_r2)

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("🚀 GENERA NUOVO CALENDARIO"):
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
    if st.button("🗑️ RESETTA SISTEMA"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h2 style='text-align: center; font-family: Orbitron; color: white;'>{st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h2>", unsafe_allow_html=True)
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
                <div style="color:#888; font-size:0.65rem; text-align:center; margin: 5px 0; font-weight: bold;">TRAIN PASS</div>
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

    # --- VERIFICA INTEGRITÀ ---
    st.markdown('<div class="btn-verifica">', unsafe_allow_html=True)
    if st.button("🛡️ VERIFICA INTEGRITÀ TRENO"):
        cal = st.session_state['master_cal']
        capi, pass_list = [d['Capo'] for d in cal], [d['Pass'] for d in cal]
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
            st.success("✅ INTEGRITÀ CONFERMATA: Nessun doppio turno trovato!")
    st.markdown('</div>', unsafe_allow_html=True)
