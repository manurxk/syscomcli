"""
Capturas de pantalla del manual de usuario (app/static/img/ayuda/<seccion>/NN_nombre.jpg).

Abre Chrome sin interfaz (headless), inicia sesión en el sistema, marca los elementos con el
estilo de la guía (borde violeta + círculo numerado, los números coinciden con los pasos del
texto) y guarda un recorte JPG de 1116 px de ancho, el mismo formato que las capturas existentes.

Habla con Chrome por el protocolo DevTools con un cliente WebSocket mínimo escrito con la
biblioteca estándar: no hay que instalar nada (ni Playwright ni Selenium).

Las contraseñas NUNCA se escriben en este archivo; se leen de variables de entorno:
    CAPTURAS_RECEPCION_USER / CAPTURAS_RECEPCION_PASS   (por defecto recep2 / la de seed_prueba.py)
    CAPTURAS_ADMIN_USER / CAPTURAS_ADMIN_PASS           (usuario ADMINISTRADOR + CLINICO sin MFA, ej. psicoadmin)

Uso (desde la raíz del repositorio, con el sistema corriendo en el puerto 5005):
    python docs/scripts/capturas_manual.py citas
    $env:CAPTURAS_ADMIN_PASS='...'; python docs/scripts/capturas_manual.py funcionarios consultas

Cada inicio de sesión queda registrado en la auditoría como un login normal; al terminar se cierra la sesión.
"""
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from urllib.parse import urlparse

import requests

BASE = os.getenv('CAPTURAS_BASE_URL', 'http://localhost:5005')
SALIDA = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'static', 'img', 'ayuda')
ANCHO = 1116          # ancho de las capturas existentes (sin el menú lateral)
ALTO = 900
PUERTO_DEVTOOLS = 9333
CHROME = next((c for c in (
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium',
) if os.path.exists(c)), None)

# Estilo de la guía: borde violeta y círculo numerado a la izquierda del elemento
JS_MARCADORES = r"""
// Sin desplazamiento animado (Bootstrap usa scroll-behavior: smooth): las posiciones se miden ya quietas
document.documentElement.style.scrollBehavior = 'auto';
document.querySelectorAll('.table-responsive').forEach(t => t.style.scrollBehavior = 'auto');
// Menú lateral escondido, como en las capturas de la guía
document.body.classList.add('sidebar-collapse');
window.__marcar = function (sel, n, idx) {
  const els = document.querySelectorAll(sel);
  const el = els[idx || 0];
  if (!el) return false;
  el.scrollIntoView({block: 'nearest', inline: 'nearest'});
  el.style.outline = '3px solid #7c3aed';
  el.style.outlineOffset = '2px';
  el.style.borderRadius = el.style.borderRadius || '6px';
  if (n) {
    const r = el.getBoundingClientRect();
    const b = document.createElement('div');
    b.textContent = n;
    b.className = '__marca';
    Object.assign(b.style, {
      position: 'fixed', left: (r.left - 30) + 'px', top: (r.top + r.height / 2 - 11) + 'px',
      width: '22px', height: '22px', borderRadius: '50%', background: '#7c3aed', color: '#fff',
      font: 'bold 12px Arial, sans-serif', display: 'flex', alignItems: 'center',
      justifyContent: 'center', zIndex: 2147483647, boxShadow: '0 0 0 2px #fff'
    });
    document.body.appendChild(b);
  }
  return true;
};
window.__rect = function (sel, idx) {
  const el = document.querySelectorAll(sel)[idx || 0];
  if (!el) return null;
  const r = el.getBoundingClientRect();
  return {x: r.left, y: r.top, w: r.width, h: r.height};
};
true;
"""


