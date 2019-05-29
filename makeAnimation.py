import os
import imageio

dir_path = os.path.dirname(os.path.realpath(__file__))
with imageio.get_writer(dir_path+'/warpAnimation.mp4', mode='I') as writer:
    for filename in sorted(os.listdir(dir_path+"/Frames/"),key=lambda f: int(''.join(filter(str.isdigit, f)) or -1)):
        if filename.endswith(".png"):
            print(filename)
            image = imageio.imread(dir_path+"/Frames/"+filename)
            writer.append_data(image)
