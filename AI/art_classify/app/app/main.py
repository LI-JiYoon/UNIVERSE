import torch
from torchvision import transforms
from fastapi import FastAPI, UploadFile
import cv2
import numpy as np

device =  torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = torch.load('./model/artstyle_classify_model.pth', map_location=device)
model.to(device)
model.eval()

artstyles = {0: '디지털페인팅', 1: '소묘', 2: '수채화', 3: '유화',  4: '펜화'}
transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

app = FastAPI()

@app.post("/uploadimg/")
async def create_upload_file(file: UploadFile):
    file_buf = await file.read()
    print("file_buf done")

    encoded_img = np.fromstring(file_buf, dtype = np.uint8)
    print("encoded_img done")
    image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    print("img decode done")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print("img bgr2rgb done")

    #raw_image = Image.open('/content/drive/MyDrive/test/소묘/pencil_drawing-104-_jpg.rf.bbb135bcabb48c2f2ca753a7aa28605e.jpg')
    image = transform(image).unsqueeze(0)
    print("img transform done")

    with torch.no_grad():
        outputs = model(image)
        print("ouputs done")
        output = outputs.argmax()
        print("ouput done")
        predicted = artstyles[output.item()]
        
        return {"category" : predicted}
        