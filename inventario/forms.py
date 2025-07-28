from django import forms

class ExcelUploadForm(forms.Form):
    archivo_excel = forms.FileField(label='Selecciona un archivo Excel')
    
# editar - eliminar 
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

