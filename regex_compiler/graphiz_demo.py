import graphviz
gra = graphviz.Digraph()
gra.node('0', '0')
gra.node('1', '1')
gra.node('2', '2')
gra.edge('0', '1', label = 'a')
gra.edge('1', '2', label = 'b')
gra.edge('2', '2', label = 'b')
gra.render('graph.gv', view = False)