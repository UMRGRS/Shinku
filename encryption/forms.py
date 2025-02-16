from django import forms

class encrypt_form(forms.Form):
    cypher_choices = [('symmetric', 'Simétrico'), ('aes', 'AES'), ('rsa', 'RSA')]
    
    data_to_encrypt = forms.CharField(label="Información para encriptar", max_length=50)
    cypher_choice = forms.ChoiceField(label='Tipo de encriptado', choices=cypher_choices)
    
    
class decrypt_form(forms.Form):
    cypher_choices = [('symmetric', 'Simétrico'), ('aes', 'AES'), ('rsa', 'RSA')]
    
    data_to_decrypt = forms.CharField(label="Información para desencriptar", max_length=1000)
    cypher_choice = forms.ChoiceField(label='Tipo de desencriptado', choices=cypher_choices)
    

