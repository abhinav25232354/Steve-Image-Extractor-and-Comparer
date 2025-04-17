from cryptography.fernet import Fernet

# Generate a new Fernet key
new_key = Fernet.generate_key().decode()

# Print the key to use in your app
print(new_key)
