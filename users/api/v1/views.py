from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


class CheckUserExistByEmailAPIView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        email = request.data.get('email', None)
        if not email:
            return Response({
                'detail': 'Email is required.'
            }, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            return Response({
                'detail': 'Email already exists.'
            }, status=400)

        return Response({
                'detail': 'No user found with this email.'
            }, status=200)
