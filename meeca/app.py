import streamlit as st
from scratch_3 import gen_prompt
import tempfile
import requests
import json
import os
from PIL import Image

# Set the server address for your API
server_address = "http://127.0.0.1:8188"

def queue_prompt(prompt):
    payload = {"prompt": prompt}
    response = requests.post(f"{server_address}/prompt", json=payload)
    return response

def load_images():
    images = []
    output_dir = "../output"  # Changed to look one directory back
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(output_dir, filename)
                images.append((filename, Image.open(image_path)))
    return images

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
            
            if response.status_code == 200:
                st.success("Generation request sent successfully! Check the 'View Images' tab for results.")
            else:
                st.error("Failed to send the prompt to the API.")
        else:
            st.error("Please upload both face image and pose image.")

def view_images_tab():
    st.header("View Generated Images")
    images = load_images()
    
    if not images:
        st.write("No generated images found.")
    else:
        cols = st.columns(3)
        for idx, (filename, image) in enumerate(images):
            with cols[idx % 3]:
                st.image(image, caption=filename, use_column_width=True)

def main():
    st.title("Character Generation App")

    tab1, tab2 = st.tabs(["Generate", "View Images"])
    
    with tab1:
        generate_tab()
    
    with tab2:
        view_images_tab()

if __name__ == "__main__":
    main()
