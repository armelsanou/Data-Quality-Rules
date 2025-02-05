import streamlit as st
import json
import os

# Appliquer un style CSS pour élargir la sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 50% !important;  /* Augmente la largeur de la sidebar */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

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
""" expectations_mapping = {
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
} """

# Définition des règles et de leurs descriptions
expectations_mapping = {
    "expect_column_distinct_values_to_be_in_set": {
        "label": "Vérifier les valeurs distinctes dans un ensemble",
        "description": "Cette règle permet de vérifier si toutes les valeurs distinctes d'une colonne sont incluses dans un ensemble spécifique.\nExemple : Pour une colonne 'Statut', les valeurs distinctes doivent être parmi ['Actif', 'Inactif', 'En attente']."
    },
    "expect_column_distinct_values_to_contain_set": {
        "label": "Vérifier si un ensemble est contenu dans les valeurs distinctes",
        "description": "Cette règle vérifie si un ensemble donné est inclus dans les valeurs distinctes d'une colonne.\nExemple : Vérifier que les catégories 'A' et 'B' existent bien dans une colonne 'Type'."
    },
    "expect_column_distinct_values_to_equal_set": {
        "label": "Vérifier si les valeurs distinctes sont égales à un ensemble",
        "description": "Cette règle s'assure que l'ensemble des valeurs distinctes d'une colonne correspond exactement à une liste donnée.\nExemple : Une colonne 'Statut' doit uniquement contenir ['Actif', 'Inactif']."
    },
    "expect_column_max_to_be_between": {
        "label": "Vérifier la valeur maximale dans une colonne",
        "description": "Cette règle vérifie que la valeur maximale d'une colonne se situe dans une plage définie.\nExemple : La colonne 'Prix' doit avoir un maximum compris entre 100 et 500."
    },
    "expect_column_min_to_be_between": {
        "label": "Vérifier la valeur minimale dans une colonne",
        "description": "Cette règle s'assure que la valeur minimale d'une colonne respecte une plage spécifique.\nExemple : Le salaire minimum doit être d'au moins 1000€."
    },
    "expect_column_to_exist": {
        "label": "Vérifier l'existence d'une colonne",
        "description": "Cette règle garantit qu'une colonne spécifique existe dans le dataset.\nExemple : Vérifier que la colonne 'Date de naissance' est bien présente."
    },
    "expect_column_value_lengths_to_be_between": {
        "label": "Vérifier la longueur des valeurs dans une colonne",
        "description": "Cette règle s'assure que la longueur des valeurs d'une colonne est comprise dans une plage donnée.\nExemple : Un code postal doit contenir entre 5 et 10 caractères."
    },
    "expect_column_value_lengths_to_equal": {
        "label": "Vérifier une longueur précise des valeurs",
        "description": "Cette règle impose une longueur précise aux valeurs d'une colonne.\nExemple : Un INS doit comporter exactement 3 caractères."
    },
    "expect_column_values_to_be_between": {
        "label": "Vérifier que les valeurs sont dans une plage",
        "description": "Cette règle vérifie que toutes les valeurs d'une colonne sont comprises entre un minimum et un maximum.\nExemple : L'âge des employés doit être compris entre 18 et 65 ans."
    },
    "expect_column_values_to_be_in_set": {
        "label": "Vérifier que les valeurs sont dans un ensemble",
        "description": "Cette règle s'assure que toutes les valeurs d'une colonne appartiennent à un ensemble défini.\nExemple : Une colonne 'Environnement' ne doit contenir que 'PROD' ou 'RECETTE'."
    },
    "expect_column_values_to_be_null": {
        "label": "Vérifier que les valeurs sont nulles",
        "description": "Cette règle vérifie qu'une colonne contient uniquement des valeurs nulles.\nExemple : Une colonne 'Commentaires' peut être vide pour certaines lignes."
    },
    "expect_column_values_to_be_unique": {
        "label": "Vérifier l'unicité des valeurs dans une colonne",
        "description": "Cette règle garantit qu'aucune valeur ne se répète dans une colonne.\nExemple : Une colonne 'Numéro de client' doit contenir des valeurs uniques."
    },
    "expect_column_values_to_match_regex": {
        "label": "Vérifier que les valeurs respectent une expression régulière",
        "description": "Cette règle assure que les valeurs d'une colonne respectent un format spécifique (regex).\nExemple : Une colonne 'Email' doit respecter le format 'exemple@domaine.com'."
    }
}

# Afficher le Navbar
navbar()

# Sidebar pour la gestion des règles
st.sidebar.header("Gestion des Règles de Qualité")
st.sidebar.subheader("Ajouter / Modifier une Règle")

# Boîte de dialogue pour afficher la description de la règle sélectionnée
@st.dialog("Explication de la règle")
def show_rule_info(rule_key):
    choosedRule = expectations_mapping[rule_key]
    st.write(f"**{choosedRule['label']}**")
    st.write(choosedRule["description"])
    if st.button("OK, j'ai compris !"):
        st.rerun()

expectation_label = st.sidebar.selectbox(
    "Choisissez une règle de qualité :",
    options=list(expectations_mapping.keys()),
    format_func=lambda x: expectations_mapping[x]["label"],
    #on_change=show_rule_info(expectation_label),  # Afficher la boîte de dialogue sur sélection
)

if expectation_label:
    show_rule_info(expectation_label)

# Affichage d'une alerte expliquant la règle sélectionnée
if expectation_label:
    st.sidebar.warning(expectations_mapping[expectation_label]["label"])
    st.sidebar.error(expectation_label)

# Affichage d'une fenêtre modale pour la description
if expectation_label:
    with st.expander("Description de la règle"):
        st.write(f"### {expectations_mapping[expectation_label]["label"]}")
        st.write(expectations_mapping[expectation_label]["description"])

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

if expectation_label in ["expect_column_max_to_be_between", "expect_column_min_to_be_between", "expect_column_values_to_be_between", "expect_column_value_lengths_to_be_between"]:
    params["min_value"] = st.sidebar.number_input("Valeur minimale :", value=0.0)
    params["max_value"] = st.sidebar.number_input("Valeur maximale :", value=100.0)

if expectation_label == "expect_column_value_lengths_to_equal" :
    params["value"] = st.sidebar.number_input("Valeur", value=0.0)

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

    #Affichage du boutton pour exporter au début
    st.download_button(
        label="Exporter les règles en JSON",
        data=json.dumps(st.session_state["rules"], indent=2),
        file_name=RULES_FILE,
        mime="application/json",
    )

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
        Tool for data quality - 2025
    </div>
    """,
    unsafe_allow_html=True,
)
