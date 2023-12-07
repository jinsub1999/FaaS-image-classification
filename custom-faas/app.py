from flask import Flask, jsonify, request
import io
import json
import torchvision.transforms as transforms
from PIL import Image

app = Flask(__name__)

import timm
import torch
from torch import nn, load

num_classes = 400

device = torch.device('cpu')
model = load(f"/home/app/model.pt", map_location=device)

model.eval()

image_class = {}

with open("./classes.json") as f:
    image_class = json.load(f)

def transform_image(image_bytes):
    my_transforms = transforms.Compose([
                                    transforms.Resize(256),
                                    transforms.CenterCrop(224),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    return y_hat

@app.route('/', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_id = get_prediction(image_bytes=img_bytes)
        class_idx = class_id.item()

        return jsonify({'class_id': f"{class_idx}", 'class_name': image_class[f"{class_idx}"]})
