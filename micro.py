# --- LIBRERIA JS AGGIORNATA E PIÙ ROBUSTA ---
def add_screenshot_logic():
    components.html("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'take_screenshot') {
            // Cerchiamo l'area del calendario nel documento principale
            const element = window.parent.document.querySelector('.print-container');
            
            if (element) {
                html2canvas(element, {
                    backgroundColor: "#000000",
                    scale: 2,
                    useCORS: true,
                    allowTaint: true
                }).then(canvas => {
                    const dataUrl = canvas.toDataURL("image/png");
                    const link = document.createElement('a');
                    link.href = dataUrl;
                    link.download = 'calendario_aosr_elite.png';
                    // Trucco per forzare il download su Chrome/Edge/Safari
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }).catch(err => {
                    console.error("Errore cattura:", err);
                });
            } else {
                alert("Area calendario non trovata! Riprova tra un secondo.");
            }
        }
    });
    </script>
    """, height=0)

# ... (tutto il resto del tuo codice rimane uguale) ...

# --- MODIFICA SOLO IL BOTTONE FINALE COSI ---
if st.button("📸 SCARICA FOTO CALENDARIO (PNG)", type="primary", use_container_width=True):
    # Questo invia il segnale al pezzo di codice sopra
    components.html("<script>window.parent.postMessage({type: 'take_screenshot'}, '*');</script>", height=0)
    st.success("Richiesta inviata al browser! Se non parte il download, controlla se il browser ha bloccato i pop-up per questa pagina.")
