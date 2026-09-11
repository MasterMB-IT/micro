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
st.set_page_config(page_title="AOSR Express 2099 - Hyperloop Manager", layout="wide")

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

# --- STILE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800;900&family=Rajdhani:wght@600;700&display=swap');
    .stApp { background: radial-gradient(circle at 50% 10%, #150d2a 0%, #080811 100%); color: #e0e6ed; }
    .train-title { font-family: 'Orbitron', sans-serif; text-align: center; color: #00f3ff; text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff; font-size: 3rem; font-weight: 900; margin-bottom: 20px; }
    .cal-header-container { display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 15px; }
    .cal-header-text { font-family: 'Orbitron', sans-serif; color: #ff007f; text-shadow: 0 0 10px #ff007f; font-size: 2rem; margin: 0; }
    .sala-comando { background: rgba(16, 12, 34, 0.75); backdrop-filter: blur(12px); border: 1px solid #00f3ff; border-radius: 12px; padding: 25px; margin-bottom: 30px; }
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0px !important; }
    .calendar-cell { background: rgba(15, 15, 30, 0.85); border: 1px solid rgba(0, 243, 255, 0.25); padding: 12px 10px; color: #ffffff; display: flex; flex-direction: column; transition: all 0.3s ease; margin: -0.5px; position: relative; }
    .calendar-cell:hover { border-color: #ff007f; box-shadow: 0 0 15px rgba(255, 0, 127, 0.4); z-index: 10; transform: translateY(-2px); }
    .h-norm { min-height: 230px !important; }
    .h-comp { min-height: 175px !important; }
    .card-placeholder { background: rgba(5, 5, 12, 0.4); border: 1px dashed rgba(255,255,255,0.1); }
    .day-badge { background: linear-gradient(135deg, #7b2cbf, #ff007f); color: #ffffff; font-family: 'Orbitron', sans-serif; font-weight: 800; padding: 3px 8px; border-radius: 4px; font-size: 0.72rem; width: fit-content; margin-bottom: 8px; }
    .role-label { color: #00f3ff; font-size: 0.65rem; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; font-weight: 700; border-bottom: 1px solid rgba(0, 243, 255, 0.2); margin-top: 6px; }
    .name-text { font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; border-left: 3px solid #ff007f; padding-left: 6px; overflow: hidden; white-space: nowrap; margin-top: 3px; color: #ffffff !important; }
    .stButton>button { border-radius: 6px !important; font-family: 'Orbitron', sans-serif !important; font-size: 0.8rem !important; }
    .btn-genera button { background: transparent !important; color: #00f3ff !important; border: 1px solid #00f3ff !important; }
    .btn-genera button:hover { background: #00f3ff !important; color: #080811 !important; }
    div[data-testid="stPopover"] > button { height: 26px !important; width: 100% !important; margin-top: 8px !important; font-size: 0.7rem !important; border: 1px solid #7b2cbf !important; background: rgba(123, 44, 191, 0.2) !important; color: #00f3ff !important; }
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
                            nc = st.selectbox("Capo", opts_all, index=opts_all.index(r['Capo']) if r['Capo'] in opts_all else 0, key=f"sel_c_{key_prefix}_{giorno}")
                            np = st.selectbox("Pass", opts_all, index=opts_all.index(r['Pass']) if r['Pass'] in opts_all else 0, key=f"sel_p_{key_prefix}_{giorno}")
                            
                            if st.button("SALVA", key=f"s_{key_prefix}_{giorno}", use_container_width=True):
                                for idx, m_item in enumerate(st.session_state['master_cal']):
                                    if m_item["Giorno"] == giorno:
                                        st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np})
                                        break
                                st.rerun()

# --- DASHBOARD PRINCIPALE ---
st.markdown('<div class="train-title">🚝 AOSR HYPERLOOP 2099</div>', unsafe_allow_html=True)
st.markdown('<div class="sala-comando">', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1, 1, 1.5, 1.5])
with c1: st.session_state['sel_mese'] = st.selectbox("📅 MESE", MESI_ITA, index=8)
with c2: st.session_state['sel_anno'] = st.number_input("📆 ANNO", 2024, 2030, 2026)
with c3: sel_phase = st.selectbox("⚖️ FASE BILANCIAMENTO", ["Fase 1 (Primi 2 Mesi)", "Fase 2 (Transizione Mese 3)", "Fase 3 (A Regime)"])
with c4: merito_days_input = st.multiselect("🎖️ 5 GIORNI MERITO (R4)", list(range(12, 32)), default=[12, 15, 18, 22, 28])

st.markdown('<div style="margin-top:15px; padding-top:15px; border-top:1px solid rgba(0,243,255,0.2)">', unsafe_allow_html=True)
cb1, cb2, cb3, cb4, cb5 = st.columns([1.5, 1.2, 1.4, 1, 1])

with cb1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("⚡ GENERA CALENDARIO ALLEANZA", use_container_width=True):
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
            
    st.markdown('</div>', unsafe_allow_html=True)

with cb2:
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
            st.toast("Salvato con successo!")
            st.rerun()

with cb3:
    # PULSANTE ANNULLA ULTIMO SALVATAGGIO
    if st.button("🔙 ANNULLA ULTIMO SALVATAGGIO", use_container_width=True):
        if st.session_state['history']:
            last_saved = st.session_state['history'].pop()
            save_history()
            st.toast(f"Rimesso indietro lo storico! Eliminato: {last_saved['data']}")
            st.rerun()
        else:
            st.toast("Nessun salvataggio presente nello storico!")

with cb4:
    if st.button("🌐 RESET", use_container_width=True):
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = [{"Giorno": g, "Capo": "---", "Pass": "---"} for g in range(1, num_gg + 1)]

with cb5:
    view_mode = st.toggle("🎞️ VISTA COMPATTA", value=False)

st.markdown('</div>', unsafe_allow_html=True)

# --- RENDERING GRIGLIA ---
if 'master_cal' in st.session_state:
    st.markdown(f"""
        <div class="cal-header-container">
            <span class="cal-header-text">AOSR - {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</span>
        </div>
    """, unsafe_allow_html=True)
    draw_grid(st.session_state['master_cal'], compact=view_mode, key_prefix="master")

# --- PANNELLO ARCHIVIO E CRONOLOGIA ---
st.markdown("<br><hr style='border:1px solid rgba(0,243,255,0.2)'><br>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#ff007f; font-family:Orbitron; text-align:center;'>📜 ARCHIVIO MESI E GESTIONE SALVATAGGI</h2>", unsafe_allow_html=True)

if st.session_state['history']:
    st.caption("Qui puoi visualizzare o cancellare qualsiasi mese salvato in precedenza. Eliminando un mese, lo storico dei giocatori tornerà indietro automaticamente.")
    
    for idx, item in enumerate(reversed(st.session_state['history'])):
        real_idx = len(st.session_state['history']) - 1 - idx
        with st.expander(f"📌 {item['data']} (Salvato il {item['ts']})"):
            c_del1, c_del2 = st.columns([4, 1])
            with c_del2:
                if st.button("🗑️ ELIMINA QUESTO MESE", key=f"del_hist_{real_idx}", use_container_width=True):
                    st.session_state['history'].pop(real_idx)
                    save_history()
                    st.toast("Mese eliminato dallo storico!")
                    st.rerun()
            
            with c_del1:
                st.caption("Anteprima Turni Salvati:")
                df_hist_preview = pd.DataFrame(item['cal'])
                st.dataframe(df_hist_preview, use_container_width=True, hide_index=True)
else:
    st.info("Nessun mese salvato in memoria.")

# --- PANNELLO STATISTICHE COMPLETO ---
st.markdown("<br><hr style='border:1px solid rgba(0,243,255,0.2)'><br>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#00f3ff; font-family:Orbitron; text-align:center;'>📊 STATISTICHE E MODIFICA STORICO</h2>", unsafe_allow_html=True)

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

tab_stat1, tab_stat2 = st.tabs(["📋 TABELLA GENERALE", "✏️ MODIFICA MANUALMENTE LO STORICO"])

with tab_stat1:
    st.dataframe(df_stats, use_container_width=True, hide_index=True)

with tab_stat2:
    st.caption("Sovrascrivi qui le presenze di qualsiasi membro. L'algoritmo userà immediatamente questi valori.")
    target_player = st.selectbox("Seleziona Giocatore:", all_active_names, key="override_player_select")
    
    if target_player:
        norm_target = smart_normalize_name(target_player)
        curr_c = capo_hist_total.get(norm_target, 0)
        curr_p = pass_hist_total.get(norm_target, 0)
        
        col_m1, col_m2 = st.columns(2)
        new_c = col_m1.number_input(f"⚡ Turni CAPO per {target_player}:", min_value=0, max_value=100, value=curr_c)
        new_p = col_m2.number_input(f"💺 Turni PASSEGGERO per {target_player}:", min_value=0, max_value=100, value=curr_p)
            
        col_btn_sav, col_btn_res = st.columns(2)
        if col_btn_sav.button("💾 APPLICA E SALVA", use_container_width=True):
            st.session_state['manual_overrides'][norm_target] = {"capo": new_c, "pass": new_p}
            save_overrides()
            st.toast("Salvato!")
            st.rerun()
            
        if norm_target in st.session_state['manual_overrides']:
            if col_btn_res.button("🔄 RIPRISTINA ORIGINALE", use_container_width=True):
                del st.session_state['manual_overrides'][norm_target]
                save_overrides()
                st.rerun()
