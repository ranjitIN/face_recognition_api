import os 
import cv2
from numpy import savez_compressed
from numpy import asarray
import numpy as np
from keras_facenet import FaceNet
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
import joblib
from numpy import asarray


faceEmbedingsPath = "face_recognition/faceAI/dataset/faces_embedings.npz" 
faceDatasetPath = "face_recognition/faceAI/dataset/faces.npz"
svc_model_path = "face_recognition/faceAI/dataset/model.pkl"

# register a face
def reigister_Face(personId,imagePath:str):
  try:
    print("register face")
    # Get the base directory of your Django project
    imagePath = imagePath.replace("/media/","")
    print(imagePath)
    imagePath = os.path.join(settings.MEDIA_ROOT, imagePath)
    face = load_image(imagePath)
    if os.path.exists(faceDatasetPath):
        # append image in dataset 
        append_in_dataset(personId,face)
        # find face embedings 
        print("extractFaceEmbdings")
        faceEmbdings, labels = extractFaceEmbdings(personId,face)
        train_model(face_embd=faceEmbdings,labels=labels)
    else:
        faces = np.array([face])
        labels = np.array([personId])
        saveFacesInNpz(faces=faces,labels=labels)
        faceEmbdings, labels = extractFaceEmbdings(personId,face)
        train_model(face_embd=faceEmbdings,labels=labels)
  except Exception as e:
    raise e

def append_in_dataset(personId,face):
  facedataset = np.load(faceDatasetPath, allow_pickle=True)
  labels = facedataset['labels']
  faces = facedataset['faces']
  faces = np.concatenate((faces, [face]))
  labels = np.concatenate((labels, [personId]))
  saveFacesInNpz(labels=labels,faces=faces)

def extractFaceEmbdings(personId,face):
  print("extract face")
  embedder = FaceNet()
  face_embd = embedder.embeddings([face])
  face_embd = asarray(face_embd)
  if os.path.exists(faceEmbedingsPath):
    faceEmbdings_dataset = np.load(faceEmbedingsPath, allow_pickle=True)
    facesEmbdings, labels = faceEmbdings_dataset['embds'],faceEmbdings_dataset['labels']
    facesEmbdings = np.concatenate((facesEmbdings,face_embd))
    labels = np.concatenate((labels,[personId]))
    print("save face embdigs")
    saveFaceEmbedingsInnpz(labels,facesEmbdings)
    return facesEmbdings, labels
  else:
    facesEmbdings = np.array(face_embd)
    labels = np.array([personId])
    saveFaceEmbedingsInnpz(labels,facesEmbdings)
    return facesEmbdings,labels

# predict face

# load dataset 
def load_dataset(directory:str):
  x, y = [],[]
  i=1
  print("dataset")
  for subdir in os.listdir(directory):
    print(subdir)
    path = os.path.join(directory,subdir)
    #load all faces in subdirectory
    faces = load_all_Images(path)
    labels = [subdir for _ in range(len(faces))]
    x.extend(faces)
    y.extend(labels)
    i=i+1
  return asarray(x),asarray(y) 

def saveFacesInNpz(labels,faces):
  savez_compressed(faceDatasetPath,faces=faces,labels=labels)

def saveFaceEmbedingsInnpz(labels,facesEmbdings):
  savez_compressed(faceEmbedingsPath,embds=facesEmbdings,labels=labels)

   

def load_image(path:str):
   return cv2.imread(path)
    
def load_all_Images(directory):
   images = []
   imageFiles = os.listdir(directory)
   for filename in imageFiles:
    image_path = os.path.join(directory, filename)
    img = cv2.imread(image_path)
    images.append(img)
   return images

def train_model(face_embd,labels):
  in_encode = Normalizer(norm='l2')
  faces = in_encode.transform(face_embd)
  out_encode = LabelEncoder()
  out_encode.fit(labels)
  labels = out_encode.transform(labels)
  #define svm classifier model 
  model=SVC(kernel='linear', probability=True)
  model.fit(faces,labels)
  joblib.dump(value=model,filename=svc_model_path)

def recognise_face(image):
  image = np.array(image)
  embedder = FaceNet()
  faceEmbdings_dataset = np.load(faceEmbedingsPath, allow_pickle=True)
  labels = faceEmbdings_dataset['labels']
  face_embd = embedder.embeddings([image])
  face_embd = asarray(face_embd)
  model = joblib.load(svc_model_path)
  out_encode = LabelEncoder()
  out_encode.fit(labels)
  result = model.predict(face_embd)
  score = model.decision_function(face_embd)
  if abs(score) > 0.4:
    class_index = result[0]
    print(class_index)
    predict_name = out_encode.inverse_transform(result)
    return predict_name[0]
  else:
    return "unknown"


