from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def userregistration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Obtener datos del request
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            role = data.get('role', 'user')
            
            # Validaciones básicas
            if not all([first_name, last_name, email, username, password, confirm_password]):
                return JsonResponse({
                    'success': False,
                    'message': 'Todos los campos son requeridos'
                }, status=400)
            
            if password != confirm_password:
                return JsonResponse({
                    'success': False, 
                    'message': 'Las contraseñas no coinciden'
                }, status=400)
            
            # Verificar si el email ya existe
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Este correo electrónico ya está registrado'
                }, status=400)
            
            # Verificar si el username ya existe  
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Este nombre de usuario ya existe'
                }, status=400)
            
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': role,
                    'full_name': f"{user.first_name} {user.last_name}"
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error en el registro: {str(e)}'
            }, status=500)
    
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido. Use POST'
    }, status=405)

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Email y contraseña son requeridos'
                }, status=400)
            
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
                
                if user is not None:
                    auth_login(request, user)
                    return JsonResponse({
                        'success': True,
                        'message': f'Bienvenido {user.username}',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email
                        }
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Credenciales incorrectas'
                    }, status=401)
                    
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Credenciales incorrectas'
                }, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'JSON inválido'
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido. Use POST'
    }, status=405)

@csrf_exempt
def logout_api(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Sesión cerrada correctamente'
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido. Use POST'
    }, status=405)

def check_auth_api(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }
        })
    else:
        return JsonResponse({
            'authenticated': False,
            'message': 'Usuario no autenticado'
        })