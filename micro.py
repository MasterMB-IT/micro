import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar
from collections import defaultdict

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Express 2099 - Hyperloop Manager", layout="wide")

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

# --- DATABASE MEMBRI ---
def init_db():
    leaders = [
        "亗 Hool 亗 (R5)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", 
        "PΞPPΞ (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", 
        "09ALEX24 (R4)", "ShinyPasta (R4)", "ΨWallΨ (R4)", "彡M A S T E Ʀ彡 (R4)"
    ]
    
    r3_r2 = [
        "Dragons slayer", "Morten1212", "J๏รєקקђoNe", "Zokra", "BadBigBoss", 
        "Sir Vonski", "Limaximus", "ARIO73", "Scolligo", "dome b", "Pitt9595", 
        "MartinSK", "Ｍａメツ", "xFlotchy", "ᶜᵃᵖᵒ ΘᴥΘ", "JaxxTronic", "NOVEMBERGENZ", 
        "Trivellatore", "TheDane001", "Purpix7", "Ξ Bugs Bunny Ξ", "Billy1906", 
        "Mik I", "cruel neve", "Bendico", "Elchicogyot", "Comandante Maveric", 
        "Dark doom", "perseusxxx", "Reklaus", "SPio24", "F3nryU", "Strunztruppen", 
        "ᴮᵃⁿᵃⁿᵃ B", "Wolf006", "Sir Lance of N8Watch", "MissDrinks", "Aryron", 
        "Kɘrnel Panic", "Leechai", "Anubis 7", "GennaroM", "holdfast", "DarkGiollo", 
        "PakII", "yeah yeah Coco Jambo", "GER176", "Giuseppec84", "mike92i", "krompir",
        "tchik", "Dark lalla", "zaaaaaaaayyyy", "controvento6", "torhil", "MeSHeL", 
        "Ꮭ ᏗᎶᏋᏁᏖ0", "G Σrry", "uncle g", "Pielaur", "Stefano00000", "VincenzoPoma89", 
        "Whale Panda", "Squirtle ITA", "Skiteto", "27Francesco", "BANDOLERO26", 
        "ღNeyღ", "Ghandal", "MUSCHIOLINI", "Bunnyᘻ", "rnd66", "CaSeLLo", "Mmtyy", 
        "bonnyand", "AresArwen", "MeIo65", "o GARGANTUA o", "x The Lord x", "Tricheco", 
        "BRNcommando", "Brancii", "ImAde", "CΔMÍÍㆍᴥㆍ", "ℒιzzιℯ 82", "Peter Sveter", 
        "LeFada13", "Riki Sajo", "Pembe komutan", "Pupisnic"
    ]
    
    data = [{"Nome": "---", "Grado": "Nessuno"}] + \
           [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + \
           [{"Nome": n, "Grado": "R3/R2"} for n in r3_r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state: 
    st.session_state['players_db'] = init_db()

db = st.session_state['players_db']

leaders_list = sorted(db[db['Grado'] == "R5/R4"]['Nome'].tolist())
all_names_list = sorted(db['Nome'].tolist())

# --- DATI STORICI INIZIALI (BASE 5 MESI) ---
HISTORICAL_5_MONTHS = {
    "capo_counts": {
        "Hool": 2, "MASTER": 4, "SHINYPASTA": 4, "PEPPE": 3, "UNCLE G BROTHER": 2,
        "RICKY AROUND": 3, "09ALEX24": 3, "BLOODYBLADE": 1, "LE 12 SCIMMIE": 2,
        "STARBETTY": 1, "SAGITTARIUS A1": 3, "WHALE PANDA": 2, "JEPPE": 1, "GOZ": 3,
        "STUNTMARK": 1, "WALL 7": 4, "CRUEL NEVE": 3, "ZOKRA": 3, "XFLOTCHY": 3,
        "GIUSEPPEC84": 2, "BENITO MUSCHIONI": 2, "BADBIGBOSS": 3, "ANA BUNNY": 1,
        "LALLA 96": 1, "MAメツ": 3, "NOVEMBERGENZ": 2, "GHOST": 2, "ECHOZERO": 1,
        "SPIO24": 3, "TRICHECO": 1, "MOUK57": 2, "MORTEN1212": 3, "MELO65": 1,
        "MARTINSK": 2, "CASELLO": 1, "SCOLLIGO": 2, "LIMAXIMUS": 2, "SIR VONSKI": 2,
        "F3NRYU": 2, "DARKGIOLLO": 2, "STRAMM": 2, "REKLAUS": 2, "ANUBIS 7": 1,
        "BRANCII": 1, "VENUS 31": 1, "JOS591": 1, "X THE LORD X": 2, "MIKE92I": 1,
        "PITT9595": 2, "TOHIK": 2, "KINGGRUFFALO": 1, "BENDICO": 1, "27FRANCESCO": 1,
        "GHANDAL": 1, "MARKUS DEFENDED": 1, "GENNAROM": 1, "BANDOLERO26": 1,
        "JOSEPPONE": 3, "MIK I": 1, "BRNCOMMANDO": 1, "SQUIRTLE": 1, "PSYKOS": 1,
        "MARIA": 1
    },
    "pass_counts": {
        "MAメツ": 4, "SHINYPASTA": 2, "MASTER": 3, "09ALEX24": 2, "GOZ": 1,
        "SAGITTARIUS A1": 2, "STARBETTY": 2, "RICKY AROUND": 2, "PEPPE": 2,
        "UNCLE G BROTHER": 3, "LE 12 SCIMMIE": 2, "HOOL": 3, "G ERRY": 2,
        "WOLFOO6": 3, "ARYRON": 2, "BENDICO": 2, "MISSDRINKS": 1, "MX63": 1,
        "STEFANO00000": 2, "PAKII": 2, "BANDOLERO26": 1, "MARKUS DEFENDED": 1,
        "WALL 7": 3, "EDDWARD": 2, "KROMPIR": 3, "GHANDAL": 1, "ZOKRA": 2,
        "CAMIIIII 08": 2, "JOSEPPONE": 3, "HULKSPAKKA": 2, "BADBIGBOSS": 2, 
        "YEAH YEAH OOOO": 1, "NOVEMBERGENZ": 2, "XFLOTCHY": 2, "BLOODYBLADE": 1, 
        "ORAISHIO": 1, "PANDORE": 1, "MESHEL": 1, "SIR LANCE OF N81": 1, 
        "VINCENZOPOMA89": 1, "ZAAAAAAAYYYYY": 2, "JAXXTRONIC": 1, "AGENT BASS": 1, 
        "ARESARWEN": 1, "PSYKOS": 2, "SQUIRTLE ITA": 1, "STUNTMARK": 1, "SIR VONSKI": 1, 
        "MOUK57": 2, "LIMAXIMUS": 1, "F3NRYU": 1, "REKLAUS": 1, "ELCHICOGYOT": 1, 
        "LALLA 96": 1, "DARKGIOLLO": 1, "SPIO24": 2, "COMANDANTE MAV": 1, "SKITETO": 1, 
        "ECHOZERO": 1, "TOMENERGY": 1, "GERRY": 1, "TRICHECO": 2, "PITT9595": 1, 
        "CRUEL NEVE": 1, "GENNAROM": 1, "HOLDFAST": 1, "ANA BUNNY": 1, "BRANCII": 2, 
        "STRUNZTRUPPEN": 2, "27FRANCESCO": 1, "LEFADA13": 1, "MELO65": 1, "PERSEUSXXX": 1, 
        "BOGE": 1, "CASELLO": 1, "TCHIK": 1, "ZIO GIOTTO": 1, "KING GRUFFALO": 1, "VENUS31": 1
    }
}

def norm_name(name):
    if not name:
        return ""
    return name.split("(")[0].strip().upper()

# --- ALGORITMO DI BILANCIAMENTO DINAMICO ---
def get_dynamic_history():
    """
    Raccoglie i dati storici iniziali e li unisce a TUTTI i calendari 
    salvati precedentemente nella sessione/JSON.
    """
    capo_counts = defaultdict(int, HISTORICAL_5_MONTHS["capo_counts"])
    pass_counts = defaultdict(int, HISTORICAL_5_MONTHS["pass_counts"])
    
    saved_history = st.session_state.get('history', [])
    
    for month_data in saved_history:
        for row in month_data.get('cal', []):
            c_name = norm_name(row.get('Capo', ''))
            p_name = norm_name(row.get('Pass', ''))
            if c_name and c_name != "---":
                capo_counts[c_name] += 1
            if p_name and p_name != "---":
                pass_counts[p_name] += 1
                
    return capo_counts, pass_counts

def get_balanced_player(pool, role_type, current_assignments_this_month):
    capo_hist, pass_hist = get_dynamic_history()
    
    candidates = []
    
    for player in pool:
        current_c = current_assignments_this_month["capo"][player]
        current_p = current_assignments_this_month["pass"][player]
        current_total = current_c + current_p
        
        n_p = norm_name(player)
        hist_c = sum(v for k, v in capo_hist.items() if k in n_p or n_p in k)
        hist_p = sum(v for k, v in pass_hist.items() if k in n_p or n_p in k)
            
        hist_role = hist_c if role_type == "capo" else hist_p
        hist_total = hist_c + hist_p
        
        never_done_role = 1 if hist_role == 0 else 2
        
        candidates.append({
            "player": player,
            "never_done": never_done_role,
            "current_total": current_total,
            "hist_total": hist_total,
            "rand": random.random()
        })
        
    candidates.sort(key=lambda x: (x["never_done"], x["current_total"], x["hist_total"], x["rand"]))
    return candidates[0]["player"]

# --- STILE NEON / CYBERPUNK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800;900&family=Rajdhani:wght@600;700&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at 50% 10%, #150d2a 0%, #080811 100%);
        color: #e0e6ed;
    }
    
    .train-title { 
        font-family: 'Orbitron', sans-serif; 
        text-align: center; 
        color: #00f3ff; 
        text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 40px #9d4edd; 
        font-size: 3.2rem; 
        font-weight: 900;
        letter-spacing: 3px;
        margin-bottom: 25px; 
    }
    
    .cal-header-container { 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        gap: 20px; 
        margin-bottom: 15px; 
    }
    
    .cal-header-text { 
        font-family: 'Orbitron', sans-serif; 
        color: #ff007f; 
        text-shadow: 0 0 10px #ff007f, 0 0 20px #ff007f; 
        font-size: 2.2rem; 
        letter-spacing: 2px;
        margin: 0; 
    }
    
    .train-icon { 
        font-size: 2.8rem; 
        filter: drop-shadow(0 0 10px #00f3ff);
    }
    
    .sala-comando { 
        background: rgba(16, 12, 34, 0.75); 
        backdrop-filter: blur(12px); 
        border: 1px solid #00f3ff; 
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 15px rgba(157, 78, 221, 0.15);
        border-radius: 12px; 
        padding: 25px; 
        margin-bottom: 30px; 
    }

    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0px !important; }

    .calendar-cell { 
        background: rgba(15, 15, 30, 0.85); 
        border: 1px solid rgba(0, 243, 255, 0.25);
        padding: 12px 10px; 
        color: #ffffff; 
        display: flex; 
        flex-direction: column; 
        transition: all 0.3s ease;
        margin: -0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .calendar-cell::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, #00f3ff, #ff007f);
        opacity: 0.3;
    }
    
    .calendar-cell:hover { 
        border-color: #ff007f;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.4), inset 0 0 10px rgba(0, 243, 255, 0.2); 
        z-index: 10; 
        transform: translateY(-2px);
    }
    
    .h-norm { min-height: 230px !important; }
    .h-comp { min-height: 175px !important; }
    .card-placeholder { background: rgba(5, 5, 12, 0.4); border: 1px dashed rgba(255,255,255,0.1); }
    
    .day-badge { 
        background: linear-gradient(135deg, #7b2cbf, #ff007f); 
        color: #ffffff; 
        font-family: 'Orbitron', sans-serif; 
        font-weight: 800; 
        padding: 3px 8px; 
        border-radius: 4px; 
        font-size: 0.72rem; 
        width: fit-content; 
        margin-bottom: 8px; 
        box-shadow: 0 0 8px rgba(255, 0, 127, 0.5);
    }
    
    .role-label { 
        color: #00f3ff; 
        font-size: 0.65rem; 
        font-family: 'Rajdhani', sans-serif; 
        text-transform: uppercase; 
        font-weight: 700; 
        letter-spacing: 1px;
        border-bottom: 1px solid rgba(0, 243, 255, 0.2); 
        margin-top: 6px; 
    }
    
    .name-text { 
        font-family: 'Rajdhani', sans-serif; 
        font-size: 0.95rem; 
        font-weight: 700; 
        text-transform: uppercase; 
        border-left: 3px solid #ff007f; 
        padding-left: 6px; 
        overflow: hidden; 
        white-space: nowrap; 
        margin-top: 3px; 
        color: #ffffff !important; 
        text-shadow: 0 0 5px rgba(255,255,255,0.3);
    }
    
    .stButton>button { 
        border-radius: 6px !important; 
        font-family: 'Orbitron', sans-serif !important; 
        font-size: 0.8rem !important;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
    }
    
    .btn-genera button { 
        background: transparent !important; 
        color: #00f3ff !important; 
        border: 1px solid #00f3ff !important;
        box-shadow: 0 0 10px rgba(0,243,255,0.2) !important;
    }
    .btn-genera button:hover {
        background: #00f3ff !important;
        color: #080811 !important;
        box-shadow: 0 0 20px #00f3ff !important;
    }

    .btn-vuoto button { 
        background: transparent !important; 
        color: #a0aab2 !important; 
        border: 1px solid #4a5568 !important;
    }
    .btn-vuoto button:hover {
        background: #4a5568 !important;
        color: #ffffff !important;
    }

    .btn-assegna button { 
        background: transparent !important; 
        color: #39ff14 !important; 
        border: 1px solid #39ff14 !important;
        box-shadow: 0 0 10px rgba(57, 255, 20, 0.2) !important;
    }
    .btn-assegna button:hover {
        background: #39ff14 !important;
        color: #080811 !important;
        box-shadow: 0 0 20px #39ff14 !important;
    }
    
    div[data-testid="stPopover"] > button { 
        height: 26px !important; 
        width: 100% !important; 
        margin-top: 8px !important; 
        font-size: 0.7rem !important; 
        border: 1px solid #7b2cbf !important;
        background: rgba(123, 44, 191, 0.2) !important;
        color: #00f3ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weekday_idx(day, month_name, year):
    month_idx = MESI_ITA.index(month_name) + 1
    return datetime(year, month_idx, day).weekday()

# --- RENDERING GRIGLIA ---
def draw_grid(data, compact=False, is_history=False, key_prefix="grid"):
    mese_nom = st.session_state.get('sel_mese', "Settembre")
    anno_val = st.session_state.get('sel_anno', 2026)
    
    first_day_wd = get_weekday_idx(1, mese_nom, anno_val)
    full_display_list = [{"type": "empty"}] * first_day_wd
    for item in data:
        full_display_list.append({"type": "data", "content": item})
    
    n_cols = 10 if compact else 7
    h_cls = "h-comp" if compact else "h-norm"
    opts_all = ["---"] + all_names_list

    for i in range(0, len(full_display_list), n_cols):
        cols = st.columns(n_cols)
        chunk = full_display_list[i:i + n_cols]
        for j, item in enumerate(chunk):
            with cols[j]:
                if item["type"] == "empty":
                    st.markdown(f'<div class="calendar-cell card-placeholder {h_cls}"></div>', unsafe_allow_html=True)
                else:
                    r = item["content"]
                    giorno = r['Giorno']
                    wd_idx = get_weekday_idx(giorno, mese_nom, anno_val)
                    wd_display = GIORNI_ABBR[wd_idx] if compact else GIORNI_SETTIMANA[wd_idx]
                    
                    st.markdown(f"""
                    <div class="calendar-cell {h_cls}">
                        <div class="day-badge">⚡ {wd_display} {giorno}</div>
                        <div class="role-label">⚡ CAPO TRENO {"🛰️" if giorno <= 11 else ""}</div>
                        <div class="name-text">{r['Capo']}</div>
                        <div class="role-label">💺 PASSEGGERO VIP</div>
                        <div class="name-text">{r['Pass']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not is_history and not compact:
                        with st.popover("⚙️ MODIFICA"):
                            st.caption(f"Configurazione Giorno {giorno}")
                            metodo = st.radio("Metodo", ["Lista", "Manuale"], key=f"met_{key_prefix}_{giorno}", horizontal=True)
                            
                            if metodo == "Lista":
                                nc = st.selectbox("Capo", opts_all, index=opts_all.index(r['Capo']) if r['Capo'] in opts_all else 0, key=f"sel_c_{key_prefix}_{giorno}")
                                np = st.selectbox("Pass", opts_all, index=opts_all.index(r['Pass']) if r['Pass'] in opts_all else 0, key=f"sel_p_{key_prefix}_{giorno}")
                            else:
                                nc = st.text_input("Nome Capo", value=r['Capo'], key=f"txt_c_{key_prefix}_{giorno}")
                                np = st.text_input("Nome Pass", value=r['Pass'], key=f"txt_p_{key_prefix}_{giorno}")
                            
                            if st.button("SALVA", key=f"s_{key_prefix}_{giorno}", use_container_width=True):
                                for idx, m_item in enumerate(st.session_state['master_cal']):
                                    if m_item["Giorno"] == giorno:
                                        st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np})
                                        break
                                st.rerun()

# --- INTERFACCIA UTENTE ---
st.markdown('<div class="train-title">🚝 AOSR HYPERLOOP 2099</div>', unsafe_allow_html=True)
st.markdown('<div class="sala-comando">', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.5, 2])
with c1:
    st.session_state['sel_mese'] = st.selectbox("📅 MESE", MESI_ITA, index=8)
    st.session_state['sel_anno'] = st.number_input("📆 ANNO", 2024, 2030, 2026)
with c2: sel_leaders = st.multiselect("🛸 PILOTI (R5/R4)", leaders_list)
with c3: sel_r3_r2 = st.multiselect("🛰️ PASSEGGERI (R3/R2)", db[db['Grado'] == "R3/R2"]['Nome'].tolist())

st.markdown('<div style="margin-top:20px; padding-top:20px; border-top:1px solid rgba(0,243,255,0.2)">', unsafe_allow_html=True)
cb1, cb1b, cb2, cb3, cb4 = st.columns(5)

with cb1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("⚡ GENERA BILANCIATO", use_container_width=True):
        p_l = (sel_leaders if sel_leaders else leaders_list)
        p_o = (sel_r3_r2 if sel_r3_r2 else db[db['Grado']=="R3/R2"]['Nome'].tolist())
        
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = []
        
        current_assignments = {
            "capo": defaultdict(int),
            "pass": defaultdict(int)
        }
        
        for g in range(1, num_gg + 1):
            if g <= 11:
                c = get_balanced_player(p_l, "capo", current_assignments)
                p = get_balanced_player([x for x in p_o if x != c], "pass", current_assignments)
            else:
                c = get_balanced_player(p_o, "capo", current_assignments)
                p = get_balanced_player([x for x in p_o if x != c], "pass", current_assignments)
            
            current_assignments["capo"][c] += 1
            current_assignments["pass"][p] += 1
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
            
    st.markdown('</div>', unsafe_allow_html=True)

with cb1b:
    st.markdown('<div class="btn-vuoto">', unsafe_allow_html=True)
    if st.button("🌐 RESET TABELLA", use_container_width=True):
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = [{"Giorno": g, "Capo": "---", "Pass": "---"} for g in range(1, num_gg + 1)]
    st.markdown('</div>', unsafe_allow_html=True)

with cb2:
    if st.button("🔍 CHECK REGOLE", use_container_width=True):
        if 'master_cal' in st.session_state:
            err_g = [f"GG {r['Giorno']}" for r in st.session_state['master_cal'] if r['Giorno'] <= 11 and r['Capo'] not in leaders_list and r['Capo'] != "---"]
            if err_g: st.warning(f"Note: Capi non-R4 nei primi 11gg: {', '.join(err_g)}")
            else: st.success("Pianificazione conforme!")

with cb3:
    st.markdown('<div class="btn-assegna">', unsafe_allow_html=True)
    if st.button("💾 SALVA IN MEMORIA", use_container_width=True):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({
                "data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}",
                "mese": st.session_state['sel_mese'],
                "anno": st.session_state['sel_anno'],
                "ts": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "cal": [dict(d) for d in st.session_state['master_cal']]
            })
            save_history()
            st.toast("AOSR Salvato nel Database!")

with cb4:
    if st.button("🧹 SVUOTA", use_container_width=True):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()

st.write("")
view_mode = st.toggle("🎞️ VISTA COMPATTA MATRIX", value=False)
st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE PRINCIPALE ---
if 'master_cal' in st.session_state:
    st.markdown(f"""
        <div class="cal-header-container">
            <span class="train-icon">🚅</span>
            <h2 class="cal-header-text">AOSR - {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h2>
            <span class="train-icon">🚅</span>
        </div>
    """, unsafe_allow_html=True)
    
    draw_grid(st.session_state['master_cal'], compact=view_mode, key_prefix="master")

# --- ARCHIVIO STORICO ---
if st.session_state['history']:
    st.markdown("<br><br><h2 style='color:#00f3ff; font-family:Orbitron; text-align:center; text-shadow: 0 0 10px #00f3ff;'>📜 ARCHIVIO AOSR</h2>", unsafe_allow_html=True)
    for idx, item in enumerate(reversed(st.session_state['history'])):
        real_idx = len(st.session_state['history']) - 1 - idx
        with st.expander(f"📦 AOSR {item['data']} (Registrato il {item['ts']})"):
            draw_grid(item['cal'], compact=True, is_history=True, key_prefix=f"hist_{real_idx}")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📝 CARICA & MODIFICA", key=f"edit_{real_idx}", use_container_width=True):
                    st.session_state['master_cal'] = [dict(d) for d in item['cal']]
                    st.session_state['sel_mese'] = item.get('mese', st.session_state['sel_mese'])
                    st.session_state['sel_anno'] = item.get('anno', st.session_state['sel_anno'])
                    st.rerun()
            with col_btn2:
                if st.button("🗑️ ELIMINA RECORD", key=f"del_{real_idx}", use_container_width=True):
                    st.session_state['history'].pop(real_idx)
                    save_history()
                    st.rerun()
