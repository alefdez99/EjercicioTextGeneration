import requests
import json

# API Configuration
url = "http://127.0.0.1:5000/v1/completions"
headers = {"Content-Type": "application/json"}

def request_data():
    # Request data to user
    print("\n--- Configuración de la historia ---")
    main_name = input("Nombre del personaje principal: ")
    secondary_name = input("Nombre del personaje secundario: ")
    place = input("Lugar donde transcurre el relato: ")
    action = input("Acción que acontece en la historia: ")

    # Request user for creativity (temperature)
    print("\nNivel de creatividad:")
    print("1. Creatividad alta")
    print("2. Creatividad media")
    print("3. Creatividad baja")
    creativity = input("Seleccione el nivel (1/2/3): ").strip()

    # Map creativity option to temperature
    temperature_map = {"1": 0.9, "2": 0.7, "3": 0.3}
    temperature = temperature_map.get(creativity, 0.7)  # Default to media

    return main_name, secondary_name, place, action, temperature

def generate_story(main_name, secondary_name, place, action, temperature):
    # Generate story using the API

    # Prompt
    prompt = (
        f"Escribe una historia interesante y creativa con los siguientes elementos:\n"
        f"- Personaje principal: {main_name}\n"
        f"- Personaje secundario: {secondary_name}\n"
        f"- Lugar: {place}\n"
        f"- Acción importante: {action}\n"
        f"Escribe una historia completa, con un principio, desarrollo y final claro."
    )

    # Body request
    body = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": 500,  # Adjusted for longer stories
        "top_p": 1.0,  # Sampling parameter for diversity
        "frequency_penalty": 0.2,  # Reduce repetitiveness
        "presence_penalty": 0.5  # Encourage introducing new concepts
    }

    try:
        # Request to the API
        response = requests.post(url=url, headers=headers, json=body)
        response.raise_for_status()
        message_response = response.json()
        story = message_response["choices"][0]["text"].strip()

        return story
    except requests.exceptions.RequestException as e:
        return f"Error al conectarse con la API: {e}"
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error al procesar la respuesta de la API: {e}"

while True:
        # Request data
        main_name, secondary_name, place, action, temperature = request_data()
        story = generate_story(main_name, secondary_name, place, action, temperature)

        # Display story
        print("\n--- Historia Generada ---\n")
        print(story)
        print("\n-------------------------\n")

        # Ask if the user wants to generate another story
        another = input("¿Quieres generar otra historia? (s/n): ").strip().lower()
        if another != "s":
            print("¡Hasta pronto!")
            break
    