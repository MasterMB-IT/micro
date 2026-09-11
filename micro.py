import streamlit as st
import pandas as pd
import random
import json
import os
import re
import unicodedata
from datetime import datetime
import calendar
from collections import defaultdict

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR EXPRESS - Windows 95 Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

GIORNI_SETTIMANA = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
GIORNI_ABBR = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

DB_FILE = "cronologia_treni.json"
OVERRIDES_FILE = "manual_overrides.json"

# --- PERSISTENZA DATI ---
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

def save_overrides():
    with open(OVERRIDES_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state['manual_overrides'], f, ensure_ascii=False, indent=4)

def load_overrides():
    if os.path.exists(OVERRIDES_FILE):
        try:
            with open(OVERRIDES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

if 'history' not in st.session_state:
    st.session_state['history'] = load_history()

if 'manual_overrides' not in st.session_state:
    st.session_state['manual_overrides'] = load_overrides()

# --- DATABASE MEMBRI ATTIVI ---
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
        "Trivellatore", "TheDane001", "Purpix7", "Bugs Bunny", "Billy1906", 
        "Mik I", "cruel neve", "Bendico", "Elchicojyot", "Comandante Maveric", 
        "Dark Doom", "perseusxxx", "Reklaus", "SPio24", "F3nryU", "Struntruppen", 
        "ᴮᵃⁿᵃⁿᵃ B", "Wolf006", "Sir Lance of N8Watch", "MissDrinks", "Aryron", 
        "Kɘrnel Panic", "Leechai", "Anubis 7", "GennaroM", "holdfast", "DarkGiollo", 
        "PakII", "yeah yeah Coco Jambo", "GER176", "Giuseppec84", "mike92i", "krompir",
        "tchik", "Dark lalla", "zaaaaaaaayyyy", "controvento6", "torhil", "MeSHeL", 
        "Ꮭ ᏗᎶᏋᏁᏖ0", "G Σrry", "uncle g", "Pielaur", "Stefano00000", "VincenzoPoma89", 
        "Whale Panda", "Squirtle ITA", "Skiteto", "27Francesco", "BANDOLERO26", 
        "ღNeyღ", "Ghandal", "MUSCOLEENI", "Bunnyᘻ", "rnd66", "CaSeLLo", "Mmtyy", 
        "bonnyand", "AresArwen", "MeIo65", "o GARGANTUA o", "x The Lord x", "Tricheco", 
        "BRNcommando", "Brancii", "ImAde", "CAMìì", "ℒιzzιℯ 82", "Peter Sveter", 
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
r3_r2_list = sorted(db[db['Grado'] == "R3/R2"]['Nome'].tolist())
all_active_names = sorted(db[db['Nome'] != "---"]['Nome'].tolist())

# --- ALIAS E PULIZIA NOMI ---
def smart_normalize_name(name):
    if not name or name == "---":
        return ""
    
    str_name = str(name).strip()
    
    EXACT_MAP = {
        "彡M A S T E Ʀ彡 (R4)": "MASTER", "彡M A S T E Ʀ彡": "MASTER", "MASTER": "MASTER", "MASTER (R4)": "MASTER",
        "Ｍａメツ": "MA", "MA": "MA", "MAX": "MA", "MAメツ": "MA", "MAメツ (R4)": "MA",
        "PΞPPΞ (R4)": "PEPPE", "PΞPPΞ": "PEPPE", "PEPPE": "PEPPE", "PEPPE (R5)": "PEPPE", "PEPPE (R4)": "PEPPE",
        "yeah yeah Coco Jambo": "GOZ", "yeah yeah": "GOZ", "GOZ": "GOZ",
        "J๏รєקקђoNe": "JOSEPPONE", "JOSEPPONE": "JOSEPPONE", "JOSEPPONE (R4)": "JOSEPPONE",
        "Dark Doom": "DARKDOOM", "Markus Defender": "DARKDOOM", "MARKUS DEFENDE": "DARKDOOM", "DARK DOOM": "DARKDOOM", "DARKDOOM": "DARKDOOM",
        "Elchicojyot": "ELCHICOJYOT", "Zio Giotto": "ELCHICOJYOT", "ZIO GIOTTO": "ELCHICOJYOT", "ELCHICOJYOT": "ELCHICOJYOT", "ELCHICOGYOT": "ELCHICOJYOT",
        "ΨWallΨ (R4)": "WALL", "ΨWallΨ": "WALL", "WALL (R4)": "WALL", "WALL": "WALL", "WALL7": "WALL", "WALL 7": "WALL", "WALL 7 (R4)": "WALL",
        "Struntruppen": "STRUNZTRUPPEN", "Strunztruppen": "STRUNZTRUPPEN", "MX63": "STRUNZTRUPPEN",
        "MUSCOLEENI": "MUSCHIOLINI", "BENITO MUSCHIO": "MUSCHIOLINI", "BENITO MUSCHIOI": "MUSCHIOLINI", "MUSCHIOLINI": "MUSCHIOLINI",
        "Bugs Bunny": "BUGSBUNNY", "Bug Bunny": "BUGSBUNNY", "GHOST": "BUGSBUNNY", "Ξ Bugs Bunny Ξ": "BUGSBUNNY",
        "CAMìì": "CAMII", "CAMIIIII 08": "CAMII", "CΔMÍÍㆍᴥㆍ": "CAMII",
        "Ꮭ ᏗᎶᏋᏁᏖ0": "AGENT0", "AGENT BASS": "AGENT0",
        "Bunnyᘻ": "BUNNYM", "ANA BUNNY": "BUNNYM",
        "Stefano00000": "STEFANO00000",
        "Reklaus": "REKLAUS", "REKLAUS": "REKLAUS"
    }
    if str_name in EXACT_MAP:
        return EXACT_MAP[str_name]
        
    clean = re.sub(r'\(.*?\)', '', str_name)
    clean = unicodedata.normalize('NFKC', clean)
    clean = unicodedata.normalize('NFKD', clean).encode('ASCII', 'ignore').decode('utf-8')
    clean = clean.upper()

    replacements = {
        'Ʀ': 'R', 'Ξ': 'E', '亗': '', 'Ψ': '', '๏': 'O', 'ร': 'S', 'ק': 'P', 
        'ђ': 'H', 'Σ': 'E', 'Δ': 'A', 'ℒ': 'L', 'ι': 'I', 'ℯ': 'E',
        'ღ': '', 'ᘻ': 'M', 'Ꮭ': 'L', 'Ꮧ': 'A', 'Ꮆ': 'G', 'Ꮛ': 'E', 'Ꮑ': 'N', 'Ꮦ': 'T', 'ì': 'I'
    }
    for char, repl in replacements.items():
        clean = clean.replace(char, repl)
        
    clean = re.sub(r'[^A-Z0-9]', '', clean)
    
    if "YEAH" in clean or "COCO" in clean or "JAMBO" in clean or "GOZ" in clean: return "GOZ"
    if "JOSEPPONE" in clean or ("J" in clean and "PEP" in clean): return "JOSEPPONE"
    if "PEPPE" in clean: return "PEPPE"
    if "MASTER" in clean: return "MASTER"
    if clean in ["MA", "MAX"]: return "MA"
    if "MARKUS" in clean or "DARKDOOM" in clean: return "DARKDOOM"
    if "ELCHICO" in clean or "ZIOGIOTTO" in clean: return "ELCHICOJYOT"
    if "WALL" in clean: return "WALL"
    if "MUSCOL" in clean or "MUSCH" in clean: return "MUSCHIOLINI"
    if "STRUN" in clean or "STRUNT" in clean: return "STRUNZTRUPPEN"
    if "BUG" in clean and "BUNNY" in clean: return "BUGSBUNNY"
    if "CAMII" in clean: return "CAMII"
    if "AGENT" in clean or "LAGENTO" in clean: return "AGENT0"
    if "BUNNY" in clean or "ANA" in clean: return "BUNNYM"
    if "REKLAUS" in clean: return "REKLAUS"
        
    return clean.strip()

ACTIVE_PLAYERS_MAP = {smart_normalize_name(p): p for p in all_active_names}

HISTORICAL_5_MONTHS = {
    "capo_counts": {
        "09ALEX24": 5, "LE 12 SCIMMIE": 5, "RICKY AROUND": 5, "SAGITTARIUS A1": 5, 
        "SHINYPASTA": 5, "WALL": 5, "MASTER": 5, "HOOL": 5, "PEPPE": 5, "JOSEPPONE": 5, 
        "XFLOTCHY": 5, "ZOKRA": 5, "MA": 4, "GOZ": 4, "BADBIGBOSS": 4, "SPIO24": 4, 
        "CRUEL NEVE": 4, "DARKGIOLLO": 4, "F3NRYU": 4, "LIMAXIMUS": 4, "PITT9595": 4, 
        "SCOLLIGO": 4, "NOVEMBERGENZ": 3, "SIR VONSKI": 3, "UNCLEG BROTHER": 3, 
        "WHALE PANDA": 3, "MORTEN1212": 3, "MARTINSK": 3, "SQUIRTLE ITA": 3, 
        "X THE LORD X": 3, "GHANDAL": 3, "GIUSEPPEC84": 3, "BENDICO": 2, 
        "DARKDOOM": 2, "27FRANCESCO": 2, "BRANCII": 2, "GENNAROM": 2, "MUSCHIOLINI": 2, 
        "STRUNZTRUPPEN": 2, "TORHIL": 2, "BANDOLERO26": 2, "BRNCOMMANDO": 2, "MIK I": 2, 
        "TRICHECO": 1, "MEIO65": 1, "CASELLO": 1, "REKLAUS": 1, "ANUBIS 7": 1, 
        "MIKE92I": 1, "ZAAAAAAAYYYYY": 1, "ELCHICOJYOT": 1, "PERSEUSXXX": 1
    },
    "pass_counts": {
        "09ALEX24": 6, "SAGITTARIUS A1": 5, "SHINYPASTA": 5, "NOVEMBERGENZ": 5, 
        "RICKY AROUND": 4, "MASTER": 4, "HOOL": 4, "PEPPE": 4, "WALL": 4, 
        "MA": 4, "JOSEPPONE": 4, "BADBIGBOSS": 4, "BENDICO": 4, "BRANCII": 4, 
        "STRUNZTRUPPEN": 4, "TRICHECO": 4, "WOLF006": 4, "LE 12 SCIMMIE": 3, 
        "XFLOTCHY": 3, "ZOKRA": 3, "GOZ": 3, "SPIO24": 3, "ZAAAAAAAYYYYY": 3, 
        "GERRY": 3, "ARYRON": 3, "STEFANO00000": 3, "PAKII": 3, "KROMPIR": 3, 
        "BUGSBUNNY": 3, "UNCLEG BROTHER": 2, "LIMAXIMUS": 2, "CRUEL NEVE": 2, 
        "SIR VONSKI": 2, "SQUIRTLE ITA": 2, "GENNAROM": 2, "27FRANCESCO": 2, 
        "CASELLO": 2, "REKLAUS": 2, "ELCHICOJYOT": 2, "MEIO65": 2, "PERSEUSXXX": 2, 
        "CAMII": 2, "COMANDANTE MAVERIC": 2, "SKITETO": 2, "JAXXTRONIC": 2, 
        "ARESARWEN": 2, "LEFADA13": 2, "TCHIK": 2, "PITT9595": 1, "DARKGIOLLO": 1, 
        "F3NRYU": 1, "BANDOLERO26": 1, "MUSCHIOLINI": 1, "HOLDFAST": 1, 
        "MISSDRINKS": 1, "MESHEL": 1, "SIR LANCE OF N8Watch": 1, "VINCENZOPOMA89": 1, 
        "AGENT0": 1, "BUNNYM": 1
    }
}

def get_dynamic_history():
    capo_counts = defaultdict(int)
    pass_counts = defaultdict(int)
    
    for k, v in HISTORICAL_5_MONTHS["capo_counts"].items():
        norm_k = smart_normalize_name(k)
        if norm_k in ACTIVE_PLAYERS_MAP: capo_counts[norm_k] = max(capo_counts[norm_k], v)

    for k, v in HISTORICAL_5_MONTHS["pass_counts"].items():
        norm_k = smart_normalize_name(k)
        if norm_k in ACTIVE_PLAYERS_MAP: pass_counts[norm_k] = max(pass_counts[norm_k], v)
    
    for month_data in st.session_state.get('history', []):
        for row in month_data.get('cal', []):
            c_norm = smart_normalize_name(row.get('Capo', ''))
            p_norm = smart_normalize_name(row.get('Pass', ''))
            if c_norm in ACTIVE_PLAYERS_MAP: capo_counts[c_norm] += 1
            if p_norm in ACTIVE_PLAYERS_MAP: pass_counts[p_norm] += 1
                
    for norm_k, vals in st.session_state.get('manual_overrides', {}).items():
        if "capo" in vals: capo_counts[norm_k] = vals["capo"]
        if "pass" in vals: pass_counts[norm_k] = vals["pass"]

    return capo_counts, pass_counts

# --- ALGORITMO DI BILANCIAMENTO ---
def get_advanced_balanced_player(pool, role_type, current_assignments, phase="Fase 1 (Primi 2 Mesi)"):
    capo_hist, pass_hist = get_dynamic_history()
    
    if phase == "Fase 1 (Primi 2 Mesi)":
        w_hist = 0.25
        sigma = 1.5
    elif phase == "Fase 2 (Transizione Mese 3)":
        w_hist = 0.50
        sigma = 1.0
    else:
        w_hist = 1.00
        sigma = 0.5

    candidates = []
    for player in pool:
        norm_p = smart_normalize_name(player)
        
        curr_c = current_assignments["capo"][player]
        curr_p = current_assignments["pass"][player]
        curr_total = curr_c + curr_p
        
        hist_c = capo_hist.get(norm_p, 0)
        hist_p = pass_hist.get(norm_p, 0)
        hist_role = hist_c if role_type == "capo" else hist_p
        
        score = (hist_role * w_hist) + (curr_total * 2.5) + random.uniform(0, sigma)
        
        candidates.append({"player": player, "score": score})
    
    candidates.sort(key=lambda x: x["score"])
    return candidates[0]["player"]

# --- CSS ANNI '90 / WINDOWS 95 ---
st.markdown("""
    <style>
    /* STILE GENERALE DESKTOP ANNI 90 */
    .stApp { 
        background-color: #008080 !important; /* Teal classico di Win95 */
        font-family: 'Courier New', 'MS Sans Serif', monospace !important;
        color: #000000 !important;
    }
    
    /* WINDOW CONTAINER 95 */
    .win95-container {
        background-color: #c0c0c0;
        border-top: 3px solid #ffffff;
        border-left: 3px solid #ffffff;
        border-right: 3px solid #000000;
        border-bottom: 3px solid #000000;
        padding: 4px;
        box-shadow: 2px 2px 0px #000000;
        margin-bottom: 20px;
    }

    .win95-titlebar {
        background: linear-gradient(90deg, #000080, #1084d0);
        color: #ffffff;
        font-weight: bold;
        padding: 3px 6px;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        font-family: Arial, sans-serif;
    }

    /* ALLINEAMENTO UNIFORME ELEMENTI */
    div[data-testid="stHorizontalBlock"] {
        align-items: flex-end !important;
        gap: 8px !important;
    }

    /* INPUTS & SELECTBOXES 95 INSET */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border-top: 2px solid #000000 !important;
        border-left: 2px solid #000000 !important;
        border-right: 2px solid #dfdfdf !important;
        border-bottom: 2px solid #dfdfdf !important;
        border-radius: 0px !important;
        color: #000000 !important;
        min-height: 38px !important;
    }

    /* PULSANTI RETRO 95 OUTSET */
    .stButton > button {
        height: 38px !important;
        background-color: #c0c0c0 !important;
        border-top: 2px solid #ffffff !important;
        border-left: 2px solid #ffffff !important;
        border-right: 2px solid #000000 !important;
        border-bottom: 2px solid #000000 !important;
        border-radius: 0px !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-family: 'Courier New', monospace !important;
        box-shadow: none !important;
    }
    
    .stButton > button:active {
        border-top: 2px solid #000000 !important;
        border-left: 2px solid #000000 !important;
        border-right: 2px solid #ffffff !important;
        border-bottom: 2px solid #ffffff !important;
        padding: 2px 0px 0px 2px !important;
    }

    /* CALENDARIO E SCHEDE */
    .calendar-cell {
        background-color: #c0c0c0;
        border-top: 2px solid #ffffff;
        border-left: 2px solid #ffffff;
        border-right: 2px solid #000000;
        border-bottom: 2px solid #000000;
        padding: 6px;
        margin: -1px;
    }
    
    .h-norm { min-height: 200px !important; }
    .h-comp { min-height: 150px !important; }

    .day-badge {
        background-color: #000080;
        color: #ffffff;
        font-weight: bold;
        padding: 2px 4px;
        font-size: 12px;
        margin-bottom: 6px;
    }

    .role-label {
        font-size: 11px;
        font-weight: bold;
        color: #000000;
        margin-top: 4px;
        border-bottom: 1px solid #808080;
    }

    .name-text {
        font-size: 13px;
        background-color: #ffffff;
        border-top: 1px solid #000000;
        border-left: 1px solid #000000;
        border-right: 1px solid #dfdfdf;
        border-bottom: 1px solid #dfdfdf;
        padding: 2px 4px;
        margin-top: 2px;
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* LABELS */
    label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weekday_idx(day, month_name, year):
    month_idx = MESI_ITA.index(month_name) + 1
    return datetime(year, month_idx, day).weekday()

def draw_grid(data, compact=False, is_history=False, key_prefix="grid"):
    mese_nom = st.session_state.get('sel_mese', "Settembre")
    anno_val = st.session_state.get('sel_anno', 2026)
    
    first_day_wd = get_weekday_idx(1, mese_nom, anno_val)
    full_display_list = [{"type": "empty"}] * first_day_wd
    for item in data:
        full_display_list.append({"type": "data", "content": item})
    
    n_cols = 10 if compact else 7
    h_cls = "h-comp" if compact else "h-norm"
    opts_all = ["---"] + sorted(all_active_names)

    for i in range(0, len(full_display_list), n_cols):
        cols = st.columns(n_cols)
        chunk = full_display_list[i:i + n_cols]
        for j, item in enumerate(chunk):
            with cols[j]:
                if item["type"] == "empty":
                    st.markdown(f'<div class="calendar-cell {h_cls}" style="background-color:#a0a0a0;"></div>', unsafe_allow_html=True)
                else:
                    r = item["content"]
                    giorno = r['Giorno']
                    wd_idx = get_weekday_idx(giorno, mese_nom, anno_val)
                    wd_display = GIORNI_ABBR[wd_idx] if compact else GIORNI_SETTIMANA[wd_idx]
                    
                    st.markdown(f"""
                    <div class="calendar-cell {h_cls}">
                        <div class="day-badge">{wd_display.upper()} {giorno}</div>
                        <div class="role-label">CAPO TRENO</div>
                        <div class="name-text">{r['Capo']}</div>
                        <div class="role-label">PASSEGGERO</div>
                        <div class="name-text">{r['Pass']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not is_history and not compact:
                        with st.popover("EDIT"):
                            st.caption(f"Giorno {giorno}")
                            nc = st.selectbox("Capo", opts_all, index=opts_all.index(r['Capo']) if r['Capo'] in opts_all else 0, key=f"sel_c_{key_prefix}_{giorno}")
                            np = st.selectbox("Pass", opts_all, index=opts_all.index(r['Pass']) if r['Pass'] in opts_all else 0, key=f"sel_p_{key_prefix}_{giorno}")
                            
                            if st.button("OK", key=f"s_{key_prefix}_{giorno}", use_container_width=True):
                                for idx, m_item in enumerate(st.session_state['master_cal']):
                                    if m_item["Giorno"] == giorno:
                                        st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np})
                                        break
                                st.rerun()

# --- FINESTRA PRINCIPALE WINDOWS 95 ---
st.markdown("""
<div class="win95-container">
    <div class="win95-titlebar">
        <span>C:\\AOSR_EXPRESS\\SYSTEM\\SCHEDULER.EXE</span>
        <span>[X]</span>
    </div>
""", unsafe_allow_html=True)

# CONTROLLI / DASHBOARD
c1, c2, c3, c4 = st.columns([1, 1, 1.5, 1.5])
with c1: st.session_state['sel_mese'] = st.selectbox("MESE:", MESI_ITA, index=8)
with c2: st.session_state['sel_anno'] = st.number_input("ANNO:", 2024, 2030, 2026)
with c3: sel_phase = st.selectbox("BILANCIAMENTO:", ["Fase 1 (Primi 2 Mesi)", "Fase 2 (Transizione Mese 3)", "Fase 3 (A Regime)"])
with c4: merito_days_input = st.multiselect("GIORNI MERITO (R4):", list(range(12, 32)), default=[12, 15, 18, 22, 28])

st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)

