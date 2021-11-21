import networkx as nx
from networkx import NetworkXNoPath
from doctest import testmod
import matplotlib.pyplot as plt

DEFAULT_IN_CASE_THERE_NO_PATH = 77.7


def draw_graph(g, source, target, edges_from_path, prices):
    s = ''
    pos = nx.spring_layout(g, seed=8)
    nx.draw_networkx_nodes(g, pos, node_size=700)
    nx.draw_networkx_nodes(g, pos, nodelist=[source, target], node_color="tab:gray", node_size=700)
    nx.draw_networkx_edges(g, pos, edgelist=[(u, v) for (u, v, d) in g.edges(data=True)], width=6)
    nx.draw_networkx_edges(g, pos, edgelist=edges_from_path, width=6, edge_color="tab:green")
    nx.draw_networkx_labels(g, pos, font_size=20, font_family="sans-serif")
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    # for pair in prices:
    #    s += 'Edge: (', str(pair[0][0]), ', ', str(pair[0][1]), ') ->', str(pair[1]), '\n'

    title = 'graph from ', source, ' to ', target
    # plt.text(1,1,s)
    plt.title(title)
    plt.show()


def vcg_cheapest_path(g, source, target) -> None:
    """
    >>> g1 = nx.Graph()
    >>> g1.add_edge(1, 2, weight=3)
    >>> g1.add_edge(2, 3, weight=1)
    >>> g1.add_edge(3, 4, weight=1)
    >>> g1.add_edge(2, 4, weight=4)
    >>> g1.add_edge(1, 4, weight=10)
    >>> g1.add_edge(1, 3, weight=5)
    >>> vcg_cheapest_path(g1, 1, 4)
    the price of edge  (1, 2)  is:  4
    the price of edge  (2, 3)  is:  2
    the price of edge  (3, 4)  is:  3
    the price of all other edge is: 0
    Total price:  9.0

    >>> g2 = nx.complete_graph(6)
    >>> edge_updates = {}
    >>> for (a,b,_) in g2.edges(data=True):
    ...     edge_updates[a,b] = {'weight':1 }
    >>> nx.set_edge_attributes(g2, edge_updates)
    >>> vcg_cheapest_path(g2, 1, 5)
    the price of edge  (1, 5)  is:  2
    the price of all other edge is: 0
    Total price:  2.0

    >>> g2.remove_edge(1,5)
    >>> vcg_cheapest_path(g2, 1, 5)
    the price of edge  (1, 0)  is:  1
    the price of edge  (0, 5)  is:  1
    the price of all other edge is: 0
    Total price:  2.0

    >>> g3 = nx.Graph()
    >>> g3.add_edge(1, 2, weight=3)
    >>> g3.add_edge(2, 3, weight=1)
    >>> g3.add_edge(3, 4, weight=1)
    >>> vcg_cheapest_path(g3, 1, 4)
    the price of edge  (1, 2)  is:  77.7 because we don't have any path without this edge.
    the price of edge  (2, 3)  is:  77.7 because we don't have any path without this edge.
    the price of edge  (3, 4)  is:  77.7 because we don't have any path without this edge.
    the price of all other edge is: 0
    Total price:  233.1

    >>> g4 = nx.Graph()
    >>> g4.add_edge(1, 2, weight=3)
    >>> g4.add_edge(2, 3, weight=1)
    >>> g4.add_edge(3, 4, weight=1)
    >>> g4.add_edge(2, 4, weight=4)
    >>> vcg_cheapest_path(g4, 1, 4)
    the price of edge  (1, 2)  is:  77.7 because we don't have any path without this edge.
    the price of edge  (2, 3)  is:  3
    the price of edge  (3, 4)  is:  3
    the price of all other edge is: 0
    Total price:  83.7

    """
    prices = {}
    sum_all_price = 0
    weight_sum, path = nx.single_source_dijkstra(g, source=source, target=target, weight='weight')
    edges_from_path = list(zip(path, path[1:] + path[:1]))  # cut the path to edges
    edges_from_path.pop(-1)

    for edge in edges_from_path:
        edge_weight = g[edge[0]][edge[1]]['weight']
        sum_without_edge = weight_sum - edge_weight

        g.remove_edge(edge[0], edge[1])
        price = 0
        try:
            new_path = nx.shortest_path_length(g, source=source, target=target, weight='weight')
            price = new_path - sum_without_edge
            print("the price of edge ", edge, " is: ", price)  # doctest:SKIP
        except NetworkXNoPath:
            price = DEFAULT_IN_CASE_THERE_NO_PATH
            print("the price of edge ", edge, " is: ", price, "because we don't have any path without this edge.")
        finally:
            prices[edge] = price
            g.add_edge(edge[0], edge[1], weight=edge_weight)
            sum_all_price += price
    draw_graph(g, source, target, edges_from_path, prices)
    print("the price of all other edge is: 0 ")
    print("Total price: ", "{:.1f}".format(sum_all_price))  # doctest:SKIP
    print(prices)


if __name__ == '__main__':
    testmod(name='vcg_cheapest_path', verbose=True)
