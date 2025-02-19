import streamlit as st
import pandas as pd

# 🏠 Titre de l'application
st.title("📊 Scoring du Nesting des Souris 🐭")

# Demander le nombre de souris à scorer
nombre_souris = st.number_input("Nombre de souris", min_value=1, step=1, value=1)

# Initialisation des listes pour stocker les données
souris = []
papier_scores = []
coton_scores = []
nid_scores = []
hauteur_scores = []

# Formulaire interactif pour chaque souris
for i in range(nombre_souris):
    st.subheader(f"Souris {i+1}")
    nom = st.text_input(f"Nom de la souris {i+1}", key=f"nom{i}")
    papier = st.slider(f"Score papier (0-5)", 0, 5, key=f"papier{i}")
    coton = st.slider(f"Score coton (0-5)", 0, 5, key=f"coton{i}")
    nid = st.slider(f"Score final du nid (0-5)", 0, 5, key=f"nid{i}")
    hauteur = st.number_input(f"Hauteur du nid (cm) pour {nom}", min_value=0.0, step=0.1, key=f"hauteur{i}")

    # Normalisation de la hauteur du nid (échelle de 0 à 5)
    max_hauteur = 10  # Hauteur maximale attendue (modifiable)
    score_hauteur = min((hauteur / max_hauteur) * 5, 5)

    souris.append(nom)
    papier_scores.append(papier)
    coton_scores.append(coton)
    nid_scores.append(nid)
    hauteur_scores.append(score_hauteur)

# Bouton pour générer et télécharger le fichier Excel
if st.button("📂 Générer le fichier Excel"):
    data = {
        "Souris": souris,
        "Papier_Score": papier_scores,
        "Coton_Score": coton_scores,
        "Score_Nid": nid_scores,
        "Hauteur_Nid (cm)": hauteur_scores
    }

    df = pd.DataFrame(data)

    # 🧮 Calcul des scores
    df["Score_Materiaux"] = (df["Papier_Score"] + df["Coton_Score"]) / 2
    df["Score_Nid_Ajusté"] = (0.7 * df["Score_Nid"]) + (0.3 * df["Hauteur_Nid (cm)"])
    df["Score_Final"] = (0.4 * df["Score_Materiaux"]) + (0.6 * df["Score_Nid_Ajusté"])

    # Sauvegarde du fichier Excel
    file_path = "Scoring_Nesting.xlsx"
    df.to_excel(file_path, index=False)

    # Affichage des résultats
    st.success("✅ Fichier Excel généré avec succès !")
    st.download_button("📥 Télécharger le fichier Excel", open(file_path, "rb"), file_name="Scoring_Nesting.xlsx")

