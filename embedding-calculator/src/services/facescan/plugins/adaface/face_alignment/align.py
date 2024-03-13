from src.services.facescan.plugins.adaface.face_alignment  import mtcnn
from src.services.facescan.plugins.pytorch_detector.detect import retina_detector
import src.services.facescan.plugins.adaface.inference as inference
import argparse
from PIL import Image
from tqdm import tqdm
import random
from datetime import datetime
from src.constants import ENV

device = ENV.DEVICE
detector_name = ENV.DETECTOR_NAME

#mtcnn_model = mtcnn.MTCNN(device='cuda:0', crop_size=(112, 112))
mtcnn_model = mtcnn.MTCNN(device=device, crop_size=(112, 112))

def add_padding(pil_img, top, right, bottom, left, color=(0,0,0)):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def get_aligned_face(image_path, rgb_pil_image=None):
    if rgb_pil_image is None:
        img = Image.open(image_path).convert('RGB')
    else:
        assert isinstance(rgb_pil_image, Image.Image), 'Face alignment module requires PIL image or path to the image'
        img = rgb_pil_image
    # find face
    try:
        if detector_name == 'mtcnn':
            bboxes, faces = mtcnn_model.align_multi(img)
        elif "retinaface" in detector_name:
            content_type = image_path.content_type.split('/')[-1]
            bboxes, faces = retina_detector(img, content_type)
    except Exception as e:
        print('Face detection Failed due to error.')
        print(e)
        faces = None
        bboxes = None

    return faces, bboxes


