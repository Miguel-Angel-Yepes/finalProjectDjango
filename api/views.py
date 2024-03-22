from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from .models import Inventario, Usuarios
from django.views.decorators.cache import never_cache

@never_cache

# Vista para agregar un nuevo producto al inventario
def agregar(request):
    # Aplica el middleware de autenticación
    auth_response = middleware_autenticacion(request)
    if auth_response is not None:
        return auth_response

    # Lista de categorías disponibles para el producto
    categorias = ["Frutas y verduras", "Lácteos", "Aseo", "Aseo Personal", "Carne", "Carnes Frías", "Panadería y reposteria", "Alimentos no precederos", "Bebidas", "Licores", "Congelados", "Dulces"]

    if request.method == 'POST':
        # Obtiene los datos del formulario de entrada
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        isdiscount = request.POST.get('isdiscount')
        discount = request.POST.get('discount')

        # Convierte la cadena 'True' o 'False' a valores booleanos
        if isdiscount == 'True':
            isdiscount = True
        else:
            isdiscount = False

        # Crea un nuevo objeto de Inventario con los datos proporcionados
        nuevo_producto = Inventario.objects.create(
            name=name,
            price=float(price),
            stock=int(stock),
            category=category,
            isdiscount=isdiscount,
            discount=discount,
            state='ACTIVO'  
        )

        return redirect('gestion')  # Redirecciona a la vista de gestión después de agregar correctamente el producto

    return render(request, 'agregar.html', {"categorias": categorias})  # Renderiza la vista del formulario de agregar producto

@never_cache
def gestion(request):

    # Aplica el middleware de autenticación
    auth_response = middleware_autenticacion(request)
    if auth_response is not None:
        return auth_response

    # Obtiene el ID del usuario de la sesión y su nombre
    usuario_id = request.session.get('usuario_id')
    usuario = Usuarios.objects.get(id=usuario_id)
    nombre_usuario = usuario.user

    # Verifica si se ha mostrado el mensaje de bienvenida
    mostrar_mensaje_bienvenida = request.session.pop('mostrar_mensaje_bienvenida', False)

    # Lista de categorías disponibles para filtrar productos
    categorias = ["Frutas y verduras", "Lácteos", "Aseo", "Aseo Personal", "Carne", "Carnes Frías", "Panadería y reposteria", "Alimentos no precederos", "Bebidas", "Licores", "Congelados", "Dulces"]

    # Obtiene todos los productos del inventario
    inventarios = Inventario.objects.all()

    # Obtiene las categorías seleccionadas (si hay alguna)
    categorias_seleccionadas = request.GET.getlist('categoria')
    # Verifica si se debe filtrar por descuento
    filtrar_descuento = 'descuento' in request.GET
    # Obtiene el estado seleccionado (si hay alguno)
    estado = request.GET.get('estado')

    # Aplica los filtros seleccionados
    if categorias_seleccionadas:
        inventarios = inventarios.filter(category__in=categorias_seleccionadas)

    if filtrar_descuento:
        inventarios = inventarios.filter(isdiscount=True)

    if estado:
        inventarios = inventarios.filter(state=estado)

    # Realiza procesamiento adicional en los productos
    for inventario in inventarios:
        if inventario.isdiscount:
            inventario.precio_reducido = inventario.price - (inventario.price * inventario.discount / 100)
        else:
            inventario.precio_reducido = inventario.price

    # Renderiza la página de gestión con los productos filtrados y otros datos necesarios
    return render(request, 'gestion.html', {
        'inventarios': inventarios,
        'nombre_usuario': nombre_usuario,
        'categorias': categorias,
        'categorias_seleccionadas': categorias_seleccionadas,
        'filtrar_descuento': filtrar_descuento,
        'estado': estado,
        'mostrar_mensaje_bienvenida': mostrar_mensaje_bienvenida,
    })

@never_cache
# Vista para actualizar la información de un producto en el inventario
def actualizar(request, producto_id):
    # Aplica el middleware de autenticación
    auth_response = middleware_autenticacion(request)
    if auth_response is not None:
        return auth_response

    # Obtiene el producto del inventario con el ID proporcionado
    producto = Inventario.objects.get(pk=producto_id)
    
    # Lista de categorías disponibles para el producto
    categorias = ["Frutas y verduras", "Lácteos", "Aseo", "Aseo Personal", "Carne", "Carnes Frías", "Panadería y reposteria", "Alimentos no precederos", "Bebidas", "Licores", "Congelados", "Dulces"]

    if request.method == 'POST':
        # Obtiene los datos del formulario de actualización
        producto.name = request.POST.get('name')
        producto.price = request.POST.get('price')
        producto.stock = request.POST.get('stock')
        producto.category = request.POST.get('category')
        producto.isdiscount = request.POST.get('isdiscount')
        
        # Convierte la cadena 'False' a 0 para el descuento si no se aplica
        if producto.isdiscount == 'False':
            producto.discount = 0
        else:
            producto.discount = request.POST.get('discount')

        # Verifica si el stock es válido
        if int(producto.stock) <= 0:
            # Si la solicitud es AJAX, devuelve un mensaje de error
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Stock inválido'}, status=400)
            else:
                # Si la solicitud no es AJAX, renderiza la página de actualización con un mensaje de error
                return render(request, 'actualizar.html', {'error_message': 'Stock inválido', 'producto': producto, 'categorias': categorias})
        else:
            producto.state = request.POST.get('state')
        
        producto.save()

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # Si la solicitud es AJAX, devuelve un mensaje de éxito
            return JsonResponse({'message': 'Producto actualizado correctamente'})
        else:
            # Si la solicitud no es AJAX, redirecciona a la vista de gestión después de la actualización
            return redirect('gestion')

    data = {
        'producto': producto,
        'categorias': categorias
    }
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Si la solicitud es AJAX, devuelve los datos del producto en formato JSON
        return JsonResponse(data)
    else:
        # Si la solicitud no es AJAX, renderiza la página de actualización con los datos del producto
        return render(request, 'actualizar.html', data)

