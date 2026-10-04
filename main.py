import base64
import os
import requests
from dotenv import load_dotenv

# Charge la clé d'API depuis le fichier .env
load_dotenv()

API_KEY = os.getenv("RODIUMAI_API_KEY")

# Vérification rapide si la clé est trouvée
if not API_KEY:
    print(
        "Erreur : La clé RODIUMAI_API_KEY n'a pas été trouvée dans le fichier .env !"
    )
    exit()

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Variable pour suivre l'étape actuelle (1, 2 ou 3)
etape = 3

while True:
    # ==================== ÉTAPE 1 : CHAT ====================
    if etape == 1:
        print("\n=== Étape 1 : Chat ===")
        question = input("Votre question : ")

        url = "https://api.rodiumai.io/v1/chat/completions"
        payload = {
            "model": "openai/gpt-4o",  
            "messages": [{"role": "user", "content": question}],
        }

        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                # Extraction classique de la réponse et du coût
                contenu = data["choices"][0]["message"]["content"]
                cost = data.get("cost_rodi", "Non spécifié")

                print("\n[Réponse du modèle]")
                print(contenu)
                print(f"Coût : {cost} RODI")
            else:
                error_code = response.status_code
                print(
                    f"Erreur HTTP : {error_code} - {response.text}"
                )

        except Exception as e:
            print(f"Erreur de connexion : {e}")

        # Choix de l'utilisateur à l'étape 1 (pas d'option 'b')
        choix = (
            input(
                "\nRester sur cette étape (r) ou passer à la suivante (s) ? "
            )
            .strip()
            .lower()
        )
        if choix == "s":
            etape = 2
        elif choix == "r":
            etape = 1
        # Si choix == 'r', la boucle recommence avec etape = 1

    # ==================== ÉTAPE 2 : IMAGE ====================
    elif etape == 2:
        print("\n=== Étape 2 : Image ===")
        description = input("Décrivez l'image : ")

        url = "https://api.rodiumai.io/v1/images/generations"
        payload = {
            "model": "google/gemini-3.1-flash-lite-image",
            "prompt": description,
            "response_format": "b64_json",
        }

        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                b64_string = data["data"][0]["b64_json"]

                # Décodage du base64 et sauvegarde dans image.png
                image_data = base64.b64decode(b64_string)
                with open("image.png", "wb") as f:
                    f.write(image_data)

                print("Image enregistrée : image.png")
            else:
                error_code = response.status_code
                print(
                    f"Erreur HTTP : {error_code} - {response.text}"
                )

        except Exception as e:
            print(f"Erreur de connexion : {e}")

        # Choix à l'étape 2 (r, s, b)
        choix = (
            input(
                "\nRevenir en arrière (b), rester (r) ou passer à la suivante (s) ? "
            )
            .strip()
            .lower()
        )
        if choix == "b":
            etape = 1
        else:
            if choix == "s":
                etape = 3

    # ==================== ÉTAPE 3 : VIDÉO ====================
    elif etape == 3:
        print("\n=== Étape 3 : Vidéo ===")
        description = input("Décrivez la vidéo : ")

        url = "https://api.rodiumai.io/v1/videos/generations"
        payload = {
            "model": "google/veo-3.1-fast",
            "prompt": description,
            "duration": 2,  # Durée courte demandée pour économiser les crédits
        }

        try:
            # Timeout de 150 secondes (2 min 30 s) imposé par la consigne
            response = requests.post(
                url, json=payload, headers=headers, timeout=150
            )

            if response.status_code == 200:
                # Si l'API renvoie directement les octets du fichier mp4
                with open("video.mp4", "wb") as f:
                    f.write(response.content)

                print("Vidéo enregistrée : video.mp4")
            else:
                error_code = response.status_code
                print(
                    f"Erreur HTTP : {error_code} - {response.text}"
                )

        except Exception as e:
            print(f"Erreur de connexion : {e}")

        # Choix à l'étape 3 (r, b, q) — Pas d'option 's' car c'est la dernière étape
        choix = (
            input(
                "\nRevenir en arrière (b), rester (r) ou quitter le programme (q) ? "
            )
            .strip()
            .lower()
        )
        if choix == "b":
            etape = 2
        elif choix == "q":
            print("Fin du programme.")
            break