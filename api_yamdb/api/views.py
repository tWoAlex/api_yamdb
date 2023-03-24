from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status, viewsets, filters, permissions

from reviews.models import User

from .serializers import RegistrationSerializer, TokenAproveSerializer, \
    UserSerializer
from .permissions import IsAdmin


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        message=(
            f"Ваш код подтверждения: {confirmation_code}."
            ' Пожалуйста, отправьте его POST запросом по схеме: \n{"username":'
            '<Никнейм, указанный при регистрации> \n"confirmation_code":'
            '<полученный код>}'
        ),
        subject="Регистрация на платформе YaMDb",
        recipient_list=[user.email],
        from_email=None,
    )


@api_view(("POST",))
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    username = serializer.initial_data.get("username")
    email = serializer.initial_data.get("email")
    user = None
    if username:
        user = User.objects.filter(username=username, email=email).first()
    if user:
        send_confirmation_code(user)
        return Response(serializer.initial_data, status=status.HTTP_200_OK)

    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(username=serializer.validated_data["username"])
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def send_jwt_token(request):
    serializer = TokenAproveSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data["username"])

    if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'patch', 'post', 'delete')

    @action(
        methods=["get", "patch", ], url_path="me", detail=False,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserSerializer, )
    def self_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "PATCH":
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            serializer.Meta.read_only_fields = ('role',)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
