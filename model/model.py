import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.componente = []
        self.setAlbum = []
        self.graph = None
        self.idmap = {}

    def buildGraph(self, d):
        self.graph = nx.Graph()

        allNodes = DAO.getAllNodes(d)
        for n in allNodes:
            self.idmap[n.AlbumId] = n
        self.graph.add_nodes_from(allNodes)
        self.getAllArchi2(d)


    def getAllArchi(self, d):
        lista = DAO.getAllArchi(d)  # (AlbumId, PlaylistId, TrackId)
        for a1 in lista:
            for a2 in lista:
                if a1[0] != a2[0] and a1[1] == a2[1]:
                    self.graph.add_edge(self.idmap[a1[0]], self.idmap[a2[0]])


    def getAllArchi2(self, d):
        lista = DAO.getAllArchi2(d)
        for a1,a2 in lista:
            self.graph.add_edge(self.idmap[a1], self.idmap[a2])


    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getAllNodes(self):
        return self.graph.nodes()
    # return self.idmap.values()

    def getComponente(self, a1):
        for c in nx.connected_components(self.graph):
            if a1 in c:
                durata = 0
                for album in c:
                    durata += DAO.getDurata(album.AlbumId)[0]
                return len(c), durata

    def getSetAlbum(self, dTot, a1):
        for c in nx.connected_components(self.graph):
            if a1 in c:
                self.componente = c
        self.setAlbum = [a1]
        self.ricorsione(dTot, [a1])
        return self.setAlbum

    def ricorsione(self, dTot, parziale):
        if len(parziale) > len(self.setAlbum):
            self.setAlbum = copy.deepcopy(parziale)
        else:
            for a in self.componente:
                if self.condizione(dTot, a, parziale):
                    parziale.append(a)
                    self.ricorsione(dTot, parziale)
                    parziale.pop()

    def condizione(self, dTot, a, parziale):
        if a in parziale:
            return False
        durata = DAO.getDurata(a.AlbumId)[0]
        for album in parziale:
            durata += DAO.getDurata(album.AlbumId)[0]
        if durata > dTot:
            return False
        return True



