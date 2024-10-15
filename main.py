from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

estoque = {}


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(
            Label(text="Aplicativo de Controle de Estoque", font_size=24))

        # Botões do menu principal
        self.add_widget(Button(text="Inserir Item",
                        on_press=self.inserir_item))
        self.add_widget(Button(text="Remover Item",
                        on_press=self.remover_item))
        self.add_widget(Button(text="Ver Estoque", on_press=self.ver_estoque))
        self.add_widget(Button(text="Sair", on_press=self.sair_app))

    def sair_app(self, instance):
        App.get_running_app().stop()

    def inserir_item(self, instance):
        self.popup_inserir = Popup(
            title='Inserir Item', content=InsertItemPopup(), size_hint=(0.8, 0.5))
        self.popup_inserir.open()

    def remover_item(self, instance):
        self.popup_remover = Popup(
            title='Remover Item', content=RemoveItemPopup(), size_hint=(0.8, 0.5))
        self.popup_remover.open()

    def ver_estoque(self, instance):
        estoque_str = "Estoque:\n"
        for nome, info in estoque.items():
            estoque_str += f"{nome}: {info['quantidade']} unidades a R${info['valor']:.2f}\n"
        self.popup_estoque = Popup(title='Estoque Completo', content=Label(
            text=estoque_str), size_hint=(0.8, 0.5))
        self.popup_estoque.open()


class InsertItemPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(InsertItemPopup, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text="Nome do Item:"))
        self.nome_input = TextInput()
        self.add_widget(self.nome_input)

        self.add_widget(Label(text="Quantidade Comprada:"))
        self.quantidade_input = TextInput()
        self.add_widget(self.quantidade_input)

        self.add_widget(Label(text="Valor Unitário:"))
        self.valor_input = TextInput()
        self.add_widget(self.valor_input)

        self.add_widget(Button(text="Salvar", on_press=self.salvar_item))

    def salvar_item(self, instance):
        nome = self.nome_input.text
        quantidade = int(self.quantidade_input.text)
        valor = float(self.valor_input.text)

        if nome in estoque:
            estoque[nome]["quantidade"] += quantidade
        else:
            estoque[nome] = {"quantidade": quantidade, "valor": valor}

        self.nome_input.text = ''
        self.quantidade_input.text = ''
        self.valor_input.text = ''

        popup = Popup(title='Sucesso', content=Label(
            text=f"Item {nome} inserido/atualizado com sucesso!"), size_hint=(0.5, 0.5))
        popup.open()


class RemoveItemPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(RemoveItemPopup, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text="Nome do Item:"))
        self.nome_input = TextInput()
        self.add_widget(self.nome_input)

        self.add_widget(Label(text="Quantidade a Remover:"))
        self.quantidade_input = TextInput()
        self.add_widget(self.quantidade_input)

        self.add_widget(
            Button(text="Remover", on_press=self.remover_do_estoque))

    def remover_do_estoque(self, instance):
        nome = self.nome_input.text
        quantidade = int(self.quantidade_input.text)

        if nome in estoque and estoque[nome]["quantidade"] >= quantidade:
            estoque[nome]["quantidade"] -= quantidade
            popup = Popup(title='Sucesso', content=Label(
                text=f"Removido {quantidade} do item {nome}."), size_hint=(0.5, 0.5))
            popup.open()
        else:
            popup = Popup(title='Erro', content=Label(
                text="Item não encontrado ou quantidade insuficiente."), size_hint=(0.5, 0.5))
            popup.open()


class MyApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    MyApp().run()
