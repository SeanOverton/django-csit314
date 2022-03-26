from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.contrib.auth.models import User
from .models import CustomUser as User
from .models import RoadsideCallout
from .serializers import RegisterSerializer, CalloutSerializer, UserSubscriptionsSerializer
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import mixins
from django.http import JsonResponse

class HelloView(APIView):
    #this indicates auth token is required
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class CreateRoadsideCalloutView(generics.CreateAPIView, 
                ):
    permission_classes = (IsAuthenticated,)
    serializer_class = CalloutSerializer

class UpdateRoadsideCalloutView(generics.CreateAPIView):
    queryset = RoadsideCallout.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CalloutSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        date = request.data['date']

        callout = RoadsideCallout.objects.get(username=username, date=date)

        updated_callout = CalloutSerializer(callout, request.data)

        status=""

        if updated_callout.is_valid():
            updated_callout.update(callout, updated_callout)
            status = 'OK'
        else:
            # TODO: definitely could do with some better info here
            status = 'INVALID'
        
        return Response({
            "status": status
        })

class AllRoadsideCalloutsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = list(RoadsideCallout.objects.values())

        try:
            #TODO: should be able to come up with a more generic filter here?
            if(request.GET.get('status', '') != ''):
                queryset = list(RoadsideCallout.objects.filter(status=request.GET['status']).values())
            if(request.GET.get('mechanic', '') != ''):
                queryset = list(RoadsideCallout.objects.filter(mechanic=request.GET['mechanic']).values())
        except KeyError:
            pass

        return JsonResponse(queryset, safe=False)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'user_type': user.user_type
        })

class UpdateSubscriptionsView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSubscriptionsSerializer