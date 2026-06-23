from model.model import Model
from UI.view import View
import flet as ft

class Controller:
    def __init__(self, view : View, model : Model):
        self._view = view
        self._model = model

    def handler_crea_grafo(self, e):
        try:
            n_min_bus = int(self._view._txt_nBus.value)
        except ValueError:
            self._view.show_alert("Inserire un numero valido.")

        if n_min_bus <= 0:
            self._view.show_alert("Inserire un numero maggiore di zero.")
        else:
            self._model.build_graph(n_min_bus)
            self._view._lst_result.controls.clear()
            self._view._lst_result.controls.append(ft.Text(f"Grafo correttamente creato. Nodi: {self._model._graph.number_of_nodes()}  - Archi: {self._model._graph.number_of_edges()}"))
            self._view._btnUtentiConnessi.disabled = False
            self._view._ddUtente.disabled = False
            self._view._txtL.disabled = False
            self._view._ddUtente.options = [ft.dropdown.Option(self._model.id_user_map[n]) for n in self._model.nodes]
            self._view.update_page()


    def handler_utenti_connessi(self, e):
        connessi = self._model.get_connessi()

        self._view._lst_result.controls.clear()
        for c in connessi:
            self._view._lst_result.controls.append(ft.Text(f"{c.name} ({c.user_id}) - strength ="))
            self._view.update_page()

    def handle_crea_grafo(self,e):
        try:
            lun = int(self._view._txtL.value)
        except ValueError:
            self._view.show_alert("Inserire un numero valido.")

        best_path, best_score = self._model.compute_best_path(lun)



