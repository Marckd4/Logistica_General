from django.db import models

class Producto(models.Model):
    categoria = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    pasillo = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=100)
    cod_ean = models.CharField(max_length=50)
    cod_dun = models.CharField(max_length=50)
    cod_sistema = models.CharField(max_length=50)
    descripcion = models.TextField()
    unidad = models.CharField(max_length=20)
    pack = models.CharField(max_length=20)
    factorx = models.FloatField()
    cajas = models.IntegerField()
    saldo = models.FloatField()
    stock_fisico = models.FloatField()
    observacion = models.TextField(blank=True, null=True)
    fecha_venc = models.DateField()
    fecha_imp = models.DateField()
    contenedor = models.CharField(max_length=50)
    fecha_inv = models.DateField()
    encargado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.descripcion} ({self.cod_ean})"
