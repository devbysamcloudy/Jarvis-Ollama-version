import os
import shutil

CATEGORIES = {
    'Images':    ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.md', '.doc', '.csv', '.xls'],
    'Music':     ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'Videos':    ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'],
    'Archives':  ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso'],
    'Code':      ['.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.cpp', '.java', '.php', '.json', '.yml', '.yaml', '.sh'],
    'Others':    []
}


def _resolve_path(folder_path=None):
    if not folder_path:
        return os.getcwd()

    home = os.path.expanduser("~")
    onedrive = os.path.join(home, "OneDrive")

    def best_path(folder_name):
        onedrive_path = os.path.join(onedrive, folder_name)
        home_path = os.path.join(home, folder_name)
        if os.path.exists(onedrive_path):
            return onedrive_path
        return home_path

    shortcuts = {
        "desktop":   best_path("Desktop"),
        "downloads": best_path("Downloads"),
        "documents": best_path("Documents"),
        "pictures":  best_path("Pictures"),
        "music":     best_path("Music"),
        "videos":    best_path("Videos"),
    }

    lower = folder_path.strip().lower()
    if lower in shortcuts:
        return shortcuts[lower]

    if os.path.isabs(folder_path):
        return folder_path

    return os.path.abspath(folder_path)


class FileOrganizer:

    def location(self, folder_path=None):
        path = _resolve_path(folder_path)
        msg = f"Folder: {path}"
        print(msg)
        return {"path": path}

    def list_files(self, folder_path=None):
        path = _resolve_path(folder_path)
        if not os.path.exists(path):
            return {"error": f"Folder not found: {path}"}
        items = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]
        return {"path": path, "files": items, "count": len(items)}

    def organize_by_type(self, folder_path=None):
        path = _resolve_path(folder_path)
        if not os.path.exists(path):
            return {"error": f"Folder not found: {path}"}

        for folder in CATEGORIES.keys():
            folder_full = os.path.join(path, folder)
            if not os.path.exists(folder_full):
                os.mkdir(folder_full)

        items = os.listdir(path)
        files = [i for i in items if os.path.isfile(os.path.join(path, i))]
        moved = 0
        actions = []

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            dest_folder = "Others"
            for folder, extensions in CATEGORIES.items():
                if ext in extensions:
                    dest_folder = folder
                    break
            source = os.path.join(path, file)
            destination = os.path.join(path, dest_folder, file)
            try:
                shutil.move(source, destination)
                moved += 1
                actions.append({"file": file, "to": dest_folder})
            except Exception as e:
                print(f"Could not move {file}: {e}")

        msg = f"Organized {moved} files in {path}"
        return {"path": path, "moved": moved, "actions": actions, "message": msg}

    def undo_organize(self, folder_path=None):
        path = _resolve_path(folder_path)
        if not os.path.exists(path):
            return {"error": f"Folder not found: {path}"}

        folders = list(CATEGORIES.keys())
        moved_back = 0
        actions = []

        for folder in folders:
            folder_full = os.path.join(path, folder)
            if os.path.exists(folder_full):
                for file in os.listdir(folder_full):
                    file_path = os.path.join(folder_full, file)
                    if os.path.isfile(file_path):
                        destination = os.path.join(path, file)
                        try:
                            shutil.move(file_path, destination)
                            moved_back += 1
                            actions.append({"file": file, "from": folder})
                        except Exception as e:
                            print(f"Could not restore {file}: {e}")

        for folder in folders:
            folder_full = os.path.join(path, folder)
            if os.path.exists(folder_full):
                try:
                    os.rmdir(folder_full)
                except:
                    pass

        msg = f"Restored {moved_back} files in {path}"
        return {"path": path, "restored": moved_back, "actions": actions, "message": msg}


_organizer = FileOrganizer()

def location(folder_path=None):
    return _organizer.location(folder_path)

def list_files(folder_path=None):
    return _organizer.list_files(folder_path)

def organize_by_type(folder_path=None):
    return _organizer.organize_by_type(folder_path)

def undo_organize(folder_path=None):
    return _organizer.undo_organize(folder_path)