# PULSANTI ALLINEATI RIGIDI
cb1, cb2, cb3, cb4, cb5 = st.columns([1.5, 1.3, 1.5, 1, 1])

with cb1:
    if st.button("GENERA", use_container_width=True):
        p_l = leaders_list
        p_o = r3_r2_list
        all_players = sorted(list(set(p_l + p_o)))
        
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = []
        
        current_assignments = {"capo": defaultdict(int), "pass": defaultdict(int)}
        
        for g in range(1, num_gg + 1):
            if g in merito_days_input:
                c = "--- (DA ASSEGNARE)"
                p = "--- (DA ASSEGNARE)"
            elif g <= 11:
                c = get_advanced_balanced_player(p_l, "capo", current_assignments, phase=sel_phase)
                p = get_advanced_balanced_player([x for x in all_players if x != c], "pass", current_assignments, phase=sel_phase)
            else:
                c = get_advanced_balanced_player(all_players, "capo", current_assignments, phase=sel_phase)
                p = get_advanced_balanced_player([x for x in all_players if x != c], "pass", current_assignments, phase=sel_phase)
            
            if c in all_players: current_assignments["capo"][c] += 1
            if p in all_players: current_assignments["pass"][p] += 1
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})

with cb2:
    if st.button("SALVA", use_container_width=True):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({
                "data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}",
                "mese": st.session_state['sel_mese'],
                "anno": st.session_state['sel_anno'],
                "ts": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "cal": [dict(d) for d in st.session_state['master_cal']]
            })
            save_history()
            st.toast("Salvato!")
            st.rerun()

