"""
Script d'annotation manuelle du corpus
Usage : python script_annotation.py
"""
import csv
import os

INPUT_FILE  = "corpus_emails_bureau_ordre.csv"
OUTPUT_FILE = "corpus_annote_final.csv"

SERVICES = [
    "Direction Générale", "Ressources Humaines", "Comptabilité",
    "Juridique", "Informatique", "Service Général", "Non classifié"
]
TYPES    = ["Demande", "Réclamation", "Information", "Convocation", "Rapport"]
URGENCES = ["Normal", "Urgent", "Critique"]

def choix(options, label):
    print(f"\n  {label} :")
    for i, o in enumerate(options, 1):
        print(f"    {i}. {o}")
    while True:
        try:
            v = int(input("  Votre choix (numéro) : "))
            if 1 <= v <= len(options):
                return options[v-1]
        except ValueError:
            pass
        print("  ⚠ Entrée invalide, recommencez.")

def annoter():
    with open(INPUT_FILE, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    # Reprendre là où on s'est arrêté
    done_ids = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, encoding="utf-8-sig") as f:
            done_ids = {r["id"] for r in csv.DictReader(f)}

    to_do = [r for r in rows if r["id"] not in done_ids]
    print(f"\n📧 {len(to_do)} emails à annoter ({len(done_ids)} déjà traités)\n")

    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8-sig") as f:
        fields = list(rows[0].keys()) + ["service_final","type_final","urgence_final"]
        writer = csv.DictWriter(f, fieldnames=fields)
        if not done_ids:
            writer.writeheader()

        for i, row in enumerate(to_do, 1):
            print(f"\n{'='*60}")
            print(f"Email {i}/{len(to_do)} — {row['id']}")
            print(f"De     : {row['nom_expediteur']} <{row['expediteur']}>")
            print(f"Sujet  : {row['sujet']}")
            print(f"Extrait: {row['corps'][:200]}...")
            print(f"\n  [Suggestion IA] Service: {row['service']} | Type: {row['type']} | Urgence: {row['urgence']}")

            valider = input("\n  Valider la suggestion ? (o=oui / n=non / q=quitter) : ").strip().lower()
            if valider == 'q':
                print("\n✅ Annotation sauvegardée. Relancez le script pour continuer.")
                break
            elif valider == 'o':
                row["service_final"] = row["service"]
                row["type_final"]    = row["type"]
                row["urgence_final"] = row["urgence"]
                row["annote_par"]    = "humain-validé"
            else:
                row["service_final"] = choix(SERVICES, "Service destinataire")
                row["type_final"]    = choix(TYPES,    "Type de courrier")
                row["urgence_final"] = choix(URGENCES, "Urgence")
                row["annote_par"]    = "humain-corrigé"

            writer.writerow(row)
            f.flush()
            print(f"  ✓ Sauvegardé → {row['service_final']} / {row['type_final']} / {row['urgence_final']}")

if __name__ == "__main__":
    annoter()
