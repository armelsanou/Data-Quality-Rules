import streamlit as st
import json
import os

# Fonction pour afficher le navbar
def navbar():
    # Navbar sous la Sidebar
    st.sidebar.markdown("---")  # Ligne de séparation
    st.sidebar.markdown(
        """
        <style>
            .navbar {
                background-color: #004080;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        </style>
        <div class="navbar">
            <a href="/" style="color: white; text-decoration: none;">🏠 Accueil</a> | 
            <a href="#" style="color: white; text-decoration: none;">📊 Dashboard</a> | 
            <a href="#" style="color: white; text-decoration: none;">⚙️ Paramètres</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Définition du fichier JSON pour stocker les règles
RULES_FILE = "rules.json"

# Chargement automatique des règles au démarrage
if "rules" not in st.session_state:
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r", encoding="utf-8") as file:
            try:
                st.session_state["rules"] = json.load(file)
            except json.JSONDecodeError:
                st.session_state["rules"] = []
    else:
        st.session_state["rules"] = []

# Définition des règles et de leurs libellés lisibles
expectations_mapping = {
    "expect_column_distinct_values_to_be_in_set": "Vérifier les valeurs distinctes dans un ensemble",
    "expect_column_distinct_values_to_contain_set": "Vérifier si un ensemble est contenu dans les valeurs distinctes",
    "expect_column_distinct_values_to_equal_set": "Vérifier si les valeurs distinctes sont égales à un ensemble",
    "expect_column_max_to_be_between": "Vérifier la valeur maximale dans une colonne",
    "expect_column_min_to_be_between": "Vérifier la valeur minimale dans une colonne",
    "expect_column_to_exist": "Vérifier l'existence d'une colonne",
    "expect_column_value_lengths_to_be_between": "Vérifier la longueur des valeurs dans une colonne",
    "expect_column_value_lengths_to_equal": "Vérifier une longueur précise des valeurs",
    "expect_column_values_to_be_between": "Vérifier que les valeurs sont dans une plage",
    "expect_column_values_to_be_in_set": "Vérifier que les valeurs sont dans un ensemble",
    "expect_column_values_to_be_null": "Vérifier que les valeurs sont nulles",
    "expect_column_values_to_be_unique": "Vérifier l'unicité des valeurs dans une colonne",
    "expect_column_values_to_match_regex": "Vérifier que les valeurs respectent une expression régulière",
}

# Afficher le Navbar
navbar()

# Sidebar pour la gestion des règles
st.sidebar.header("Gestion des Règles de Qualité")
st.sidebar.subheader("Ajouter / Modifier une Règle")

expectation_label = st.sidebar.selectbox(
    "Choisissez une règle de qualité :",
    options=list(expectations_mapping.keys()),
    format_func=lambda x: expectations_mapping[x],
)

column_name = st.sidebar.text_input("Nom de la colonne :")

# Champs dynamiques pour les paramètres
params = {}
if expectation_label in [
    "expect_column_distinct_values_to_be_in_set",
    "expect_column_distinct_values_to_contain_set",
    "expect_column_distinct_values_to_equal_set",
    "expect_column_values_to_be_in_set",
]:
    value_set = st.sidebar.text_area("Liste des valeurs (séparées par des virgules) :")
    if value_set:
        params["value_set"] = [v.strip() for v in value_set.split(",")]

if expectation_label in ["expect_column_max_to_be_between", "expect_column_min_to_be_between", "expect_column_values_to_be_between"]:
    params["min_value"] = st.sidebar.number_input("Valeur minimale :", value=0.0)
    params["max_value"] = st.sidebar.number_input("Valeur maximale :", value=100.0)

if expectation_label == "expect_column_values_to_match_regex":
    params["regex"] = st.sidebar.text_input("Expression régulière :")

# Ajout ou modification d'une règle
if st.sidebar.button("Ajouter / Modifier la règle"):
    if not column_name.strip():
        st.sidebar.error("Le nom de la colonne est obligatoire.")
    else:
        config = {
            "expectation_config": {
                "expectation_type": expectation_label.lower(),
                "kwargs": {"column": column_name, **params},
                "meta": {},
            }
        }

        # Vérification de l'existence de la règle
        duplicate_rule = next(
            (rule for rule in st.session_state["rules"] if rule["expectation_config"] == config["expectation_config"]),
            None,
        )

        if duplicate_rule:
            st.sidebar.warning("Cette règle existe déjà.")
        else:
            st.session_state["rules"].append(config)
            with open(RULES_FILE, "w", encoding="utf-8") as file:
                json.dump(st.session_state["rules"], file, indent=2)

            st.sidebar.success("Règle ajoutée avec succès !")
            st.rerun()

# Affichage des règles enregistrées
st.header("Liste des Règles de Qualité")
if st.session_state["rules"]:
    rules_table = [
        {
            "Règle": expectations_mapping.get(rule["expectation_config"]["expectation_type"], rule["expectation_config"]["expectation_type"]),
            "Colonne": rule["expectation_config"]["kwargs"]["column"],
            "Paramètres": rule["expectation_config"]["kwargs"],
        }
        for rule in st.session_state["rules"]
    ]
    st.table(rules_table)

    for index, rule in enumerate(st.session_state["rules"]):
        st.write(f"### Règle {index + 1}")
        st.json(rule)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Modifier", key=f"edit_{index}"):
                st.session_state["edit_index"] = index
                st.session_state["edit_rule"] = rule

        with col2:
            if st.button("Supprimer", key=f"delete_{index}"):
                st.session_state["rules"].pop(index)
                with open(RULES_FILE, "w", encoding="utf-8") as file:
                    json.dump(st.session_state["rules"], file, indent=2)
                st.rerun()

    st.download_button(
        label="Exporter les règles en JSON",
        data=json.dumps(st.session_state["rules"], indent=2),
        file_name=RULES_FILE,
        mime="application/json",
    )
else:
    st.info("Aucune règle ajoutée pour le moment.")

st.markdown("---")
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #555;
        }
    </style>
    <div class="footer">
        Développé avec ❤️ par Sanou - 2025
    </div>
    """,
    unsafe_allow_html=True,
)
