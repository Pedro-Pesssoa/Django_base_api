from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# TODO ver se esse import é nescessario. Taambém retirar da api blçockCode caso não seja
from drf_yasg import openapi
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from accounts.models import User, PasswordResetCode
from accounts.serializers import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer
)


class PasswordResetViewSet(viewsets.ViewSet):
    """
    ViewSet para operações de recuperação de senha
    """
    
    @action(detail=False, methods=['post'], url_path='request')
    def request_reset(self, request):
        """
        Solicita recuperação de senha
        Envia o código de segurança para o email que foi passado
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                code = user.generate_reset_code()
                PasswordResetCode.objects.create(user=user, code=code)
                
                send_mail(
                    subject='Código de Recuperação de Senha',
                    message=f'Seu código de recuperação é: {code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                
                return Response({
                    'message': 'Código de recuperação enviado para seu email'
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                pass
                
        return Response({
            'message': 'Se o email estiver cadastrado, você receberá um código.'
        }, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], url_path='verify')
    def verify_code(self, request):
        """
        Verifica se o código de recuperação é válido
        Compara código que foi passado com o que está registrado no banco
        """
        serializer = PasswordResetVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            try:
                user = User.objects.get(email=email)
                reset_code = PasswordResetCode.objects.filter(
                    user=user, code=code
                ).first()
                
                if reset_code and reset_code.is_valid():
                    return Response({
                        'valid': True,
                        'message': 'Código válido'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'valid': False,
                        'message': 'Código inválido ou expirado'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except User.DoesNotExist:
                return Response({
                    'valid': False,
                    'message': 'Usuário não encontrado'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], url_path='confirm')
    def confirm_reset(self, request):
        """
        Confirma e redefine a senha
        Compara novamente os códigos de segurança
        Recebe a senha nova e cadastra
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(email=email)
                reset_code = PasswordResetCode.objects.filter(
                    user=user, code=code
                ).first()
                
                if reset_code and reset_code.is_valid():
                    user.set_password(new_password)
                    user.save()
                    
                    reset_code.is_used = True
                    reset_code.save()
                    
                    return Response({
                        'message': 'Senha redefinida com sucesso'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': 'Código inválido ou expirado'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except User.DoesNotExist:
                return Response({
                    'message': 'Usuário não encontrado'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)