from django.shortcuts import render
from .models import Producto



def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/productos.html', {'productos': productos})


#importar excel .
import openpyxl
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto

def importar_excel(request):
    if request.method == 'POST':
        archivo = request.FILES.get('excel')
        if not archivo:
            messages.error(request, "No se ha seleccionado ningún archivo.")
            return redirect('importar_excel')

        if not archivo.name.endswith('.xlsx'):
            messages.error(request, "Solo archivos .xlsx son soportados.")
            return redirect('importar_excel')

        try:
            wb = openpyxl.load_workbook(archivo)
            hoja = wb.active

            # Limpia todos los productos antes de importar (refrescar datos)
            Producto.objects.all().delete()

            for fila in hoja.iter_rows(min_row=2, values_only=True):
                Producto.objects.create(
                    categoria=fila[0],
                    empresa=fila[1],
                    pasillo=fila[2],
                    ubicacion=fila[3],
                    cod_ean=fila[4],
                    cod_dun=fila[5],
                    cod_sistema=fila[6],
                    descripcion=fila[7],
                    unidad=fila[8],
                    pack=fila[9],
                    factorx=fila[10] or 0,
                    cajas=fila[11] or 0,
                    saldo=fila[12] or 0,
                    stock_fisico=fila[13] or 0,
                    observacion=fila[14],
                    fecha_venc=fila[15],
                    fecha_imp=fila[16],
                    contenedor=fila[17],
                    fecha_inv=fila[18],
                    encargado=fila[19],
                )

            messages.success(request, "Base de datos actualizada con éxito.")
            return redirect('importar_excel')

        except Exception as e:
            messages.error(request, f"Error al importar: {e}")
            return redirect('importar_excel')

    return render(request, 'importar_excel.html')


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







