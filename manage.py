import sqlite3
import sys

DB_NAME = 'players.db'

def show_players():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, team, league, position FROM players ORDER BY id')
    players = cursor.fetchall()
    
    print("\n=== LISTA POLSKICH PIŁKARZY ===")
    print(f"{'ID':<5} {'Nazwisko':<30} {'Klub':<25} {'Liga':<20} {'Pozycja':<10}")
    print("-" * 95)
    
    for player in players:
        print(f"{player[0] or '':<5} {player[1] or '':<30} {player[2] or '':<25} {player[3] or '':<20} {player[4] or '':<10}")
    
    print(f"\nŁącznie: {len(players)} piłkarzy")
    conn.close()

def delete_player(player_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, team FROM players WHERE id = ?', (player_id,))
    player = cursor.fetchone()
    
    if player:
        cursor.execute('DELETE FROM players WHERE id = ?', (player_id,))
        conn.commit()
        print(f"✓ Usunięto: {player[0] or 'Brak nazwy'} ({player[1] or 'Brak klubu'}) - ID: {player_id}")
    else:
        print(f"✗ Nie znaleziono piłkarza o ID {player_id}")
    
    conn.close()

def check_status():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Pokaż schemat
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='players'")
    schema = cursor.fetchone()
    
    print("\n=== STATUS BAZY DANYCH ===\n")
    
    # Statystyki
    cursor.execute('SELECT COUNT(*), MIN(id), MAX(id) FROM players')
    stats = cursor.fetchone()
    count, min_id, max_id = stats
    
    print(f"Liczba piłkarzy: {count}")
    print(f"Najmniejsze ID: {min_id}")
    print(f"Największe ID: {max_id}")
    
    if max_id:
        print(f"Następne ID: {max_id + 1}")
    
    # Sprawdź czy są luki
    cursor.execute('SELECT id FROM players ORDER BY id')
    ids = [row[0] for row in cursor.fetchall()]
    
    if ids:
        expected_ids = set(range(min_id, max_id + 1))
        actual_ids = set(ids)
        missing = expected_ids - actual_ids
        
        if missing:
            print(f"\nBrakujące ID (luki): {sorted(missing)}")
            print("ℹ️  To normalne - luki powstają po usunięciu rekordów")
        else:
            print("\n✓ Brak luk w numeracji ID")
    
    print("\n=== ZARZĄDZANIE ID ===")
    print("✓ Tabela używa PRIMARY KEY (bez AUTOINCREMENT)")
    print("✓ SQLite automatycznie przydziela ID = MAX(id) + 1")
    print("✓ Nie musisz niczego naprawiać!")
    
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_players()
    elif sys.argv[1] == "delete" and len(sys.argv) == 3:
        delete_player(int(sys.argv[2]))
    elif sys.argv[1] == "status":
        check_status()
    else:
        print("\nUżycie:")
        print("  python manage.py           - wyświetl wszystkich piłkarzy")
        print("  python manage.py delete 5  - usuń piłkarza o ID 5")
        print("  python manage.py status    - pokaż status bazy")


