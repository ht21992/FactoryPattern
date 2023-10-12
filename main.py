import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
from FactoryPattern.Character import CharacterFactory
from FactoryPattern.Characteristic import CharacteristicFactory
from FactoryPattern.Stat import StatFactory


class CharacterCreationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Creation")

        # Create 3 columns
        self.left_frame = ttk.Frame(root, padding=20)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.center_frame = ttk.Frame(root, padding=20)
        self.center_frame.grid(row=0, column=1, padx=10, pady=10)

        self.right_frame = ttk.Frame(root, padding=20)
        self.right_frame.grid(row=0, column=2, padx=10, pady=10)

        # Character Name Entry
        self.name_label = ttk.Label(
            self.left_frame, text="Enter your character's name:"
        )
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.left_frame)
        self.name_entry.grid(row=1, column=0, padx=5, pady=5)

        # Character Class Dropdown
        self.class_label = ttk.Label(self.left_frame, text="Choose a class:")
        self.class_label.grid(row=2, column=0, padx=5, pady=5)
        self.class_var = tk.StringVar()
        self.class_var.set("Warrior")  # Default class
        self.class_dropdown = ttk.Combobox(
            self.left_frame,
            state="readonly",
            textvariable=self.class_var,
            values=["Warrior", "Mage", "Thief"],
        )
        self.class_dropdown.grid(row=3, column=0, padx=5, pady=5)

        # Create Character Button
        self.create_button = ttk.Button(
            self.left_frame, text="Create Character", command=self.create_character
        )
        self.create_button.grid(row=4, column=0, padx=5, pady=10)

        # Character Characteristics Display
        self.characteristics_label = ttk.Label(
            self.center_frame, text="Characteristics:"
        )
        self.characteristics_label.grid(row=0, column=0, padx=5, pady=5)
        self.characteristics_text = tk.Text(self.center_frame, height=4, width=40)
        self.characteristics_text.grid(row=1, column=0, padx=5, pady=5)

        # Character Stats Display
        self.stats_label = ttk.Label(self.center_frame, text="Stats:")
        self.stats_label.grid(row=2, column=0, padx=5, pady=5)
        self.stats_text = tk.Text(self.center_frame, height=8, width=40)
        self.stats_text.grid(row=3, column=0, padx=5, pady=5)

        # Create a dictionary to store character widgets
        self.character_gif_labels = {"Warrior": None, "Mage": None, "Thief": None}

    def create_character(self):
        player_name = self.name_entry.get() or "Player"
        class_choice = self.class_var.get() or "Mage"

        character = CharacterFactory.create_character(class_choice, player_name)

        if character:
            self.characteristics_text.delete(1.0, tk.END)
            self.stats_text.delete(1.0, tk.END)

            characteristics = CharacteristicFactory.create_characteristics(
                class_choice, player_name
            )
            stats = StatFactory.create_stats(class_choice)

            self.characteristics_text.insert(
                tk.END, "\n".join(char.describe() for char in characteristics)
            )
            self.stats_text.insert(
                tk.END, "\n".join(f"{stat.name}: {stat.value}" for stat in stats)
            )

            # Display the corresponding character GIF image
            self.display_character_gif(class_choice)
        else:
            print("Invalid class choice.")

    def display_character_gif(self, class_choice):
        # Hide the previous character's GIF label if it exists
        if self.character_gif_labels[class_choice]:
            self.character_gif_labels[class_choice].grid_forget()

        # Load and display the new GIF image based on the class
        if class_choice == "Warrior":
            gif_path = "warrior.gif"  # Replace with the path to the Warrior GIF
        elif class_choice == "Mage":
            gif_path = "mage.gif"  # Replace with the path to the Mage GIF
        elif class_choice == "Thief":
            gif_path = "thief.gif"  # Replace with the path to the Thief GIF
        else:
            return  # No GIF for the default class

        try:
            # Read the GIF
            gif = Image.open(os.path.join("Images", gif_path))
            gif_frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]

            # Resize each frame to a common size (e.g., 300x300)
            resized_frames = [frame.resize((300, 300)) for frame in gif_frames]

            # Create a list of PhotoImage objects
            photo_frames = [ImageTk.PhotoImage(frame) for frame in resized_frames]

            # Create a Label for displaying the GIF
            gif_label = ttk.Label(self.right_frame, image=photo_frames[0])
            gif_label.grid(row=0, column=0, padx=10, pady=10)

            # Store the Label in the dictionary
            self.character_gif_labels[class_choice] = gif_label

            # Schedule the animation
            self.animate_gif(photo_frames, gif_label, 0)
        except Exception as e:
            print(f"Error loading or displaying GIF: {e}")

    def animate_gif(self, gif_frames, gif_label, frame_num):
        if frame_num >= len(gif_frames):
            frame_num = 0

        # Display the frame
        gif_label.configure(image=gif_frames[frame_num])

        # Schedule the next frame
        self.root.after(100, self.animate_gif, gif_frames, gif_label, frame_num + 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterCreationApp(root)
    root.mainloop()
