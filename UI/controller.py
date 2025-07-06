import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.a1 = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        try:
            d = int(self._view._txtInDurata.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserire un intero"))
            self._view.update_page()
            return

        self._model.buildGraph(d)
        self.fillDDAlbum()

        nodi, archi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nodi} nodi e {archi} archi"))
        self._view.update_page()

    def getSelectedAlbum(self, e):
        self.a1 = e.control.data
        print(self.a1)
        
    def fillDDAlbum(self):
        allAlbums = self._model.getAllNodes()
        for a in allAlbums:
            self._view._ddAlbum.options.append(ft.dropdown.Option(key = a, data = a, on_click=self.getSelectedAlbum))
        self._view.update_page()

    def handleAnalisiComp(self, e):
        if self.a1 is None:
            self._view.txt_result.controls.append(ft.Text(f"Album non selezionato"))
            self._view.update_page()
            return
        dim, durata = self._model.getComponente(self.a1)
        self._view.txt_result.controls.append(ft.Text(f"dimensione componente connessa : {dim}, durata complessiva in minuti {durata}"))
        self._view.update_page()


    def handleGetSetAlbum(self, e):
        try:
            dTot = int(self._view._txtInSoglia.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserire un intero"))
            self._view.update_page()
            return

        setAlbum = self._model.getSetAlbum(dTot, self.a1)
        self._view.txt_result.controls.append(ft.Text(f"dimensione set di album: {len(setAlbum)}"))
        for a in setAlbum:
            self._view.txt_result.controls.append(ft.Text(a))
        self._view.update_page()