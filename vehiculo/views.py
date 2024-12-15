from django.shortcuts import render, redirect
from .models import Vehiculo
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Permission


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Por favor, completa todos los campos.')
            return redirect('login')
        else:

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('index') 
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                return redirect('login') 

    return render(request, 'login.html')

@login_required
@permission_required('vehiculo.add_vehiculomodel', raise_exception=True)
def add_vehiculo(request):
    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        serial_carroceria = request.POST.get('serial_carroceria')
        serial_motor = request.POST.get('serial_motor')
        categoria = request.POST.get('categoria')
        precio = request.POST.get('precio')

        if not (marca and modelo and serial_carroceria and serial_motor and categoria and precio):
            return HttpResponse("Todos los campos son obligatorios", status=400)

        try:
            precio = float(precio)
        except ValueError:
            return HttpResponse("El precio debe ser un número válido.", status=400)

        vehiculo = Vehiculo(
            marca=marca,
            modelo=modelo,
            serial_carroceria=serial_carroceria,
            serial_motor=serial_motor,
            categoria=categoria,
            precio=precio,
        )
        vehiculo.save()

        return redirect('ver_vehiculo', vehiculo_id=vehiculo.id)

    return render(request, 'add_vehiculo.html')

@login_required
@permission_required('vehiculo.visualizar_catalogo', raise_exception=True)
def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'listar_vehiculos.html', {'vehiculos': vehiculos})


def index(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, "index.html", {"vehiculos": vehiculos})
    
def ver_vehiculo(request, vehiculo_id):
    try:
        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    except Vehiculo.DoesNotExist:
        messages.error(request, "Vehículo no encontrado.")
        return redirect('listar_vehiculos') 
    context = {
        'vehiculo': vehiculo
    }
    return render(request, 'ver_vehiculo.html', context)

def registrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro_usuario.html')

        if get_user_model().objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'registro_usuario.html')

        if get_user_model().objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'registro_usuario.html')

        try:
            User = get_user_model()
            user = User(username=username, email=email)
            user.set_password(password1)

            user.save()

            permiso = Permission.objects.get(codename='visualizar_catalogo')
            user.user_permissions.add(permiso)

            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login')

        except IntegrityError as e:
            messages.error(request, f'Ocurrió un error al registrar el usuario. Error: {str(e)}')
            return render(request, 'registro_usuario.html')

        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado. Error: {str(e)}')
            return render(request, 'registro_usuario.html')
    return render(request, 'registro_usuario.html')

def logout_view(request):
    logout(request)
    return redirect('login')  