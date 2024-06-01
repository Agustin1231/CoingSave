from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import sqlite3

conexion = sqlite3.connect("ahorro")
cursor = conexion.cursor()

cursor.execute("create table if not exists registroAhorro(Cantidad int)")

class IngresarAhorro(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint= (1, .5) 
        self.orientation= "vertical"
        self.spacing = "25dp"
        self.padding= ("0dp", "15dp")

        cursor.execute("SELECT SUM(cantidad) FROM registroAhorro")
        resultado = cursor.fetchone()
        total_ahorrado = resultado[0] if resultado[0] is not None else 0

        self.label = Label(
            text=  f"$ {total_ahorrado}",
            font_size= "24dp",
            color= "#38DA4C"
        )

        self.ahorro = TextInput(
            size_hint= (1 ,.25),
            pos_hint= {"center_x": .5},
            padding= ("15dp", "10dp"),
            multiline= False,
            input_type = 'number',
            font_size= "14dp",
            hint_text = "¿Cuánto ahorraste?",
            background_color= "#292A2E",
            hint_text_color= "#797B86"
        )

        self.ahorrar = Button(
            text= "Ahorrar",
            size_hint= (1 ,.25),
            pos_hint= {"center_x": .5}, 
            background_normal = '', 
            font_size= "14dp",
            background_color= "#38DA4C",
            color="#1A3B12"
        )

        self.ahorrar.bind(on_press=self.agregarAhorro)

        self.add_widget(self.label)
        self.add_widget(self.ahorro)
        self.add_widget(self.ahorrar)


    def agregarAhorro(self, instance):
        if self.ahorro.text == "" or not self.ahorro.text.isdigit():
            self.ahorro.text= ""
        else: 
            cantidadAhorrada = (int(self.ahorro.text),)  # Convertir a entero y crear una tupla de un solo elemento
            cursor.execute("INSERT INTO registroAhorro (cantidad) VALUES (?)", cantidadAhorrada)
            conexion.commit()

            cursor.execute("SELECT SUM(cantidad) FROM registroAhorro")
            resultado = cursor.fetchone()
            total_ahorrado = resultado[0] if resultado[0] is not None else 0

            self.label.text = f"$ {total_ahorrado}"
            self.ahorro.text= ""

class CoingSave(App):
    pass

CoingSave().run()
