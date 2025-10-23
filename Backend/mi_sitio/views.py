from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from admin_users.models import PersonResponsible, Role_employee
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
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

#----------- Registro y edicion de empleados --------------
@csrf_exempt  
def employee_registration(request):
    "Recibe el nombre y rol de un empleado del sistema y los guarda en DB"

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            role_name = data.get('role')
            
            if not all([first_name, last_name, role_name]):
                
                return JsonResponse({
                    'message': 'Todos los campos son requeridos para hacer un registro'
                }, status=400)
            
            try:
                assigned_role = Role_employee.objects.get(name=role_name)
            except ObjectDoesNotExist:

                return JsonResponse({
                    "success": False,
                    "message": "Ese rol no exite en la empresa" #Esto por el momento, ya que me imagino que los roles solo seran seleccionados y no escritos
                }, status=400)
            
            # Verificamos si ya existe este registro
            if PersonResponsible.objects.filter(first_name = first_name, last_name = last_name, role = assigned_role).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Ya existe un registro con esta informacion'
                }, status=400)
            
            # Creamos el registro para el empleado
            employee = PersonResponsible.objects.create(
                first_name = first_name,
                last_name = last_name,
                role = assigned_role
            )
            
            return JsonResponse({
                "message": "Registro de responsable creado con éxito.",
                "id de empleado": employee.id,
                "first_name": employee.first_name,
                "rol": employee.role.name
            }, status=201) 
           
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

@csrf_exempt 
def employee_list(request):
    "Obtiene los registros de empleados y los devuelve"

    if request.method == 'GET':

        try:

            all_employee = PersonResponsible.objects.all()
            employees = []

            for i in all_employee:
                employees.append({
                    "id_employee": i.id,
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                    "role": i.role.name
                })

            return JsonResponse({
                "seccess": True,
                "message": "Lista de empleados:",
                "Registros": employees
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al mostrar la lista: {str(e)}'
            }, status=500)

@csrf_exempt     
def edit_employee(request, pk):
    "Recibe la solicitud y el ID (desde la URL) para editar los campos del registro correspondiente al ID"

    if request.method == 'PATCH':

        try:

            data = json.loads(request.body)
            employee = get_object_or_404(PersonResponsible, pk = pk)
           
            if "role" in data:

                role_name = data.get('role')
                role = Role_employee.objects.get(name = role_name)
                employee.role = role

            if "first_name" in data: employee.first_name = data.get('first_name')

            if "last_name" in data: employee.last_name = data.get('last_name')

            employee.save()
            return JsonResponse({
                "success": True,
                "message": f"Usuario con ID {pk} fue actualizado."
            }, status=200)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"Error al actualizar: {str(e)}"
            }, status=500)