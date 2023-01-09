from bibgrafo.grafo_matriz_adj_nao_dir import GrafoMatrizAdjacenciaNaoDirecionado
from bibgrafo.grafo_errors import *


class MeuGrafo(GrafoMatrizAdjacenciaNaoDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''
        vertices_naoAd = set()
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                aresta_nova = f'{self.vertices[i]}-{self.vertices[j]}'
                if len(self.matriz[i][j]) == 0:
                    vertices_naoAd.add(aresta_nova)

        return vertices_naoAd

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for i in range(len(self.vertices)):
            if len(self.matriz[i][i]) > 0:
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        grau = 0
        arestas = []
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if (self.matriz[i][j] != {}):
                    for k in self.matriz[i][j]:
                        if self.matriz[i][j][k].rotulo not in arestas:
                            if self.matriz[i][j][k].v1.rotulo == V:
                                grau += 1
                            if self.matriz[i][j][k].v2.rotulo == V:
                                grau += 1
                            arestas.append(self.matriz[i][j][k].rotulo)
        return grau


    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        for i in range(len(self.vertices)):
            for j in range(i, len(self.vertices)):
                if len(self.matriz[i][j]) > 1:
                    return True
        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: O vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        temp = set()

        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if (self.matriz[i][j] != {}):
                    for k in self.matriz[i][j]:
                        V1 = (V == self.matriz[i][j][k].v1.rotulo)
                        V2 = (V == self.matriz[i][j][k].v2.rotulo)
                        if (V1 or V2): temp.add(k)
        return temp

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        if self.ha_laco() or self.ha_paralelas():
            return False

        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                if len(self.matriz[i][j]) == 0:
                    return False
        return True