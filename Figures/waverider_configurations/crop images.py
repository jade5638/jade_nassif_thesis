from PIL import Image
import os

os.chdir('C:\\Users\\USER\\OneDrive - Cranfield University\\IRP\\Figures\\waverider_configurations\\images\\raw')
# Load the image
last_image=9
for i in range(last_image):
    
    index=i+1

    # crop top view 
    top_view_image_path = f'waverider_{index}_top_view.png'
    top_view_image = Image.open(top_view_image_path)
    crop_box_top_view = (30, 80, 1080-30,920 )
    cropped_image_top_view = top_view_image.crop(crop_box_top_view)
    path = f'../cropped//waverider_{index}_top_view.png'
    cropped_image_top_view.save(path)

    # crop side view 
    side_view_image_path = f'waverider_{index}_side_view.png'
    side_view_image = Image.open(side_view_image_path)
    crop_box_side_view = (30, 440, 1080-50,720 )
    cropped_image_side_view = side_view_image.crop(crop_box_side_view)
    path = f'../cropped//waverider_{index}_side_view.png'
    cropped_image_side_view.save(path)

    # crop back view 
    back_view_image_path = f'waverider_{index}_back_view.png'
    back_view_image = Image.open(back_view_image_path)
    crop_box_back_view = (30, 440, 1080-30,700 )
    cropped_image_back_view = back_view_image.crop(crop_box_back_view)
    path = f'../cropped//waverider_{index}_back_view.png'
    cropped_image_back_view.save(path)