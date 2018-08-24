import networkx as nx
import dmoz_data
#import matplotlib.pyplot as plt
def model_graph(parent,root,g):
    if len(root.child)>0:
        for c in root.child:
            x=root.child[c]
            g.add_node(c)
            g.add_edge(parent,c,weight=x)

            #g.add_nodes_from([n_name,child])
        #for level in root.references:
         #   obj=category[level]
           # model_graph(obj,g)

def graph_plot():
    for node_check in main_cat:
        v=main_cat[node_check]
        model_graph(node_check,v,g)

g=nx.DiGraph()
graph_plot()
nx.draw(g)
#plt.show()
graph_pos=nx.spring_layout(g)
nx.draw_networkx_nodes(g,graph_pos,node_size=2000,
                           alpha=0.3, node_color='blue')
nx.draw_networkx_edges(g,graph_pos,width=1,
                           alpha=0.3,edge_color='red')
nx.draw_networkx_labels(g, graph_pos,font_size=12,
                            font_family='sans-serif')
#if 'business' in g:
print nx.dfs_successors(g,'business')
plt.show()