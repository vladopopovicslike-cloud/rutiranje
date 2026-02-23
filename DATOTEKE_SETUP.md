# 📁 Dodavanje Excel Datoteka

## ✅ Šta je urađeno

Svi kodovi su promijenjeni da koriste **relativnu putanju** `data/` umjesto Windows putanja `G:\My Drive\`:

### Promijenjene putanje:

| Stara putanja (Windows) | Nova putanja (Linux friendly) |
|---|---|
| `G:\My Drive\hello_instance.txt` | `data/hello_instance.txt` |
| `G:\My Drive\instances_sve.xlsx` | `data/instances_sve.xlsx` |
| `G:\My Drive\hello.xlsx` | `data/hello.xlsx` |
| `G:\My Drive\hello_time.xlsx` | `data/hello_time.xlsx` |
| `G:\My Drive\hello_rjesenje.xlsx` | `data/hello_rjesenje.xlsx` |
| `G:\My Drive\sema_zapamcena6` | `data/sema_zapamcena6` |
| `G:\My Drive\postavka.xlsx` | `data/postavka.xlsx` |
| `D:\postavka1.xlsx` | `data/postavka1.xlsx` |

---

## 📂 Struktura foldera

```
rutiranje/
│
├── main.py
├── data/                          ← Kreiram se automatski
│   ├── instances_sve.xlsx         ← TREBATE DODATI
│   ├── hello.xlsx                 ← TREBATE DODATI
│   ├── hello_time.xlsx            ← TREBATE DODATI
│   ├── hello_rjesenje.xlsx        ← TREBATE DODATI
│   ├── postavka.xlsx              ← TREBATE DODATI
│   ├── postavka1.xlsx             ← TREBATE DODATI
│   ├── hello_instance.txt         ← Generiše se automatski
│   └── sema_zapamcena6            ← Generiše se automatski
│
├── [ostali Python moduli]
└── requirements.txt
```

---

## 🚀 Kako koristiti

### Korak 1: Dodaj Excel datoteke

1. **Pripremi Excel datoteke sa svog računara**
2. **Dragi i pustiš ih u VS Code `data/` folder**, ili:
   - Koristi file explorer da kopiraš datoteke u `/workspaces/rutiranje/data/`
   - Ili koristi `scp` / copy paste preko VS Code File Explorer-a

### Korak 2: Pokreni program

```bash
cd /workspaces/rutiranje
python3 main.py
```

Program će automatski učitati sve datoteke iz `data/` foldera! ✨

---

## ⚠️ Važne napomene

✅ **Sve putanje su sada relativne** - ne trebate Windows putanje  
✅ **Kompatibilno sa Linux/Mac/Windows** - radi gdje god  
✅ **Python 3 konverija** - svi Python 2 kodovi su konvertovani  
✅ **Sve biblioteke instalirane** - 7 vanjskih paketa je dostupno  

---

## 📋 Checklist prije pokretanja

- [ ] Kopirao/a sam sve `.xlsx` datoteke u `data/` folder
- [ ] Provjerio/a sam da se datoteke nalaze u `/workspaces/rutiranje/data/`
- [ ] Pokrećem `python3 main.py`

---

## Ako nešto ne radi

1. **Provjerite da li su datoteke u `data/` foldera**
   ```bash
   ls -la /workspaces/rutiranje/data/
   ```

2. **Provjerite da kodovi mogu da se kompajliraju**
   ```bash
   python3 -m py_compile *.py
   ```

3. **Provjerite verziju Python-a**
   ```bash
   python3 --version
   ```
