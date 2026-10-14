"""
Script de validation et statistiques du corpus annoté
Usage : python valider_corpus.py
"""
import csv
from collections import Counter

FILE = "corpus_annote_final.csv"

try:
    with open(FILE, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
except FileNotFoundError:
    print(f"❌ Fichier {FILE} introuvable. Annotez d'abord avec script_annotation.py")
    exit()

print(f"\n{'='*55}")
print(f"  RAPPORT DE VALIDATION DU CORPUS")
print(f"{'='*55}")
print(f"\n  Total emails annotés : {len(rows)}")

key = "service_final" if "service_final" in rows[0] else "service"

print(f"\n  Distribution par service :")
for s, c in Counter(r[key] for r in rows).most_common():
    bar = "█" * (c // 2)
    print(f"    {s:<30} {c:>3}  {bar}")

key_t = "type_final" if "type_final" in rows[0] else "type"
print(f"\n  Distribution par type :")
for t, c in Counter(r[key_t] for r in rows).most_common():
    print(f"    {t:<25} {c:>3}")

key_u = "urgence_final" if "urgence_final" in rows[0] else "urgence"
print(f"\n  Distribution par urgence :")
for u, c in Counter(r[key_u] for r in rows).most_common():
    print(f"    {u:<15} {c:>3}")

# Vérifications qualité
print(f"\n  Contrôles qualité :")
issues = 0
for r in rows:
    if not r.get("sujet","").strip():
        print(f"    ⚠ Email {r['id']} : sujet vide")
        issues += 1
    if not r.get("corps","").strip():
        print(f"    ⚠ Email {r['id']} : corps vide")
        issues += 1

if issues == 0:
    print(f"    ✅ Aucun problème détecté")

# Recommandation
total = len(rows)
print(f"\n  Recommandation entraînement :")
if total < 200:
    print(f"    ⚠ {total} emails — insuffisant (minimum 300 recommandé)")
elif total < 400:
    print(f"    ⚡ {total} emails — acceptable pour un test initial")
else:
    print(f"    ✅ {total} emails — suffisant pour l'entraînement")

print(f"\n{'='*55}\n")
