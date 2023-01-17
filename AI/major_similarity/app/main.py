import numpy as np
import platform
import uuid
import json
import time
import cv2
import requests
#from typing import Union
from fastapi import FastAPI, UploadFile, Form
import cv2
#import easyocr
import numpy as np
import time
from major_category import *
from major_cosin import *


api_url = 'https://ygwcxs5g56.apigw.ntruss.com/custom/v1/19333/5b21c65940d46e657afa89af4da151b182c35574f333cebaa42952f969fb6f15/general'
secret_key = 'WlFNcE1oaHVPS3VVWnFsZ3V6eGlybENiT3pCZk1LRXM='
path = './data/id_Card_'
#창 닫아도 서버 계속 실행   nohup uvicorn myapp:app &
#sys.path.append('.')

#reader = easyocr.Reader(['ko'], gpu=False)




#def id_ocr(result):
#    result = reader.readtext(img, detail=0)
#    for x in result:
#      if ('대학' in  x) | ('학과' in  x):
#        major = x
#        break
    
#    return major
   
#################################################################################

app = FastAPI()

@app.get("/")
def start():
  return { "hello" : "000000000000000000000000000000000000"}

@app.post("/uploadIDCardImage/")
async def create_upload_file(file: UploadFile):
    now =time.time()
    file_buf = await file.read()
    
    encoded_img = np.fromstring(file_buf, dtype = np.uint8)
    image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  

    img_path = path + str(now) + '.jpg'
    cv2.imwrite(img_path, image)
    files = [('file', open(img_path,'rb'))] 

    request_json = {'images': [{'format': 'jpg',
                                'name': 'demo'
                               }],
                    'requestId': str(uuid.uuid4()),
                    'version': 'V2',
                    'timestamp': int(round(time.time() * 1000))
                   }
                   
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    
    headers = {'X-OCR-SECRET': secret_key,}
    
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    
    result = response.json()
    
    
    major = str()
  
    for field in result['images'][0]['fields']:
     if ('대학' in  field['inferText']) | ('학과' in  field['inferText']):
       major = field['inferText']
       break

    major_list = get_recommendations(major)
    result = category(major_list)
    

    return {"major": result}


    

