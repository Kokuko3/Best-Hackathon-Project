import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

# Define the same transformations as during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load the trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=True)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 3)  # Match your training setup

# Load trained weights
model.load_state_dict(torch.load("final_model.pth", map_location=device))  # Change "final_model.pth" if needed
model = model.to(device)
model.eval()


def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")  # Ensure it's 3-channel RGB
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension
    return image.to(device)


def predict(image_path, model, class_names):
    image = preprocess_image(image_path)

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
    
    predicted_class = class_names[predicted.item()]
    return predicted_class

# Example usage
class_names = ["Happy", "Hungry", "Scared"]  # Replace with your actual class names
image_path = "spectrogramOutputs/test/B/B_BAC01_MC_MN_SIM01_103.png"  # Path to the spectrogram image
prediction = predict(image_path, model, class_names)

print(f"Predicted class: {prediction}")