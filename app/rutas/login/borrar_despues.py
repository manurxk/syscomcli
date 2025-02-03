from werkzeug.security import generate_password_hash

usu_clave="123"
su_clave = generate_password_hash(usu_clave)
print (usu_clave)