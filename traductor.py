import os
import sys
import io
import warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'
old_stderr = sys.stderr
sys.stderr = io.StringIO()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import argostranslate.translate

sys.stderr = old_stderr

def traducir(texto, from_code, to_code):
    sys.stderr = io.StringIO()
    installed = argostranslate.translate.get_installed_languages()
    from_lang = next((l for l in installed if l.code == from_code), None)
    to_lang = next((l for l in installed if l.code == to_code), None)
    sys.stderr = old_stderr
    if not from_lang or not to_lang:
        return "Error: modelo no encontrado."
    return from_lang.get_translation(to_lang).translate(texto)

class TraductorApp(App):
    title = 'Traduce con Lucia'
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.spinner = Spinner(text='Español -> Ingés', values=['Español -> Inglés', 'Inglés -> Español'], size_hint=(1, 0.1))
        
        layout.add_widget(self.spinner)

        layout.add_widget(Label(text='Texto a traducir: ', size_hint=(1, 0.05)))
        self.entrada = TextInput(size_hint=(1, 0.3), multiline=True)
        layout.add_widget(self.entrada)
        
        btn = Button(text='Traducir: ', size_hint=(1, 0.1))
        btn.bind(on_press=self.traducir_texto)
        layout.add_widget(btn)

        layout.add_widget(Label(text='Traducción: ', size_hint=(1, 0.05)))
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

if __name__ == '__main__':
    TraductorApp().run()