import openai
from dotenv import load_dotenv
import google.generativeai as genai
import os
import requests
import PIL.Image
import base64
from io import BytesIO

load_dotenv()

print(os.getenv('GEMINI_API_KEY'))
print(os.getenv('NVIDIA_API_KEY'))
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel("gemini-1.5-flash")
organ = PIL.Image.open("drawing_output.png")
responseP2T = model.generate_content(["Tell me about this. I am submitting a sketch that depicts common, everyday objects and scenes. I aim to create more realistic and practical images that reflect the way we experience life daily, focusing on natural details and authenticity.", organ])
print(responseP2T.text)

invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl"

headers = {
    "Authorization": f"Bearer {NVIDIA_API_KEY}",
    "Accept": "application/json",
}

payload = {
    "text_prompts": [
        {
            "text": f"{responseP2T}",
            "weight": 1
        },
        {
            "text":  "" ,
            "weight": -1
        }
    ],
    "cfg_scale": 5,
    "sampler": "K_DPM_2_ANCESTRAL",
    "seed": 0,
    "steps": 25
}

response = requests.post(invoke_url, headers=headers, json=payload)

response.raise_for_status()
response_body = response.json()

# Decode the base64 string
image_data = base64.b64decode(response_body['artifacts'][0]['base64'])

# Create an image from the decoded data
image = PIL.Image.open(BytesIO(image_data))

# Show the image
image.show()

# Optionally, save the image to a file
image.save('generated_image.png')
print("Image saved as generated_output.png")




