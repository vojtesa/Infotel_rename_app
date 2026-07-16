# Rename App — Batch File & Folder Name Normalizer

Windows desktop utility that recursively renames files and folders in a directory tree —
stripping Czech diacritics and replacing problematic special characters — while protecting
a configurable list of names that must never change. Built during my part-time work at
[InfoTel, spol. s.r.o.](https://www.infotel.cz/) to prepare project documentation for
upload to a client's legacy portal that only accepts a restricted, essentially ASCII-only
character set.

<!-- TODO: add a screenshot of the app window here -->
<!-- ![Rename App GUI](docs/screenshot.png) -->

## Why

InfoTel delivers project documentation to Vodafone through the operator's aging supplier
portal. The portal predates Unicode-friendly web stacks and rejects file and folder names
containing anything beyond a basic (essentially ASCII) character set — Czech diacritics
(`ě, š, č, ř…`) and special characters (`# + ( ) , ;`…) make uploads fail. The archives
contain thousands of files named by hand over the years, so every delivery used to mean
tedious manual renaming. On top of that, the archive uses **standardized folder names**
(e.g. `CW-19_Technicka_zprava`, `FO-12_DSPS_linie`) that must stay exactly as they are.

This tool automates the cleanup and makes it safe:

- **Dry run first** — a preview mode lists every rename that *would* happen, without
  touching a single file
- **Do-not-rename list** — protected names are skipped entirely, so the standardized
  archive structure survives the cleanup
- **Extensions are preserved** — only the base file name is normalized

## Features

- Recursive bottom-up walk of the selected directory (files and folders)
- Character substitution table editable in the GUI — add, remove, or reset rules to the
  built-in defaults
- Editable do-not-rename list, also managed from the GUI
- Settings persisted to `settings.json`, so a customized configuration survives restarts
- Log panel showing every performed (or previewed) rename

## Tech stack

Pure Python standard library — Tkinter GUI, `os.walk` traversal, JSON config.
**No third-party runtime dependencies.** PyInstaller is used only for building the `.exe`.

## Getting started

### Run from source

```bash
git clone https://github.com/vojtesa/Infotel_rename_app.git
cd Infotel_rename_app
python main.py
```

Requires Python 3.10+ (nothing to `pip install`).

### Build the Windows executable

```bash
pip install pyinstaller
pyinstaller main.spec
```

A prebuilt `.exe` is available under
[Releases](https://github.com/vojtesa/Infotel_rename_app/releases).

## Notes & limitations

- Renames are applied directly on the filesystem — always run **Dry run** first; there is
  no undo.
- Substitution is plain ordered text replacement; rule order in the settings matters
  (e.g. `–` → `-` runs before `-` → `_`).
- The default do-not-rename list mirrors InfoTel's archive convention — replace it with
  your own via the settings dialog.

---

## Návod k použití (CZ)

Aplikace připraví názvy souborů a složek pro nahrání do starého portálu Vodafonu, který
přijímá jen omezenou (v podstatě ASCII) znakovou sadu — odstraní diakritiku a nahradí
problematické znaky.

1. Vyber složku, kterou chceš vyčistit (tlačítko **Procházet…**).
2. Klikni na **Dry run** — v logu uvidíš, co všechno *by se* přejmenovalo, ale nic se
   nezmění.
3. Pokud výpis vypadá dobře, klikni na **Přejmenovat** — změny se provedou a vypíšou
   do logu.
4. V **Nastavení** můžeš upravit tabulku náhrad znaků i seznam názvů, které se nikdy
   přejmenovat nesmí. Uložené nastavení přežije restart aplikace, tlačítkem
   *Vrátit výchozí znaky* se vrátíš k výchozím hodnotám.

**Poznámky:**

- Přejmenování nejde vzít zpět — vždy si nejdřív projeď Dry run.
- Přípony souborů zůstávají netknuté, normalizuje se jen název.

---

**Author:** Vojtěch Tesař
