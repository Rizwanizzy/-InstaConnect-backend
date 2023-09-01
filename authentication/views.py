from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from .serializers import CustomTokenCreateSerializer
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from djoser.views import TokenCreateView

# Create your views here.


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomTokenCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/login"  # <--- make sure this line is correct!
    client_class = OAuth2Client


class AdminTokenCreateView(TokenCreateView):
    def create(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.user
        print("before checking superuser")
        # Check if the user is a superuser
        if user.is_superuser:
            print("superuser is true")
            # Generate the token
            token, created = self.token_model.objects.get_or_create(user=user)
            if not created:
                # Update the created time of the token to keep it valid
                self.token_model.objects.filter(user=user).update(created=self.token_model.current_time)
            
            # Return the token
            return Response({'token': token.key})

        # If the user is not a superuser, return an error response
        return Response({"detail": "Superuser login required."}, status=status.HTTP_400_BAD_REQUEST)