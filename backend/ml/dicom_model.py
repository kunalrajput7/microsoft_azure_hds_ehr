import os
import torch
import torchvision.transforms as transforms
import pydicom
import numpy as np
from torchvision.models import resnet18
import base64
from io import BytesIO
from PIL import Image


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
    # Load and preprocess for prediction
    dcm = pydicom.dcmread(dicom_path)
    image_array = dcm.pixel_array.astype(np.float32)
    image_norm = (image_array - np.min(image_array)) / (np.max(image_array) - np.min(image_array))
    image_rgb = np.stack([image_norm] * 3, axis=-1)

    # For prediction
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((224, 224))
    ])
    img_tensor = transform(image_rgb).unsqueeze(0)

    # Inference
    with torch.no_grad():
        output = model(img_tensor)
        prob = torch.sigmoid(output).item()
        prediction = "Pneumonia" if prob >= 0.5 else "Normal"

    # --- Extract metadata ---
    metadata = {
        "PatientID": getattr(dcm, "PatientID", "Unknown"),
        "Modality": getattr(dcm, "Modality", "Unknown"),
        "StudyDate": getattr(dcm, "StudyDate", "Unknown"),
        "BodyPartExamined": getattr(dcm, "BodyPartExamined", "Unknown"),
        "Rows": getattr(dcm, "Rows", "Unknown"),
        "Columns": getattr(dcm, "Columns", "Unknown"),
    }

    # --- Convert image to base64 ---
    image_uint8 = (image_rgb * 255).astype(np.uint8)
    pil_img = Image.fromarray(image_uint8)
    buffered = BytesIO()
    pil_img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    return {
        "prediction": prediction,
        "confidence": round(prob, 3),
        "metadata": metadata,
        "image_base64": img_b64
    }