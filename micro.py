import os
import json
import re
import unicodedata
import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURAZIONE E FILE JSON
# ==========================================
DB_FILE = "cronologia_treni.json"
OVERRIDES_FILE = "manual_overrides.json"

st.set_page_config(
    page_title="Gestore Treni AOSR",
    page_icon="🚆",
    layout="wide"
)

# ==========================================
# FUNZIONI DI LETTURA E SALVATAGGIO SICURO
# ==========================================
def load_json_file(file_path, default_data):
    """Carica un file JSON se esiste, altrimenti restituisce il valore di default."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Errore nel caricamento di {file_path}: {e}")
    return default_data

def save_json_file(file_path, data):
    """Salva i dati su file JSON in maniera atomica forzando il flush del disco."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception as e:
        st.error(f"Errore durante il salvataggio in {file_path}: {e}")
        return False

# ==========================================
# INIZIALIZZAZIONE SESSION STATE
# ==========================================
# Caricamento o creazione del calendario predefinito (Settembre 2026)
default_september = [
    {"giorno": 1, "capo_treno": "SHINYPASTA (R4)", "passeggero_vip": "IMADE"},
    {"giorno": 2, "capo_treno": "ΨWALLΨ (R4)", "passeggero_vip": "WHALE PANDA"},
    {"giorno": 3, "capo_treno": "SAGITTARIUS A1 (R4)", "passeggero_vip": "TRIVELLATORE"},
    {"giorno": 4, "capo_treno": "Ｍａメツ (R4)", "passeggero_vip": "PEMBE KOMUTAN"},
    {"giorno": 5, "capo_treno": "亗 HOOL 亗 (R5)", "passeggero_vip": "LEECHAI"},
    {"giorno": 6, "capo_treno": "RICKY AROUND (R4)", "passeggero_vip": "PURPIX7"},
    {"giorno": 7, "capo_treno": "09ALEX24 (R4)", "passeggero_vip": "ZAAAAAAAAYYYYY"},
    {"giorno": 8, "capo_treno": "彡M A S T E R彡 (R4)", "passeggero_vip": "BONNYAND"},
    {"giorno": 9, "capo_treno": "LE 12 SCIMMIE (R4)", "passeggero_vip": "DARK LALLA"},
    {"giorno": 10, "capo_treno": "PΞPPΞ (R4)", "passeggero_vip": "RIKKI SAJO"},
    {"giorno": 11, "capo_treno": "XFLOTCHY (R4)", "passeggero_vip": "PUPISNIC"},
    {"giorno": 12, "capo_treno": "ZOKRA", "passeggero_vip": "MUSCOLEENI"},
    {"giorno": 13, "capo_treno": "ARESARWEN", "passeggero_vip": "RND66"},
    {"giorno": 14, "capo_treno": "PAKII", "passeggero_vip": "ღNeyღ"},
    {"giorno": 15, "capo_treno": "YEAH YEAH COCO JAMBO", "passeggero_vip": "UNCLE G BROTHER"},
    {"giorno": 16, "capo_treno": "SIR LANCE OF N8WATCH", "passeggero_vip": "ᶜᵃᵖᵒ ΘᴥΘ"},
    {"giorno": 17, "capo_treno": "HOLDFAST", "passeggero_vip": "MMTYY"},
    {"giorno": 18, "capo_treno": "MORTEN1212", "passeggero_vip": "DRAGONS SLAYER"},
    {"giorno": 19, "capo_treno": "JAXXTRONIC", "passeggero_vip": "さGhandyる"},
    {"giorno": 20, "capo_treno": "COMANDANTE MAVERIC", "passeggero_vip": "CONTROVENTO6"},
    {"giorno": 21, "capo_treno": "Ξ GHOST Ξ", "passeggero_vip": "X THE LORD X"},
    {"giorno": 22, "capo_treno": "BRANCII", "passeggero_vip": "ᴮᵃⁿᵃⁿᵃ B"},
    {"giorno": 23, "capo_treno": "MARTINSK", "passeggero_vip": "PØNTΔTINΔTØRΞ"},
    {"giorno": 24, "capo_treno": "TCHIK", "passeggero_vip": "INIURIA"},
    {"giorno": 25, "capo_treno": "VINCENZOPOMA89", "passeggero_vip": "o GARGANTUA o"},
    {"giorno": 26, "capo_treno": "ARYRON", "passeggero_vip": "MISSDRINKS"},
    {"giorno": 27, "capo_treno": "F3NRYU", "passeggero_vip": "DOME B"},
    {"giorno": 28, "capo_treno": "J๏รєקקђoNe", "passeggero_vip": "NOVEMBERGENZ"},
    {"giorno": 29, "capo_treno": "KROMPIR", "passeggero_vip": "THEDANE001"},
    {"giorno": 30, "capo_treno": "WOLF006", "passeggero_vip": "G ΣRRY"}
]

