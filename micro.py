import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Deluxe Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

GIORNI_SETTIMANA = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
GIORNI_ABBR = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

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

if 'history' not in st.session_state:
    st.session_state['history'] = load_history()

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["Uncle g", "G Erry", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    
    data = [{"Nome": "---", "Grado": "Nessuno"}] + \
            [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + \
            [{"Nome": n, "Grado": "R3"} for n in r3] + \
            [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state: st.session_state['players_db'] = init_db()
db = st.session_state['players_db']

leaders_list = sorted(db[db['Grado'] == "R5/R4"]['Nome'].tolist())
r3_list = sorted(db[db['Grado'] == "R3"]['Nome'].tolist())
early_leaders_list = sorted(leaders_list + r3_list)
all_names_list = sorted(db['Nome'].tolist())

# --- CSS E COMPONENTE JS PER ISTANTANEA ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background: linear-gradient(rgba(30, 20, 10, 0.8), rgba(15, 10, 5, 0.95)), url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop'); background-size: cover; background-attachment: fixed; }
    .train-title { font-family: 'Rye', cursive; text-align: center; color: #ffcc66; text-shadow: 5px 5px 0px #4b2e1b; font-size: 4rem; margin-bottom: 20px; }
    .sala-comando { background: rgba(25, 15, 5, 0.85); backdrop-filter: blur(10px); border: 2px solid #ffcc66; border-radius: 20px; padding: 25px; margin-bottom: 30px; border-top: 5px solid #ffcc66; }
    
    /* Griglia Calendario */
    #capture-area { background: #4b2e1b; padding: 10px; border-radius: 10px; }
    .calendar-cell { background: #fdf5e6; border: 1px solid rgba(93, 64, 55, 0.4); padding: 12px 8px; background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png'); display: flex; flex-direction: column; transition: 0.2s; margin: -0.5px; }
    .h-norm { height: 230px !important; }
    .h-comp { height: 175px !important; }
    
    .day-badge { background: #8b0000; color: white; font-family: 'Montserrat', sans-serif; font-weight: 900; padding: 2px 8px; border-radius: 2px; font-size: 0.75rem; width: fit-content; margin-bottom: 6px; }
    .role-label { color: #5d4037; font-size: 0.6rem; font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800; border-bottom: 1px solid rgba(93, 64, 55, 0.15); margin-top: 6px; }
    
    /* Forza Nomi Neri */
    .name-text { font-family: 'Special Elite', cursive; font-size: 0.88rem; font-weight: 900; text-transform: uppercase; border-left: 3px solid #d4a373; padding-left: 6px; overflow: hidden; white-space: nowrap; margin-top: 2px; color: #000000 !important; }
    
    .stButton>button { border-radius: 6px !important; font-family: 'Rye', cursive !important; border: 2px solid #2b1d0e !important; }
    .btn-snapshot button { background: #ffcc66 !important; color: #2b1d0e !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# Funzione Javascript per catturare lo schermo
def trigger_snapshot():
    components.html("""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script>
            setTimeout(() => {
                const element = window.parent.document.getElementById('capture-area');
                html2canvas(element, {
                    backgroundColor: "#1e140a",
                    scale: 2
                }).then(canvas => {
                    const link = document.createElement('a');
                    link.download = 'AOSR_Express_Calendario.png';
                    link.href = canvas.toDataURL("image/png");
                    link.click();
                });
            }, 500);
        </script>
    """, height=0)

def get_weekday_idx(day, month_name, year):
    month_idx = MESI_ITA.index(month_name) + 1
    return datetime(year, month_idx, day).weekday()

# --- RENDERING GRIGLIA ---
def draw_grid(data, compact=False, is_history=False, key_prefix="grid"):
    mese = st.session_state.get('sel_mese', "Gennaio")
    anno = st.session_state.get('sel_anno', 2026)
    
    first_day_wd = get_weekday_idx(1, mese, anno)
    full_display_list = [{"type": "empty"}] * first_day_wd
    for item in data:
        full_display_list.append({"type": "data", "content": item})
    
    n_cols = 10 if compact else 7
    h_cls = "h-comp" if compact else "h-norm"
    opts_early = ["---"] + early_leaders_list
    opts_all = ["---"] + all_names_list

    # Div contenitore per l'istantanea
    st.markdown('<div id="capture-area">', unsafe_allow_html=True)
    
    for i in range(0, len(full_display_list), n_cols):
        cols = st.columns(n_cols)
        chunk = full_display_list[i:i + n_cols]
        for j, item in enumerate(chunk):
            with cols[j]:
                if item["type"] == "empty":
                    st.markdown(f'<div class="calendar-cell card-placeholder {h_cls}" style="background:rgba(0,0,0,0.1)"></div>', unsafe_allow_html=True)
                else:
                    r = item["content"]
                    giorno = r['Giorno']
                    wd_idx = get_weekday_idx(giorno, mese, anno)
                    wd_display = GIORNI_ABBR[wd_idx] if compact else GIORNI_SETTIMANA[wd_idx]
                    
                    st.markdown(f"""
                    <div class="calendar-cell {h_cls}">
                        <div class="day-badge">{wd_display} {giorno}</div>
                        <div class="role-label">CAPO {"⭐" if giorno <= 11 else ""}</div>
                        <div class="name-text">{r['Capo']}</div>
                        <div class="role-label">PASSEGGERO</div>
                        <div class="name-text">{r['Pass']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not is_history and not compact:
                        with st.popover("MODIFICA"):
                            opts_capo = opts_early if giorno <= 11 else opts_all
                            idx_c = opts_capo.index(r['Capo']) if r['Capo'] in opts_capo else 0
                            idx_p = opts_all.index(r['Pass']) if r['Pass'] in opts_all else 0
                            nc = st.selectbox(f"Capo {giorno}", opts_capo, index=idx_c, key=f"c_{key_prefix}_{giorno}")
                            np = st.selectbox(f"Pass {giorno}", opts_all, index=idx_p, key=f"p_{key_prefix}_{giorno}")
                            if st.button("SALVA", key=f"s_{key_prefix}_{giorno}"):
                                for idx, m_item in enumerate(st.session_state['master_cal']):
                                    if m_item["Giorno"] == giorno:
                                        st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np})
                                        break
                                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- INTERFACCIA ---
st.markdown('<div class="train-title"> 🚂 AOSR EXPRESS</div>', unsafe_allow_html=True)
st.markdown('<div class="sala-comando">', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
with c1:
    st.session_state['sel_mese'] = st.selectbox("📅 MESE", MESI_ITA, index=datetime.now().month - 1)
    st.session_state['sel_anno'] = st.number_input("📆 ANNO", 2024, 2030, 2026)
with c2: sel_leaders = st.multiselect("🤠 R5/R4", leaders_list)
with c3: sel_r3 = st.multiselect("🌵 R3", r3_list)
with c4: sel_r2 = st.multiselect("🐎 R2", db[db['Grado'] == "R2"]['Nome'].tolist())

st.markdown('<div style="margin-top:20px; padding-top:20px; border-top:1px solid rgba(255,204,102,0.2)">', unsafe_allow_html=True)
cb1, cb1b, cb2, cb3, cb4, cb5 = st.columns([1, 1, 1, 1, 1, 1.5])

with cb1:
    if st.button("⚒️ GENERA AUTO", use_container_width=True):
        p_l = (sel_leaders if sel_leaders else leaders_list) + (sel_r3 if sel_r3 else r3_list)
        p_o = (sel_r3 if sel_r3 else r3_list) + (sel_r2 if sel_r2 else db[db['Grado']=="R2"]['Nome'].tolist())
        random.shuffle(p_l); random.shuffle(p_o)
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11: 
                c = p_l[(g-1)%len(p_l)]; p = p_o[g%len(p_o)]
            else: 
                c = p_o[p_idx % len(p_o)]; p = p_o[(p_idx+1) % len(p_o)]; p_idx += 2
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})

with cb3:
    if st.button("🟩 ASSEGNA", use_container_width=True):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({
                "data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}",
                "mese": st.session_state['sel_mese'], "anno": st.session_state['sel_anno'],
                "ts": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "cal": [dict(d) for d in st.session_state['master_cal']]
            })
            save_history()
            st.toast("Calendario Salvato!")

with cb5:
    st.markdown('<div class="btn-snapshot">', unsafe_allow_html=True)
    if st.button("📸 SCARICA ISTANTANEA", use_container_width=True):
        if 'master_cal' in st.session_state:
            trigger_snapshot()
    st.markdown('</div>', unsafe_allow_html=True)

with cb4:
    if st.button("🏜️ RESET", use_container_width=True):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()

view_mode = st.toggle("🎞️ VISTA COMPATTA", value=False)
st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h2 style='text-align:center; color:#ffcc66; font-family:Rye; margin-bottom:0px;'>{st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h2>", unsafe_allow_html=True)
    draw_grid(st.session_state['master_cal'], compact=view_mode, key_prefix="master")

# --- ARCHIVIO ---
if st.session_state['history']:
    st.markdown("<br><br><h2 style='color:#ffcc66; font-family:Rye; text-align:center;'>📜 CRONOLOGIA</h2>", unsafe_allow_html=True)
    for idx, item in enumerate(reversed(st.session_state['history'])):
        real_idx = len(st.session_state['history']) - 1 - idx
        with st.expander(f"📦 {item['data']} (Creato il {item['ts']})"):
            draw_grid(item['cal'], compact=True, is_history=True, key_prefix=f"hist_{real_idx}")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📝 MODIFICA QUESTO", key=f"edit_{real_idx}", use_container_width=True):
                    st.session_state['master_cal'] = [dict(d) for d in item['cal']]
                    st.session_state['sel_mese'] = item.get('mese', st.session_state['sel_mese'])
                    st.session_state['sel_anno'] = item.get('anno', st.session_state['sel_anno'])
                    st.rerun()
            with col_btn2:
                if st.button("🗑️ ELIMINA", key=f"del_{real_idx}", use_container_width=True):
                    st.session_state['history'].pop(real_idx)
                    save_history()
                    st.rerun()
