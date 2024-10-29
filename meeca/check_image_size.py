import os
from PIL import Image
import shutil

def check_and_copy_large_images(source_dir, min_size=900):
    # Create target directory by appending _big to source
    target_dir = f"{source_dir}_big"
    os.makedirs(target_dir, exist_ok=True)
    
    # Track statistics
    total_images = 0
    copied_images = 0
    
    # Iterate through all files in source directory
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            image_path = os.path.join(source_dir, filename)
            try:
                # Open and check image dimensions
                with Image.open(image_path) as img:
                    width, height = img.size
                    if width >= min_size and height >= min_size:
                        # Copy image
                        shutil.copy2(image_path, os.path.join(target_dir, filename))
                        
                        # Copy corresponding caption file if it exists
                        caption_filename = os.path.splitext(filename)[0] + '.txt'
                        caption_path = os.path.join(source_dir, caption_filename)
                        if os.path.exists(caption_path):
                            shutil.copy2(caption_path, os.path.join(target_dir, caption_filename))
                        
                        copied_images += 1
                    total_images += 1
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    print(f"Processed {total_images} images")
    print(f"Copied {copied_images} images meeting size requirements")
    return target_dir

if __name__ == "__main__":
    source_directory = "/home/mclean/Pictures/captioned_characters_elitebabe"
    check_and_copy_large_images(source_directory)

