from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Mensagens)
admin.site.register(Usuario)
admin.site.register(Turma)