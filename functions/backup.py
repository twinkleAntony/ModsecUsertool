import shutil
import datetime
import os

# Take backup of file with timestamp
def backup(file_name):
    try:
        if os.path.exists(file_name):
            backup_file_name = f"{file_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            shutil.copy(file_name, backup_file_name)
            print(f"Backup created: {backup_file_name}")
            return backup_file_name
        else:
            print(f"Error: File not found - {file_name}")
            return None
    except Exception as e:
        print(f"Error creating backup for {file_name}: {e}")
        return None

