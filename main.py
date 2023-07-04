import sys
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw




def version():
    v = "Mastery Manager - v0.0"
    return v

window = tk.Tk()
# change background
window.configure(bg='blue')
# change cursor
cursor_image = tk.PhotoImage(file="C:/Users/Meg/Documents/VSCode/Python projects/MasterieManager/MasteryManager/images/mastery_0.gif")
window.configure(cursor=cursor_image)
window.title(version())


def display_mastery():
    # Create a list of image file names
    image_files = ["temp/champ1.jpg", "temp/champ2.jpg", "temp/champ3.jpg", "temp/champ4.jpg",
                    "temp/champ5.jpg", "temp/champ6.jpg", "temp/champ7.jpg", "temp/champ8.jpg"]
    
    # Iterate over the image files and create a label for each image
    for i in range(1):
        # Open the image file using the PIL library
        image = Image.open(image_files[i])
        
        # Resize the image to a desired size
        image = image.resize((110, 110))

        """
        # Create a mask with rounded corners
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        radius = 30  # Adjust the radius value as desired
        draw.rounded_rectangle((0, 0, image.width, image.height), radius, fill=255)
        """
        
        
        # Create a Tkinter-compatible image object
        image_tk = ImageTk.PhotoImage(image)
        
        # Create a label to display the image
        label = tk.Label(window, image=image_tk)
        label.grid(row=0, column=i, padx=10, pady=10)
        label.image = image_tk

        # Load the badge image
        badge_image = Image.open("C:/Users/Meg/Documents/VSCode/Python projects/MasterieManager/MasteryManager/images/mastery_7.png")
        
        # Resize the badge image to the desired size
        badge_image = badge_image.resize((30, 30))
        
        # Create a Tkinter-compatible image object for the badge image
        badge_image_tk = ImageTk.PhotoImage(badge_image)
        
        # Create a label for the badge image
        badge_label = tk.Label(window, image=badge_image_tk)

        # Place the badge label on top of the label displaying the first image
        badge_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NW)
        
        # Keep a reference to the badge image object to prevent garbage collection
        badge_label.image = badge_image_tk
        
    
        # Display the second row with 2 images
    for i in range(1, 3):
        image = Image.open(image_files[i])
        image = image.resize((90, 90))
        image_tk = ImageTk.PhotoImage(image)
        label = tk.Label(window, image=image_tk)
        label.grid(row=1, column=i-1, padx=10, pady=10)
        label.image = image_tk
    
    # Display the remaining rows with 4 images each
    for i in range(3, len(image_files)):
        image = Image.open(image_files[i])
        image = image.resize((75, 75))
        image_tk = ImageTk.PhotoImage(image)
        label = tk.Label(window, image=image_tk)
        label.grid(row=(i-3) // 4 + 2, column=(i-3) % 4, padx=10, pady=10)
        label.image = image_tk

display_mastery()

window.mainloop()

