import tkinter as tk
from tkinter import messagebox
import json
import os
import lists

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "replacement": [],
    "do_not_rename": []
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        out = DEFAULT_SETTINGS.copy()
        out.update({k: data.get(k, out[k]) for k in out})
        return out
    except Exception:
        return DEFAULT_SETTINGS.copy()

def open_settings_in_separate_file(apps_self):
    settings = tk.Toplevel(apps_self.window)
    settings.title("Nastavení — Replacement a Do Not Rename")
    settings.geometry("900x600")
    settings.grab_set()

    # ======================================================
    #   HLAVNÍ SCROLL KONTEJNER
    # ======================================================

    container = tk.Frame(settings)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def on_config(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scroll_frame.bind("<Configure>", on_config)

    # Scroll kolečkem myši
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", _on_mousewheel_linux)
    canvas.bind_all("<Button-5>", _on_mousewheel_linux)

    # ======================================================
    #   HLAVNÍ FRAME – dvě strany
    # ======================================================

    main_frame = tk.Frame(scroll_frame)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ======================================================
    #   LEVÁ STRANA – REPLACEMENT
    # ======================================================

    left = tk.LabelFrame(main_frame, text="Replacement (náhrady znaků)", padx=10, pady=10)
    left.pack(side="left", fill="both", expand=True, padx=5)

    # Frame pouze pro řádky
    replacement_rows_frame = tk.Frame(left)
    replacement_rows_frame.pack(fill="both", expand=True)

    replacement_rows = []

    def add_replacement_row(old="", new=""):
        row = tk.Frame(replacement_rows_frame)

        # Už NEŘEŠÍME before=children[0], jen normálně packnem
        row.pack(fill="x", pady=2)

        old_var = tk.StringVar(value=old)
        new_var = tk.StringVar(value=new)

        tk.Entry(row, textvariable=old_var, width=5).pack(side="left", padx=5)
        tk.Label(row, text="→").pack(side="left")
        tk.Entry(row, textvariable=new_var, width=5).pack(side="left", padx=5)

        item = (old_var, new_var)

        def delete_row():
            if item in replacement_rows:
                replacement_rows.remove(item)
            row.destroy()

        tk.Button(row, text="Odstranit", command=delete_row).pack(side="left", padx=5)

        replacement_rows.append(item)

    # Načtení existujících hodnot
    for old, new in apps_self.list_characters.list_of_characters:
        add_replacement_row(old, new)

    # Sekce pro přidání nové položky
    tk.Label(left, text="Přidat novou náhradu:").pack(anchor="w", pady=(10, 0))

    add_rep_frame = tk.Frame(left)
    add_rep_frame.pack(anchor="w", pady=5)

    new_old = tk.StringVar()
    new_new = tk.StringVar()

    tk.Entry(add_rep_frame, textvariable=new_old, width=5).pack(side="left", padx=5)
    tk.Label(add_rep_frame, text="→").pack(side="left")
    tk.Entry(add_rep_frame, textvariable=new_new, width=5).pack(side="left", padx=5)

    def add_replacement_and_clear():
        add_replacement_row(new_old.get(), new_new.get())
        new_old.set("")
        new_new.set("")

    tk.Button(
        add_rep_frame,
        text="Přidat",
        command=add_replacement_and_clear
    ).pack(side="left", padx=10)

    # ======================================================
    #   PRAVÁ STRANA – DO NOT RENAME
    # ======================================================

    right = tk.LabelFrame(main_frame, text="Do Not Rename (nezměnit tyto názvy)", padx=10, pady=10)
    right.pack(side="left", fill="both", expand=True, padx=5)

    donot_rows_frame = tk.Frame(right)
    donot_rows_frame.pack(fill="both", expand=True)

    donot_rows = []

    def add_donot_row(value=""):
        row = tk.Frame(donot_rows_frame)

        # Zase: žádné before, jen klasický pack
        row.pack(fill="x", pady=2)

        var = tk.StringVar(value=value)
        tk.Entry(row, textvariable=var, width=40).pack(side="left", padx=5)

        def delete_row():
            donot_rows.remove(var)
            row.destroy()

        tk.Button(row, text="Odstranit", command=delete_row).pack(side="left", padx=5)

        donot_rows.append(var)

    # Načti existující hodnoty
    for item in apps_self.substitutor.do_not_rename:
        add_donot_row(item)

    # Přidání další položky
    tk.Label(right, text="Přidat nový název:").pack(anchor="w", pady=(10, 0))

    add_dn_frame = tk.Frame(right)
    add_dn_frame.pack(anchor="w", pady=5)

    new_dn = tk.StringVar()
    tk.Entry(add_dn_frame, textvariable=new_dn, width=40).pack(side="left", padx=5)

    def add_dn_and_clear():
        add_donot_row(new_dn.get())
        new_dn.set("")

    tk.Button(
        add_dn_frame,
        text="Přidat",
        command=add_dn_and_clear
    ).pack(side="left", padx=10)

    # ======================================================
    #   NASTAVIT VYCHOZI list znak
    # ======================================================

    def set_default():
        # 1) vyčistit UI řádky (LEVÁ i PRAVÁ)
        for w in replacement_rows_frame.winfo_children():
            w.destroy()
        for w in donot_rows_frame.winfo_children():
            w.destroy()

        # 2) vyčistit „model“ seznamy (LEVÁ i PRAVÁ) – to je důležité proti duplikaci
        replacement_rows.clear()
        donot_rows.clear()

        # 3) znovu naplnit z lists.py (LEVÁ i PRAVÁ)
        for old, new in lists.replacement:
            add_replacement_row(old, new)

        for name in lists.do_not_rename:
            add_donot_row(name)

        # 4) propsat do běžící appky (aby Rename/Dry run hned používaly default)
        apps_self.list_characters.set_replacement(lists.replacement)
        apps_self.substitutor.set_do_not_rename(lists.do_not_rename)

        # 5) uložit do settings.json (aby to přetrvalo restart)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {"replacement": lists.replacement, "do_not_rename": lists.do_not_rename},
                f, ensure_ascii=False, indent=2
            )

        messagebox.showinfo("Hotovo", "Vráceno na výchozí hodnoty (replacement + do_not_rename).")



    
    tk.Button(
        settings,
        text="Vrátit výchozí znaky",
        bg="#f0ad4e",
        fg="black",
        width=20,
        command=set_default
    ).pack(pady=5)


    # ======================================================
    #   ULOŽIT
    # ======================================================

    def ulozit():
        try:
            new_replacement = []
            for old, new in replacement_rows:
                o = old.get()
                n = new.get()
                if o == "" and n == "":
                    continue
                new_replacement.append((o, n))

            new_do_not_rename = [v.get() for v in donot_rows]

            apps_self.list_characters.set_replacement(new_replacement)
            apps_self.substitutor.set_do_not_rename(new_do_not_rename)

            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(
                    {"replacement": new_replacement, "do_not_rename": new_do_not_rename},
                    f, ensure_ascii=False, indent=2
                )
            # messagebox.showinfo("Hotovo", "Nastavení bylo uloženo.")
            settings.destroy()

        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se uložit: {e}")

    tk.Button(
        settings,
        text="Uložit změny",
        bg="#0275d8",
        fg="white",
        width=15,
        command=ulozit
    ).pack(pady=10)
