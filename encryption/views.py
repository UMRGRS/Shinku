from django.shortcuts import render
from .forms import encrypt_form, decrypt_form

# Create your views here.

def encrypt_decrypt(request):
    
    if request.method == "POST":
        action = request.GET.get('action', 'none')
        if action == 'encrypt':
            encrypt_f = encrypt_form(request.POST)
            
            if encrypt_f.is_valid():
                print(encrypt_f.cleaned_data)
                
            decrypt_f = decrypt_form()
            
        if action == 'decrypt':
            decrypt_f = decrypt_form(request.POST)
            
            if decrypt_f.is_valid():
                print(decrypt_f.cleaned_data)
                
            encrypt_f = encrypt_form()

    else:
        encrypt_f = encrypt_form()
        decrypt_f = decrypt_form()
    return render(request, "encryption/encrypt_decrypt_test.html", {"encrypt_form" : encrypt_f, "decrypt_form" : decrypt_f})