@never_cache
# Vista para ver los detalles de un producto en el inventario
def detalles_producto(request, producto_id):
    # Aplica el middleware de autenticación
    auth_response = middleware_autenticacion(request)
    if auth_response is not None:
        return auth_response
    
    # Obtiene el producto del inventario o devuelve un error 404 si no se encuentra
    producto = get_object_or_404(Inventario, pk=producto_id)
    
    # Renderiza la página de detalles del producto
    return render(request, 'detalles.html', {'producto': producto})


@never_cache
# Vista para eliminar un producto del inventario
def eliminar(request, producto_id):
    # Aplica el middleware de autenticación
    auth_response = middleware_autenticacion(request)
    if auth_response is not None:
        return auth_response
    
    # Obtiene el producto del inventario o devuelve un error 404 si no se encuentra
    producto = get_object_or_404(Inventario, pk=producto_id)

    # Cambia el estado del producto a 'INACTIVO' y el stock a cero, luego guarda los cambios
    producto.state = 'INACTIVO'
    producto.stock = '0'
    producto.isdiscount = 'False'
    producto.discount = '0'
    producto.save()

    return redirect('gestion')

@never_cache
def login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        users = Usuarios.objects.filter(user=identifier) | Usuarios.objects.filter(email=identifier)

        if users.exists() and users[0].password == password:
            request.session['usuario_id'] = users[0].id
            request.session['mostrar_mensaje_bienvenida'] = True  
            return redirect('gestion')  # Redirecciona al usuario al inicio después de iniciar sesión correctamente
        else:
            error_message = 'Credenciales inválidas'
            return render(request, 'login.html', {'error_message': error_message})  # Renderiza la vista de login con un mensaje de error
    else:
        return render(request, 'login.html')  # Renderiza la vista de login sin ningún mensaje

@never_cache
# Vista para crear una nueva cuenta de usuario
def crear_cuenta(request):
    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el usuario
        email = request.POST.get('email')
        user = request.POST.get('username')
        password = request.POST.get('password')

        # Validar el correo electrónico
        if '@' not in email:
            error_message = "Ingrese una dirección de correo electrónico válida."
            return render(request, 'crearCuenta.html', {'error_message': error_message})

        # Validar la longitud del usuario y contraseña
        if len(user) < 5:
            error_message = "El usuario debe tener al menos 5 caracteres."
            return render(request, 'crearCuenta.html', {'error_message': error_message})

        if len(password) < 6:
            error_message = "La contraseña debe tener al menos 8 caracteres."
            return render(request, 'crearCuenta.html', {'error_message': error_message})

        # Verificar si el correo electrónico ya está registrado
        if Usuarios.objects.filter(email=email).exists():
            error_message = "Este correo electrónico ya está registrado."
            return render(request, 'crearCuenta.html', {'error_message': error_message})

        # Verificar si el usuario ya está registrado
        if Usuarios.objects.filter(user=user).exists():
            error_message = "Este usuario ya está registrado."
            return render(request, 'crearCuenta.html', {'error_message': error_message})

        # Crear un nuevo usuario si pasa todas las validaciones
        nuevo_usuario = Usuarios.objects.create(
            email=email,
            user=user,
            password=password
        )
        nuevo_usuario.save()

        # Redirigir al usuario a la página de inicio de sesión
        return redirect('login')
    else:
        # Si la solicitud no es de tipo POST, mostrar el formulario de creación de cuenta
        return render(request, 'crearCuenta.html')

@never_cache
def cerrar_sesion(request):
    # Verifica si el usuario está actualmente autenticado
    if 'usuario_id' in request.session:
        # Elimina el ID de usuario de la sesión
        del request.session['usuario_id']
        
    # Configura los encabezados de respuesta para evitar el almacenamiento en caché
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    # Redirige al usuario a la página de inicio de sesión después de cerrar sesión
    return response

def middleware_autenticacion(request):
    # Verifica si el usuario está autenticado
    if 'usuario_id' not in request.session:
        # Si el usuario no está autenticado, redirige a la página de inicio de sesión
        return redirect('login')
    # Si el usuario está autenticado, permite que la solicitud continúe
    return None
