from PIL import Image, ImageTk
import tkinter as tk
import pygame
import os

# Global variable to keep track of the sound state
sound_playing = False

def play_error_sound():
    global sound_playing
    # Initialize the pygame mixer
    pygame.mixer.init()
    
    # Path to the MP3 sound file
    sound_path = os.path.join(os.path.dirname(__file__), 'error-sound-39539.mp3')
    
    # Check if the file exists before attempting to play it
    if os.path.isfile(sound_path):
        try:
            # Load the MP3 file
            pygame.mixer.music.load(sound_path)
            # Play the MP3 file (play once)
            pygame.mixer.music.play()
            # Set the sound state to playing
            sound_playing = True
        except Exception as e:
            print(f"Error playing sound: {e}")
    else:
        print(f"Sound file not found: {sound_path}")

def stop_error_sound():
    global sound_playing
    if sound_playing:
        # Stop the sound if it's currently playing
        pygame.mixer.music.stop()
        # Reset the sound state
        sound_playing = False

def show_error():
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def reopen_error():
        # Function to reopen the error message window
        error_window = tk.Toplevel(root)
        error_window.title("System Error")
        error_window.geometry("300x200")
        error_window.resizable(False, False)

        # Center the window
        center_window(error_window)

        # Construct the full file path for the image
        image_path = os.path.join(os.path.dirname(__file__), 'Horse_image.png')

        # Check if the image file exists before attempting to load it
        if os.path.isfile(image_path):
            try:
                # Load and resize the image using Pillow
                image = Image.open(image_path)
                image = image.resize((50, 50), Image.LANCZOS)

                # Convert the image to PhotoImage
                icon = ImageTk.PhotoImage(image)

                # Display the image
                icon_label = tk.Label(error_window, image=icon)
                icon_label.image = icon  # Keep a reference to avoid garbage collection
                icon_label.pack(pady=10)
            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            print(f"Image file not found: {image_path}")

        # Display the message
        message_label = tk.Label(error_window, text="You Have Been Hacked !!!", font=("Arial", 12))
        message_label.pack(pady=5)

        # OK and Cancel buttons
        button_frame = tk.Frame(error_window)
        button_frame.pack(pady=10)

        # OK Button: Plays the sound
        ok_button = tk.Button(button_frame, text="OK", command=lambda: (play_error_sound(), None))
        ok_button.pack(side="left", padx=10)

        # Cancel Button: Stops the sound, closes the window, and reopens a new error message window
        cancel_button = tk.Button(button_frame, text="Cancel", command=lambda: (stop_error_sound(), error_window.destroy(), reopen_error()))
        cancel_button.pack(side="right", padx=10)

        # Prevent the window from being closed with the 'X' button
        error_window.protocol("WM_DELETE_WINDOW", lambda: (stop_error_sound(), error_window.destroy(), reopen_error()))

        # Handle minimize button
        error_window.protocol("WM_ICONIFY", lambda: None)

        # Handle key press to close all error windows
        def on_key_press(event):
            if event.keysym == '4':
                root.quit()
                root.destroy()

        root.bind("<KeyPress>", on_key_press)

        # Keep the main loop running until the error_window is closed
        root.wait_window(error_window)

    # Initialize the main Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Start by showing the error message
    reopen_error()

if __name__ == "__main__":
    show_error()



