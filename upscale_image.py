import requests
import io
import base64
from PIL import Image

def upscale_image(image_url, output_file):
    # Load the image from the URL
    response = requests.get(image_url)
    im = Image.open(io.BytesIO(response.content)).convert("RGB")
    
    # Convert the image to base64
    img_bytes = io.BytesIO()
    im.save(img_bytes, format='PNG')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    
    # Define the API endpoint and payload
    url = 'https://6071d63ba6a431d7e2.gradio.live/sdapi/v1/img2img'
    payload = {
        "init_images": [img_base64],
        "script_name": "outpainting mk2",
        "script_args": []  # Add the necessary script arguments here
    }
    
    # Send the request to the API
    response = requests.post(url, json=payload)
    
    # Handle the response
    if response.status_code == 200:
        result_img_base64 = response.json()['images'][0].split(",")[-1]
        result_img = Image.open(io.BytesIO(base64.b64decode(result_img_base64)))
        result_img.save(output_file)
        print(f"Upscaled image saved to {output_file}")
    else:
        print(f"Failed to upscale the image. Status code: {response.status_code}")

# Test the function with a sample image URL
image_url = 'https://www.dropbox.com/scl/fi/78u9j4vkuupmngn53mt6w/a_funny_creature_with_a_guitar_looking_at_something__a777a19f-2bf9-444c-9513-4be2fd5f5f54.png?rlkey=l58j1ygkhz37fe6mtq175voov&dl=1'
upscale_image(image_url, 'upscaled_image.png')
