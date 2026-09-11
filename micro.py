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
st.set_page_config(page_title="AOSR EXPRESS - Gestione Treni", layout="wide")

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

# --- CSS MINIMALE, MODERNO AD ALTA LEGGIBILITÀ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* STILE MODERNO SLATE / DARK */
    .stApp { 
        background-color: #0f172a !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* INTESTAZIONE */
    .app-title {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        color: #38bdf8;
        letter-spacing: 0.5px;
        margin-bottom: 20px;
    }

    /* CONTENITORI ALLINEATI */
    div[data-testid="stHorizontalBlock"] {
        align-items: flex-end !important;
    }

    /* INPUTS & SELECT */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        min-height: 42px !important;
    }

    /* PULSANTI ELEGANTI */
    .stButton > button {
        height: 42px !important;
        background-color: #0284c7 !important;
        border: none !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: background-color 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #0369a1 !important;
        color: #ffffff !important;
    }

    /* SCHEDA CALENDARIO PULITA PER ALLEATI */
    .clean-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    .card-header {
        background-color: #334155;
        color: #f8fafc;
        font-weight: 700;
        font-size: 12px;
        text-align: center;
        padding: 4px;
        border-radius: 4px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .role-container {
        margin-top: 6px;
    }

    .role-badge-capo {
        font-size: 10px;
        font-weight: 700;
        color: #38bdf8;
        text-transform: uppercase;
    }

    .role-badge-pass {
        font-size: 10px;
        font-weight: 700;
        color: #4ade80;
        text-transform: uppercase;
    }

    .player-name {
        background-color: #0f172a;
        color: #ffffff;
        font-size: 13px;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 4px;
        border-left: 3px solid #38bdf8;
        margin-top: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .player-name-pass {
        border-left-color: #4ade80;
    }

    label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weekday_idx(day, month_name, year):
    month_idx = MESI_ITA.index(month_name) + 1
    return datetime(year, month_idx, day).weekday()

def draw_grid(data, is_history=False, key_prefix="grid"):
    mese_nom = st.session_state.get('sel_mese', "Settembre")
    anno_val = st.session_state.get('sel_anno', 2026)
    
    first_day_wd = get_weekday_idx(1, mese_nom, anno_val)
    full_display_list = [{"type": "empty"}] * first_day_wd
    for item in data:
        full_display_list.append({"type": "data", "content": item})
    
    n_cols = 7
    opts_all = ["---"] + sorted(all_active_names)

    for i in range(0, len(full_display_list), n_cols):
        cols = st.columns(n_cols)
        chunk = full_display_list[i:i + n_cols]
        for j, item in enumerate(chunk):
            with cols[j]:
                if item["type"] == "empty":
                    st.markdown('<div style="min-height: 140px;"></div>', unsafe_allow_html=True)
                else:
                    r = item["content"]
                    giorno = r['Giorno']
                    wd_idx = get_weekday_idx(giorno, mese_nom, anno_val)
                    wd_display = GIORNI_SETTIMANA[wd_idx]
                    
                    st.markdown(f"""
                    <div class="clean-card">
                        <div class="card-header">{wd_display[:3].upper()} {giorno}</div>
                        <div class="role-container">
                            <div class="role-badge-capo">👑 Capo Treno</div>
                            <div class="player-name">{r['Capo']}</div>
                        </div>
                        <div class="role-container" style="margin-top: 8px;">
                            <div class="role-badge-pass">🎫 Passeggero</div>
                            <div class="player-name player-name-pass">{r['Pass']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not is_history:
                        with st.popover("Modifica", use_container_width=True):
                            st.caption(f"Giorno {giorno}")
                            nc = st.selectbox("Capo Treno", opts_all, index=opts_all.index(r['Capo']) if r['Capo'] in opts_all else 0, key=f"sel_c_{key_prefix}_{giorno}")
                            np = st.selectbox("Passeggero", opts_all, index=opts_all.index(r['Pass']) if r['Pass'] in opts_all else 0, key=f"sel_p_{key_prefix}_{giorno}")
                            
                            if st.button("Salva", key=f"s_{key_prefix}_{giorno}", use_container_width=True):
                                for idx, m_item in enumerate(st.session_state['master_cal']):
                                    if m_item["Giorno"] == giorno:
                                        st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np})
                                        break
                                st.rerun()

# --- HEADER ---
st.markdown('<div class="app-title">🚆 CALENDARIO TRENI AOSR</div>', unsafe_allow_html=True)

# DASHBOARD DI CONTROLLO SQUADRATA
c1, c2, c3, c4 = st.columns([1, 1, 1.5, 1.5])
with c1: st.session_state['sel_mese'] = st.selectbox("Mese:", MESI_ITA, index=8)
with c2: st.session_state['sel_anno'] = st.number_input("Anno:", 2024, 2030, 2026)
with c3: sel_phase = st.selectbox("Algoritmo:", ["Fase 1 (Primi 2 Mesi)", "Fase 2 (Transizione Mese 3)", "Fase 3 (A Regime)"])
with c4: merito_days_input = st.multiselect("Giorni Riservati R4:", list(range(12, 32)), default=[12, 15, 18, 22, 28])

st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)

# PULSANTI AZIONE ALLINEATI
cb1, cb2, cb3, cb4 = st.columns([1.5, 1.2, 1.2, 1])

with cb1:
    if st.button("✨ Genera Turni", use_container_width=True):
        p_l = leaders_list
        p_o = r3_r2_list
        all_players = sorted(list(set(p_l + p_o)))
        
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = []
        
        current_assignments = {"capo": defaultdict(int), "pass": defaultdict(int)}
        
        for g in range(1, num_gg + 1):
            if g in merito_days_input:
                c = "--- (RISERVATO)"
                p = "--- (RISERVATO)"
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
    if st.button("💾 Salva in Archivio", use_container_width=True):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({
                "data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}",
                "mese": st.session_state['sel_mese'],
                "anno": st.session_state['sel_anno'],
                "ts": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "cal": [dict(d) for d in st.session_state['master_cal']]
            })
            save_history()
            st.toast("Salvato con successo!")
            st.rerun()

with cb3:
    if st.button("↩️ Annulla Ultimo", use_container_width=True):
        if st.session_state['history']:
            st.session_state['history'].pop()
            save_history()
            st.toast("Annullato!")
            st.rerun()

with cb4:
    if st.button("🧹 Reset", use_container_width=True):
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = [{"Giorno": g, "Capo": "---", "Pass": "---"} for g in range(1, num_gg + 1)]

st.markdown("<br>", unsafe_allow_html=True)

# --- TABS PER VISIONE GRAFICA ED ESPORTAZIONE PER ALLEATI ---
tab_grafica, tab_alleati, tab_stats = st.tabs(["📅 CALENDARIO VISIVO", "💬 ESPORTA TESTO PER CHAT/ALLEATI", "📊 STATISTICHE"])

with tab_grafica:
    if 'master_cal' in st.session_state:
        st.markdown(f"#### Mese di {st.session_state['sel_mese']} {st.session_state['sel_anno']}")
        draw_grid(st.session_state['master_cal'], key_prefix="master")

with tab_alleati:
    if 'master_cal' in st.session_state:
        st.markdown("#### Testo Formattato per Telegram / Discord / WhatsApp")
        st.caption("Copia il testo sottostante e incollalo nella chat dell'alleanza:")
        
        text_export = f"📅 **CALENDARIO TRENI - {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}**\n\n"
        for r in st.session_state['master_cal']:
            giorno = r['Giorno']
            wd_idx = get_weekday_idx(giorno, st.session_state['sel_mese'], st.session_state['sel_anno'])
            wd_name = GIORNI_ABBR[wd_idx]
            text_export += f"• **{wd_name} {giorno:02d}**: Capo 👑 `{r['Capo']}` | Pass 🎫 `{r['Pass']}`\n"
            
        st.code(text_export, language="markdown")

with tab_stats:
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

    st.dataframe(df_stats, use_container_width=True, hide_index=True)

# --- ARCHIVIO ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 📁 ARCHIVIO STORICO")

if st.session_state['history']:
    for idx, item in enumerate(reversed(st.session_state['history'])):
        real_idx = len(st.session_state['history']) - 1 - idx
        with st.expander(f"Mese: {item['data']} (Salvato il {item['ts']})"):
            c_del1, c_del2 = st.columns([5, 1])
            with c_del2:
                if st.button("Elimina", key=f"del_hist_{real_idx}", use_container_width=True):
                    st.session_state['history'].pop(real_idx)
                    save_history()
                    st.rerun()
            with c_del1:
                st.dataframe(pd.DataFrame(item['cal']), use_container_width=True, hide_index=True)