# Modifiche manuali predefinite della tabella dello storico
default_overrides = {
    "09ALEX24 (R4)": {"turni_capo": 5, "turni_passeggero": 6, "totale_presenze": 11},
    "Sagittarius A1 (R4)": {"turni_capo": 5, "turni_passeggero": 5, "totale_presenze": 10},
    "ShinyPasta (R4)": {"turni_capo": 5, "turni_passeggero": 5, "totale_presenze": 10},
    "J๏รєקקђoNe": {"turni_capo": 5, "turni_passeggero": 4, "totale_presenze": 9},
    "PΞPPΞ (R4)": {"turni_capo": 5, "turni_passeggero": 4, "totale_presenze": 9},
    "Ricky Around (R4)": {"turni_capo": 5, "turni_passeggero": 4, "totale_presenze": 9},
    "ΨWallΨ (R4)": {"turni_capo": 5, "turni_passeggero": 4, "totale_presenze": 9},
    "亗 Hool 亗 (R5)": {"turni_capo": 5, "turni_passeggero": 4, "totale_presenze": 9},
    "彡M A S T E R彡 (R4)": {"turni_capo": 5, "turni_passeggero": 4, "totale_presenze": 9},
    "BadBigBoss": {"turni_capo": 4, "turni_passeggero": 4, "totale_presenze": 8}
}

if 'history' not in st.session_state:
    st.session_state['history'] = load_json_file(DB_FILE, default_september)

if 'manual_overrides' not in st.session_state:
    st.session_state['manual_overrides'] = load_json_file(OVERRIDES_FILE, default_overrides)

# ==========================================
# UTILITY ESPORTAZIONE CSV
# ==========================================
@st.cache_data
def convert_df_to_csv(df):
    """Converte un DataFrame Pandas in stringa CSV codificata UTF-8."""
    return df.to_csv(index=False).encode('utf-8')

# ==========================================
# INTERFACCIA PRINCIPALE
# ==========================================
st.title("📊 STATISTICHE E MODIFICA STORICO")

# Navigazione a Schede (Tabs)
tab1, tab2 = st.tabs(["📊 TABELLA GENERALE", "✏️ MODIFICA MANUALMENTE LO STORICO"])