with cb3:
    if st.button("ANNULLA", use_container_width=True):
        if st.session_state['history']:
            st.session_state['history'].pop()
            save_history()
            st.toast("Annullato!")
            st.rerun()

with cb4:
    if st.button("RESET", use_container_width=True):
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = [{"Giorno": g, "Capo": "---", "Pass": "---"} for g in range(1, num_gg + 1)]

with cb5:
    view_mode = st.toggle("COMPATTA", value=False)

st.markdown('</div>', unsafe_allow_html=True)

# --- RENDERING GRIGLIA ---
if 'master_cal' in st.session_state:
    st.markdown(f"### PROGRAMMAZIONE: {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}")
    draw_grid(st.session_state['master_cal'], compact=view_mode, key_prefix="master")

# --- ARCHIVIO MESI ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### ARCHIVIO DATI HISTORICAL")

if st.session_state['history']:
    for idx, item in enumerate(reversed(st.session_state['history'])):
        real_idx = len(st.session_state['history']) - 1 - idx
        with st.expander(f"FILE: {item['data']}.DAT ({item['ts']})"):
            c_del1, c_del2 = st.columns([4, 1])
            with c_del2:
                if st.button("ELIMINA", key=f"del_hist_{real_idx}", use_container_width=True):
                    st.session_state['history'].pop(real_idx)
                    save_history()
                    st.rerun()
            with c_del1:
                st.dataframe(pd.DataFrame(item['cal']), use_container_width=True, hide_index=True)

