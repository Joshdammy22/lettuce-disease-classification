from app import create_app
from app.models import *

def populate_disease_info():
    diseases = [
        {
            "name": "Wilt_and_leaf_blight_on_lettuce",
            "description": "Wilt and leaf blight cause wilting and browning of leaves, leading to reduced photosynthesis and plant death.",
            "causes": "Fungal pathogens such as Fusarium oxysporum and Alternaria species. Pests like aphids and nematodes can also cause or exacerbate these diseases.",
            "recommendation_text": "Ensure proper soil drainage and avoid overwatering. Use fungicides like mancozeb or chlorothalonil. Remove and destroy infected plants to prevent the spread of the disease."
        },
        {
            "name": "Septoria_Blight_on_lettuce",
            "description": "Septoria blight causes circular spots on leaves with gray centers and dark borders, leading to premature leaf drop.",
            "causes": "Septoria lactucae, a fungal pathogen. Leafhoppers and aphids can transmit the pathogen and contribute to the spread of the disease.",
            "recommendation_text": "Apply fungicides such as copper-based fungicides or chlorothalonil. Practice crop rotation and avoid overhead watering. Remove and destroy infected plant debris."
        },
        {
            "name": "Powdery_mildew_on_lettuce",
            "description": "Powdery mildew appears as white powdery spots on leaves, stems, and buds, affecting plant growth.",
            "causes": "Fungal pathogens such as Erysiphe cichoracearum. Pests such as whiteflies and spider mites can create conditions that favor the development of powdery mildew.",
            "recommendation_text": "Use sulfur-based fungicides or potassium bicarbonate. Ensure good air circulation around the plants. Remove and destroy infected leaves to reduce the spread of spores."
        },
        {
            "name": "Downy_mildew_on_lettuce",
            "description": "Downy mildew causes yellowing of leaves and a downy growth on the undersides, leading to leaf death.",
            "causes": "Fungal pathogens such as Bremia lactucae. Thrips and aphids can act as vectors, spreading the disease among plants.",
            "recommendation_text": "Apply fungicides like fosetyl-al or metalaxyl. Avoid overhead irrigation and ensure proper plant spacing. Remove and destroy infected plants and plant debris."
        }
    ]

    for disease in diseases:
        existing_disease = DiseaseInfo.query.filter_by(name=disease["name"]).first()
        if not existing_disease:
            new_disease = DiseaseInfo(
                name=disease["name"],
                description=disease["description"],
                causes=disease["causes"],
                recommendation_text=disease["recommendation_text"]  # Add this line
            )
            db.session.add(new_disease)

    db.session.commit()

if __name__ == '__main__':
    app = create_app()  # Ensure you call your application factory function to create the app instance
    with app.app_context():
        populate_disease_info()
        print("Disease info populated successfully.")
