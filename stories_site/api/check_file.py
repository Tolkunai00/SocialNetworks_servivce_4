from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
import io
import uvicorn
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),
    transforms.Resize((32, 32)),
    transforms.ToTensor()
])


class CifarClassifaction(nn.Module):
    def __init__(self):
        super().__init__()
        self.first = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.second = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Linear(256, 10)
        )

    def forward(self, image):
        image = self.first(image)
        image = self.second(image)
        return image


cifar_app = APIRouter()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model =CifarClassifaction()
model.load_state_dict(torch.load('stories_site/nn_model/cifar_model (3).pth', map_location=device))
model.to(device)
model.eval()


classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

@cifar_app.post('/predict')
async def cifar_image(image: UploadFile = File(...)):
    try:
        image_data = await image.read()

        if not image_data:
            raise HTTPException(status_code=400, detail='Файл табылган жок')

        img = Image.open(io.BytesIO(image_data)).convert('RGB')
        img_tensor = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            y_pred =model(img_tensor)
            pred = y_pred.argmax(dim=1).item()

        prediction = classes[pred]

        return {'predict': prediction,
                'detail': 'Мындай суротту жуктоого болбойт'}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