class ChromeDevTools:
    """Cliente mínimo del protocolo DevTools sobre WebSocket (RFC 6455), solo stdlib."""

    def __init__(self, ws_url):
        u = urlparse(ws_url)
        self.sock = socket.create_connection((u.hostname, u.port), timeout=60)
        clave = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f"GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\n"
                           f"Connection: Upgrade\r\nSec-WebSocket-Key: {clave}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        respuesta = b''
        while b'\r\n\r\n' not in respuesta:
            respuesta += self.sock.recv(4096)
        if b' 101 ' not in respuesta.split(b'\r\n')[0]:
            raise RuntimeError('Chrome rechazó la conexión DevTools: ' + respuesta.split(b'\r\n')[0].decode())
        self.siguiente_id = 0

    def _enviar(self, texto):
        datos = texto.encode()
        cabecera = bytearray([0x81])
        n = len(datos)
        if n < 126:
            cabecera.append(0x80 | n)
        elif n < 65536:
            cabecera.append(0x80 | 126)
            cabecera += struct.pack('>H', n)
        else:
            cabecera.append(0x80 | 127)
            cabecera += struct.pack('>Q', n)
        mascara = os.urandom(4)
        self.sock.sendall(bytes(cabecera) + mascara + bytes(b ^ mascara[i % 4] for i, b in enumerate(datos)))

    def _leer(self, n):
        datos = b''
        while len(datos) < n:
            parte = self.sock.recv(n - len(datos))
            if not parte:
                raise RuntimeError('Chrome cerró la conexión')
            datos += parte
        return datos

    def _recibir(self):
        mensaje = b''
        while True:
            b1, b2 = self._leer(2)
            n = b2 & 0x7f
            if n == 126:
                n = struct.unpack('>H', self._leer(2))[0]
            elif n == 127:
                n = struct.unpack('>Q', self._leer(8))[0]
            datos = self._leer(n)
            codigo = b1 & 0x0f
            if codigo == 0x8:
                raise RuntimeError('Chrome cerró la conexión')
            if codigo == 0x9:                       # ping -> pong
                self.sock.sendall(bytes([0x8a, 0x80]) + os.urandom(4))
                continue
            mensaje += datos
            if b1 & 0x80:
                return json.loads(mensaje)

    def llamar(self, metodo, **parametros):
        self.siguiente_id += 1
        self._enviar(json.dumps({'id': self.siguiente_id, 'method': metodo, 'params': parametros}))
        while True:
            msg = self._recibir()
            if msg.get('id') == self.siguiente_id:
                if 'error' in msg:
                    raise RuntimeError(f"{metodo}: {msg['error']}")
                return msg.get('result', {})

    def js(self, expresion):
        r = self.llamar('Runtime.evaluate', expression=expresion, returnByValue=True, awaitPromise=True)
        if 'exceptionDetails' in r:
            raise RuntimeError(f"JS: {r['exceptionDetails'].get('text')} en {expresion[:80]}")
        return r.get('result', {}).get('value')

    def esperar(self, expresion, segundos=15):
        fin = time.time() + segundos
        while time.time() < fin:
            if self.js(expresion):
                return True
            time.sleep(0.3)
        raise RuntimeError(f'No se cumplió: {expresion}')

    def ir(self, ruta, listo='true'):
        self.llamar('Page.navigate', url=BASE + ruta)
        time.sleep(0.5)
        self.esperar("document.readyState === 'complete'")
        self.esperar(listo)
        self.js(JS_MARCADORES)
        time.sleep(1.0)                              # animaciones (menú lateral) y tablas
        self.ajustar_alto()

    def ajustar_alto(self):
        """Ventana tan alta como la página: Chrome solo dibuja lo visible, así toda la página
        queda dibujada, sin desplazamiento, y las coordenadas de los recortes son las de la página."""
        alto = self.js("Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)")
        self.llamar('Emulation.setDeviceMetricsOverride', width=ANCHO, height=max(ALTO, int(alto)),
                    deviceScaleFactor=1, mobile=False)
        time.sleep(0.5)
        self.js("window.scrollTo(0, 0); true")

    def capturar(self, archivo, x=0, y=0, ancho=ANCHO, alto=None):
        alto = alto or ALTO
        r = self.llamar('Page.captureScreenshot', format='jpeg', quality=88,
                        clip={'x': max(0, x), 'y': max(0, y), 'width': ancho, 'height': alto, 'scale': 1})
        destino = os.path.normpath(os.path.join(SALIDA, archivo))
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, 'wb') as f:
            f.write(base64.b64decode(r['data']))
        print('  captura', archivo, f'{ancho}x{int(alto)}')


