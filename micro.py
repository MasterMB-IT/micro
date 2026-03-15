import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Express - Definitive Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS: RIPRISTINO TOTALE E UNIFORMITÀ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@900&display=swap');

    .stApp { 
        background: linear-gradient(rgba(30, 20, 10, 0.85), rgba(15, 10, 5, 0.95)), 
                    url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; background-attachment: fixed;
    }

    .train-title {
        font-family: 'Rye', cursive; text-align: center; color: #ffcc66;
        text-shadow: 4px 4px 0px #4b2e1b; font-size: 3.5rem; margin-bottom: 20px;
    }

    /* UFFICIO ASSEGNAZIONI: STILE ORIGINALE */
    .ufficio-container {
        background: rgba(25, 25, 25, 0.5);
        border: 1px solid rgba(255, 204, 102, 0.4);
        border-radius: 10px; padding: 25px; margin-bottom: 30px;
    }

    /* CARDS: ALTEZZA FISSA E PROFONDITÀ */
    .pergamena-card {
        background: #fdf5e6; border: 2px solid #5d4037;
        padding: 15px; border-radius: 4px; color: #2b1d0e;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        box-shadow: 6px 6px 0px rgba(0,0,0,0.5);
        height: 220px !important; /* Forza altezza uguale per tutti */
        display: flex; flex-direction: column; justify-content: space-between;
        margin-bottom: 20px;
    }

    .day-badge {
        background: #8b0000; color: white; font-family: 'Montserrat', sans-serif;
        font-weight: 900; padding: 3px 10px; border-radius: 3px; font-size: 0.9rem;
        width: fit-content; margin-bottom: 10px; box-shadow: 2px 2px 0px #333;
    }

    .role-label { 
        color: #5d4037; font-size: 0.65rem; letter-spacing: 1px;
        font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800;
        border-bottom: 1px dashed rgba(93, 64, 55, 0.3); margin-top: 5px;
    }

    .name-text { 
        font-family: 'Special Elite', cursive; font-size: 0.95rem; font-weight: 900; 
        margin: 5px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }

    /* PULSANTI COLORATI */
    .stButton>button {
        width: 100% !important; border-radius: 5px !important;
        font-family: 'Montserrat', sans-serif !important; font-weight: 900 !important;
        height: 48px !important; text-transform: uppercase !important;
    }
    
    /* Hover Effects */
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }

    hr { border-top: 2px solid #ffcc66 !important; opacity: 0.2; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["G Erry", "Uncle g brother", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    data = [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + [{"Nome": n, "Grado": "R3"} for n in r3] + [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state: st.session_state['players_db'] = init_db()
if 'history' not in st.session_state: st.session_state['history'] = []
db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- TITOLO ---
st.markdown('<div class="train-title">🚂 AOSR EXPRESS</div>', unsafe_allow_html=True)

# --- PANEL CENTRALE ---
with st.container():
    st.markdown('<div class="ufficio-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffcc66; font-family:Rye; margin-bottom:20px;'>📜 REGISTRO DEL CAPOTRENO</h4>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
    with c1:
        st.session_state['sel_mese'] = st.selectbox("Periodo", MESI_ITA, index=2)
        st.session_state['sel_anno'] = st.number_input("Anno", 2024, 2030, 2026)
    with c2: s_r4 = st.multiselect("Sceriffi R5/R4", db[db['Grado']=="R5/R4"]['Nome'].tolist())
    with c3: s_r3 = st.multiselect("Banditi R3", db[db['Grado']=="R3"]['Nome'].tolist())
    with c4: s_r2 = st.multiselect("Fuorilegge R2", db[db['Grado']=="R2"]['Nome'].tolist())

    st.markdown("<br>", unsafe_allow_html=True)
    
    # PULSANTIERA
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("⚒️ GENERA CONVOGLIO"):
            pool_r4 = s_r4 if s_r4 else db[db['Grado']=="R5/R4"]['Nome'].tolist()
            pool_others = (s_r3 if s_r3 else db[db['Grado']=="R3"]['Nome'].tolist()) + (s_r2 if s_r2 else db[db['Grado']=="R2"]['Nome'].tolist())
            random.shuffle(pool_r4); random.shuffle(pool_others)
            num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
            st.session_state['master_cal'] = []
            p_idx = 0
            for g in range(1, num_gg + 1):
                if g <= 11: c, p = pool_r4[(g-1)%len(pool_r4)], pool_r4[g%len(pool_r4)]
                else: c, p = pool_others[p_idx % len(pool_others)], pool_others[(p_idx + 1) % len(pool_others)]; p_idx += 2
                st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
    
    with b2:
        if st.button("🔍 VERIFICA DOPPIONI"):
            if 'master_cal' in st.session_state:
                errors = [f"GG {r['Giorno']}" for r in st.session_state['master_cal'] if r['Capo'] == r['Pass']]
                if errors: st.error(f"⚠️ Errore! Stessa persona in: {', '.join(errors)}")
                else: st.success("✅ Tutto regolare, Sceriffo!")

    with b3:
        if st.button("🟩 ASSEGNAZIONE"):
            if 'master_cal' in st.session_state:
                st.session_state['history'].append({
                    "data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}",
                    "ts": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "cal": list(st.session_state['master_cal'])
                })
                st.toast("Calendario congelato in cronologia!")

    with b4:
        if st.button("🌵 RESET"):
            if 'master_cal' in st.session_state: del st.session_state['master_cal']
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- RENDERING GRIGLIA ---
def render_train_grid(data, is_history=False):
    num_cols = 7
    for i in range(0, len(data), num_cols):
        cols = st.columns(num_cols)
        chunk = data[i:i + num_cols]
        for j, r in enumerate(chunk):
            with cols[j]:
                is_r4 = any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome'])
                c_col = "#8b0000" if is_r4 else "#1b4d3e"
                st.markdown(f"""
                    <div class="pergamena-card">
                        <div>
                            <div class="day-badge">GG {r['Giorno']}</div>
                            <div class="role-label">CAPOTRENO</div>
                            <div class="name-text" style="color:{c_col};">🤠 {r['Capo']}</div>
                        </div>
                        <div>
                            <div class="role-label">PASSEGGERO</div>
                            <div class="name-text" style="color:#5d4037;">🐎 {r['Pass']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if not is_history:
                    with st.popover("⚙️", use_container_width=True):
                        nc = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"c_{r['Giorno']}")
                        np = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"p_{r['Giorno']}")
                        if st.button("SALVA", key=f"s_{r['Giorno']}"):
                            idx = next(idx for idx, it in enumerate(st.session_state['master_cal']) if it["Giorno"] == r['Giorno'])
                            st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np}); st.rerun()

# --- DISPLAY ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h3 style='text-align:center; color:#ffcc66; font-family:Rye;'>📅 {st.session_state['sel_mese'].upper()}</h3>", unsafe_allow_html=True)
    render_train_grid(st.session_state['master_cal'])

# --- CRONOLOGIA A GRIGLIA ---
if st.session_state['history']:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#ffcc66; font-family:Rye; text-align:center;'>📜 ARCHIVIO STORICO</h2>", unsafe_allow_html=True)
    for idx, item in enumerate(reversed(st.session_state['history'])):
        with st.expander(f"📦 CONVOGLIO: {item['data']} (Assegnato il {item['ts']})"):
            render_train_grid(item['cal'], is_history=True)
            if st.button("ELIMINA RECORD", key=f"del_{idx}"):
                st.session_state['history'].pop(-(idx+1)); st.rerun()
