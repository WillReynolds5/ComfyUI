import streamlit as st
import random
import tempfile
import requests
import json
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import base64


# Set the server address for your API
server_address = "http://localhost:8188"


def gen_prompt(pos_prompt, neg_prompt, face_image_data, pose_image_data, denoise_setting, seed=None):
    import os

    if seed is None:
        seed = random.randint(0, 1_000_000)

    # Load the character generation JSON file
    with open('meeca/character_gen_v2.json', 'r') as file:
        character_gen_data = json.load(file)

    # Modify the positive and negative prompts
    character_gen_data["17"]["inputs"]["text"] = pos_prompt
    character_gen_data["18"]["inputs"]["text"] = neg_prompt

    # Set the seed
    character_gen_data["19"]["inputs"]["seed"] = seed

    # Include the image data
    character_gen_data["11"]["inputs"]["image"] = pose_image_data
    character_gen_data["29"]["inputs"]["image"] = face_image_data

    # Set the k sampler denoising setting
    character_gen_data["19"]["inputs"]["denoise"] = denoise_setting
    # Determine the next index for filename_prefix
    outputs_dir = "output"
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    return character_gen_data

def queue_prompt(prompt):
    import uuid
    client_id = str(uuid.uuid4())  # Generate a unique client ID per request
    payload = {"prompt": prompt, "client_id": client_id}
    response = requests.post(f"{server_address}/prompt", json=payload)
    return response.json()

def generate_tab():
    st.header("Generate Image")
    
    # Input prompts
    positive_prompt = st.text_area(
        "Positive Prompt",
        value="((masterpiece, best quality)), award winning, 4k, 8k, gorgeous women, super model"
    )
    negative_prompt = st.text_area(
        "Negative Prompt",
        value="text, watermark, underexposed, ugly, jpeg, (worst quality, low quality, lowres, low details, oversaturated, undersaturated, overexposed, grayscale, bw, bad photo, bad art:1.4), (font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), cropped, out of frame, cut off, jpeg artifacts, out of focus, glitch, duplicate, (amateur:1.3), merging, clipping, mutant, glitch, uncanny, cross eye, broken face, astronaut, helmet, blurry, (jewelry, bad anatomy, Polymastia)"
    )

    # Image uploads
    face_image_file = st.file_uploader("Upload Face Image", type=['jpg', 'jpeg', 'png'])
    pose_image_file = st.file_uploader("Upload Pose Image", type=['jpg', 'jpeg', 'png'])

    # Seed input
    seed_option = st.checkbox("Specify Seed", value=False)
    seed = None
    if seed_option:
        seed = st.number_input("Seed", min_value=0, max_value=1_000_000, value=0, step=1)

    # Denoise setting input
    denoise_setting = st.slider("K Sampler Denoising Setting", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    # Generate button
    if st.button("Generate"):
        if face_image_file is not None and pose_image_file is not None:

            # Save the uploaded files to temporary paths
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_face:
                tmp_face.write(face_image_file.read())
                face_image_path = tmp_face.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_pose:
                tmp_pose.write(pose_image_file.read())
                pose_image_path = tmp_pose.name

            # Generate the prompt
            prompt = gen_prompt(
                positive_prompt,
                negative_prompt,
                face_image_path,
                pose_image_path,
                denoise_setting,
                seed
            )

            # Send the workflow to the API
            response = queue_prompt(prompt)
            
            if response.get('prompt_id', None):
                st.success("Generation request sent successfully! Check the 'View Images' tab for results.")
                
                # Store the prompt ID in session state
                if 'prompt_ids' not in st.session_state:
                    st.session_state['prompt_ids'] = []
                st.session_state['prompt_ids'].append(response['prompt_id'])
                
                # Optionally, set the last prompt_id
                st.session_state['prompt_id'] = response['prompt_id']
            else:
                st.error("Failed to send the prompt to the API.")
        else:
            st.error("Please upload both face image and pose image.")

def inpainting_tab():
    st.header("Inpainting")

    # Sidebar options
    drawing_mode = "freedraw"
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 7)

    # Input prompts
    positive_prompt = st.text_area("Positive Prompt", value="Enter positive prompt here")
    negative_prompt = st.text_area("Negative Prompt", value="Enter negative prompt here")

    # Image upload
    uploaded_image = st.file_uploader("Upload Image for Inpainting", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        # Open the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Save the uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_image:
            image.save(tmp_image, format="PNG")
            image_path = tmp_image.name

        # Get original image dimensions
        img_width, img_height = image.size

        # Define maximum dimensions
        max_width, max_height = 800, 800

        # Calculate scaling factor
        scaling_factor = min(max_width / img_width, max_height / img_height, 1)

        # Resize image if necessary
        if scaling_factor < 1:
            new_width = int(img_width * scaling_factor)
            new_height = int(img_height * scaling_factor)
            image = image.resize((new_width, new_height), Image.LANCZOS)
        else:
            new_width, new_height = img_width, img_height

        # Create a canvas component with dynamic dimensions
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color="#000000",
            background_color="#000000",
            background_image=image,
            update_streamlit=True,
            height=new_height,
            width=new_width,
            drawing_mode=drawing_mode,
            point_display_radius=0,
            key="canvas",
        )

        # Display the resulting mask
        if canvas_result.image_data is not None:
            st.image(canvas_result.image_data, caption="Mask", use_column_width=True)

            # Convert the image data to a PIL Image
            mask_image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')

            # Ensure the mask and image have the same dimensions
            if mask_image.size != image.size:
                mask_image = mask_image.resize(image.size, Image.LANCZOS)

            # Save the mask to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_mask:
                mask_image.save(tmp_mask, format="PNG")
                mask_path = tmp_mask.name

            # Add a button to trigger the inpainting process
            if st.button("Run Inpainting"):
                # Generate the inpainting prompt
                prompt = gen_inpainting_prompt(
                    positive_prompt,
                    negative_prompt,
                    image_path,
                    mask_path
                )

                # Send the workflow to the API
                response = queue_prompt(prompt)

                if response.get('prompt_id', None):
                    st.success("Inpainting request sent successfully! Check the 'View Images' tab for results.")
                    
                    # Store the prompt ID in session state
                    if 'prompt_ids' not in st.session_state:
                        st.session_state['prompt_ids'] = []
                    st.session_state['prompt_ids'].append(response['prompt_id'])
                    
                    # Optionally, set the last prompt_id
                    st.session_state['prompt_id'] = response['prompt_id']
                else:
                    st.error("Failed to send the inpainting prompt to the API.")

