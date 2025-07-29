from django.shortcuts import render
from .models import Producto



def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/productos.html', {'productos': productos})


#importar excel .

import pandas as pd
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import Producto

def importar_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_excel']
            df = pd.read_excel(archivo)

            for _, row in df.iterrows():
                Producto.objects.create(
                    categoria=row['Categoria'],
                    empresa=row['Empresa'],
                    pasillo=row['Pasillo'],
                    ubicacion=row['Ubicación'],
                    cod_ean=row['Cod_EAN'],
                    cod_dun=row['Cod_DUN'],
                    cod_sistema=row['Cod_Sistema'],
                    descripcion=row['Descripción'],
                    unidad=row['Unidad'],
                    pack=row['Pack'],
                    factorx=row['Factorx'],
                    cajas=row['Cajas'],
                    saldo=row['Saldo'],
                    stock_fisico=row['Stock Físico'],
                    observacion=row.get('Observación', ''),
                    fecha_venc=row['Fecha_Venc'],
                    fecha_imp=row['Fecha_IMP'],
                    contenedor=row['Contenedor'],
                    fecha_inv=row['Fecha_INV'],
                    encargado=row['Encargado']
                )
            return redirect('lista_productos')
    else:
        form = ExcelUploadForm()
    return render(request, 'inventario/importar_excel.html', {'form': form})


#exportar excel .

import pandas as pd
from django.http import HttpResponse
from .models import Producto

def exportar_excel(request):
    productos = Producto.objects.all().values(
        'categoria', 'empresa', 'pasillo', 'ubicacion', 'cod_ean', 'cod_dun', 'cod_sistema',
        'descripcion', 'unidad', 'pack', 'factorx', 'cajas', 'saldo', 'stock_fisico',
        'observacion', 'fecha_venc', 'fecha_imp', 'contenedor', 'fecha_inv', 'encargado'
    )
    df = pd.DataFrame(productos)

    # Crear respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=productos_bodega.xlsx'
    
    # Escribir el DataFrame al response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Productos')

    return response


#editar y eliminar 

from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {'form': form})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})


#busqueda de tabla

from django.db.models import Q

def lista_productos(request):
    productos = Producto.objects.all()
    query = request.GET.get('q')

    if query:
        productos = productos.filter(
            Q(categoria__icontains=query) |
            Q(empresa__icontains=query) |
            Q(pasillo__icontains=query) |
            Q(ubicacion__icontains=query) |
            Q(cod_ean__icontains=query) |
            Q(cod_dun__icontains=query) |
            Q(cod_sistema__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(unidad__icontains=query) |
            Q(pack__icontains=query) |
            Q(factorx__icontains=query) |
            Q(cajas__icontains=query) |
            Q(saldo__icontains=query) |
            Q(stock_fisico__icontains=query) |
            Q(observacion__icontains=query) |
            Q(contenedor__icontains=query) |
            Q(encargado__icontains=query)
        )

    return render(request, 'inventario/productos.html', {'productos': productos})


# consulta ubicacion 


# scaner ubicacion

    
# inicio 


from django.shortcuts import render

def inicio(request):
    return render(request, 'inventario/inicio.html')



# usuarios 

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registro_usuario.html', {'form': form})



#proteccion de vistas 

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def inicio(request):
    return render(request, 'inventario/inicio.html')




# escanear codigo camara - lector 

from django.shortcuts import render

def escaner_ubicacion(request):
    return render(request, 'inventario/escanear.html')


#capturar codigo 128b

# views.py
from django.http import JsonResponse
from .models import Producto

def buscar_por_ubicacion(request):
    ubicacion = request.GET.get('ubicacion', '')
    productos = Producto.objects.filter(ubicacion=ubicacion)
    datos = list(productos.values('cod_sistema', 'descripcion', 'cod_ean', 'cod_dun', 'cajas'))
    return JsonResponse({'productos': datos})







