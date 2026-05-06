import os, sys
import os, sys
# Funciona en Android y en Windows
if os.path.exists('/sdcard'):
    log_path = '/sdcard/error_traductor.txt'
else:
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error_traductor.txt')
log_file = open(log_path, 'w')
sys.stderr = log_file
sys.stdout = log_file
print("Iniciando app...")
import warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'
print("Importando Kivy...")
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
print("Importando argostranslate...")
import argostranslate.translate
import argostranslate.package
print("Instalando modelos...")
def instalar_modelos():
    try:
        posibles_dirs = [
            os.path.dirname(os.path.abspath(__file__)),
            os.environ.get('ANDROID_ARGUMENT', ''),
            os.environ.get('ANDROID_PRIVATE', ''),
        ]
        archivos = ['translate-es_en.argosmodel', 'translate-en_es.argosmodel']
        for directorio in posibles_dirs:
            for archivo in archivos:
                ruta = os.path.join(directorio, archivo)
                print(f"Buscando: {ruta} -> existe: {os.path.exists(ruta)}")
                if os.path.exists(ruta):
                    argostranslate.package.install_from_path(ruta)
                    print(f"Instalado: {archivo}")
    except Exception as e:
        print(f"Error instalando modelos: {e}")
instalar_modelos()
def traducir(texto, from_code, to_code):
    try:
        installed = argostranslate.translate.get_installed_languages()
        print(f"Idiomas instalados: {[l.code for l in installed]}")
        from_lang = next((l for l in installed if l.code == from_code), None)
        to_lang = next((l for l in installed if l.code == to_code), None)
        if not from_lang or not to_lang:
            return "Error: modelo no encontrado."
        return from_lang.get_translation(to_lang).translate(texto)
    except Exception as e:
        print(f"Error traduciendo: {e}")
        return f"Error: {e}"
print("Construyendo UI...")
class TraductorApp(App):
    title = 'Traduce con Lucia'
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.spinner = Spinner(
            text='Español -> Inglés',
            values=['Español -> Inglés', 'Inglés -> Español'],
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.spinner)
        layout.add_widget(Label(text='Texto a traducir:', size_hint=(1, 0.05)))
        self.entrada = TextInput(size_hint=(1, 0.3), multiline=True)
        layout.add_widget(self.entrada)
        btn = Button(text='Traducir', size_hint=(1, 0.1))
        btn.bind(on_press=self.traducir_texto)
        layout.add_widget(btn)
        layout.add_widget(Label(text='Traducción:', size_hint=(1, 0.05)))
        self.salida = TextInput(size_hint=(1, 0.3), multiline=True, readonly=True)
        layout.add_widget(self.salida)
        marca = Label(
            text='Adony J. Valiente',
            size_hint=(1, 0.05),
            halign='right',
            valign='middle',
            color=(1, 1, 1, 0.4),
            font_size='12sp'
        )
        marca.bind(size=marca.setter('text_size'))
        layout.add_widget(marca)
        print("UI lista")
        log_file.flush()
        return layout
    def traducir_texto(self, instance):
        texto = self.entrada.text.strip()
        if not texto:
            self.salida.text = "Escribe algo para traducir."
            return
        if self.spinner.text == 'Español -> Inglés':
            self.salida.text = traducir(texto, 'es', 'en')
        else:
            self.salida.text = traducir(texto, 'en', 'es')
print("Lanzando app...")
log_file.flush()
if __name__ == '__main__':
    TraductorApp().run()
