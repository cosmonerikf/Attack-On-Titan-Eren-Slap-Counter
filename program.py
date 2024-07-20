import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pygame
import os

class HitCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AOT Hit Counter")
        self.root.geometry("800x600")  # Set window size to larger dimensions
        self.root.resizable(True, True)  # Allow resizing

        # Set the application icon
        self.root.iconbitmap(r"C:\Users\cosmo\Downloads\Source\program.ico")

        # Initialize the mixer module in pygame
        pygame.mixer.init()

        # File to store the counter values
        self.counter_file = 'counter.txt'
        self.count, self.total_episodes = self.load_counter_data()

        # Load the background image
        self.original_image = Image.open(r"C:\Users\cosmo\Downloads\wp1837539.jpg")
        self.bg_image = ImageTk.PhotoImage(self.original_image.resize((800, 600), Image.LANCZOS))
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Load the custom font
        self.custom_font = "Blood Crow Condensed"  # Change this to your desired font

        # Define styles
        self.define_styles()

        # Create and place widgets
        self.create_widgets()
        self.update_average()
        self.resize_widgets(False)

        # Bind the configure event to handle window resizing
        self.root.bind('<Configure>', self.resize_image)

        # Force a redraw of the window to ensure the background image appears correctly
        self.root.update()
        self.resize_image()

    def load_counter_data(self):
        if os.path.exists(self.counter_file):
            with open(self.counter_file, 'r') as file:
                content = file.read().strip()
                if content:
                    try:
                        return map(int, content.split())
                    except ValueError:
                        pass
        return 0, 1  # Default to 0 count and 1 episode if parsing fails or file does not exist

    def save_counter_data(self):
        with open(self.counter_file, 'w') as file:
            file.write(f'{self.count} {self.total_episodes}')

    def play_sound(self):
        if self.sound_enabled.get():
            pygame.mixer.music.load(r"C:\Users\cosmo\Downloads\youtube_4Gk_ROalMXQ_audio.mp3")
            pygame.mixer.music.play(loops=0)

    def clicked_increment(self):
        self.count += 1
        self.update_ui()

    def clicked_decrement(self):
        if self.count > 0:
            self.count -= 1
            self.update_ui()
        else:
            messagebox.showwarning("Warning", "Hit count cannot be negative.")

    def reset_counter(self):
        self.count = 0
        self.update_ui()

    def update_ui(self):
        self.label1.config(text=f'{self.count} times')
        self.play_sound()
        self.save_counter_data()
        self.update_average()

    def update_episodes(self):
        try:
            new_episodes = int(self.episode_entry.get())
            if new_episodes > 0:
                self.total_episodes = new_episodes
                self.save_counter_data()
                self.update_average()
            else:
                messagebox.showerror("Invalid input", "Episode number must be positive.")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")

    def update_average(self):
        if self.total_episodes > 0:
            average_hits = self.count / self.total_episodes
            self.avg_label.config(text=f'Average hits per episode: {average_hits:.2f}')

    def resize_image(self, event=None):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        new_bg_image = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=new_bg_image)
        self.bg_label.image = new_bg_image  # Keep a reference to avoid garbage collection

    def toggle_fullscreen(self):
        is_fullscreen = not self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', is_fullscreen)
        self.resize_image()
        self.resize_widgets(is_fullscreen)

    def resize_widgets(self, is_fullscreen):
        font_size = 32 if is_fullscreen else 24
        self.label.config(font=(self.custom_font, font_size))
        self.label1.config(font=(self.custom_font, font_size * 2))
        self.episode_label.config(font=(self.custom_font, font_size))
        self.episode_entry.config(font=(self.custom_font, font_size))
        self.avg_label.config(font=(self.custom_font, font_size))
        
        button_style = "Fullscreen.TButton" if is_fullscreen else "Custom.TButton"
        self.update_button.config(style=button_style)
        self.increment_button.config(style=button_style)
        self.decrement_button.config(style=button_style)
        self.reset_button.config(style=button_style)
        self.sound_toggle.config(style=button_style)
        self.fullscreen_button.config(style=button_style)

    def toggle_sound(self):
        current_state = self.sound_enabled.get()
        self.sound_enabled.set(not current_state)
        self.update_sound_button()

    def update_sound_button(self):
        if self.sound_enabled.get():
            self.sound_toggle.config(text="Sound Enabled", style="Enabled.TButton")
        else:
            self.sound_toggle.config(text="Sound Disabled", style="Disabled.TButton")

    def define_styles(self):
        style = ttk.Style()
        style.configure("Custom.TButton", font=(self.custom_font, 16))
        style.configure("Custom.TCheckbutton", font=(self.custom_font, 16))
        style.configure("Fullscreen.TButton", font=(self.custom_font, 32))
        style.configure("Fullscreen.TCheckbutton", font=(self.custom_font, 32))
        
        # Define additional styles for enabled/disabled sound button
        style.configure("Enabled.TButton", font=(self.custom_font, 16), background="lightgreen", foreground="black")
        style.configure("Disabled.TButton", font=(self.custom_font, 16), background="lightcoral", foreground="black")

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Eren Hit Counter", font=(self.custom_font, 24), bg='white', fg='black')
        self.label.grid(column=0, row=0, padx=10, pady=10, columnspan=3)

        self.count_frame = tk.Frame(self.root, borderwidth=2, relief="groove", bg='white')
        self.count_frame.grid(column=0, row=1, padx=10, pady=10, columnspan=3)

        self.label1 = tk.Label(self.count_frame, text=f'{self.count} times', font=(self.custom_font, 32), bg='white', fg='black')
        self.label1.pack(padx=20, pady=20)

        self.episode_label = tk.Label(self.root, text="Enter total episodes:", font=(self.custom_font, 16), bg='white', fg='black')
        self.episode_label.grid(column=0, row=2, padx=10, pady=10)

        self.episode_entry = tk.Entry(self.root, font=(self.custom_font, 16))
        self.episode_entry.grid(column=1, row=2, padx=10, pady=10)
        self.episode_entry.insert(0, str(self.total_episodes))

        self.update_button = ttk.Button(self.root, text="Update Episodes", command=self.update_episodes, style="Custom.TButton")
        self.update_button.grid(column=2, row=2, padx=10, pady=10)

        self.increment_button = ttk.Button(self.root, text="+", command=self.clicked_increment, style="Custom.TButton", width=5)
        self.increment_button.grid(column=2, row=3, padx=10, pady=10)

        self.decrement_button = ttk.Button(self.root, text="-", command=self.clicked_decrement, style="Custom.TButton", width=5)
        self.decrement_button.grid(column=0, row=3, padx=10, pady=10)

        self.reset_button = ttk.Button(self.root, text="Reset Counter", command=self.reset_counter, style="Custom.TButton")
        self.reset_button.grid(column=1, row=3, padx=10, pady=10)

        self.sound_enabled = tk.BooleanVar(value=True)
        self.sound_toggle = ttk.Button(self.root, text="Sound Enabled", command=self.toggle_sound, style="Enabled.TButton")
        self.sound_toggle.grid(column=1, row=4, padx=10, pady=10)

        self.avg_label = tk.Label(self.root, text='Average hits per episode: 0.00', font=(self.custom_font, 16), bg='white', fg='black')
        self.avg_label.grid(column=0, row=5, padx=10, pady=10, columnspan=3)

        self.fullscreen_button = ttk.Button(self.root, text="Toggle Fullscreen", command=self.toggle_fullscreen, style="Custom.TButton")
        self.fullscreen_button.grid(column=1, row=6, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = HitCounterApp(root)
    root.mainloop()
    