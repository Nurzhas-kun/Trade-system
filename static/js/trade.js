function selectTrade(skinIdOffered, skinIdRequested) {
    document.getElementById('skin_id_offered').value = skinIdOffered;
    document.getElementById('skin_id_requested').value = skinIdRequested;
    document.getElementById('tradeForm').submit();  // Automatically submit the form after selecting a trade
}
