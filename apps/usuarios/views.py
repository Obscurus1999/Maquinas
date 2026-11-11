from django.shortcuts import redirect, render
from .forms import RegistroForm


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()  # El formulario maneja la creación de forma atómica
            return redirect('usuarios:login')
    else:
        form = RegistroForm()
        
    return render(request, 'usuarios/registro.html', {'form': form})