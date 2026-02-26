"""Example showing how to work with the pre‑computed schema file
`data/sema_zapamcena6`.

This script mimics the logic that appears in `main.py` and demonstrates
how to load the pickle, inspect its structure, and regenerate a fresh
sequence of schemas if the file is missing or corrupted.

Run it from the workspace root with:

    python example_sema.py
"""

import pickle
import os

import postavkaUlaza

FILENAME = "data/sema_zapamcena6"


def load_or_generate(path: str, n_schemes: int = 1):
    """Load the list of schemes from `path` or regenerate with
    ``postavkaUlaza.generisanje_sema`` if the file cannot be read.

    The return value is the same list that the main program expects:
    each element is a 5‑tuple
    ``(randomklijenti_poz, kolicine_poz, randomklijenti_neg,
    kolicine_neg, randomklijenti_svi)``.
    """
    try:
        with open(path, "rb") as f:
            schemes = pickle.load(f)
        print(f"loaded {len(schemes)} schemes from {path}")
    except Exception as exc:
        print(f"failed to load {path}: {exc}\nre‑generating")
        schemes = postavkaUlaza.generisanje_sema(n_schemes)
        try:
            with open(path, "wb") as f:
                pickle.dump(schemes, f)
            print(f"wrote regenerated schemes to {path}")
        except Exception as write_exc:
            print(f"could not write file: {write_exc}")
    return schemes


def describe_scheme(scheme, index=None):
    """Pretty‑print the components of a single scheme."""
    (poz, pozqty, neg, negqty, allclients) = scheme
    header = f"Scheme {index}:" if index is not None else "Scheme:" 
    print(header)
    print("  positive clients count", len(poz))
    print("  positive quantities", pozqty)
    print("  negative clients count", len(neg))
    print("  negative quantities", negqty)
    print("  combined list length", len(allclients))
    print("  sample of combined list", allclients[:10])
    print()


def main():
    schemes = load_or_generate(FILENAME, n_schemes=6)
    for i, s in enumerate(schemes, start=1):
        describe_scheme(s, index=i)


if __name__ == "__main__":
    main()
