import streamlit as st
import pandas as pd
import calendar
import random
import io
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- DATABASE ---
if 'players_db' not in st.session_state:
    data = []
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3: data.append({"Nome": n, "Grado": "R3"})
    
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2: data.append({"Nome": n, "Grado": "R2"})
    st.session_state['players_db'] = pd.DataFrame(data)
    st.session_state['sel_mese'] = "Marzo"
    st.session_state['sel_anno'] = 2026

# --- FUNZIONE EXPORT EXCEL (PER EVITARE L'ERRORE CSV) ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Calendario')
    return output.getvalue()

# --- INTERFACCIA ---
if not st.session_state.get('print_mode', False):
    st.title("🚂 AOSR EXPRESS MANAGER")
    
    if st.button("🚀 GENERA NUOVO CALENDARIO"):
        db = st.session_state['players_db']
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        pool = db[db['Grado'] != "R5/R4"]['Nome'].tolist()
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
            cal.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
        st.session_state['master_cal'] = cal

if 'master_cal' in st.session_state:
    df_cal = pd.DataFrame(st.session_state['master_cal'])
    
    # --- VISUALIZZAZIONE CALENDARIO (OMESSA PER BREVITA') ---
    st.markdown(f"## Calendario {st.session_state['sel_mese']} {st.session_state['sel_anno']}")
    st.dataframe(df_cal, use_container_width=True) # Tabella pulita in App

    # --- SEZIONE DOWNLOAD ---
    st.markdown("### 📥 Scarica i Risultati")
    col1, col2 = st.columns(2)
    
    # Download EXCEL (Risolve il problema delle colonne unite)
    excel_data = to_excel(df_cal)
    col1.download_button(
        label="📊 Scarica in EXCEL (Colonne divise)",
        data=excel_data,
        file_name=f"Calendario_AOSR_{st.session_state['sel_mese']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Bottone per Modalità Foto (quello che avevamo fatto prima)
    if col2.button("📸 Modalità Foto (Screenshot)"):
        st.session_state['print_mode'] = True
        st.rerun()

if st.session_state.get('print_mode', False):
    if st.button("🔙 Torna alla gestione"):
        st.session_state['print_mode'] = False
        st.rerun()
