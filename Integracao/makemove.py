import cv2
import os

name = '2018-11-01 15:57:16'
image_folder = '../../Resultados/'+name
video_name = 'Log/' + name + '.avi'

images=[]
for cont in range(1, 567):
    for img in os.listdir(image_folder):
        if img.endswith(str(cont)+"_final.jpg"):
            images.append(img)
            
#images = [img for img in os.listdir(image_folder) if img.endswith("final.jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), 30, (width,height)) 

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()