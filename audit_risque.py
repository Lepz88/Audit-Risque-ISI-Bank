import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Le vrai fichier de la banque (Sale et avec des pièges)
donnees_banque = {
    'ID_Client': ['CL-001', 'CL-002', 'CL-003', 'CL-004', 'CL-005', 'CL-006', 'CL-002', 'CL-008', 'CL-009', 'CL-010'],
    'Date_Ouverture': ['2023-01-15', '2025-11-20', '2024-05-10', '2026-02-01', '2021-08-30', '2025-12-05', '2025-11-20', '2026-01-10', '2024-09-22', np.nan],
    'Nom': ['Amath', 'Binta', 'Cheikh', 'Diarra', 'Fatou', 'Gaye', 'Binta', 'Haby', 'Issa', 'Jules'],
    'Age': [35, 22, 48, 19, 55, 30, 22, np.nan, 41, 28],
    'Solde_FCFA': [1500000, -50000, 25000000, 15000, -200000, 800000, -50000, 3000000, -10000, 50000],
    'Credit_En_Cours': [True, False, True, False, True, False, False, True, False, False]
}

df_isibank = pd.DataFrame(donnees_banque)

print("--- BASE DE DONNÉES BRUTE (ISI-BANK) ---")
# Suppression des doublons
df_isibank = df_isibank.drop_duplicates()

#Supprime radicalement les clients dont le dossier est incomplet (qui n'ont pas d'âge ou pas de date d'ouverture).
df_isibank = df_isibank.dropna(subset=['Age', 'Date_Ouverture'])
# Conversion de date
df_isibank['Date_Ouverture'] = pd.to_datetime(df_isibank['Date_Ouverture'])
print("\n--- BASE DE DONNÉES NETTOYÉE ---")
print(df_isibank)
print("\n--- AUDIT DES TYPES DE DONNÉES ---")
print(df_isibank.info())

#Crée une nouvelle colonne appelée Alerte_Rouge. Elle doit contenir True si le Solde_FCFA est strictement inférieur à 0, sinon False.
df_isibank['Alerte_Rouge'] = df_isibank['Solde_FCFA'] < 0


# Crée une nouvelle colonne appelée Categorie_client. Elle doit contenir trois catégories: Dette, Standard et Vip.
bins = [-np.inf, 0, 1000000, np.inf]
labels = ['Dette', 'Standard', 'Vip'] 
df_isibank['Categorie_client'] = pd.cut(df_isibank['Solde_FCFA'], bins=bins, labels=labels)
print("\n--- AUDIT DES DONNÉES ---")
print(df_isibank)

#Crée une variable resume_financier qui regroupe (groupby) les données par Categorie_client et calcule la somme (sum) du Solde_FCFA.
resume_financier = df_isibank.groupby('Categorie_client', observed=True)['Solde_FCFA'].sum()
print("\n--- RESUME FINANCIER ---")
print(resume_financier)

df_graphique = resume_financier.reset_index()

# --- 1. CONFIGURATION DE L'ESPACE DE TRAVAIL ---
plt.figure(figsize=(9, 6))

# --- 2. LA PSYCHOLOGIE DES COULEURS (Correction de la casse : 'Vip') ---
couleurs_metier = {'Dette': 'red', 'Standard': "Blue", 'Vip': 'green'}

# --- 3. LE GRAPHIQUE (Mise à jour 2026 : ajout de hue et legend=False) ---
ax = sns.barplot(
    x='Categorie_client', 
    y='Solde_FCFA', 
    data=df_graphique, 
    palette=couleurs_metier,
    hue='Categorie_client',  # Évite le warning de dépréciation
    legend=False             # Cache la légende redondante
)

# --- 4. ESTHÉTIQUE ET LISIBILITÉ DU MANAGEMENT ---
plt.title("Bilan Financier par Segment Client (ISI-Bank)", fontsize=14, fontweight='bold', pad=20)
plt.ylabel("Solde Total (FCFA)", fontsize=12, fontweight='bold')
plt.xlabel("Segment Stratégique", fontsize=12, fontweight='bold')

# --- 5. L'EXIGENCE COMPTABLE (Suppression des exposants scientifiques) ---
plt.ticklabel_format(style='plain', axis='y')

# --- 6. L'ARME FATALE (Affichage des chiffres exacts sur chaque barre) ---
for container in ax.containers:
    ax.bar_label(container, fmt='%d FCFA', padding=5, fontsize=11, fontweight='bold')

# --- 7. AJUSTEMENT FINAL ET AFFICHAGE ---
plt.tight_layout()
plt.show()