#gui.py
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import ListCharacters, Substitutor
import lists
from gui_settings import open_settings_in_separate_file
import gui_settings



class AppGui:
    def __init__(self):
        settings = gui_settings.load_settings()
        self.window = tk.Tk()
        self.window.title("Plawex Character Substitution")
        self.window.geometry("800x600")
        self.window.configure(padx=15, pady=15)

        # Objektové třídy
        self.list_characters = ListCharacters.ListCharacters(
            settings.get("replacement", lists.replacement)
            )
        self.substitutor = Substitutor.Substitutor(
            self.list_characters, 
            settings.get("do_not_rename", lists.do_not_rename)
            )

        print(vars(self.substitutor))
        # -----------------------------
        # HLAVNÍ TITULEK
        # -----------------------------
        tk.Label(self.window, text="Nástroj pro přejmenování souborů a složek",
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))

        # -----------------------------
        # BLOK S VÝBĚREM SLOŽKY
        # -----------------------------
        folder_frame = tk.Frame(self.window)
        folder_frame.pack(fill="x", pady=10)

        tk.Label(folder_frame, text="Vyber složku:", font=("Segoe UI", 10)).pack(anchor="w")

        chooser_row = tk.Frame(folder_frame)
        chooser_row.pack(fill="x", pady=5)

        self.path_var = tk.StringVar()
        tk.Entry(chooser_row, textvariable=self.path_var, width=60).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(chooser_row, text="Procházet…", width=12, command=self.select_folder)\
            .pack(side=tk.LEFT)

        # -----------------------------
        # OVLÁDACÍ TLAČÍTKA
        # -----------------------------
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(fill="x", pady=(10, 15))

        tk.Button(buttons_frame, text="Přejmenovat", width=15,
                  bg="#d9534f", fg="white", command=self.rename)\
            .pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="Dry run", width=15,
                  bg="#0275d8", fg="white", command=self.dry_run)\
            .pack(side=tk.LEFT, padx=5)

        tk.Label(buttons_frame,
                 text="Dry run pouze vypíše, co by se přejmenovalo, ale nic nezmění.",
                 font=("Segoe UI", 9), fg="gray")\
            .pack(side=tk.LEFT, padx=10)
        
        tk.Button(buttons_frame, text="Nastavení", width=15,
                bg="#5cb85c", fg="white", command=lambda: open_settings_in_separate_file(self))\
            .pack(side=tk.LEFT, padx=5)


        # -----------------------------
        # LOG PANEL
        # -----------------------------
        log_frame = tk.Frame(self.window)
        log_frame.pack(fill="both", expand=True)

        tk.Label(log_frame, text="Log výstupu:", font=("Segoe UI", 10))\
            .pack(anchor="w", pady=(0, 5))

        self.log_box = scrolledtext.ScrolledText(
            log_frame,
            width=100,
            height=25,
            font=("Consolas", 10),
            borderwidth=2,
            relief="sunken"
        )
        self.log_box.pack(fill="both", expand=True)

        self.window.mainloop()

    # -----------------------------
    # FUNKCE GUI
    # -----------------------------
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def print_out(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def rename(self):
        path = self.path_var.get()
        if not os.path.isdir(path):
            messagebox.showerror("Chyba", "Neplatná cesta.")
            return

        logs = self.substitutor.substitute(path, dry_run=False)
        self.log_box.delete(1.0, tk.END)
        for line in logs:
            self.print_out(line)

        messagebox.showinfo("Hotovo", "Přejmenování dokončeno.")

    def dry_run(self):
        path = self.path_var.get()
        if not os.path.isdir(path):
            messagebox.showerror("Chyba", "Neplatná cesta.")
            return

        logs = self.substitutor.substitute(path, dry_run=True)
        self.log_box.delete(1.0, tk.END)
        for line in logs:
            self.print_out(line)




