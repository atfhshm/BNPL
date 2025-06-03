from django.contrib.auth import authenticate
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
)

from apps.api.v1.auth.serializers import (
    TokenObtainPairSerializer,
    TokenPairSerializer,
    TokenRefreshResponseSerializer,
    UserRegisterSerializer,
)
from apps.api.v1.user.serializers import UserSerializer
from apps.user.models import User
from bnpl.jwt import get_tokens
from bnpl.serializers import DetailSerializer, get_serializer_validation_errors


class AuthView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary='Register a new customer',
        description='Register a new customer',
        tags=['Auth'],
        request=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: TokenPairSerializer,
        },
        examples=[
            get_serializer_validation_errors(UserRegisterSerializer),
        ],
    )
    @action(detail=False, methods=['post'], url_path='customer-register')
    def customer_register(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(
            user_type=User.UserType.CUSTOMER,
            last_login=timezone.now(),
        )
        tokens: dict[str, str] = get_tokens(user)
        tokens_serializer = TokenPairSerializer(instance=tokens)
        return Response(
            data=tokens_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary='Register a new merchant',
        description='Register a new merchant',
        tags=['Auth'],
        request=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: TokenPairSerializer,
        },
        examples=[
            get_serializer_validation_errors(UserRegisterSerializer),
        ],
    )
    @action(detail=False, methods=['post'], url_path='merchant-register')
    def merchant_register(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(
            user_type=User.UserType.MERCHANT,
            last_login=timezone.now(),
        )
        tokens: dict[str, str] = get_tokens(user)
        tokens_serializer = TokenPairSerializer(instance=tokens)
        return Response(
            data=tokens_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary='Login a user',
        description='Login a user',
        tags=['Auth'],
        request=TokenObtainPairSerializer,
        responses={
            status.HTTP_200_OK: TokenPairSerializer,
            status.HTTP_401_UNAUTHORIZED: DetailSerializer,
        },
        examples=[
            get_serializer_validation_errors(TokenObtainPairSerializer),
        ],
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        login_term: str = serializer.data.get('login')
        password: str = serializer.data.get('password')
        user: User | None = authenticate(
            request, login_term=login_term, password=password
        )
        if user:
            tokens: dict[str, str] = get_tokens(user)
            tokens_serializer = TokenPairSerializer(instance=tokens)
            return Response(data=tokens_serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = DetailSerializer(instance={'detail': 'Invalid credentials'})
            return Response(
                data=serializer.data,
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @extend_schema(
        summary='Refresh a user token',
        description='Refresh a user token',
        tags=['Auth'],
        request=TokenRefreshSerializer,
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: DetailSerializer,
        },
        examples=[
            get_serializer_validation_errors(TokenRefreshSerializer),
        ],
    )
    @action(detail=False, methods=['post'], url_path='refresh')
    def refresh(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'access': serializer.validated_data['access']})

    @extend_schema(
        summary='Get current user',
        description='Get current user',
        tags=['Auth'],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: DetailSerializer,
        },
    )
    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(instance=user)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
