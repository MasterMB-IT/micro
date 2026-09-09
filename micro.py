import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar
from collections import defaultdict

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

# --- DATABASE MEMBRI AGGIORNATI ---
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

# --- DATI STORICI ESTRATTI DAI 5 MESI (APRILE - AGOSTO 2026) ---
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
        "UNCLE G BROTHER": 1, "MARIA": 1
    },
    "pass_counts": {
        "MAメツ": 4, "SHINYPASTA": 2, "MASTER": 3, "09ALEX24": 2, "GOZ": 1,
        "SAGITTARIUS A1": 2, "STARBETTY": 2, "RICKY AROUND": 2, "PEPPE": 2,
        "UNCLE G BROTHER": 3, "LE 12 SCIMMIE": 2, "HOOL": 3, "G ERRY": 2,
        "WOLFOO6": 3, "ARYRON": 2, "BENDICO": 2, "MISSDRINKS": 1, "MX63": 1,
        "STEFANO00000": 2, "PAKII": 2, "BANDOLERO26": 1, "MARKUS DEFENDED": 1,
        "WALL 7": 3, "EDDWARD": 2, "KROMPIR": 3, "GHANDAL": 1, "ZOKRA": 2,
        "CAMIIIII 08": 2, "JOSEPPONE": 3, "HULKSPAKKA": 2, "LE 12 SCIMMIE": 1,
        "BADBIGBOSS": 2, "YEAH YEAH OOOO": 1, "NOVEMBERGENZ": 2, "SAGITTARIUS A1": 1,
        "XFLOTCHY": 2, "BLOODYBLADE": 1, "ORAISHIO": 1, "PANDORE": 1, "MESHEL": 1,
        "SIR LANCE OF N81": 1, "VINCENZOPOMA89": 1, "ZAAAAAAAYYYYY": 2, "JAXXTRONIC": 1,
        "AGENT BASS": 1, "ARESARWEN": 1, "PSYKOS": 2, "SQUIRTLE ITA": 1, "STUNTMARK": 1,
        "SIR VONSKI": 1, "MOUK57": 2, "LIMAXIMUS": 1, "F3NRYU": 1, "REKLAUS": 1,
        "ELCHICOGYOT": 1, "LALLA 96": 1, "DARKGIOLLO": 1, "SPIO24": 2, "COMANDANTE MAV": 1,
        "SKITETO": 1, "ECHOZERO": 1, "TOMENERGY": 1, "GERRY": 1, "TRICHECO": 2,
        "PITT9595": 1, "CRUEL NEVE": 1, "GENNAROM": 1, "HOLDFAST": 1, "ANA BUNNY": 1,
        "BRANCII": 2, "STRUNZTRUPPEN": 2, "27FRANCESCO": 1, "LEFADA13": 1, "MELO65": 1,
        "PERSEUSXXX": 1, "BOGE": 1, "CASELLO": 1, "TCHIK": 1, "ZIO GIOTTO": 1,
        "KING GRUFFALO": 1, "VENUS31": 1
    }
}

# Normalize historical keys for matching
def norm_name(name):
    clean = name.split("(")[0].strip().upper()
    return clean

