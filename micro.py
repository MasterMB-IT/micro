import random
import calendar
from collections import defaultdict

# --- FUNZIONE SELEZIONE BILANCIATA CON SMORZAMENTO STORICO ---
def get_advanced_balanced_player(pool, role_type, current_assignments, month_index=1, manual_days_count=5):
    """
    month_index: 1 per il primo mese di utilizzo, 2 per il secondo, 3+ a regime.
    """
    capo_hist, pass_hist = get_dynamic_history()
    
    # 1. Smorzamento peso storico per i primi 2-3 mesi
    if month_index == 1:
        w_hist = 0.25  # Pesa poco lo storico: non blocca chi ha già 3+ treni
        sigma = 1.5    # Alta variabilità casuale
    elif month_index == 2:
        w_hist = 0.50  # Transizione
        sigma = 1.0
    else:
        w_hist = 1.00  # A regime: peso storico pieno
        sigma = 0.5    # Piccola componente casuale per rompere i pareggi

    candidates = []
    for player in pool:
        norm_p = smart_normalize_name(player)
        
        # Conteggi attuali
        curr_c = current_assignments["capo"][player]
        curr_p = current_assignments["pass"][player]
        curr_total = curr_c + curr_p
        
        # Conteggi storici
        hist_c = capo_hist.get(norm_p, 0)
        hist_p = pass_hist.get(norm_p, 0)
        hist_role = hist_c if role_type == "capo" else hist_p
        
        # Calcolo Score (Più è basso, prima viene scelto)
        score = (hist_role * w_hist) + (curr_total * 2.5) + random.uniform(0, sigma)
        
        candidates.append({
            "player": player,
            "score": score
        })
    
    # Ordina per punteggio crescente
    candidates.sort(key=lambda x: x["score"])
    return candidates[0]["player"]

# --- GENERATORE CALENDARIO CON REGOLE R4 ---
def generate_alliance_calendar(sel_leaders, sel_r3_r2, year, month_name, merito_days, month_idx=1):
    p_l = sel_leaders if sel_leaders else leaders_list
    p_o = sel_r3_r2 if sel_r3_r2 else r3_r2_list
    all_players = list(set(p_l + p_o))
    
    num_gg = calendar.monthrange(year, MESI_ITA.index(month_name) + 1)[1]
    calendar_out = []
    
    current_assignments = {
        "capo": defaultdict(int),
        "pass": defaultdict(int)
    }
    
    for g in range(1, num_gg + 1):
        # CASO 1: Giorni di Merito (Scelti manualmente dagli R4)
        if g in merito_days:
            c = merito_days[g].get("capo", "---")
            p = merito_days[g].get("pass", "---")
        
        # CASO 2: Primi 11 Giorni (Capotreno SOLO R4/R5)
        elif g <= 11:
            c = get_advanced_balanced_player(p_l, "capo", current_assignments, month_idx)
            p_pool = [x for x in all_players if x != c]
            p = get_advanced_balanced_player(p_pool, "pass", current_assignments, month_idx)
            
        # CASO 3: Giorni Restanti del Mese (Algoritmo Generale)
        else:
            c = get_advanced_balanced_player(all_players, "capo", current_assignments, month_idx)
            p_pool = [x for x in all_players if x != c]
            p = get_advanced_balanced_player(p_pool, "pass", current_assignments, month_idx)
            
        if c != "---": current_assignments["capo"][c] += 1
        if p != "---": current_assignments["pass"][p] += 1
        
        calendar_out.append({"Giorno": g, "Capo": c, "Pass": p})
        
    return calendar_out
