from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import torch
from torchvision import transforms, models
# Create your views here.

#Loads the pre-trained model
model = models.resnet50(pretrained=True)
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
        image = Image.open(io.BytesIO(request.FILES['image'].read()))

        #Preprocess the image
        image = transform(image).unsqueeze(0)

        #Make the prediction
        with torch.no_grad():
            outputs = model(image)

        #Get the predicted class
        _, predicted = torch.max(outputs.data, 1)

        #Convert the predicted class index to the corresponding label
        predicted_label = index_to_label(predicted.item())

        return JsonResponse({ 'label': predicted_label })