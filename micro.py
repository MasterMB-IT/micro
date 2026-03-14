import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. DATABASE NOMI ESTRATTI
leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", 
           "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", 
           "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]

r3_list = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", 
           "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", 
           "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", 
           "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", 
           "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", 
           "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", 
           "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", 
           "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", 
           "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]

st.title("🚂 Gestore Calendario Treni Alleanza")

# --- ANTE GENERAZIONE: SELEZIONE MERITEVOLI ---
st.sidebar.header("Sezione Meritevoli")
st.sidebar.write("Seleziona i membri R3 che partecipano questo mese:")
meritevoli_scelti = []
for nome in r3_list:
    if st.sidebar.checkbox(nome, key=nome):
        meritevoli_scelti.append(nome)

# --- LOGICA DI GENERAZIONE ---
if st.button("Genera Calendario Mensile"):
    giorni_mese = 30 # Può essere dinamico
    calendario = []
    
    # Primi 11 giorni: Leader
    for i in range(1, 12):
        capotreno = leaders[i-1]
        passeggero = "Da definire" # Qui puoi mettere logica per il passeggero
        calendario.append({"Giorno": i, "Capotreno": capotreno, "Passeggero": passeggero})
    
    # Resto del mese: Meritevoli
    index_m = 0
    if meritevoli_scelti:
        for i in range(12, giorni_mese + 1):
            capotreno = meritevoli_scelti[index_m % len(meritevoli_scelti)]
            calendario.append({"Giorno": i, "Capotreno": capotreno, "Passeggero": "Passeggero R3"})
            index_m += 1
            
    df = pd.DataFrame(calendario)
    
    # --- POST GENERAZIONE: EDITING ---
    st.subheader("Calendario Generato (Modificabile)")
    edited_df = st.data_editor(df) # Tabella cliccabile e modificabile!
    
    st.success("Calendario pronto! Puoi modificare le celle sopra se necessario.")
