# 📦 Instalacija Biblioteka - Rutiranje Vehicle Routing Solver

## ✅ Instalacija Uspješna!

Sve potrebne biblioteke su uspješno instalirane za Python 3.12.1

## 📋 Instalirane Biblioteke

### Vanjske (External) Biblioteke
| Biblioteka | Verzija | Namjena |
|-----------|---------|---------|
| **openpyxl** | 3.1.5 | Čitanje/pisanje Excel datoteka |
| **xlsxwriter** | 3.2.9 | Pisanje Excel datoteka |
| **numpy** | 2.4.2 | Numeričke operacije |
| **scipy** | 1.17.1 | Udaljenosti i matematička funkcionalnost |
| **pulp** | 3.3.0 | Linearna optimizacija |
| **simplejson** | 3.20.2 | JSON obrada |
| **matplotlib** | 3.10.8 | Vizualizacija ruta |

### Ugrađene (Built-in) Biblioteke
- **datetime** - Rad s datumima i vremenom
- **itertools** - Efikasne iteracijske alate
- **pickle** - Serijalizacija Python objekata
- **random** - Generiranje nasumičnih brojeva
- **json** - JSON obrada
- **collections** - Specijalizirane kolekcije podataka

## 🚀 Pokretanje Programa

### Direktno pokretanje
```bash
python3 main.py
```

### Sa debug informacijom
```bash
python3 -u main.py
```

## 📁 Datoteke za Instalaciju

Projekt sadrži tri načina instalacije zavisnosti:

### 1. Python Script (Preporučeno)
```bash
python3 setup_dependencies.py
```

### 2. Bash Script (Linux/macOS)
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Batch Script (Windows)
```cmd
setup.bat
```

### 4. Direktno s pip
```bash
pip install -r requirements.txt
```

## 🔧 Ručna Instalacija (ako je potrebna)

```bash
# Excel podrška
pip install openpyxl xlsxwriter

# Znanstveno računanje
pip install numpy scipy

# Linearna optimizacija
pip install pulp

# JSON
pip install simplejson

# Vizualizacija (opcionalno)
pip install matplotlib

# Kartografija (opcionalno - verzija 0.0.5)
pip install mplleaflet==0.0.5
```

## 📊 Arhitektura Programa

Program koristi sljedeće module:

```
main.py (glavna datoteka)
├── clarke-wright algoritmi
│   ├── clarkWright.py
│   ├── clarkWrightPovrat.py
│   ├── clarkModul.py
│   └── clarkModul2.py
├── linearna optimizacija
│   ├── LPprogrami1.py
│   ├── LPprogrami1Primjer.py
│   └── LPprogrami1aPrimjer.py
├── obrada podataka
│   ├── ulazniPodaciPrimjer.py
│   ├── postavkaUlaza.py
│   ├── postavkaUlazaNac.py
│   └── rutepovrata2.py
└── vizualizacija
    └── crtaj_rute.py
```

## 🔍 Provjera Instalacije

Provjerite da li su sve biblioteke instalirane:

```bash
python3 -c "import openpyxl, numpy, scipy, pulp, matplotlib; print('✓ Sve biblioteke su dostupne!')"
```

## ⚠️ Troubleshooting

### Greška: ModuleNotFoundError
```bash
python3 setup_dependencies.py
```

### Greška: PuLP Solver nije dostupan
PuLP se automatski pokrenuo sa CBC solverom. Za dodatne solvere:
- CPLEX: https://www.ibm.com/products/ilog-cplex-optimization-studio
- GLPK: sudo apt-get install glpk-utils (Linux)

### Greška: Excel datoteke nisu dostupne
```bash
pip install --upgrade openpyxl
```

## 📝 Komande za Razvijanje

```bash
# Provjera sintakse Python datoteka
python3 -m py_compile *.py

# Pokretanje s debug informacijom
python3 -u main.py

# Provjera verzija biblioteka
pip list | grep -E "openpyxl|numpy|scipy|pulp"
```

## 🌐 Sistemski Zahtjevi

- **Python**: 3.8+
- **OS**: Windows, Linux, macOS
- **RAM**: minimalno 512 MB
- **Disk prostor**: ~200 MB (za sve biblioteke)

## 📌 Važne Bilješke

1. **pylab je zastarjelo** - Koristi se `matplotlib.pyplot` umjesto toga
2. **mplleaflet**: Ima ograničenu verzijsku podršku (0.0.5 je preporučena)
3. **Slučajni brojevi**: `random` modul je inicijaliziran za reproduktibilne rezultate
4. **File paths**: Koriste forward slashes (/) za cross-platform kompatibilnost

## 📞 Kontakt

Za probleme s instalacijom ili funkcionalnosti programa, obratite se razvojnom timu.

---

**Status**: ✅ Sistem je spreman za rad  
**Python verzija**: 3.12.1  
**Sve biblioteke**: Instalirane  
**Testiranje**: Proslijeđeno  
