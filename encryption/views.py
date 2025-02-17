from django.shortcuts import render
from .forms import encrypt_form, decrypt_form
from .encrypt_data import cipher_suite, select_cipher, select_decipher

cipher = cipher_suite()

# Create your views here.
def encrypt_decrypt(request):
    cipher_data = None
    decipher_data = None
    if request.method == "POST":
        
        action = request.GET.get('action', 'none')
        if action == 'encrypt':
            encrypt_f = encrypt_form(request.POST)
            decrypt_f = decrypt_form()
            
            if encrypt_f.is_valid():
                cipher_data = select_cipher(cipher, encrypt_f.cleaned_data['cypher_choice'], encrypt_f.cleaned_data['data_to_encrypt'])
                decrypt_f = decrypt_form(initial={"data_to_decrypt": cipher_data, "cypher_choice": encrypt_f.cleaned_data['cypher_choice']})
            

        if action == 'decrypt':
            decrypt_f = decrypt_form(request.POST)

            if decrypt_f.is_valid():
                decipher_data = select_decipher(cipher, decrypt_f.cleaned_data['cypher_choice'], decrypt_f.cleaned_data['data_to_decrypt'])
            encrypt_f = encrypt_form()

    else:
        encrypt_f = encrypt_form()
        decrypt_f = decrypt_form()
    return render(request, "encryption/encrypt_decrypt_test.html", 
                  {"encrypt_form": encrypt_f, "decrypt_form": decrypt_f, 
                   "cipher_data": cipher_data, "decipher_data": decipher_data})

