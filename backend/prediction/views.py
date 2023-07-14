from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import torch
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights
import json
import base64
# Create your views here.

#Loads the pre-trained model
weights = ResNet50_Weights.IMAGENET1K_V2
model = resnet50(weights=weights)
model.eval()

#Define the transformation

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        #Load image from the request
        data = json.loads(request.body)
        image_data = data.get('image')

        header, image_data = image_data.split(';base64,')
        image_data = base64.b64decode(image_data)

        #open the base64 data as an image
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        #Preprocess the image
        img_tensor = transform(image).unsqueeze(0)

        #Make the prediction
        with torch.no_grad():
            prediction = model(img_tensor).squeeze(0).softmax(0)

        #Get the predicted class
        class_id = prediction.argmax().item()
        score = prediction[class_id].item()
        predicted_label = weights.meta["categories"][class_id]

        return JsonResponse({ 'label': predicted_label, 'confidence': str(score) })