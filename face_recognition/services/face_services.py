from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from ..models import Person,PersonFaceImage
from ..serializers import PersonSerialzers,PersonFaceImageSerialzer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from face_recognition.faceAI import faceAiService
from PIL import Image
import json

@api_view(['POST'])
def register_Face(request:Request,format = None):
    try:
        if request.method == "POST":
            persondata  = json.loads(request.data.get("person"))
            personSerializer = PersonSerialzers(data=persondata)
            if personSerializer.is_valid(): 
                personSerializer.save()
                imageData = {
                    "person":persondata['id'],
                    "image":request.FILES.get('image')
                }
                personImageSerializer = PersonFaceImageSerialzer(data= imageData)
                if personImageSerializer.is_valid():
                    personImageSerializer.save()
                    faceAiService.reigister_Face(personSerializer.data.get("id"),personImageSerializer.data.get("image"))
                    resultdata = {
                        "id":personSerializer.data.get("id"),
                        "name":personSerializer.data.get("name"),
                        "image":personImageSerializer.data.get("image")
                    }
                    return Response(data={"person":resultdata},status=status.HTTP_201_CREATED)
                else:
                    return Response(data={"error1":personImageSerializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data={"error2":personSerializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(data={"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def recognise_face(request:Request,format = None):
    try:
        if(request.method == "POST"):
           image =  request.FILES.get('image')
           image = Image.open(image)
           result = faceAiService.recognise_face(image)
           if result == "unknown":
               return Response(data={"status":"unknown"},status=status.HTTP_200_OK)
           else:
               person = Person.objects.get(id = result)
               personSerializer = PersonSerialzers(person)
               return Response(data={"status":personSerializer.data},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(data={"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
