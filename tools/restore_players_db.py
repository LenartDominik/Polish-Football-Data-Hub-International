import shutil
from pathlib import Path

# Ustal absolutne ścieżki
base_dir = Path(__file__).parent.parent
backup_path = base_dir / "pilkarze.db.backup_20251123_225154"
restore_path = base_dir / "players.db"

# Kopiowanie backupu na miejsce aktywnej bazy
def restore_backup():
    print(f"Backup path: {backup_path}")
    print(f"Restore path: {restore_path}")
    if not backup_path.exists():
        print(f"Backup {backup_path} nie istnieje!")
        return
    shutil.copy2(backup_path, restore_path)
    print(f"Przywrócono bazę z {backup_path} do {restore_path}")

if __name__ == "__main__":
    restore_backup()
