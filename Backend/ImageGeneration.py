import asyncio
from PIL import Image as PILImage
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    image_path = os.path.join(folder_path, f"{prompt}.jpg")  # Expect only one image
    
    if os.path.exists(image_path):
        try:
            img = PILImage.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
            img.close()
        except Exception as e:
            print(f"Unable to open {image_path}: {e}")
    else:
        print(f"Image file not found: {image_path}")

# Use DeepAI Text-to-Image API
API_URL = "https://api.deepai.org/api/text2img"
DEEPAI_API_KEY = get_key('.env', 'DeepAIApiKey')  # Ensure your DeepAI API key is in .env
headers = {"api-key": DEEPAI_API_KEY}

# Validate API key before proceeding
def validate_api_key():
    test_url = "https://api.deepai.org/api/text2img"
    try:
        response = requests.post(test_url, data={"text": "test"}, headers=headers, timeout=5)
        if response.status_code == 200:
            print("DeepAI API key validated successfully")
            return True
        elif response.status_code == 401:
            print("Error: Invalid DeepAI API key (401 Unauthorized). Please check your API key in .env")
            return False
        elif response.status_code == 429:
            print("Error: DeepAI API rate limit exceeded (429 Too Many Requests). Try again later.")
            return False
        else:
            print(f"Error: Unexpected response from DeepAI API: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error validating DeepAI API key: {e}")
        return False

async def query(payload):
    if not validate_api_key():
        print("Skipping image generation due to API key validation failure")
        return None

    for attempt in range(3):  # Retry up to 3 times
        try:
            print(f"Sending request to DeepAI API with payload: {payload} (Attempt {attempt+1})")
            response = await asyncio.to_thread(requests.post, API_URL, headers=headers, data=payload, timeout=30)
            response.raise_for_status()
            print(f"Received response from DeepAI API: {response.status_code}")
            image_url = response.json().get("output_url")
            if not image_url:
                print("Error: No image URL returned from DeepAI API")
                return None
            # Download the image from the URL
            image_response = await asyncio.to_thread(requests.get, image_url, timeout=10)
            image_response.raise_for_status()
            return image_response.content
        except requests.exceptions.RequestException as e:
            print(f"Error querying DeepAI API: {e}")
            if attempt == 2:  # Last attempt
                print("All attempts failed. Please check your network connection or API status.")
                return None
            sleep(2)  # Wait before retrying
    return None

async def generate_images(prompt: str):
    # Clean the prompt by removing "generate image" prefix if present
    if prompt.lower().startswith("generate image "):
        prompt = prompt[len("generate image "):].strip()
    print(f"Cleaned prompt for generation: {prompt}")

    # Generate only one image
    payload = {
        "text": f"{prompt}, high quality, detailed, sharp",
    }
    image_bytes = await query(payload)
    
    if image_bytes:
        image_path = fr"Data\{prompt.replace(' ', '_')}.jpg"  # Save as a single image
        try:
            print(f"Saving image to {image_path}")
            with open(image_path, "wb") as f:
                f.write(image_bytes)
        except Exception as e:
            print(f"Error saving image to {image_path}: {e}")
    else:
        print(f"Failed to generate image for prompt: {prompt}")

def GenerateImages(prompt: str):
    print(f"Starting image generation for prompt: {prompt}")
    # Ensure Data folder exists
    if not os.path.exists("Data"):
        os.makedirs("Data")
        print("Created Data folder")
    asyncio.run(generate_images(prompt))
    open_images(prompt)

while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
        if not Data:
            print("ImageGeneration.data is empty, waiting...")
            sleep(1)
            continue
        Prompt, Status = Data.split(",")
        if Status.strip() == "True":
            print("Generating Images...")
            GenerateImages(prompt=Prompt)
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            print("Status is not True, waiting...")
            sleep(1)
    except Exception as e:
        print(f"Error reading ImageGeneration.data: {e}")
        sleep(1)