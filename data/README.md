# Data Folder - Excel & Input Files

Ova mapa sadrži sve Excel datoteke i podatke potrebne za pokretanje glavnog programa.

## Datoteke koje trebate dodati:

### Excel datoteke (`.xlsx`):
1. **instances_sve.xlsx** - Glavne instance za testiranje
2. **hello.xlsx** - Matrica rastojanja
3. **hello_time.xlsx** - Matrica vremena
4. **hello_rjesenje.xlsx** - Gdje se pišu rezultati (može biti prazna ili sa šemo)
5. **postavka.xlsx** - Konfiguracija za `postavkaUlaza.py`
6. **postavka1.xlsx** - Konfiguracija za `postavkaUlazaNac.py`

### Tekstualne datoteke:
- **hello_instance.txt** - Log datoteka (kreirat će se automatski)

### Binary datoteke (pickle):
- **sema_zapamcena6** - Serializovane šeme (generiše se iz programa)

## Kako dodati datoteke:

1. Pripremi Excel datoteke na svom računaru
2. Dodaj ih u ovaj `data/` folder
3. Pokreni `main.py` - sve datoteke će biti učitane iz `data/`

## Primjer file setup-a:

```
rutiranje/
├── main.py
├── data/
│   ├── instances_sve.xlsx
│   ├── hello.xlsx
│   ├── hello_time.xlsx
│   ├── hello_rjesenje.xlsx
│   ├── postavka.xlsx
│   ├── postavka1.xlsx
│   └── hello_instance.txt (kreirat će se)
└── [ostali modul fajlovi]
```

## Napomena:

Sve putanje u kodu su sada promienjene na relativne i koriste `data/` folder.
Projekt će automatski tražiti datoteke iz ovog foldera.