# --- ALGORITMO DI SELEZIONE BILANCIATO ---
def get_balanced_player(pool, role_type, current_assignments_this_month):
    """
    Seleziona il giocatore migliore in base allo storico dei 5 mesi:
    1. Chi non ha mai ricoperto il ruolo richiesto.
    2. Chi ha il minor numero di incarichi totali (Capo + Passeggero).
    3. Evita sovrapposizioni nello stesso mese corrente.
    """
    capo_hist = HISTORICAL_5_MONTHS["capo_counts"]
    pass_hist = HISTORICAL_5_MONTHS["pass_counts"]
    
    candidates = []
    
    for player in pool:
        # Conteggio nel mese che stiamo generando ora
        current_c = current_assignments_this_month["capo"][player]
        current_p = current_assignments_this_month["pass"][player]
        current_total = current_c + current_p
        
        # Conteggio nei 5 mesi passati
        n_p = norm_name(player)
        hist_c = 0
        hist_p = 0
        for k, v in capo_hist.items():
            if k in n_p or n_p in k: hist_c += v
        for k, v in pass_hist.items():
            if k in n_p or n_p in k: hist_p += v
            
        hist_role = hist_c if role_type == "capo" else hist_p
        hist_total = hist_c + hist_p
        
        # Priorità: (1) Mai fatto questo ruolo, (2) Meno presenze mese corrente, (3) Meno presenze storiche
        never_done_role = 1 if hist_role == 0 else 2
        
        candidates.append({
            "player": player,
            "never_done": never_done_role,
            "current_total": current_total,
            "hist_total": hist_total,
            "rand": random.random()
        })
        
    # Ordina i candidati per le priorità stabilite
    candidates.sort(key=lambda x: (x["never_done"], x["current_total"], x["hist_total"], x["rand"]))
    return candidates[0]["player"]

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background: linear-gradient(rgba(30, 20, 10, 0.8), rgba(15, 10, 5, 0.95)), url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop'); background-size: cover; background-attachment: fixed; }
    .train-title { font-family: 'Rye', cursive; text-align: center; color: #ffcc66; text-shadow: 5px 5px 0px #4b2e1b; font-size: 4rem; margin-bottom: 20px; }
    .cal-header-container { display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: -10px; }
    .cal-header-text { font-family: 'Rye', cursive; color: #ffcc66; font-size: 2.5rem; margin: 0; }
    .train-icon { font-size: 3rem; color: #ffcc66; }
    .sala-comando { background: rgba(25, 15, 5, 0.85); backdrop-filter: blur(10px); border: 2px solid #ffcc66; border-radius: 20px; padding: 25px; margin-bottom: 30px; border-top: 5px solid #ffcc66; }

    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0px !important; }

    .calendar-cell { 
        background: #fdf5e6; 
        border: 1px solid rgba(93, 64, 55, 0.4);
        padding: 12px 8px; 
        color: #2b1d0e; 
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png'); 
        display: flex; 
        flex-direction: column; 
        transition: 0.2s;
        margin: -0.5px;
    }
    .calendar-cell:hover { background-color: #fff9f0; z-index: 10; box-shadow: inset 0 0 10px rgba(0,0,0,0.1); }
    .h-norm { min-height: 230px !important; }
    .h-comp { min-height: 175px !important; }
    .card-placeholder { background: rgba(0,0,0,0.1); border: 1px solid rgba(93, 64, 55, 0.2); }
    .day-badge { background: #8b0000; color: white; font-family: 'Montserrat', sans-serif; font-weight: 900; padding: 2px 8px; border-radius: 2px; font-size: 0.75rem; width: fit-content; margin-bottom: 6px; }
    .role-label { color: #5d4037; font-size: 0.6rem; font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800; border-bottom: 1px solid rgba(93, 64, 55, 0.15); margin-top: 6px; }
    .name-text { font-family: 'Special Elite', cursive; font-size: 0.88rem; font-weight: 900; text-transform: uppercase; border-left: 3px solid #d4a373; padding-left: 6px; overflow: hidden; white-space: nowrap; margin-top: 2px; color: #000000 !important; }
    
    .stButton>button { border-radius: 6px !important; font-family: 'Rye', cursive !important; border: 2px solid #2b1d0e !important; }
    .btn-genera button { background: #d4a373 !important; color: #2b1d0e !important; }
    .btn-vuoto button { background: #5a5a5a !important; color: white !important; }
    .btn-assegna button { background: #1b4d3e !important; color: #2ecc71 !important; }
    
    div[data-testid="stPopover"] > button { height: 26px !important; width: 100% !important; margin-top: 8px !important; font-size: 0.75rem !important; border: 1px solid #d4a373 !important;}
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
                        <div class="day-badge">{wd_display} {giorno}</div>
                        <div class="role-label">CAPO {"⭐" if giorno <= 11 else ""}</div>
                        <div class="name-text">{r['Capo']}</div>
                        <div class="role-label">PASSEGGERO</div>
                        <div class="name-text">{r['Pass']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not is_history and not compact:
                        with st.popover("✍️ SCRIVI"):
                            st.caption(f"Modifica Giorno {giorno}")
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

# --- INTERFACCIA ---
st.markdown('<div class="train-title">🚂 AOSR EXPRESS Manager</div>', unsafe_allow_html=True)
st.markdown('<div class="sala-comando">', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.5, 2])
with c1:
    st.session_state['sel_mese'] = st.selectbox("📅 MESE", MESI_ITA, index=8) # Settembre
    st.session_state['sel_anno'] = st.number_input("📆 ANNO", 2024, 2030, 2026)
with c2: sel_leaders = st.multiselect("🤠 R5/R4", leaders_list)
with c3: sel_r3_r2 = st.multiselect("🌵 R3/R2", db[db['Grado'] == "R3/R2"]['Nome'].tolist())

st.markdown('<div style="margin-top:20px; padding-top:20px; border-top:1px solid rgba(255,204,102,0.2)">', unsafe_allow_html=True)
cb1, cb1b, cb2, cb3, cb4 = st.columns(5)

with cb1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("⚒️ GENERA AUTO (BILANCIATO)", use_container_width=True):
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
                # Primi 11 giorni: Capo da R5/R4, Passeggero da R3/R2
                c = get_balanced_player(p_l, "capo", current_assignments)
                p = get_balanced_player([x for x in p_o if x != c], "pass", current_assignments)
            else:
                # Dal 12 in poi: Entrambi da R3/R2
                c = get_balanced_player(p_o, "capo", current_assignments)
                p = get_balanced_player([x for x in p_o if x != c], "pass", current_assignments)
            
            current_assignments["capo"][c] += 1
            current_assignments["pass"][p] += 1
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
            
    st.markdown('</div>', unsafe_allow_html=True)

with cb1b:
    st.markdown('<div class="btn-vuoto">', unsafe_allow_html=True)
    if st.button("🆕 CREA VUOTO", use_container_width=True):
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = [{"Giorno": g, "Capo": "---", "Pass": "---"} for g in range(1, num_gg + 1)]
    st.markdown('</div>', unsafe_allow_html=True)

with cb2:
    if st.button("🔍 VERIFICA", use_container_width=True):
        if 'master_cal' in st.session_state:
            err_g = [f"GG {r['Giorno']}" for r in st.session_state['master_cal'] if r['Giorno'] <= 11 and r['Capo'] not in leaders_list and r['Capo'] != "---"]
            if err_g: st.warning(f"Nota: Capi non-R4 nei primi 11gg: {', '.join(err_g)}")
            else: st.success("Tutto perfetto!")

with cb3:
    st.markdown('<div class="btn-assegna">', unsafe_allow_html=True)
    if st.button("🟩 ASSEGNA", use_container_width=True):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({
                "data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}",
                "mese": st.session_state['sel_mese'],
                "anno": st.session_state['sel_anno'],
                "ts": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "cal": [dict(d) for d in st.session_state['master_cal']]
            })
            save_history()
            st.toast("Calendario Salvato!")

with cb4:
    if st.button("🏜️ RESET", use_container_width=True):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()

st.write("")
view_mode = st.toggle("🎞️ VISTA COMPATTA (Senza modifiche)", value=False)
st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    st.markdown(f"""
        <div class="cal-header-container">
            <span class="train-icon">🚂</span>
            <h2 class="cal-header-text">AOSR Express - {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h2>
            <span class="train-icon">🚂</span>
        </div>
    """, unsafe_allow_html=True)
    
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
