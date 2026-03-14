import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .aosr-header {
        background: linear-gradient(135deg, #1a1f2c 0%, #0b0e14 100%);
        padding: 25px; border-radius: 15px; border: 2px solid #00c8ff;
        text-align: center; margin-bottom: 20px;
    }
    .aosr-title { font-family: 'Orbitron', sans-serif; color: #00c8ff; font-size: 2.2rem; letter-spacing: 3px; margin: 0; }
    
    .p-box { padding: 6px 10px; border-radius: 6px; margin: 3px 0; font-size: 0.85rem; text-transform: uppercase; font-weight: bold; }
    .r5-r4-card { background: rgba(255, 71, 87, 0.2); border-left: 4px solid #ff4757; color: #ff4757; }
    .r3-card { background: rgba(46, 213, 115, 0.2); border-left: 4px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.2); border-left: 4px solid #a29bfe; color: #a29bfe; }

    /* Area Foto */
    .print-container { 
        background-color: #000000 !important; 
        padding: 40px !important; 
        border: 4px solid #00c8ff;
        border-radius: 10px;
    }
    .summary-card {
        background: #111; border: 1px solid #333; padding: 12px; 
        text-align: center; border-radius: 10px; margin-bottom: 15px;
        min-height: 110px;
    }
    .day-label { color: #00c8ff; font-weight: 900; font-size: 0.9rem; border-bottom: 1px solid #222; margin-bottom: 8px; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- DATABASE ---
if 'players_db' not in st.session_state:
    data = []
    # R4/R5
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    # R3
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3: data.append({"Nome": n, "Grado": "R3"})
    # R2
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2: data.append({"Nome": n, "Grado": "R2"})
    st.session_state['players_db'] = pd.DataFrame(data)
    st.session_state['sel_mese'] = list(calendar.month_name)[datetime.now().month]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = db['Nome'].tolist()

# --- LOGICA SCREENSHOT ---
# Questa versione usa un trigger più diretto per forzare il download
def screenshot_component():
    components.html("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
    window.parent.document.addEventListener('screenshot_event', function() {
        const area = window.parent.document.querySelector('.print-container');
        if(area) {
            html2canvas(area, { backgroundColor: "#000000", scale: 2 }).then(canvas => {
                const base64image = canvas.toDataURL("image/png");
                const link = document.createElement('a');
                link.href = base64image;
                link.download = 'Calendario_AOSR.png';
                window.parent.document.body.appendChild(link);
                link.click();
                window.parent.document.body.removeChild(link);
            });
        }
    });
    </script>
    """, height=0)

# --- HEADER ---
st.markdown('<div class="aosr-header"><div class="aosr-title">AOSR EXPRESS MANAGER</div></div>', unsafe_allow_html=True)

# --- CONFIGURAZIONE ---
with st.expander("⚙️ IMPOSTAZIONI", expanded=True):
    c1, c2 = st.columns([1,2])
    st.session_state['sel_mese'] = c1.selectbox("Mese", list(calendar.month_name)[1:], index=list(calendar.month_name).index(st.session_state['sel_mese'])-1)
    st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    meritevoli = db[db['Grado'] != "R5/R4"]['Nome'].tolist()
    sel_meritevoli = c2.multiselect("Seleziona Partecipanti (Vuoto = TUTTI)", meritevoli)

if st.button("🚀 GENERA / AGGIORNA CALENDARIO", use_container_width=True):
    pool = sel_meritevoli if sel_meritevoli else meritevoli
    random.shuffle(pool)
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    num_gg = calendar.monthrange(st.session_state['sel_anno'], list(calendar.month_name).index(st.session_state['sel_mese']))[1]
    
    cal = []
    p_idx = 0
    for g in range(1, num_gg + 1):
        if g <= 11:
            c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
        else:
            c = pool[p_idx % len(pool)]; p_idx += 1
            p = pool[p_idx % len(pool)]; p_idx += 1
        cal.append({"Giorno": g, "Capo": c, "Pass": p})
    st.session_state['master_cal'] = cal

# --- DISPLAY ---
if 'master_cal' in st.session_state:
    screenshot_component() # Inizializza il modulo foto
    
    m_titolo = st.session_state['sel_mese'].upper()
    a_titolo = st.session_state['sel_anno']
    st.markdown(f"### 🖼️ CALENDARIO {m_titolo} {a_titolo}")
    
    # Area da scaricare
    st.markdown('<div class="print-container">', unsafe_allow_html=True)
    cols_per_row = 6
    for i in range(0, len(st.session_state['master_cal']), cols_per_row):
        row_data = st.session_state['master_cal'][i : i + cols_per_row]
        grid = st.columns(cols_per_row)
        for idx, r in enumerate(row_data):
            g_c = db[db['Nome']==r['Capo']]['Grado'].values[0] if r['Capo'] in all_names else "R3"
            g_p = db[db['Nome']==r['Pass']]['Grado'].values[0] if r['Pass'] in all_names else "R3"
            c_c = "#ff4757" if g_c == "R5/R4" else "#2ed573" if g_c == "R3" else "#a29bfe"
            p_c = "#ff4757" if g_p == "R5/R4" else "#2ed573" if g_p == "R3" else "#a29bfe"
            grid[idx].markdown(f"""
            <div class="summary-card">
                <div class="day-label">GG {r['Giorno']}</div>
                <div style="color:{c_c}; font-size:0.8rem; font-weight:bold;">{r['Capo']}</div>
                <div style="color:#444; font-size:0.5rem; margin:2px 0;">&</div>
                <div style="color:{p_c}; font-size:0.8rem; font-weight:bold;">{r['Pass']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- BOTTONE DI SCARICAMENTO ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SCARICA FOTO CALENDARIO (PNG)", type="primary", use_container_width=True):
        components.html("""
            <script>
            const event = new Event('screenshot_event');
            window.parent.document.dispatchEvent(event);
            </script>
        """, height=0)
        st.info("Download avviato! Controlla la cartella Download del tuo PC.")
