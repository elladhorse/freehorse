from PIL import Image, ImageTk
import tkinter as tk
import pygame
import os
import random

# Global variables
sound_playing = False
viruses = []

def play_error_sound():
    global sound_playing
    pygame.mixer.init()
    sound_path = os.path.join(os.path.dirname(__file__), 'sounds', 'error-sound-39539.mp3')
    if os.path.isfile(sound_path):
        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            sound_playing = True
        except Exception as e:
            print(f"Error playing sound: {e}")
    else:
        print(f"Sound file not found: {sound_path}")

def stop_error_sound():
    global sound_playing
    if sound_playing:
        pygame.mixer.music.stop()
        sound_playing = False

def spawn_virus():
    virus_image_path = os.path.join(os.path.dirname(__file__), 'images', 'virus_symbol.png')
    if os.path.isfile(virus_image_path):
        try:
            image = Image.open(virus_image_path)
            image = image.resize((50, 50), Image.LANCZOS)
            icon = ImageTk.PhotoImage(image)
            
            virus_label = tk.Label(root, image=icon)
            virus_label.image = icon  # Keep a reference to avoid garbage collection
            
            # Randomly place the virus on the screen
            x = random.randint(0, root.winfo_width() - 50)
            y = random.randint(0, root.winfo_height() - 50)
            virus_label.place(x=x, y=y)
            
            virus_label.bind("<Button-1>", lambda event, label=virus_label: remove_virus(label))
            
            viruses.append(virus_label)
        except Exception as e:
            print(f"Error loading virus image: {e}")
    else:
        print(f"Virus image file not found: {virus_image_path}")

def remove_virus(virus_label):
    if virus_label in viruses:
        viruses.remove(virus_label)
        virus_label.destroy()

def clear_viruses():
    for virus in viruses:
        virus.destroy()
    viruses.clear()

def show_error():
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def reopen_error():
        play_error_sound()
        
        global error_window
        error_window = tk.Toplevel(root)
        error_window.title("System Error")
        error_window.geometry("300x200")
        error_window.resizable(True, True)

        center_window(error_window)

        image_path = os.path.join(os.path.dirname(__file__), 'images', 'Danger_warning.png')
        if os.path.isfile(image_path):
            try:
                image = Image.open(image_path)
                image = image.resize((50, 50), Image.LANCZOS)
                icon = ImageTk.PhotoImage(image)
                icon_label = tk.Label(error_window, image=icon)
                icon_label.image = icon
                icon_label.pack(pady=10)
            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            print(f"Image file not found: {image_path}")

        message_label = tk.Label(error_window, text="You Have Been Hacked", font=("Arial", 12))
        message_label.pack(pady=5)

        button_frame = tk.Frame(error_window)
        button_frame.pack(pady=10)

        ok_button = tk.Button(button_frame, text="OK", command=lambda: (play_error_sound(), None))
        ok_button.pack(side="left", padx=10)

        cancel_button = tk.Button(button_frame, text="Cancel", command=lambda: (play_error_sound(), stop_error_sound(), error_window.destroy(), reopen_error()))
        cancel_button.pack(side="right", padx=10)

        error_window.protocol("WM_DELETE_WINDOW", lambda: (play_error_sound(), error_window.destroy(), reopen_error()))

        root.bind('<KeyPress-4>', lambda event: (stop_error_sound(), clear_viruses(), error_window.destroy()))
        root.bind('<Button-1>', on_click)

        for _ in range(10):
            root.after(random.randint(1000, 5000), spawn_virus)

        root.wait_window(error_window)

    def on_click(event):
        if error_window and error_window.winfo_ismapped():
            play_error_sound()

    global root
    root = tk.Tk()
    root.withdraw()

    reopen_error()

if __name__ == "__main__":
    show_error()