# --- STATISTICHE ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### STATISTICHE E DATABASE")

capo_hist_total, pass_hist_total = get_dynamic_history()

stats_data = []
for norm_key, real_name in ACTIVE_PLAYERS_MAP.items():
    c_count = capo_hist_total.get(norm_key, 0)
    p_count = pass_hist_total.get(norm_key, 0)
    stats_data.append({
        "Giocatore": real_name,
        "Turni Capo": c_count,
        "Turni Passeggero": p_count,
        "Totale Presenze": c_count + p_count
    })

df_stats = pd.DataFrame(stats_data).sort_values(by=["Totale Presenze", "Giocatore"], ascending=[False, True]).reset_index(drop=True)

tab_stat1, tab_stat2 = st.tabs(["TABELLA GENERALE", "OVERRIDE MANUALE"])

with tab_stat1:
    st.dataframe(df_stats, use_container_width=True, hide_index=True)

with tab_stat2:
    target_player = st.selectbox("Seleziona Giocatore:", all_active_names, key="override_player_select")
    if target_player:
        norm_target = smart_normalize_name(target_player)
        curr_c = capo_hist_total.get(norm_target, 0)
        curr_p = pass_hist_total.get(norm_target, 0)
        
        col_m1, col_m2 = st.columns(2)
        new_c = col_m1.number_input(f"Turni CAPO ({target_player}):", min_value=0, max_value=100, value=curr_c)
        new_p = col_m2.number_input(f"Turni PASSEGGERO ({target_player}):", min_value=0, max_value=100, value=curr_p)
            
        col_btn_sav, col_btn_res = st.columns(2)
        if col_btn_sav.button("APPLICA OVERRIDE", use_container_width=True):
            st.session_state['manual_overrides'][norm_target] = {"capo": new_c, "pass": new_p}
            save_overrides()
            st.toast("Salvato!")
            st.rerun()
            
        if norm_target in st.session_state['manual_overrides']:
            if col_btn_res.button("RIPRISTINA", use_container_width=True):
                del st.session_state['manual_overrides'][norm_target]
                save_overrides()
                st.rerun()