# ------------------------------------------
# TAB 1: TABELLA GENERALE E STATISTICHE
# ------------------------------------------
with tab1:
    st.subheader("Riepilogo Totale Presenze e Turni")

    # Elaborazione delle statistiche aggregate
    stats_map = {}
    
    # 1. Calcolo presenze dalla cronologia salvata
    for item in st.session_state['history']:
        capo = item.get("capo_treno", "")
        pass_vip = item.get("passeggero_vip", "")
        
        if capo:
            if capo not in stats_map:
                stats_map[capo] = {"Turni Capo": 0, "Turni Passeggero": 0}
            stats_map[capo]["Turni Capo"] += 1
            
        if pass_vip:
            if pass_vip not in stats_map:
                stats_map[pass_vip] = {"Turni Capo": 0, "Turni Passeggero": 0}
            stats_map[pass_vip]["Turni Passeggero"] += 1

    # 2. Applicazione manual_overrides se presenti
    for gioc, ov in st.session_state['manual_overrides'].items():
        if gioc not in stats_map:
            stats_map[gioc] = {"Turni Capo": 0, "Turni Passeggero": 0}
        stats_map[gioc]["Turni Capo"] = ov.get("turni_capo", stats_map[gioc]["Turni Capo"])
        stats_map[gioc]["Turni Passeggero"] = ov.get("turni_passeggero", stats_map[gioc]["Turni Passeggero"])

    # Costruzione DataFrame per la visualizzazione
    table_rows = []
    for giocatore, counts in stats_map.items():
        t_capo = counts["Turni Capo"]
        t_pass = counts["Turni Passeggero"]
        totale = t_capo + t_pass
        table_rows.append({
            "Giocatore": giocatore,
            "Turni Capo": t_capo,
            "Turni Passeggero": t_pass,
            "Totale Presenze": totale
        })

    df_general = pd.DataFrame(table_rows)
    
    if not df_general.empty:
        # Ordina per Totale Presenze decrescente
        df_general = df_general.sort_values(by=["Totale Presenze", "Turni Capo"], ascending=False).reset_index(drop=True)
        
        # Visualizza la tabella
        st.dataframe(df_general, use_container_width=True, height=450)
        
        # PULSANTE ESTRAZIONE CSV STORICO
        csv_bytes_stat = convert_df_to_csv(df_general)
        
        col_dl1, col_dl2 = st.columns([1, 3])
        with col_dl1:
            st.download_button(
                label="📥 Scarica Storico (.CSV)",
                data=csv_bytes_stat,
                file_name="storico_generale_presenze.csv",
                mime="text/csv",
                key="btn_download_stat_csv",
                help="Clicca qui per esportare la tabella dello storico direttamente in formato CSV per Excel"
            )
    else:
        st.info("Nessun dato presente nello storico.")

# ------------------------------------------
# TAB 2: MODIFICA MANUALE E OVERRIDES
# ------------------------------------------
with tab2:
    st.subheader("Modifica o Aggiungi Presenze Manuali nello Storico")
    
    # Prepariamo un dataframe modificabile con st.data_editor
    overrides_rows = []
    for giog, vals in st.session_state['manual_overrides'].items():
        overrides_rows.append({
            "Giocatore": giog,
            "Turni Capo": vals.get("turni_capo", 0),
            "Turni Passeggero": vals.get("turni_passeggero", 0)
        })
    
    df_editable = pd.DataFrame(overrides_rows)
    
    st.write("Puoi modificare direttamente i valori delle celle qui sotto o aggiungere nuovi giocatori:")
    
    edited_df = st.data_editor(
        df_editable,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_overrides"
    )
    
    col_save, col_exp = st.columns([1, 2])
    
    with col_save:
        if st.button("💾 Salva Modifiche nello Storico", type="primary"):
            # Riconvertiamo il DataFrame modificato nel dizionario
            new_overrides = {}
            for _, row in edited_df.iterrows():
                name = str(row["Giocatore"]).strip()
                if name:
                    t_capo = int(row["Turni Capo"]) if pd.notnull(row["Turni Capo"]) else 0
                    t_pass = int(row["Turni Passeggero"]) if pd.notnull(row["Turni Passeggero"]) else 0
                    new_overrides[name] = {
                        "turni_capo": t_capo,
                        "turni_passeggero": t_pass,
                        "totale_presenze": t_capo + t_pass
                    }
            
            # Aggiorna lo stato della sessione e salva su disco
            st.session_state['manual_overrides'] = new_overrides
            if save_json_file(OVERRIDES_FILE, new_overrides):
                st.success("Storico aggiornato e salvato con successo su disco!")
                st.rerun()

    with col_exp:
        # PULSANTE PER ESTRARRE I DATI MODIFICATI IN CSV
        csv_bytes_edit = convert_df_to_csv(edited_df)
        st.download_button(
            label="📥 Esporta Modifiche Manuali (.CSV)",
            data=csv_bytes_edit,
            file_name="modifiche_manuali_storico.csv",
            mime="text/csv",
            key="btn_download_manual_csv"
        )
