import tkinter as tk
from tkinter import filedialog
from Manual_Detect import ManualDetect
from Auto_Detect import AutoDetect


def browse_image():
    filename = filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                          filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("all files", "*.*")))
    image_path.set(filename)

def run_manual_detect():
    image_path_value = image_path.get()
    if image_path_value:
        global manual_detect
        manual_detect = ManualDetect(image_path_value)
        manual_detect.process_image()

def run_auto_detect():
    image_path_value = image_path.get()
    if image_path_value:
        global auto_detect
        auto_detect = AutoDetect(image_path_value)
        auto_detect.process_image()

def quit_app():
    root.quit()

if __name__ == '__main__':
    # main()
    global image_path, root
    root = tk.Tk()
    root.title("Document Scanner")

    image_path = tk.StringVar()

    tk.Label(root, text="Select Image").pack(pady=10)
    tk.Entry(root, textvariable=image_path, width=50).pack(pady=10)
    tk.Button(root, text="Browse", command=browse_image).pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Manual", command=run_manual_detect).grid(row=0, column=0, padx=(0, 20))
    tk.Button(button_frame, text="Auto", command=run_auto_detect).grid(row=0, column=1, padx=20)
    tk.Button(button_frame, text="Quit", command=quit_app).grid(row=0, column=2, padx=(20, 0))
    root.mainloop()
