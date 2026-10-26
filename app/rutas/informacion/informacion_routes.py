from flask import Blueprint, render_template

from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao

informacionmod = Blueprint('informacion', __name__, template_folder='templates')

VERSION_TEXTOS = '0.2'
ACTUALIZADO = '26/10/2026'


def _datos_clinica():
    """Datos de la clínica para el texto legal: los de la empresa cargada en el sistema (si no hay, el texto queda genérico)."""
    emp = EmpresaDao().getEmpresaPrincipal() or {}
    ruc = f"{emp.get('ruc_nit')}-{emp.get('digito_verificador')}" if emp.get('ruc_nit') else None
    return {
        'nombre': emp.get('nombre_comercial') or emp.get('razon_social') or 'la clínica',
        'nombre_pie': emp.get('nombre_comercial') or emp.get('razon_social') or 'SYSCLIN',
        'razon_social': emp.get('razon_social'),
        'ruc': ruc,
        'direccion': emp.get('direccion'),
        'ciudad': emp.get('des_ciudad'),
        'telefono': emp.get('telefono') or emp.get('celular'),
        'email': emp.get('email'),
    }


@informacionmod.route('/privacidad', methods=['GET'])
def privacidad():
    """Política de privacidad. Pública: se enlaza desde el login y el pie del sistema."""
    return render_template('informacion-privacidad.html', clinica=_datos_clinica(),
                           version=VERSION_TEXTOS, actualizado=ACTUALIZADO)


@informacionmod.route('/terminos', methods=['GET'])
def terminos():
    """Términos y condiciones de uso para el personal. Públicos: se enlazan desde el login y el pie del sistema."""
    return render_template('informacion-terminos.html', clinica=_datos_clinica(),
                           version=VERSION_TEXTOS, actualizado=ACTUALIZADO)
