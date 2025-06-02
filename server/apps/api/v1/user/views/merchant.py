from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api.v1.user.serializers import PasswordChangeSerializer, UserSerializer
from apps.user.models import User
from bnpl.pagination import PagePaginator
from bnpl.permissions import IsMerchant
from bnpl.serializers import DetailSerializer, get_serializer_validation_errors


class MerchantView(
    GenericViewSet,
    ListModelMixin,
):
    queryset = User.objects.filter(user_type=User.UserType.MERCHANT).all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PagePaginator
    http_method_names = ['get', 'patch', 'delete']

    @extend_schema(
        summary='List all merchants',
        description='List all merchants',
        tags=['Merchants'],
        responses={200: UserSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Authenticated merchant',
        description='The current authenticated merchant',
        tags=['Merchants'],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_404_NOT_FOUND: DetailSerializer,
        },
    )
    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path='me',
        permission_classes=[IsAuthenticated, IsMerchant],
    )
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            user = self.request.user
            serializer = UserSerializer(instance=user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            user = self.request.user
            serializer = UserSerializer(
                instance=user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            user = self.request.user
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary='Change user password',
        description='Change user password',
        tags=['Merchants'],
        request=PasswordChangeSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: PasswordChangeSerializer,
        },
        examples=[
            get_serializer_validation_errors(PasswordChangeSerializer),
        ],
    )
    @action(
        detail=False,
        methods=['patch'],
        url_path='me/change-password',
        permission_classes=[
            IsAuthenticated,
            IsMerchant,
        ],
    )
    def me_change_password(self, request, *args, **kwargs):
        user: User = self.request.user
        password = self.request.data.get('password')
        new_password = self.request.data.get('new_password')
        if not user.check_password(password):
            return Response(
                data={'password': ['Invalid password.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)
