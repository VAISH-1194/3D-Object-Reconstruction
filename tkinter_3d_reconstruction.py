import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry_image_path.delete(0, tk.END)
        entry_image_path.insert(0, file_path)

def run_reconstruction():
    image_path = entry_image_path.get()
    output_dir = "outputs"
    method = method_var.get()
    
    if not os.path.exists(image_path):
        messagebox.showerror("Error", "Please select a valid image file.")
        return
    
    os.makedirs("data/images", exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    image_name = os.path.basename(image_path)
    new_image_path = os.path.join("data/images", image_name)
    
    # Copy image to data/images
    os.system(f"copy \"{image_path}\" \"{new_image_path}\"")
    
    # Run the reconstruction pipeline
    command = f"python src/main.py --method {method} --input_dir data/images --output_dir {output_dir}"
    subprocess.run(command, shell=True)
    
    # Check for output file
    obj_files = [f for f in os.listdir(output_dir) if f.endswith(".obj")]
    if obj_files:
        messagebox.showinfo("Success", f"3D Model Generated: {os.path.join(output_dir, obj_files[0])}")
    else:
        messagebox.showerror("Error", "3D Model generation failed.")

# GUI Setup
root = tk.Tk()
root.title("3D Reconstruction Tool")
root.geometry("500x300")

tk.Label(root, text="Select Image:").pack(pady=5)
entry_image_path = tk.Entry(root, width=50)
entry_image_path.pack()
tk.Button(root, text="Browse", command=select_image).pack(pady=5)

# Choose Method
tk.Label(root, text="Select Reconstruction Method:").pack(pady=5)
method_var = tk.StringVar(value="mvs")
tk.Radiobutton(root, text="MVS", variable=method_var, value="mvs").pack()
tk.Radiobutton(root, text="NeRF", variable=method_var, value="nerf").pack()

tk.Button(root, text="Run Reconstruction", command=run_reconstruction).pack(pady=10)

root.mainloop()

