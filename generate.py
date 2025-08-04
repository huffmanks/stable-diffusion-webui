import requests
import json
from PIL import Image
import io
import base64
import os
import re
from datetime import datetime

# Define API Endpoints
BASE_URL = "http://127.0.0.1:7860"
OPTIONS_URL = f"{BASE_URL}/sdapi/v1/options"
TXT2IMG_URL = f"{BASE_URL}/sdapi/v1/txt2img"
USER_API_URL = "http://127.0.0.1:5001/api/users?count=100"

# Define the new model checkpoint you want to use
NEW_CHECKPOINT = "deliberateCyber_v50"
# NEW_CHECKPOINT = "cyberrealisticPony_catalystV30"

# Function to switch model checkpoint
def switch_checkpoint(model_name):
    payload = {"sd_model_checkpoint": model_name}
    response = requests.post(OPTIONS_URL, json=payload)
    if response.status_code == 200:
        print(f"Checkpoint switched to: {model_name}")
    else:
        print("Error switching checkpoint:", response.text)

# Fetch users from API
def fetch_users():
    response = requests.get(USER_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching users:", response.text)
        return []

# Slugify function to format filenames
def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()

# Convert image file to base64 (for ControlNet)
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Fetch current settings from Automatic1111
def get_current_settings():
    response = requests.get(OPTIONS_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching settings:", response.text)
        return None

# Generate images using current settings + ControlNet
def generate_images(users, control_image_path, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)

    settings = get_current_settings()
    if not settings:
        return

    controlnet_image = image_to_base64(control_image_path)

    base_prompt = "ultra realistic, soft studio lighting, clean background, high detail, sharp focus, DSLR quality, 8K, business headshot, formal suit, confident, corporate photography, LinkedIn photo, head centered with gap above head, show head to waist"

    for user in users:
        birthdate = datetime.strptime(user['birthDate'], "%m/%d/%Y")
        age = (datetime.now() - birthdate).days // 365
        hairColor = "realistic auburn red hair with soft highlights, natural shine and detailed strands" if user['hairColor'] == "red" else f"natural {user['hairColor']} hair"


        prompt = f"{user['race']} {user['gender']}, {hairColor}, realistic natural {user['eyeColor']} eyes with depth and subtle highlights, age {age} years old {base_prompt} "

        filename = f"{output_dir}/batch/{slugify(user['name'])}.jpg"

        payload = {
            "prompt": prompt,
            "negative_prompt": "cropping, heads touching the top, tight framing, heads close to edge, unnatural hair or eye color, plastic-like features, glowing or neon details, distorted anatomy, extra limbs or pupils, asymmetry, cartoonish or blurry features, AI artifacts, low quality, oversaturated or washed-out colors, unnatural lighting",
            "width": settings.get("sd_model_checkpoint_config", {}).get("width", 512),
            "height": settings.get("sd_model_checkpoint_config", {}).get("height", 512),
            "steps": settings.get("sd_model_checkpoint_config", {}).get("steps", 20),
            "cfg_scale": settings.get("sd_model_checkpoint_config", {}).get("cfg_scale", 7.0),
            "sampler_name": settings.get("sampler_name", "DPM++ 2M"),
            "schedule_type": "Automatic",
            "seed": -1,
            "batch_size": 1,
            "n_iter": 1,
            # "enable_hr": True,  # Enable High-Resolution (Hires. Fix)
            # "denoising_strength": 0.4,  # Keeps details but refines
            # "hr_scale": 2,  # 2x resolution upscale
            # "hr_upscaler": "R-ESRGAN 4x+",
            "alwayson_scripts": {
                "ControlNet": {
                    "args": [{
                        "image": f"data:image/png;base64,{controlnet_image}",
                        "module": "openpose_full",
                        "model": "control_v11p_sd15_openpose",
                        "weight": 1.0,
                        "resolution": 512,
                        "guidance_start": 0,
                        "guidance_end": 1.0,
                        "control_mode": "Balanced",
                        # "control_mode": "ControlNet is more important",
                        "resize_mode": "Resize and Fill"
                        # "resize_mode": "Just Resize"
                    }]
                }
            }
        }

        response = requests.post(TXT2IMG_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            image_data = result["images"][0]
            image_bytes = base64.b64decode(image_data)

            image = Image.open(io.BytesIO(image_bytes))
            image.save(filename, format="JPEG", quality=95)

            print(f"Saved: {filename}")
        else:
            print(f"Error generating image for {user['name']}:", response.text)

# Switch to the new model before generating images
# switch_checkpoint(NEW_CHECKPOINT)

# Fetch users and run batch generation
users = fetch_users()
controlnet_image_path = "control_image.jpg"
generate_images(users, controlnet_image_path)