import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import zipfile
import subprocess

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_label.config(text=f"Selected: {os.path.basename(file_path)}")
        process_3d_model(file_path)

def process_3d_model(image_path):
    output_dir = "outputs"
    os.makedirs("data/images", exist_ok=True)
    shutil.copy(image_path, "data/images/input_image.jpg")
    
    subprocess.run(["python", "src/main.py", "--method", "mvs", "--input_dir", "data/images", "--output_dir", output_dir])
    
    zip_filename = "3D_object.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(output_dir):
            if file.endswith(".obj") or file.endswith(".ply"):
                zipf.write(os.path.join(output_dir, file), file)
    
    messagebox.showinfo("Success", f"3D model saved as {zip_filename}")
    os.startfile(zip_filename)

root = tk.Tk()
root.title("3D Reconstruction")
root.geometry("400x200")

tk.Label(root, text="Upload an image to generate a 3D model").pack(pady=10)
image_label = tk.Label(root, text="No image selected")
image_label.pack()

tk.Button(root, text="Select Image", command=select_image).pack(pady=10)
root.mainloop()
