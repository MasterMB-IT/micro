import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- DATABASE AGGIORNATO ---
if 'players_db' not in st.session_state:
    data = []
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3: data.append({"Nome": n, "Grado": "R3"})
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2: data.append({"Nome": n, "Grado": "R2"})
    st.session_state['players_db'] = pd.DataFrame(data)
    st.session_state['sel_mese'] = list(calendar.month_name)[datetime.now().month]
    st.session_state['sel_anno'] = 2026

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .print-container { 
        background-color: #000000 !important; padding: 30px !important; 
        border: 3px solid #00c8ff; border-radius: 10px;
    }
    .summary-card {
        background: #111; border: 1px solid #333; padding: 10px; 
        text-align: center; border-radius: 8px; margin-bottom: 10px;
    }
    .day-label { color: #00c8ff; font-weight: 900; border-bottom: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DOWNLOAD SICURO ---
def capture_logic():
    components.html("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <div id="status" style="color: #00c8ff; font-family: sans-serif; font-size: 14px; margin-bottom: 10px;">
        Pronto per la cattura...
    </div>
    <button onclick="doCapture()" style="background: #2ed573; border: none; padding: 15px 30px; color: black; font-weight: bold; border-radius: 5px; cursor: pointer; width: 100%;">
        CLICCA QUI PER SCARICARE L'IMMAGINE
    </button>
    
    <script>
    function doCapture() {
        const area = window.parent.document.querySelector('.print-container');
        const status = document.getElementById('status');
        status.innerText = "Elaborazione immagine... attendi...";
        
        html2canvas(area, { backgroundColor: "#000000", scale: 2 }).then(canvas => {
            const link = document.createElement('a');
            link.href = canvas.toDataURL("image/png");
            link.download = 'Calendario_AOSR.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            status.innerText = "✅ SCARICATO CON SUCCESSO!";
        }).catch(err => {
            status.innerText = "❌ Errore. Usa lo screenshot manuale.";
        });
    }
    </script>
    """, height=120)

# --- INTERFACCIA ---
st.title("🚂 AOSR EXPRESS MANAGER")

with st.expander("⚙️ IMPOSTAZIONI", expanded=True):
    c1, c2 = st.columns([1,2])
    st.session_state['sel_mese'] = c1.selectbox("Mese", list(calendar.month_name)[1:], index=list(calendar.month_name).index(st.session_state['sel_mese'])-1)
    st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])

if st.button("🚀 GENERA CALENDARIO", use_container_width=True):
    db = st.session_state['players_db']
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    pool = db[db['Grado']!="R5/R4"]['Nome'].tolist()
    random.shuffle(pool)
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

if 'master_cal' in st.session_state:
    st.markdown(f"### 🖼️ CALENDARIO {st.session_state['sel_mese'].upper()}")
    
    # Area Calendario
    st.markdown('<div class="print-container">', unsafe_allow_html=True)
    cols_per_row = 6
    for i in range(0, len(st.session_state['master_cal']), cols_per_row):
        row_data = st.session_state['master_cal'][i : i + cols_per_row]
        grid = st.columns(cols_per_row)
        for idx, r in enumerate(row_data):
            grid[idx].markdown(f"""
            <div class="summary-card">
                <div class="day-label">GG {r['Giorno']}</div>
                <div style="color:#2ed573; font-size:0.8rem; font-weight:bold;">{r['Capo']}</div>
                <div style="color:#a29bfe; font-size:0.8rem; font-weight:bold;">{r['Pass']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("📥 SALVATAGGIO FOTO")
    # Il componente di cattura viene visualizzato qui
    capture_logic()
