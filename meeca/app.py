import streamlit as st
import random
import tempfile
import requests
import json
import base64

# Set the server address for your API
server_address = "http://localhost:8188"

# Add your API endpoint URL
API_ENDPOINT = 'https://d14226xey1.execute-api.us-west-1.amazonaws.com/meeca2-dev/avatars'

def gen_prompt(pos_prompt, neg_prompt, background_prompt, face_image_data, pose_image_data, seed=None):
    import os

    if seed is None:
        seed = random.randint(0, 1_000_000)

    # Load the character generation JSON file
    with open('meeca/charactergen.json', 'r') as file:
        character_gen_data = json.load(file)

    # Modify the positive, negative, and background prompts
    character_gen_data["17"]["inputs"]["text"] = pos_prompt
    character_gen_data["18"]["inputs"]["text"] = neg_prompt
    character_gen_data["86"]["inputs"]["text"] = background_prompt

    # Set the seed
    character_gen_data["19"]["inputs"]["seed"] = seed

    # Set the grounding dino prompt to 'women'
    character_gen_data["14"]["inputs"]["prompt"] = "women"

    # Include the image data
    character_gen_data["11"]["inputs"]["image"] = pose_image_data
    character_gen_data["29"]["inputs"]["image"] = face_image_data

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
        value="text, watermark, underexposed, ugly, jpeg"
    )
    background_prompt = st.text_area(
        "Background Prompt",
        value="luxury hotel room"
    )

    # Image uploads
    face_image_file = st.file_uploader("Upload Face Image", type=['jpg', 'jpeg', 'png'])
    pose_image_file = st.file_uploader("Upload Pose Image", type=['jpg', 'jpeg', 'png'])

    # Seed input
    seed_option = st.checkbox("Specify Seed", value=False)
    seed = None
    if seed_option:
        seed = st.number_input("Seed", min_value=0, max_value=1_000_000, value=0, step=1)

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
                background_prompt,
                face_image_path,
                pose_image_path,
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

def view_images_tab():
    st.header("View Generated Images")
    
    if st.button("Refresh Images"):
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
        image_files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()), reverse=True)

        # Create a 4-column layout
        cols = st.columns(4)

        # Display images in the grid
        for i, image_file in enumerate(image_files):
            with cols[i % 4]:
                image_path = os.path.join(outputs_dir, image_file)
                image = Image.open(image_path)
                st.image(image, caption=image_file, use_column_width=True)

def add_avatar_tab():
    st.header("Add New Avatar")
    
    # Avatar details input
    avatar_name = st.text_input("Avatar Name")
    personality = st.text_area("Personality Description")
    
    # Image uploads
    uploaded_images = st.file_uploader(
        "Upload Avatar Images",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )
    
    # Descriptions for each image
    image_descriptions = []
    if uploaded_images:
        for idx, img_file in enumerate(uploaded_images):
            st.image(img_file, caption=f"Image {idx+1}")
            description = st.text_input(f"Description for Image {idx+1}", key=f"desc_{idx}")
            image_descriptions.append({
                'file': img_file,
                'description': description
            })
    
    # Submit button
    if st.button("Add Avatar"):
        if avatar_name and personality and image_descriptions:
            images_data = []
            for img in image_descriptions:
                img_bytes = img['file'].read()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                images_data.append({
                    'data': img_base64,
                    'description': img['description']
                })
            
            # Prepare payload
            payload = {
                'name': avatar_name,
                'personality': personality,
                'images': images_data
            }
            
            # Make POST request to your API
            response = requests.post(API_ENDPOINT, json=payload)
            
            if response.status_code == 200:
                st.success("Avatar added successfully!")
            else:
                st.error("Failed to add avatar.")
        else:
            st.error("Please provide all required information.")

def main():
    st.title("Character Generation App")
    tab1, tab2, tab3 = st.tabs(["Generate", "View Images", "Add New Avatar"])
    
    with tab1:
        generate_tab()
    
    with tab2:
        view_images_tab()
    
    with tab3:
        add_avatar_tab()

if __name__ == "__main__":
    main()
