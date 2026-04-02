import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Deluxe Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

GIORNI_SETTIMANA = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

DB_FILE = "cronologia_treni.json"

# --- FUNZIONI DI PERSISTENZA ---
def save_history():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state['history'], f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# --- INIZIALIZZAZIONE SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state['history'] = load_history()

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["Uncle g", "G Erry", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    
    data = [{"Nome": "---", "Grado": "Nessuno"}] + \
           [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + \
           [{"Nome": n, "Grado": "R3"} for n in r3] + \
           [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state: st.session_state['players_db'] = init_db()
db = st.session_state['players_db']

leaders_list = sorted(db[db['Grado'] == "R5/R4"]['Nome'].tolist())
all_names_list = sorted(db['Nome'].tolist())

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@700;900&display=swap');
    .stApp { background: linear-gradient(rgba(30, 20, 10, 0.8), rgba(15, 10, 5, 0.95)), url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop'); background-size: cover; background-attachment: fixed; }
    .train-title { font-family: 'Rye', cursive; text-align: center; color: #ffcc66; text-shadow: 5px 5px 0px #4b2e1b; font-size: 4rem; margin-bottom: 20px; }
    .sala-comando { background: rgba(25, 15, 5, 0.85); backdrop-filter: blur(10px); border: 2px solid #ffcc66; border-radius: 20px; padding: 30px; box-shadow: 0px 15px 50px rgba(0,0,0,0.9); margin-bottom: 40px; border-top: 5px solid #ffcc66; }
    .section-header { font-family: 'Rye', cursive; color: #ffcc66; font-size: 1.8rem; margin-bottom: 25px; }
    .summary-card { background: #fdf5e6; border: 3px solid #5d4037; padding: 12px 8px; border-radius: 6px; box-shadow: 6px 6px 12px rgba(0,0,0,0.5); color: #2b1d0e; margin-bottom: 5px; background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png'); display: flex; flex-direction: column; }
    .h-norm { height: 235px !important; }
    .h-comp { height: 150px !important; padding: 5px 6px !important; }
    .day-badge { background: #8b0000; color: white; font-family: 'Montserrat', sans-serif; font-weight: 900; padding: 2px 8px; border-radius: 3px; font-size: 0.8rem; width: fit-content; margin-bottom: 5px; }
    .role-label { color: #5d4037; font-size: 0.65rem; font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800; border-bottom: 1px solid rgba(93, 64, 55, 0.2); margin-top: 5px; }
    .name-text { font-family: 'Special Elite', cursive; font-size: 0.9rem; font-weight: 900; text-transform: uppercase; border-left: 4px solid #d4a373; padding-left: 8px; overflow: hidden; white-space: nowrap; }
    .stButton>button { border-radius: 8px !important; font-family: 'Rye', cursive !important; font-size: 1.1rem !important; height: 50px !important; border: 3px solid #2b1d0e !important; width: 100%; }
    .btn-genera button { background: #d4a373 !important; color: #2b1d0e !important; }
    .btn-vuoto button { background: #5a5a5a !important; color: white !important; border: 2px solid #ffffff !important; }
    .btn-verifica button { background: #5d4037 !important; color: #ffcc66 !important; }
    .btn-assegna button { background: #1b4d3e !important; color: #2ecc71 !important; }
    .btn-resetta button { background: #a44a3f !important; color: white !important; }
    div[data-testid="stPopover"] > button { height: 28px !important; width: 100% !important; margin-top: 5px !important; font-size: 0.8rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE GIORNO SETTIMANA ---
def get_weekday_name(day, month_name, year):
    month_idx = MESI_ITA.index(month_name) + 1
    dt = datetime(year, month_idx, day)
    return GIORNI_SETTIMANA[dt.weekday()]

# --- RENDERING GRIGLIA ---
def draw_grid(data, compact=False, is_history=False, key_prefix="grid"):
    n_cols = 10 if compact else 7
    h_cls = "h-comp" if compact else "h-norm"
    opts_leaders = ["---"] + leaders_list
    opts_all = ["---"] + all_names_list

    for i in range(0, len(data), n_cols):
        cols = st.columns(n_cols)
        chunk = data[i:i + n_cols]
        for j, r in enumerate(chunk):
            giorno = r['Giorno']
            wd = get_weekday_name(giorno, st.session_state['sel_mese'], st.session_state['sel_anno'])
            
            with cols[j]:
                c_c = "#8b0000" if any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                p_c = "#8b0000" if any(db[(db['Nome'] == r['Pass']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                if r['Capo'] == "---": c_c = "#888888"
                if r['Pass'] == "---": p_c = "#888888"

                st.markdown(f"""
                <div class="summary-card {h_cls}">
                    <div class="day-badge">{wd} {giorno}</div>
                    <div class="role-label">CAPOTRENO {"⭐" if giorno <= 11 else ""}</div>
                    <div class="name-text" style="color:{c_c};">{r['Capo']}</div>
                    <div class="role-label">PASSEGGERO</div>
                    <div class="name-text" style="color:{p_c};">{r['Pass']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if not is_history and not compact:
                    with st.popover("⚙️ MODIFICA"):
                        # CAPOTRENO: Solo Leader se GG <= 11
                        # PASSEGGERO: Sempre Tutti
                        opts_capo = opts_leaders if giorno <= 11 else opts_all
                        opts_pass = opts_all
                        
                        idx_c = opts_capo.index(r['Capo']) if r['Capo'] in opts_capo else 0
                        idx_p = opts_pass.index(r['Pass']) if r['Pass'] in opts_pass else 0
                        
                        nc = st.selectbox(f"Capo ({wd} {giorno})", opts_capo, index=idx_c, key=f"c_{key_prefix}_{giorno}")
                        np = st.selectbox(f"Pass ({wd} {giorno})", opts_pass, index=idx_p, key=f"p_{key_prefix}_{giorno}")
                        
                        if st.button("SALVA", key=f"s_{key_prefix}_{giorno}"):
                            for idx, item in enumerate(st.session_state['master_cal']):
                                if item["Giorno"] == giorno:
                                    st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np})
                                    break
                            st.rerun()

# --- TITOLO E PANNELLO ---
st.markdown('<div class="train-title">🚂 AOSR EXPRESS</div>', unsafe_allow_html=True)
st.markdown('<div class="sala-comando">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📜 UFFICIO ASSEGNAZIONI</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
with c1:
    st.session_state['sel_mese'] = st.selectbox("📅 MESE", MESI_ITA, index=datetime.now().month - 1)
    st.session_state['sel_anno'] = st.number_input("📆 ANNO", 2024, 2030, 2026)
with c2: sel_leaders = st.multiselect("🤠 R5/R4", leaders_list)
with c3: sel_r3 = st.multiselect("🌵 R3", db[db['Grado'] == "R3"]['Nome'].tolist())
with c4: sel_r2 = st.multiselect("🐎 R2", db[db['Grado'] == "R2"]['Nome'].tolist())

st.markdown('<div style="margin-top:30px; border-top:1px solid rgba(255,204,102,0.2); padding-top:20px;">', unsafe_allow_html=True)
cb1, cb1b, cb2, cb3, cb4 = st.columns(5)

with cb1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("⚒️ GENERA AUTO", use_container_width=True):
        p_l = sel_leaders if sel_leaders else leaders_list
        p_o = (sel_r3 if sel_r3 else db[db['Grado']=="R3"]['Nome'].tolist()) + (sel_r2 if sel_r2 else db[db['Grado']=="R2"]['Nome'].tolist())
        random.shuffle(p_l); random.shuffle(p_o)
        num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
        st.session_state['master_cal'] = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11: c, p = p_l[(g-1)%len(p_l)], p_o[g%len(p_o)] # Passeggero ora attinge da tutti
            else: c, p = p_o[p_idx % len(p_o)], p_o[(p_idx+1) % len(p_o)]; p_idx += 2
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
    st.markdown('</div>', unsafe_allow_html=True)

with cb1b:
    st.markdown('<div class="btn-vuoto">', unsafe_allow_html=True)
    if st.button("🆕 CREA VUOTO", use_container_width=True):
        num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
        st.session_state['master_cal'] = [{"Giorno": g, "Capo": "---", "Pass": "---"} for g in range(1, num_gg + 1)]
    st.markdown('</div>', unsafe_allow_html=True)

with cb2:
    st.markdown('<div class="btn-verifica">', unsafe_allow_html=True)
    if st.button("🔍 VERIFICA", use_container_width=True):
        if 'master_cal' in st.session_state:
            err_g = [f"GG {r['Giorno']}" for r in st.session_state['master_cal'] if r['Giorno'] <= 11 and r['Capo'] not in leaders_list and r['Capo'] != "---"]
            err_d = [f"GG {r['Giorno']}" for r in st.session_state['master_cal'] if r['Capo'] == r['Pass'] and r['Capo'] != "---"]
            if err_g: st.error(f"Capotreno non R4/R5 (GG 1-11): {', '.join(err_g)}")
            if err_d: st.error(f"Nomi Duplicati: {', '.join(err_d)}")
            if not err_g and not err_d: st.success("Tutto perfetto!")

with cb3:
    st.markdown('<div class="btn-assegna">', unsafe_allow_html=True)
    if st.button("🟩 ASSEGNA", use_container_width=True):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({"data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}", "ts": datetime.now().strftime("%d/%m/%Y %H:%M"), "cal": [dict(d) for d in st.session_state['master_cal']]})
            save_history()
            st.toast("Salvato!")

with cb4:
    st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
    if st.button("🏜️ RESET", use_container_width=True):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
view_mode = st.toggle("🎞️ VISTA COMPATTA", value=False)
st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h2 style='text-align:center; color:#ffcc66; font-family:Rye;'>📅 {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h2>", unsafe_allow_html=True)
    draw_grid(st.session_state['master_cal'], compact=view_mode, key_prefix="master")

# --- ARCHIVIO ---
if st.session_state['history']:
    st.markdown("<hr><h2 style='color:#ffcc66; font-family:Rye; text-align:center;'>📜 CRONOLOGIA</h2>", unsafe_allow_html=True)
    for idx in range(len(st.session_state['history']) - 1, -1, -1):
        item = st.session_state['history'][idx]
        with st.expander(f"📦 {item['data']} (Creato il {item['ts']})"):
            draw_grid(item['cal'], compact=True, is_history=True, key_prefix=f"hist_{idx}")
            if st.button("ELIMINA", key=f"del_{idx}"):
                st.session_state['history'].pop(idx)
                save_history()
                st.rerun()
