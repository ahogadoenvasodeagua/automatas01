import networkx as nx
import matplotlib.pyplot as plt

automata = {
    'estados': ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7'],
    'alfabeto': ['0', '1'],
    'inicial': 'q0',
    'finales': ['q2'],
    'transiciones': {
        ('q0', '0'): 'q1',
        ('q0', '1'): 'q5',
        ('q1', '0'): 'q6',
        ('q1', '1'): 'q2',
        ('q2', '0'): 'q0',
        ('q2', '1'): 'q2',
        ('q3', '0'): 'q2',
        ('q3', '1'): 'q6',
        ('q4', '0'): 'q7',
        ('q4', '1'): 'q5',
        ('q5', '0'): 'q2',
        ('q5', '1'): 'q6',
        ('q6', '0'): 'q6',
        ('q6', '1'): 'q4',
        ('q7', '0'): 'q6',
        ('q7', '1'): 'q2',
    }
}


def minimize_dfa(dfa):
    estados = dfa['estados']
    alfabeto = dfa['alfabeto']
    transiciones = dfa['transiciones']
    finales = dfa['finales']

    # Inicialmente, los estados no finales se agrupan juntos y los estados finales se agrupan juntos
    particion = [set(estados) - set(finales), set(finales)]

    cambio = True
    while cambio:
        cambio = False
        nueva_particion = []

        for conjunto in particion:
            grupos = {}

            for estado in conjunto:
                # Encuentra el conjunto al que pertenece cada estado
                grupo_transiciones = []
                for simbolo in alfabeto:
                    siguiente_estado = transiciones.get((estado, simbolo))
                    for idx, subset in enumerate(particion):
                        if siguiente_estado in subset:
                            grupo_transiciones.append(idx)
                            break

                grupo_transiciones = tuple(grupo_transiciones)
                if grupo_transiciones not in grupos:
                    grupos[grupo_transiciones] = {estado}
                else:
                    grupos[grupo_transiciones].add(estado)

            nueva_particion.extend(list(grupo) for grupo in grupos.values())

        if nueva_particion != particion:
            particion = nueva_particion
            cambio = True

    # Construir el nuevo conjunto de estados minimizado
    estados_minimizados = []
    for conjunto in particion:
        estados_minimizados.append(','.join(sorted(list(conjunto))))

    # Construir las transiciones para el DFA minimizado
    transiciones_minimizadas = {}
    for conjunto in particion:
        estado = ','.join(sorted(list(conjunto)))
        for simbolo in alfabeto:
            siguiente_estado = transiciones.get((list(conjunto)[0], simbolo))
            for idx, subset in enumerate(particion):
                if siguiente_estado in subset:
                    nuevo_siguiente_estado = ','.join(sorted(list(subset)))
                    transiciones_minimizadas[(estado, simbolo)] = nuevo_siguiente_estado
                    break
    print("Tabla de transiciones")
    for i in transiciones_minimizadas:
        print(i)

    return {
        'estados': estados_minimizados,
        'alfabeto': alfabeto,
        'inicial': ','.join(sorted(list([estado for estado in particion if dfa['inicial'] in estado][0]))),
        'finales': [','.join(sorted(list(estado))) for estado in particion if any(e in finales for e in estado)],
        'transiciones': transiciones_minimizadas
    }

def dibujar_grafo(automata):
    G = nx.DiGraph()

    for estado in automata['estados']:
        G.add_node(str(estado))

    for transicion, estado_siguiente in automata['transiciones'].items():
        estado_actual, simbolo = transicion
        G.add_edge(str(estado_actual), str(estado_siguiente))

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    # Dibujar el grafo sin marcadores adicionales
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_weight='bold', arrowsize=15)

    # Identificar el estado inicial y los estados finales
    estado_inicial = str(automata['inicial'])
    estados_finales = [str(estado) for estado in automata['finales']]

    # Dibujar flecha al estado inicial
    for node, (x, y) in pos.items():
        if node == estado_inicial:
            plt.annotate('', xy=(x, y), xytext=(x - 0.1, y - 0.1), arrowprops=dict(facecolor='red', shrink=0.05))

    # Dibujar nodos finales con marco doble
    for node, (x, y) in pos.items():
        if node in estados_finales:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=1000, node_color='none', edgecolors='black', linewidths=2)

    plt.title('Autómata Minimizado')
    plt.show()


# Minimizar el autómata
automata_minimizado = minimize_dfa(automata)

# Mostrar el grafo del autómata minimizado con las características solicitadas
dibujar_grafo(automata_minimizado)
