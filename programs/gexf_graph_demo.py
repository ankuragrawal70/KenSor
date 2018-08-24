from gexf import Gexf
try:
    gexf = Gexf ("Jianhua Shao", "hello world description")
    graph = gexf.addGraph ("directed", "static", "hello world hints")
    attribute_node = graph.addNodeAttribute("name", "default_value", "type like string")
    attribute_edge = graph.addEdgeAttribute("name", "default_value", "type like boolean")
    n = graph.addNode("0", "node_name")
    n1=graph.addNode("1", "node_name1")
    n1=graph.addNode("2", "node_name2")
    n1=graph.addNode("3", "node_name3")
    #n.addAttribute(attribute_node, "mashup")
    e = graph.addEdge("name", "0", "1")
    
    e.addAttribute(attribute_edge, "true")
    e1 = graph.addEdge("name", "0", "2")
    e2 = graph.addEdge("name", "1", "2")
    e3 = graph.addEdge("name", "2", "3")
    output_file = open("D://programableweb.gexf", "w")
    gexf.write(output_file)
    #outputfile.close()
except:
    print "error"
    pass
"""import networkx as nx
import enchant
import matplotlib.pyplot as plt
g=nx.Graph()
g.add_node(1)
g.add_node(2)
g.add_edge(1,2)
#nx.draw(g)
#nx.draw_random(g)
#nx.draw_circular(g)
#nx.draw_graphviz(g)
#plt.show()
d = enchant.Dict("en_US")
print d.check("hello")
"""
