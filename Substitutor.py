#Substitutor.py
import os
import ListCharacters

class Substitutor:

    def __init__(self, list_characters, do_not_rename):
        self.list_characters = list_characters
        self.do_not_rename = do_not_rename if do_not_rename else set() #pokud do_not_rename neexistuje, vytvori se prazdna mnozina ( set() )
    

    def substitute(self, root_directory, dry_run:bool):
        logs = []

        for root, dirs, files in os.walk(root_directory, topdown=False):

            #files
            for f in files:
                base, ext = os.path.splitext(f)

                if base in self.do_not_rename:
                    continue

                new_name = self.list_characters.normalize_file(f)

                if new_name != f:
                    logs.append(f"Soubor: {f} -> {new_name}")
                    if not dry_run:
                        os.rename(os.path.join(root, f), os.path.join(root, new_name))
                        
            #directories
            for d in dirs:
                if d in self.do_not_rename:
                    continue
                new_name = self.list_characters.normalize_dir(d)

                if new_name != d:
                    logs.append(f"Adresar: {d} -> {new_name}")
                    if not dry_run:
                        os.rename(os.path.join(root, d), os.path.join(root, new_name))

        return logs
    
    def set_do_not_rename(self, new_list):
        """Aktualizuje seznam názvů, které se nesmí přejmenovat."""
        self.do_not_rename = set(new_list)


