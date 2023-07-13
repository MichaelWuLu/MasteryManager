import os
from PIL import Image


# Scale images to chosen size
def scale_images():
    # find image path
    for file in os.listdir('MasterieManager/MasteryManager/images'):
        # select images to scale
        if file.endswith('settings_icon.png'):
            # open image
            image = Image.open(f'MasterieManager/MasteryManager/images/{file}')
            # resize image (values in pixels)
            image = image.resize((25, 25))
            # save image
            image.save(f'MasterieManager/MasteryManager/images/{file}')


if __name__ == "__main__":
    scale_images()
