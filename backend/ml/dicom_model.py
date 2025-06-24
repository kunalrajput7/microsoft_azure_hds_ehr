import os
import torch
import torchvision.transforms as transforms
import pydicom
import numpy as np
from torchvision.models import resnet18


model_path = os.path.join("train", "models", "dicom_model.pth")

# Load model
model = resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, 1)
model.load_state_dict(torch.load(model_path, map_location='cpu'))
model.eval()

# Preprocess function
def preprocess_dicom(dicom_file):
    dcm = pydicom.dcmread(dicom_file)
    image = dcm.pixel_array.astype(np.float32)
    image = (image - np.min(image)) / (np.max(image) - np.min(image))
    image = np.stack([image]*3, axis=-1)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((224, 224))
    ])
    return transform(image).unsqueeze(0)

# Inference function
def predict_pneumonia(dicom_path: str):
    img_tensor = preprocess_dicom(dicom_path)
    with torch.no_grad():
        output = model(img_tensor)
        prob = torch.sigmoid(output).item()
    return {
        "prediction": "Pneumonia" if prob >= 0.5 else "Normal",
        "confidence": round(prob, 3)
    }
