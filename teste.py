from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from meu_grafo_lista_adj import *


grafo_paraiba = MeuGrafo()

grafo_paraiba.adiciona_vertice("J")
grafo_paraiba.adiciona_vertice("C")
grafo_paraiba.adiciona_vertice("E")
grafo_paraiba.adiciona_vertice("P")
grafo_paraiba.adiciona_vertice("M")
grafo_paraiba.adiciona_vertice("T")
grafo_paraiba.adiciona_vertice("Z")
grafo_paraiba.adiciona_aresta('a1', 'J', 'C')
grafo_paraiba.adiciona_aresta('a2', 'C', 'E')
grafo_paraiba.adiciona_aresta('a3', 'C', 'E')
grafo_paraiba.adiciona_aresta('a4', 'P', 'C')
grafo_paraiba.adiciona_aresta('a5', 'P', 'C')
grafo_paraiba.adiciona_aresta('a6', 'T', 'C')
grafo_paraiba.adiciona_aresta('a7', 'M', 'C')
grafo_paraiba.adiciona_aresta('a8', 'M', 'T')
grafo_paraiba.adiciona_aresta('a9', 'T', 'Z')

print(grafo_paraiba.dfs("J"))


g