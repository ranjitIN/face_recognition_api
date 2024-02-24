## Face Recognition Api 

### Face Registeration:
croped face images neded for face registeration 

```python
url = "http://127.0.0.1:8000/registerFace"

payload = {'person': '{"id":"acb6372d-c3d2-42c5-851d-63f48986a80e","name":"balaji"}'}
files=[
  ('image',('ranjit_d5a86429-a08d-11ee-9fbf-10b1df98b0c0.jpg',
  open('/D:/image_database/kws/train/ranjit/ranjit_d5a86429-a08d-11ee-9fbf-10b1df98b0c0.jpg','rb'),'image/jpeg'))
]
headers = {
  'Content-Type': 'multipart/form-data'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)
```
### Face Recognition 
croped face images neded for face recognition 

```python
url = "http://127.0.0.1:8000/recogniseFace"

payload = {}
files=[
  ('image',('balaji_1a1d127d-a08f-11ee-8aae-10b1df98b0c0.jpg',
  open('/D:/image_database/kws/train/balaji/balaji_1a1d127d-a08f-11ee-8aae-10b1df98b0c0.jpg','rb'),'image/jpeg'))
]
headers = {
  'image': ''
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)
```

### uploadImage
upload image of a person. to upload mutiple image, the api need to call mutple times

```python
url = "http://127.0.0.1:8000/uploadImage"

payload = {'personId': 'acb6372d-c3d2-42c5-851d-63f48986a80e'}
files=[
  ('image',('balaji_1a1d127d-a08f-11ee-8aae-10b1df98b0c0.jpg',
  open('/D:/image_database/kws/train/balaji/balaji_1a1d127d-a08f-11ee-8aae-10b1df98b0c0.jpg','rb'),'image/jpeg'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)
```
after uploading mutiple images to complete the training call completeTraining api 

```python
url = "http://127.0.0.1:8000/completeTraining"

payload = json.dumps({
  "personid": "acb6372d-c3d2-42c5-851d-63f48986a80e",
  "uploadedImages": [
    "/media/faces/acb6372d-c3d2-42c5-851d-63f48986a80e/1708750524_balaji_1a1d127d-a08f-11ee-8aae-10b_yxl8EI8.jpg"
  ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
```

### swagger :

```bash
http://127.0.0.1:8000/swagger
```
## - Built With 🛠
- [Facenet](https://en.wikipedia.org/wiki/FaceNet#:~:text=FaceNet%20is%20a%20facial%20recognition,of%20researchers%20affiliated%20to%20Google.) - facenet model to indentify faces.
- [Tensorflow](https://en.wikipedia.org/wiki/FaceNet#:~:text=FaceNet%20is%20a%20facial%20recognition,of%20researchers%20affiliated%20to%20Google.) 
- [opencv](https://opencv.org/) - open computer visiion library
- [sklearn](https://scikit-learn.org/stable/index.html)
