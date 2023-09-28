import os
from PIL import Image


# Scale images to chosen size
def scale_images():
    # find image path
    for file in os.listdir('images'):
        # select images to scale
        if file.endswith('settings_icon.png'):
            # open image
            image = Image.open(f'images/{file}')
            # resize image (values in pixels)
            image = image.resize((25, 25))
            # save image
            image.save(f'images/{file}')


def assemble_image(championId:int, masteryLevel:int):
    for file in os.listdir('temp/champions'):
        if not file.startswith(f'champ'):
            continue
        if not file.endswith(f'{championId}.jpg'):
            continue
        
        # open champion image
        champ_img = Image.open(f'temp/champions/{file}')
        new_img = Image.new('RGBA', champ_img.size, (0, 0, 0, 0))
        
        # open mastery level image
        lvl_img = Image.open(f'images/mastery_{masteryLevel}.png')
        lvl_img = lvl_img.convert('RGBA')

        # add together
        new_img.paste(champ_img, (0, 0))
        new_img.paste(lvl_img, (0, 0), lvl_img)
        
        # save image
        new_img.convert('RGB').save(f'temp/champions/assembled_{file}', 'JPEG')
