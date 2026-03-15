import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Express - Dashboard Elite", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS: IL CAPOLAVORO VISIVO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@700;900&display=swap');

    .stApp { 
        background: linear-gradient(rgba(20, 15, 10, 0.85), rgba(10, 5, 0, 0.98)), 
                    url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; background-attachment: fixed;
    }

    .train-title {
        font-family: 'Rye', cursive; text-align: center; color: #ffcc66;
        text-shadow: 3px 3px 0px #4b2e1b; font-size: 3.8rem; margin-bottom: 25px;
    }

    /* RIQUADRO SALA COMANDO (BELLISSIMO) */
    .sala-comando {
        background: rgba(15, 15, 15, 0.8);
        border: 2px solid #ffcc66;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 40px;
        box-shadow: 0 0 20px rgba(255, 204, 102, 0.2), inset 0 0 15px rgba(0,0,0,0.5);
    }

    .sezione-titolo {
        font-family: 'Montserrat', sans-serif; font-weight: 900; color: #ffcc66;
        text-transform: uppercase; letter-spacing: 2px; font-size: 1.1rem;
        margin-bottom: 20px; border-bottom: 1px solid rgba(255, 204, 102, 0.3);
        padding-bottom: 10px;
    }

    /* CARDS DINAMICHE */
    .pergamena-card {
        background: #fdf5e6; border: 2px solid #5d4037;
        padding: 12px; border-radius: 4px; color: #2b1d0e;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        box-shadow: 4px 4px 0px rgba(0,0,0,0.6);
        display: flex; flex-direction: column; justify-content: space-between;
        margin-bottom: 15px; transition: 0.3s;
    }

    /* Altezze calibrate */
    .h-norm { height: 210px !important; }
    .h-comp { height: 145px !important; padding: 8px !important; }

    .day-badge {
        background: #8b0000; color: white; font-family: 'Montserrat', sans-serif;
        font-weight: 900; padding: 2px 8px; border-radius: 3px; font-size: 0.8rem;
        width: fit-content;
    }

    .role-label { 
        color: #5d4037; font-size: 0.6rem; letter-spacing: 1px;
        font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800;
        border-bottom: 1px dashed rgba(93, 64, 55, 0.3); margin-top: 4px;
    }

    .name-text { 
        font-family: 'Special Elite', cursive; font-size: 0.85rem; font-weight: 900; 
        margin: 2px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }
    
    .name-text-comp { font-size: 0.75rem !important; }

    /* PULSANTI */
    .stButton>button {
        width: 100% !important; border-radius: 8px !important;
        font-family: 'Montserrat', sans-serif !important; font-weight: 900 !important;
        height: 45px !important; text-transform: uppercase !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    
    /* Colori Pulsanti */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) button { background: #333 !important; color: white !important; } /* Genera */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) button { background: #2c3e50 !important; color: #5bc0de !important; } /* Verifica */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button { background: #1b4d3e !important; color: #2ecc71 !important; border: 1px solid #2ecc71 !important; } /* Assegna */
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button { background: #4a1a1a !important; color: #e74c3c !important; } /* Reset */

    hr { border-top: 2px solid #ffcc66 !important; opacity: 0.2; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE INIZIALE ---
def get_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["G Erry", "Uncle g brother", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    return pd.DataFrame([{"Nome": n, "Grado": "R5/R4"} for n in leaders] + [{"Nome": n, "Grado": "R3"} for n in r3] + [{"Nome": n, "Grado": "R2"} for n in r2])

if 'players_db' not in st.session_state: st.session_state['players_db'] = get_db()
if 'history' not in st.session_state: st.session_state['history'] = []
db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- UI ---
st.markdown('<div class="train-title">🚂 AOSR EXPRESS</div>', unsafe_allow_html=True)

# --- RIQUADRO SALA COMANDO ---
st.markdown('<div class="sala-comando">', unsafe_allow_html=True)
st.markdown('<div class="sezione-titolo">⚙️ PANNELLO DI CONTROLLO</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
with c1:
    st.session_state['sel_mese'] = st.selectbox("Periodo", MESI_ITA, index=datetime.now().month-1)
    st.session_state['sel_anno'] = st.number_input("Anno", 2024, 2030, 2026)
with c2: s_r4 = st.multiselect("Sceriffi R5/R4", db[db['Grado']=="R5/R4"]['Nome'].tolist())
with c3: s_r3 = st.multiselect("Banditi R3", db[db['Grado']=="R3"]['Nome'].tolist())
with c4: s_r2 = st.multiselect("Fuorilegge R2", db[db['Grado']=="R2"]['Nome'].tolist())

st.markdown("<br>", unsafe_allow_html=True)

# PULSANTIERA
b1, b2, b3, b4 = st.columns(4)
with b1:
    if st.button("⚒️ GENERA"):
        p_r4 = s_r4 if s_r4 else db[db['Grado']=="R5/R4"]['Nome'].tolist()
        p_oth = (s_r3 if s_r3 else db[db['Grado']=="R3"]['Nome'].tolist()) + (s_r2 if s_r2 else db[db['Grado']=="R2"]['Nome'].tolist())
        random.shuffle(p_r4); random.shuffle(p_oth)
        num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
        st.session_state['master_cal'] = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11: c, p = p_r4[(g-1)%len(p_r4)], p_r4[g%len(p_r4)]
            else: c, p = p_oth[p_idx % len(p_oth)], p_oth[(p_idx + 1) % len(p_oth)]; p_idx += 2
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})

with b2:
    if st.button("🔍 VERIFICA"):
        if 'master_cal' in st.session_state:
            err = [f"GG {r['Giorno']}" for r in st.session_state['master_cal'] if r['Capo'] == r['Pass']]
            if err: st.error(f"Conflitti in: {', '.join(err)}")
            else: st.success("Ispezione vagoni: OK!")

with b3:
    if st.button("🟩 ASSEGNAZIONE"):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({"data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}", "ts": datetime.now().strftime("%d/%m/%Y %H:%M"), "cal": list(st.session_state['master_cal'])})
            st.toast("Calendario salvato nell'Archivio!")

with b4:
    if st.button("🌵 RESET"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()

st.markdown('<div style="margin-top:20px; border-top:1px solid rgba(255,204,102,0.1); padding-top:15px;">', unsafe_allow_html=True)
view_mode = st.toggle("🎞️ VISIONE D'INSIEME (Cards più piccole)", value=False)
st.markdown('</div></div>', unsafe_allow_html=True)

# --- RENDERING GRIGLIA ---
def draw_grid(data, compact=False, is_history=False):
    n_cols = 10 if compact else 7
    h_style = "h-comp" if compact else "h-norm"
    n_style = "name-text-comp" if compact else ""
    
    for i in range(0, len(data), n_cols):
        cols = st.columns(n_cols)
        chunk = data[i:i + n_cols]
        for j, r in enumerate(chunk):
            with cols[j]:
                is_r4 = any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome'])
                c_col = "#8b0000" if is_r4 else "#1b4d3e"
                st.markdown(f"""
                    <div class="pergamena-card {h_style}">
                        <div>
                            <div class="day-badge">GG {r['Giorno']}</div>
                            <div class="role-label">CAPO</div>
                            <div class="name-text {n_style}" style="color:{c_col};">🤠 {r['Capo']}</div>
                        </div>
                        <div>
                            <div class="role-label">PASS</div>
                            <div class="name-text {n_style}" style="color:#5d4037;">🐎 {r['Pass']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if not is_history and not compact:
                    with st.popover("⚙️", use_container_width=True):
                        nc = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"c_{r['Giorno']}")
                        np = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"p_{r['Giorno']}")
                        if st.button("OK", key=f"s_{r['Giorno']}"):
                            idx = next(idx for idx, it in enumerate(st.session_state['master_cal']) if it["Giorno"] == r['Giorno'])
                            st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np}); st.rerun()

if 'master_cal' in st.session_state:
    st.markdown(f"<h3 style='text-align:center; color:#ffcc66; font-family:Rye;'>📅 {st.session_state['sel_mese'].upper()}</h3>", unsafe_allow_html=True)
    draw_grid(st.session_state['master_cal'], compact=view_mode)

if st.session_state['history']:
    st.markdown("<br><hr><h2 style='color:#ffcc66; font-family:Rye; text-align:center;'>📜 ARCHIVIO STORICO</h2>", unsafe_allow_html=True)
    for idx, item in enumerate(reversed(st.session_state['history'])):
        with st.expander(f"📦 CONVOGLIO: {item['data']} - {item['ts']}"):
            draw_grid(item['cal'], compact=True, is_history=True)
            if st.button("ELIMINA ARCHIVIO", key=f"del_{idx}"):
                st.session_state['history'].pop(-(idx+1)); st.rerun()
