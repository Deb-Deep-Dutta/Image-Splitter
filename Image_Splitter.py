"""
Image Splitter Program
Author: Deb Deep Dutta
"""
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import zipfile
import math

def split_image(image, num_slices, output_directory):
    slice_height = math.ceil(image.height / num_slices)  # Calculate slice height to evenly split the image

    images_to_zip = []  # List to store image filenames for zipping

    for i in range(num_slices):
        y_start = i * slice_height
        y_end = min(y_start + slice_height, image.height)  # Ensure the last slice fits within the image
        short_image = image.crop((0, y_start, image.width, y_end))

        # Get the original image's name and extension
        original_name, original_extension = os.path.splitext(os.path.basename(image.filename))

        # Save the short image with the modified name
        short_image_filename = os.path.join(output_directory, f"{original_name}_{i + 1}{original_extension}")
        short_image.save(short_image_filename)
        images_to_zip.append(short_image_filename)  # Add image to list for zipping

    print("Images split and saved.")

    if len(images_to_zip) > 6:
        zip_filename = os.path.join(output_directory, f"{original_name}_split_images.zip")
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for image_filename in images_to_zip:
                zipf.write(image_filename, os.path.basename(image_filename))
        print(f"Images zipped together as '{zip_filename}'.")

def select_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title="Select a Long Image")
    if file_path:
        long_image = Image.open(file_path)

        choice = simpledialog.askstring("Input", "Choose an option:\n1. A4 size\n2. Custom size\n3. Specify number of parts")

        if choice == "1":
            # Define A4 dimensions in pixels (assuming 300 DPI)
            a4_width = 2480  # 8.27 inches * 300 DPI
            a4_height = 3508  # 11.69 inches * 300 DPI
            output_directory = filedialog.askdirectory(title="Select an Output Folder")
            if output_directory:
                split_image(long_image, math.ceil(long_image.height / a4_height), output_directory)
        elif choice == "2":
            unit_choice = simpledialog.askstring("Input", "Choose a unit:\n1. Inches\n2. Centimeters\n3. Millimeters")
            if unit_choice in ["1", "2", "3"]:
                custom_height = simpledialog.askfloat("Input", "Enter the custom slice height:")
                if custom_height:
                    output_directory = filedialog.askdirectory(title="Select an Output Folder")
                    if output_directory:
                        if unit_choice == "2":
                            custom_height *= 10  # Convert cm to mm
                        elif unit_choice == "1":
                            custom_height *= 25.4  # Convert inches to mm
                        split_image(long_image, math.ceil(long_image.height / custom_height), output_directory)
                else:
                    print("Invalid input.")
            else:
                print("Invalid unit choice.")
        elif choice == "3":
            num_parts = simpledialog.askinteger("Input", "Enter the number of parts:")
            if num_parts:
                output_directory = filedialog.askdirectory(title="Select an Output Folder")
                if output_directory:
                    split_image(long_image, num_parts, output_directory)
            else:
                print("Invalid input.")
        else:
            print("Invalid choice.")

        repeat = input("Do you want to perform the task again? (yes/no): ")
        if repeat.lower() == "yes":
            select_image()

if __name__ == "__main__":
    select_image()
