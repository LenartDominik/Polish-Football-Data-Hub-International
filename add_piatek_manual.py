"""
Ręczne dodanie danych ligowych Krzysztofa Piątka dla sezonu 2025-2026
(Qatar Stars League - Al Duhail SC)

UWAGA: Wypełnij dane poniżej na podstawie Transfermarkt/Flashscore
"""
import sqlite3

# ============================================================================
# WYPEŁNIJ TE DANE (na podstawie Transfermarkt lub Flashscore)
# ============================================================================
SEASON = '2025-2026'
COMPETITION = 'Qatar Stars League'
TEAM = 'Al Duhail SC'

# Podstawowe statystyki
GAMES = 0           # Liczba meczów
GAMES_STARTS = 0    # Mecze od początku
MINUTES = 0         # Minuty grane
GOALS = 0           # Gole
ASSISTS = 0         # Asysty
YELLOW_CARDS = 0    # Żółte kartki
RED_CARDS = 0       # Czerwone kartki

# Zaawansowane (jeśli znasz, jeśli nie zostaw 0)
SHOTS = 0           # Strzały
SHOTS_ON_TARGET = 0 # Celne strzały
XG = 0.0            # Expected Goals
XA = 0.0            # Expected Assists
PASS_COMPLETION = 0.0  # % podań udanych

# ============================================================================

def add_piatek_data():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    
    # Znajdź ID Piątka
    cursor.execute("SELECT id, name FROM players WHERE name LIKE '%Piatek%' OR name LIKE '%Piątek%'")
    result = cursor.fetchone()
    
    if not result:
        print("❌ Piątek nie znaleziony w bazie!")
        conn.close()
        return
    
    player_id, player_name = result
    print(f"✅ Znaleziono gracza: {player_name} (ID: {player_id})")
    
    # Sprawdź czy dane już istnieją
    cursor.execute("""
        SELECT id FROM competition_stats
        WHERE player_id = ?
        AND season = ?
        AND competition_name = ?
    """, (player_id, SEASON, COMPETITION))
    
    if cursor.fetchone():
        print(f"⚠️ Dane dla {COMPETITION} {SEASON} już istnieją!")
        overwrite = input("Nadpisać? (yes/no): ").strip().lower()
        if overwrite != 'yes':
            print("Anulowano.")
            conn.close()
            return
        
        cursor.execute("""
            DELETE FROM competition_stats
            WHERE player_id = ?
            AND season = ?
            AND competition_name = ?
        """, (player_id, SEASON, COMPETITION))
        print("✅ Usunięto stare dane")
    
    # Dodaj nowe dane
    cursor.execute("""
        INSERT INTO competition_stats (
            player_id, season, competition_type, competition_name,
            games, games_starts, minutes, goals, assists,
            xg, xa, shots, shots_on_target, pass_completion,
            yellow_cards, red_cards
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        player_id, SEASON, 'LEAGUE', COMPETITION,
        GAMES, GAMES_STARTS, MINUTES, GOALS, ASSISTS,
        XG, XA, SHOTS, SHOTS_ON_TARGET, PASS_COMPLETION,
        YELLOW_CARDS, RED_CARDS
    ))
    
    conn.commit()
    
    print("\n" + "=" * 80)
    print("✅ DANE DODANE POMYŚLNIE!")
    print("=" * 80)
    print(f"\nGracz: {player_name}")
    print(f"Sezon: {SEASON}")
    print(f"Liga: {COMPETITION}")
    print(f"Drużyna: {TEAM}")
    print(f"\nStatystyki:")
    print(f"  Mecze: {GAMES} (starty: {GAMES_STARTS})")
    print(f"  Minuty: {MINUTES}")
    print(f"  Gole: {GOALS}")
    print(f"  Asysty: {ASSISTS}")
    print(f"  Kartki: {YELLOW_CARDS} żółte, {RED_CARDS} czerwone")
    
    if SHOTS > 0 or XG > 0:
        print(f"\nZaawansowane:")
        print(f"  Strzały: {SHOTS} (celne: {SHOTS_ON_TARGET})")
        print(f"  xG: {XG:.2f}")
        print(f"  xA: {XA:.2f}")
        print(f"  Podania: {PASS_COMPLETION:.1f}%")
    
    conn.close()
    
    print("\n✅ Sprawdź w aplikacji:")
    print("   streamlit run app/frontend/streamlit_app.py")
    print("   Wyszukaj: Piątek")

if __name__ == "__main__":
    print("=" * 80)
    print("RĘCZNE DODANIE DANYCH LIGOWYCH - Krzysztof Piątek")
    print("=" * 80)
    print(f"\nSezon: {SEASON}")
    print(f"Liga: {COMPETITION}")
    print(f"Drużyna: {TEAM}")
    print(f"\n⚠️ UWAGA: Wypełnij dane w linii 10-23 tego skryptu!")
    print(f"\nObecnie ustawione wartości:")
    print(f"  Mecze: {GAMES}")
    print(f"  Gole: {GOALS}")
    print(f"  Asysty: {ASSISTS}")
    
    if GAMES == 0:
        print(f"\n❌ Brak danych do dodania (wszystkie wartości = 0)")
        print(f"\n💡 Edytuj plik: add_piatek_manual.py")
        print(f"   Wypełnij sekcję linii 10-23 danymi z Transfermarkt/Flashscore")
        print(f"   Następnie uruchom ponownie: python add_piatek_manual.py")
    else:
        print(f"\n📊 Dane gotowe do dodania!")
        confirm = input("\nDodać te dane do bazy? (yes/no): ").strip().lower()
        if confirm == 'yes':
            add_piatek_data()
        else:
            print("Anulowano.")