def view_images_tab():
    st.header("View Generated Images")
    
    import os
    from PIL import Image
    import re

    outputs_dir = "output"
    if not os.path.exists(outputs_dir):
        st.error(f"Directory not found: {outputs_dir}")
        return

    image_files = [f for f in os.listdir(outputs_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]

    if not image_files:
        st.info("No images found in the outputs directory.")
        return

    # Sort image files in descending order based on the number in the filename
    image_files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else 0, reverse=True)

    # Create a 4-column layout
    cols = st.columns(4)

    # Display images in the grid
    for i, image_file in enumerate(image_files):
        with cols[i % 4]:
            image_path = os.path.join(outputs_dir, image_file)
            image = Image.open(image_path)
            st.image(image, caption=image_file, use_column_width=True)
            
            # Add a delete button for each image
            if st.button(f"Delete {image_file}", key=f"delete_{i}"):
                os.remove(image_path)
                st.success(f"Deleted {image_file}")
                st.rerun()  # Refresh the page to update the image list

def gen_inpainting_prompt(pos_prompt, neg_prompt, image_path, mask_path):
    import json

    # Load the inpainting JSON file
    with open('meeca/inpainting.json', 'r') as file:
        inpainting_data = json.load(file)

    # Modify the positive and negative prompts
    inpainting_data["79"]["inputs"]["text"] = pos_prompt
    inpainting_data["80"]["inputs"]["text"] = neg_prompt

    # Read the image and mask data as bytes
    with open(image_path, 'rb') as img_file:
        image_data = img_file.read()
    with open(mask_path, 'rb') as mask_file:
        mask_data = mask_file.read()

    # Encode the image and mask data to Base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    encoded_mask = base64.b64encode(mask_data).decode('utf-8')

    # Include the Base64-encoded image and mask data
    inpainting_data["77"]["inputs"]["image"] = encoded_image
    inpainting_data["86"]["inputs"]["mask"] = encoded_mask

    return inpainting_data

def main():
    st.title("Character Generation App")
    tab1, tab2, tab3 = st.tabs(["Generate", "Inpainting", "View Images"])  # Removed "Add New Avatar" tab
    
    with tab1:
        generate_tab()
    
    with tab2:
        inpainting_tab()

    with tab3:
        view_images_tab()

if __name__ == "__main__":
    main()
