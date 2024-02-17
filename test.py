from face_recognition.faceAI import faceAiService
import numpy as np

faceEmbedingsPath = "face_recognition/faceAI/dataset/faces_embedings.npz" 

faceEmbdings_dataset = np.load(faceEmbedingsPath, allow_pickle=True)
facesEmbdings, labels = faceEmbdings_dataset['embds'],faceEmbdings_dataset['labels']

data = np.load("D:/workspace/face_recognition_facenet/Indian-celeb-embeddings.npz",allow_pickle=True)

embed_trainx, embed_trainy = data['arr_0'],data['arr_1']

print(labels)

print(embed_trainy)