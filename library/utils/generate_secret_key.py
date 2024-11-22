from django.core.management.utils import get_random_secret_key

# Gera uma chave secreta usando o Django
secret_key = get_random_secret_key()
print(secret_key)
