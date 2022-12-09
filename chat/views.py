from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MessageSerializer
from .models import Message

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def class_chat(request, class_name):
    return render(request, 'chat/class.html', {
        'class_name': class_name
    })

class MessageAPI(APIView):
    def get(self, request):
        queryset = Message.objects.all()
        print(queryset)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)