from flask import Blueprint, render_template, session, redirect, url_for

perfilmod = Blueprint('perfil', __name__, template_folder='templates')

@perfilmod.route('/perfil-index')
def perfilIndex():
    """
    Página principal del perfil de usuario
    Solo accesible si el usuario está logueado
    """
    # DEBUG: Ver qué hay en la sesión
    print("=" * 50)
    print("DEBUG PERFIL - Contenido de session:")
    print(f"Session completa: {dict(session)}")
    print(f"'id_usuario' en session: {'id_usuario' in session}")
    print(f"Valor de id_usuario: {session.get('id_usuario')}")
    print("=" * 50)
    
    # Verificar que el usuario esté logueado
    # CORREGIDO: Usar 'id_usuario' en lugar de 'id'
    if 'id_usuario' not in session:
        print("⚠️ ERROR: Usuario no tiene id_usuario en sesión, redirigiendo al login")
        return redirect(url_for('login.login'))
    
    return render_template('perfil-index.html')