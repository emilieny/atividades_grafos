from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *
from collections import deque
from copy import deepcopy
from math import inf


class MeuGrafo(GrafoListaAdjacencia):

    def prim(self, ):
        prim = MeuGrafo()
        teste = self.ordena()
        test1 = teste[0]
        proximo = self.arestas[test1].v1.rotulo
        visitados = []
        prim.adiciona_vertice(proximo)
        while True:
            if len(self.vertices) == len(prim.vertices):
                break
            sobre = self.arestas_sobre_vertice(proximo)
            menor = inf
            menor_aresta = ''
            for a in sobre:
                if self.arestas[a].peso <= menor:
                    if not prim.existe_rotulo_vertice(self.oposto(proximo, self.arestas[a])):
                        menor_aresta = self.arestas[a]
                        menor = self.arestas[a].peso
            visitados.append(menor_aresta)
            if menor_aresta.v1.rotulo == proximo:
                proximo = menor_aresta.v2.rotulo
            else:
                proximo = menor_aresta.v1.rotulo
            if not prim.existe_rotulo_vertice(proximo):
                prim.adiciona_vertice(proximo)
                prim.adiciona_aresta(menor_aresta)

        return prim

    def oposto(self, V, a):
        if a.v1.rotulo == V:
            V = a.v2.rotulo
            return V
        else:
            V = a.v1.rotulo
            return V

    def Kruskall(self):
        arvore_kruskall = MeuGrafo()
        fila_prioridade = self.bucket_sort_kruskall()
        for v in self.vertices:
            arvore_kruskall.adiciona_vertice(v.rotulo)

        for i in range(len(fila_prioridade)):
            for a in fila_prioridade[i]:
                aresta = self.arestas[a]
                kruskall_dfs = arvore_kruskall.dfs(aresta.v1.rotulo)

                if kruskall_dfs.existe_rotulo_vertice(aresta.v1.rotulo) and kruskall_dfs.existe_rotulo_vertice(
                        aresta.v2.rotulo):
                    pass
                else:
                    arvore_kruskall.adiciona_aresta(aresta)

        return arvore_kruskall

    def ordena(self):
        ordenada = []
        menor = inf
        for a in self.arestas:
            if self.arestas[a].peso <= menor and not a in ordenada:
                menor = self.arestas[a].peso
        while len(ordenada) < len(self.arestas):
            for a in self.arestas:
                if self.arestas[a].peso == menor:
                    ordenada.append(a)
            menor += 1
        return ordenada

    def bucket_sort_kruskall(self):
        lista_pesos = []
        for a in self.arestas:
            if not self.arestas[a].peso in lista_pesos:
                lista_pesos.append(self.arestas[a].peso)
        lista_pesos.sort()
        bucket = list()
        for i in range(len(lista_pesos)):
            bucket.append([])
            for a in self.arestas:
                if self.arestas[a].peso == lista_pesos[i]:
                    bucket[i].append(a)
        return bucket

    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''

        arestasGrafos = set()

        for a in self.arestas:
            arestaAtual = self.arestas[a]
            verticesArestas = f'{arestaAtual.v1.rotulo}-{arestaAtual.v2.rotulo}'
            arestasGrafos.add(verticesArestas)

        vertices_nao_adj = set()
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                novaAresta = f'{self.vertices[i]}-{self.vertices[j]}'
                if novaAresta not in arestasGrafos and novaAresta[::-1] not in arestasGrafos:
                    vertices_nao_adj.add(novaAresta)

        return vertices_nao_adj


    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for a in self.arestas:
            if self.arestas[a].v1 == self.arestas[a].v2:
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        g = 0
        for a in self._arestas:
            if self._arestas[a].v1.rotulo == V:
                g += 1
            if self.arestas[a].v2.rotulo == V:
                g += 1
        return g


    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        arestas = set()

        for a in self.arestas:
            arestaAtual = self.arestas[a]
            verticesArestas = f'{arestaAtual.v1}-{arestaAtual.v2}'

            if verticesArestas in arestas or verticesArestas[::-1] in arestas:
                return True
            arestas.add(verticesArestas)

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
        aux = set()
        for a in self.arestas:
            if self.arestas[a].v1.rotulo == V or self.arestas[a].v2.rotulo == V:
                aux.add(a)

        return aux

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        if self.ha_laco() or self.ha_paralelas():
            return False

        grau_esperado = (len(self.vertices) - 1)
        for i in self.vertices:
            if self.grau(i.rotulo) != grau_esperado:
                return False
        return True


    def gerar_verticesAd(self):
        verticesAd = {}

        for a in self.arestas:
            arestaAtual = self.arestas[a]

            if arestaAtual.v1.rotulo not in verticesAd:
                verticesAd[arestaAtual.v1.rotulo] = [(arestaAtual.v2.rotulo, a)]
            else:
                verticesAd[arestaAtual.v1.rotulo].append((arestaAtual.v2.rotulo, a))

            if arestaAtual.v2.rotulo not in verticesAd:
                verticesAd[arestaAtual.v2.rotulo] = [(arestaAtual.v1.rotulo, a)]
            else:
                verticesAd[arestaAtual.v2.rotulo].append((arestaAtual.v1.rotulo, a))

        return verticesAd


    def dfs_recursivo(self, V, dfs, vertices_visitados, verticesAd):
        vertices_visitados.add(V)

        for (vertices_ad, rotuloAresta) in verticesAd[V]:
            if vertices_ad not in vertices_visitados:
                dfs.adiciona_aresta(rotuloAresta, V, vertices_ad)
                self.dfs_recursivo(vertices_ad, dfs, vertices_visitados, verticesAd)

    def dfs(self, V=''):
        if not self.existe_rotulo_vertice(V):
           raise VerticeInvalidoError

        verticesAd = self.gerar_verticesAd()

        dfs = MeuGrafo(self.vertices[::])
        vertices_visitados = set()

        if V not in verticesAd:
            return dfs
        self.dfs_recursivo(V, dfs, vertices_visitados, verticesAd)
        return dfs


    def bfs(self, V=''):
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        grafo_bfs = MeuGrafo(self.vertices[::])
        verticesPassados = set([V])
        fila = deque([V])

        verticesAdjacentes = self.gerar_verticesAd()

        if V not in verticesAdjacentes:
            return grafo_bfs


        while len(fila) != 0:
            verticeAtual = fila.popleft()

            for (verticeAdjacente, rotuloAresta) in verticesAdjacentes[verticeAtual]:
                if verticeAdjacente not in verticesPassados:
                    grafo_bfs.adiciona_aresta(rotuloAresta, verticeAtual, verticeAdjacente)
                    verticesPassados.add(verticeAdjacente)
                    fila.append(verticeAdjacente)
        return grafo_bfs

    def list_arestas_vertice(self, V):
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        else:
            conjunto = []
            for a in self.arestas:
                if self.arestas[a].v1.rotulo == V or self.arestas[a].v2.rotulo == V:
                    conjunto.append(a)
            return conjunto

    def caminho(self, n):
        V = self._vertices[0].rotulo
        arvore = self.dfs(V)
        caminho = list()
        listArestas = []
        caminho.append(V)
        result, tam = self.aux_caminho_rec(V, arvore, caminho, n, listArestas)
        if tam != n:
            return False
        else:
            return result

    def aux_caminho_rec(self, V, arvore, caminho, n, listArestas):
        arestas_no_vertice = arvore.list_arestas_vertice(V)
        for a in arestas_no_vertice:
            if not a in caminho:
                if V == arvore.arestas[a].v1.rotulo:
                    r = arvore.arestas[a].v2.rotulo
                else:
                    r = arvore.arestas[a].v1.rotulo

                if len(listArestas)+1 < n:
                    if arvore.grau(r) > 1:
                        caminho.append(a)
                        caminho.append(r)
                        listArestas.append(a)
                        self.aux_caminho_rec(r, arvore, caminho, n, listArestas)
                    else:
                        caminho.append(a)
                        caminho.append(r)
                        listArestas.append(a)
                        return caminho
        return caminho, len(listArestas)

    def ha_ciclo(self):

        for a in self.arestas:
            retorno = set()
            ciclo = MeuGrafo()
            V = self.arestas[a].v1.rotulo
            ciclo.adiciona_vertice(V)

            return self.ciclo_rec(retorno, V, ciclo)

    def ciclo_rec(self, retorno, V, ciclo):

        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        if len(retorno) > 0:
            return True

        if len(self.vertices) == len(ciclo.vertices):
            return False

        rotulo = self.arestas_sobre_vertice(V)
        rotulos = list(rotulo)
        rotulos.sort()

        for a in rotulos:
            if not ciclo.existe_rotulo_vertice(a):
                if V == self.arestas[a].v1.rotulo:
                    r = self.arestas[a].v2.rotulo
                else:
                    r = self.arestas[a].v1.rotulo

                if ciclo.existe_rotulo_vertice(r):
                    retorno.add(r)
                else:
                    ciclo.adiciona_vertice(r)
                    ciclo.adiciona_aresta(self.arestas[a])
                self.ciclo_rec(retorno, r, ciclo)
        return ciclo

    def conexo(self):
        if len(self.vertices) == 0:
            return False

        arvore = self.dfs(self.vertices[0].rotulo)
        return len(self.vertices) == len(arvore.vertices)

    def menor_peso(self, arestas_adj):
        menor = inf

        for a in arestas_adj:
            if self.arestas[a].peso <= menor:
                if self.arestas[a].peso == menor:
                    if self.arestas[a].rotulo < self.arestas[ares_ret].rotulo:
                        menor = self.arestas[a].peso
                        ares_ret = a
                else:
                    menor = self.arestas[a].peso
                    ares_ret = a

        return ares_ret

    def vert_oposto(self, vert, a):
        for v in vert:
            if v.rotulo == self._arestas[a].v1.rotulo:
                r = self._arestas[a].v2.rotulo
                return r
            elif v.rotulo == self._arestas[a].v2.rotulo:
                r = self._arestas[a].v1.rotulo
                return r

    def prim(self):
        arvore_prim = MeuGrafo()
        v = self.vertices[0].rotulo
        arvore_prim.adiciona_vertice(v)

        ares_vis = set()
        while len(arvore_prim.vertices) < len(self.vertices):
            ares_adj = set()
            for r in arvore_prim.vertices:
                for a in self.arestas_sobre_vertice(r.rotulo):
                    if not arvore_prim.existe_rotulo_aresta(a) and not a in ares_vis:
                        ares_adj.add(a)
            menor_peso = self.menor_peso(ares_adj)
            ares_vis.add(menor_peso)
            r = self.vert_oposto(arvore_prim.vertices, menor_peso)
            if not arvore_prim.existe_rotulo_vertice(r):
                arvore_prim.adiciona_vertice(r)
                arvore_prim.adiciona_aresta(self._arestas[menor_peso])
        return arvore_prim

    def prim_modificado(self):
        arvore_prim = MeuGrafo()
        v = self.arestas[self.menor_peso(self.arestas)].v1.rotulo
        arvore_prim.adiciona_vertice(v)

        ares_vis = set()
        while len(arvore_prim.vertices) < len(self.vertices):
            ares_adj = set()
            for r in arvore_prim.vertices:
                for a in self.arestas_sobre_vertice(r.rotulo):
                    if not arvore_prim.existe_rotulo_aresta(a) and not a in ares_vis:
                        ares_adj.add(a)
            menor_peso = self.menor_peso(ares_adj)
            ares_vis.add(menor_peso)
            r = self.vert_oposto(arvore_prim.vertices, menor_peso)
            if not arvore_prim.existe_rotulo_vertice(r):
                arvore_prim.adiciona_vertice(r)
                arvore_prim.adiciona_aresta(self._arestas[menor_peso])
        return arvore_prim

    def ordena(self):
        ordenada = []
        menor = inf
        while len(ordenada) < len(self.arestas):
            for a in self.arestas:
                if self.arestas[a].peso <= menor and not a in ordenada:
                    menor = self.arestas[a].peso
            for a in self.arestas:
                if self.arestas[a].peso == menor:
                    ordenada.append(a)
            menor += 1
        return ordenada

    def kruskall(self):
        arvore_kruskall = MeuGrafo()
        fila_prioridade = self.ordena()
        for v in self.vertices:
            arvore_kruskall.adiciona_vertice(v.rotulo)

        for a in fila_prioridade:
            aresta = self.arestas[a]
            kruskall_dfs = arvore_kruskall.dfs(aresta.v1.rotulo)

            if kruskall_dfs.existe_rotulo_vertice(aresta.v1.rotulo) and kruskall_dfs.existe_rotulo_vertice(
                    aresta.v2.rotulo):
                pass
            else:
                arvore_kruskall.adiciona_aresta(aresta)

        return arvore_kruskall

    def bucket_sort_kruskall(self):
        lista_pesos = []
        for a in self.arestas:
            if not self.arestas[a].peso in lista_pesos:
                lista_pesos.append(self.arestas[a].peso)
        lista_pesos.sort()
        bucket = list()
        for i in range(len(lista_pesos)):
            bucket.append([])
            for a in self.arestas:
                if self.arestas[a].peso == lista_pesos[i]:
                    bucket[i].append(a)
        return bucket

    def kruskall_modificado(self):
        arvore_kruskall = MeuGrafo()
        fila_prioridade = self.bucket_sort_kruskall()
        for v in self.vertices:
            arvore_kruskall.adiciona_vertice(v.rotulo)

        for i in range(len(fila_prioridade)):
            for a in fila_prioridade[i]:
                aresta = self.arestas[a]
                kruskall_dfs = arvore_kruskall.dfs(aresta.v1.rotulo)

                if kruskall_dfs.existe_rotulo_vertice(aresta.v1.rotulo) and kruskall_dfs.existe_rotulo_vertice(
                        aresta.v2.rotulo):
                    pass
                else:
                    arvore_kruskall.adiciona_aresta(aresta)

        return arvore_kruskall