def iniciar_sesion(usuario, clave):
    s = requests.Session()
    tok = re.search(r'name="csrf_token" value="([^"]+)"', s.get(BASE + '/login').text).group(1)
    r = s.post(BASE + '/login', data={'usuario_nombre': usuario, 'usuario_clave': clave, 'csrf_token': tok},
               allow_redirects=False)
    if r.status_code != 302 or 'login' in (r.headers.get('Location') or '') or 'mfa' in (r.headers.get('Location') or ''):
        raise RuntimeError(f'No se pudo iniciar sesión como {usuario} (¿contraseña o MFA?)')
    return s


def abrir_chrome(sesion_http, carpeta_perfil):
    proceso = subprocess.Popen([CHROME, '--headless=new', f'--remote-debugging-port={PUERTO_DEVTOOLS}',
                                f'--user-data-dir={carpeta_perfil}', f'--window-size={ANCHO},{ALTO}',
                                '--hide-scrollbars', '--remote-allow-origins=*', 'about:blank'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            paginas = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PUERTO_DEVTOOLS}/json/list'))
            pagina = next(p for p in paginas if p['type'] == 'page')
            break
        except Exception:
            time.sleep(0.2)
    else:
        proceso.kill()
        raise RuntimeError('Chrome no abrió el puerto DevTools')
    cdp = ChromeDevTools(pagina['webSocketDebuggerUrl'])
    cdp.llamar('Network.enable')
    cdp.llamar('Emulation.setDeviceMetricsOverride', width=ANCHO, height=ALTO, deviceScaleFactor=1, mobile=False)
    # Tema claro: el sistema sigue el tema del navegador si el usuario no eligió uno
    cdp.llamar('Emulation.setEmulatedMedia', features=[{'name': 'prefers-color-scheme', 'value': 'light'}])
    host = urlparse(BASE).hostname
    for c in sesion_http.cookies:
        cdp.llamar('Network.setCookie', name=c.name, value=c.value, domain=host, path='/')
    return proceso, cdp


def con_navegador(usuario, clave, tarea):
    sesion = iniciar_sesion(usuario, clave)
    perfil = tempfile.mkdtemp(prefix='capturas_chrome_')
    proceso = None
    try:
        proceso, cdp = abrir_chrome(sesion, perfil)
        tarea(cdp)
    finally:
        if proceso:
            proceso.kill()
            proceso.wait()
        sesion.get(BASE + '/logout')
        shutil.rmtree(perfil, ignore_errors=True)


# ---------------------------------------------------------------- secciones

def capturas_citas(cdp):
    """Corregir una cita cerrada, vista de recepción (pide usuario y contraseña del administrador)."""
    cdp.ir('/agendamiento/citas/citas-index',
           "document.querySelector('#tbl tbody tr button[name=\"btn_corregir\"]') !== null")
    cdp.js("$('#tbl').DataTable().search('Completada').draw(); true")
    time.sleep(0.6)
    cdp.js("const t = document.querySelector('#tbl').closest('.table-responsive') || document.querySelector('#tbl').parentElement; "
           "t.scrollLeft = t.scrollWidth; window.scrollTo(0, 0); true")
    time.sleep(0.3)
    cdp.js("__marcar('#tbl tbody tr:first-child button[name=\"btn_corregir\"]', 1)")
    tarjeta = cdp.js("__rect('#tbl')")
    filas = cdp.js("__rect('#tbl tbody tr', 3)") or cdp.js("__rect('#tbl tbody tr:last-child')")
    cdp.capturar('citas/03_corregir_boton.jpg', y=tarjeta['y'] - 70, alto=filas['y'] + filas['h'] - tarjeta['y'] + 85)

    cdp.js("document.querySelectorAll('.__marca').forEach(m => m.remove()); "
           "document.querySelector('#tbl tbody tr:first-child button[name=\"btn_corregir\"]').click(); true")
    cdp.esperar("document.querySelector('.swal2-popup #corrMotivo') !== null")
    time.sleep(0.6)
    cdp.js("document.getElementById('corrEstado').value = 'AUSENTE'; "
           "document.getElementById('corrMotivo').value = 'El paciente no vino; se marcó completada por error.'; true")
    for sel, n in (('#corrEstado', 2), ('#corrMotivo', 3), ('#corrUsuario', 4), ('.swal2-confirm', 5)):
        cdp.js(f"__marcar('{sel}', {n})")
    cdp.js("__marcar('#corrClave', 0)")
    popup = cdp.js("__rect('.swal2-popup')")
    cdp.capturar('citas/04_corregir.jpg', x=popup['x'] - 50, y=popup['y'] - 15,
                 ancho=popup['w'] + 70, alto=popup['h'] + 30)


def capturas_funcionarios(cdp):
    cdp.ir('/mantenimiento/funcionario/funcionario-index', "document.querySelector('#tbl tbody tr td') !== null")
    cdp.js("__marcar('a[href$=\"funcionario-agregar\"]', 1)")
    tabla = cdp.js("__rect('#tbl')")
    cdp.capturar('funcionarios/01_listado.jpg', y=0, alto=tabla['y'] + 40)

    cdp.ir('/mantenimiento/funcionario/funcionario-agregar', "document.querySelectorAll('#id_cargo option').length > 1")
    # Cargo clínico para que aparezca la sección "Datos de Especialista"
    cdp.js("const s = document.getElementById('id_cargo'); "
           "const o = [...s.options].find(o => /PSICO/i.test(o.text)); if (o) { s.value = o.value; $(s).trigger('change'); } true")
    cdp.esperar("document.getElementById('collapseEspecialista').classList.contains('show')")
    time.sleep(0.8)
    cdp.ajustar_alto()
    for sel, n in (('#txtNombre', 2), ('#id_cargo', 3), ('#txtMatricula', 4), ('#contenedorEspecialidades', 0),
                   ('#btnGuardar', 5)):
        cdp.js(f"__marcar('{sel}', {n})")
    alto = cdp.js("document.getElementById('btnGuardar').getBoundingClientRect().bottom + window.scrollY + 25")
    cdp.capturar('funcionarios/02_formulario.jpg', y=0, alto=alto)


def capturas_consultas(cdp):
    id_consulta = os.getenv('CAPTURAS_ID_CONSULTA', '')
    if not id_consulta:
        raise RuntimeError('Indique CAPTURAS_ID_CONSULTA (una consulta con órdenes, recetas o certificados)')
    cdp.ir(f'/clinico/consulta/consulta-editar/{id_consulta}',
           "document.querySelector('#tbody-ordenes a[title=\"Imprimir\"]') !== null")
    cdp.js("__marcar('#tbody-ordenes a[title=\"Imprimir\"]', 1)")
    bloque = cdp.js("__rect('#tbody-ordenes')")
    cdp.capturar('consultas/02_imprimir_lista.jpg', y=bloque['y'] - 80, alto=bloque['h'] + 110)

    cdp.js("document.querySelectorAll('.__marca').forEach(m => m.remove()); "
           f"ofrecerImprimir('/api/v1/ordenes/0/pdf', 'Orden guardada'); true")
    cdp.esperar("document.querySelector('.swal2-popup a.btn-primary') !== null")
    time.sleep(0.6)
    cdp.js("__marcar('.swal2-popup a.btn-primary', 1)")
    popup = cdp.js("__rect('.swal2-popup')")
    cdp.capturar('consultas/03_imprimir_aviso.jpg', x=popup['x'] - 50, y=popup['y'] - 15,
                 ancho=popup['w'] + 70, alto=popup['h'] + 30)


SECCIONES = {
    'citas': ('RECEPCION', capturas_citas),
    'funcionarios': ('ADMIN', capturas_funcionarios),
    'consultas': ('ADMIN', capturas_consultas),
}


def main(nombres):
    if not CHROME:
        raise SystemExit('No se encontró Chrome ni Edge.')
    credenciales = {
        'RECEPCION': (os.getenv('CAPTURAS_RECEPCION_USER', 'recep2'), os.getenv('CAPTURAS_RECEPCION_PASS', 'Prueba2026!')),
        'ADMIN': (os.getenv('CAPTURAS_ADMIN_USER', 'psicoadmin'), os.getenv('CAPTURAS_ADMIN_PASS')),
    }
    for nombre in nombres or SECCIONES:
        perfil, tarea = SECCIONES[nombre]
        usuario, clave = credenciales[perfil]
        if not clave:
            print(f'[omitida] {nombre}: falta la contraseña (CAPTURAS_{perfil}_PASS)')
            continue
        print(f'[{nombre}] como {usuario}')
        con_navegador(usuario, clave, tarea)


if __name__ == '__main__':
    main(sys.argv[1:])
