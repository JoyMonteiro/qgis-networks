from pylab import *
from graph_tool.all import *


'''
We want to create a graph which describes the connectivity in a
raster. The nodes in this graph will be the pixels in the raster.
The edges are present for neighbouring nodes, and weights are determined
by a weight function which is passed as an argument to the function.

The nodes in the graph are assigned indices by graph-tool in the order of
their creation. So, we create nodes in the column-first order: the absolute
index of any node corresponding to pixel at location (row,col) will then be

I = row*numCols + col

Edges are created only to nodes that are already created. So, each node will
have edges connecting it to nodes with indices lesser than its own. Since
the graph is not directed, eventually all the required edges will be created.

A weight function is an optional argument, which given two vertex indices, will
return the weight of the edge between them.
'''


def getVertexIndex(row, col, numCols):
    return (row*numCols + col)

def getRowCol(vertexIndex, numCols):

    row = vertexIndex/numCols
    col = vertexIndex%numCols
    return row,col

def createGraph(arr, weightFunction=None):

    numRows, numCols = arr.shape

    g = Graph(directed=False)

    #Add the first node
    g.add_vertex()

    if weightFunction == None:
        # Add first row
        for i in range(1, numCols):
            g.add_vertex()
            e = g.add_edge(g.vertex(getVertexIndex(0,i-1,numCols)), g.vertex(getVertexIndex(0,i,numCols)))

        # Add rest of the rows
        for row in range(1, numRows):
            v = g.add_vertex()
            g.add_edge(v, g.vertex(getVertexIndex(row-1,0,numCols)))

            for col in range(1, numCols):
                v = g.add_vertex()
                g.add_edge(v, g.vertex(getVertexIndex(row, col-1,numCols)))
                g.add_edge(v, g.vertex(getVertexIndex(row-1, col-1,numCols)))
                g.add_edge(v, g.vertex(getVertexIndex(row-1, col,numCols)))


    else:
        edge_cost = g.new_edge_property("double")
        g.edge_properties.edgeCost = edge_cost

        for i in range(1, numCols):
            g.add_vertex()
            e = g.add_edge(g.vertex(getVertexIndex(0,i-1,numCols)), g.vertex(getVertexIndex(0,i,numCols)))

            g.ep.edgeCost[e] = weightFunction(arr, (0, i-1), (0, i))

        # Add rest of the rows
        for row in range(1, numRows):
            v = g.add_vertex()
            e = g.add_edge(v, g.vertex(getVertexIndex(row-1,0,numCols)))
            g.ep.edgeCost[e] = weightFunction(arr, (row, 0), (row-1, 0))


            for col in range(1, numCols):
                v = g.add_vertex()
                e = g.add_edge(v, g.vertex(getVertexIndex(row, col-1,numCols)))
                g.ep.edgeCost[e] = weightFunction(arr, (row, col), (row, col-1))
                e = g.add_edge(v, g.vertex(getVertexIndex(row-1, col-1,numCols)))
                g.ep.edgeCost[e] = weightFunction(arr, (row, col), (row-1, col-1))
                e = g.add_edge(v, g.vertex(getVertexIndex(row-1, col,numCols)))
                g.ep.edgeCost[e] = weightFunction(arr, (row, col), (row-1, col))


    return g

# Main function for testing

if __name__ == "__main__":
    
    a = arange(16)
    a = a.reshape(4,4)

    g = createGraph(a)

    graph_draw(g, vorder=g.vertex_index, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(600,600), output='test.png')

    weights = 10*np.random.random(a.shape)
    print weights

    def weightFn(arr, v1index, v2index):
        return (weights[v1index] + weights[v2index])/2.

    g = createGraph(a, weightFunction=weightFn)

    graph_draw(g, vorder=g.vertex_index, vertex_text=g.vertex_index, vertex_font_size=18, edge_pen_width = g.ep.edgeCost,\
               output_size=(600,600), output='test2.png')

