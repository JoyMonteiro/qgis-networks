from graph_tool import *
from graph_tool.topology import *
import numpy as np


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
            g.add_edge(v, g.vertex(getVertexIndex(row-1,1,numCols)))

            for col in range(1, numCols-1):
                v = g.add_vertex()
                g.add_edge(v, g.vertex(getVertexIndex(row, col-1,numCols)))
                g.add_edge(v, g.vertex(getVertexIndex(row-1, col-1,numCols)))
                g.add_edge(v, g.vertex(getVertexIndex(row-1, col,numCols)))
                e = g.add_edge(v, g.vertex(getVertexIndex(row-1, col+1,numCols)))
                #print row, col, getVertexIndex(row,col,numCols)
                #print [vert for vert in v.all_neighbours()]

            # Add last column
            col = col + 1
            v = g.add_vertex()
            e = g.add_edge(v, g.vertex(getVertexIndex(row, col-1,numCols)))
            e = g.add_edge(v, g.vertex(getVertexIndex(row-1, col-1,numCols)))
            e = g.add_edge(v, g.vertex(getVertexIndex(row-1, col,numCols)))
            print row, col, getVertexIndex(row,col,numCols)
            print [vert for vert in v.all_neighbours()]


    else:
        edge_cost = g.new_edge_property("double")
        g.edge_properties.edgeCost = edge_cost

        # Add first row
        for i in range(1, numCols):
            g.add_vertex()
            e = g.add_edge(g.vertex(getVertexIndex(0,i-1,numCols)), g.vertex(getVertexIndex(0,i,numCols)))

            g.ep.edgeCost[e] = weightFunction(arr, (0, i-1), (0, i))

        # Add rest of the rows
        for row in range(1, numRows):
            v = g.add_vertex()
            e = g.add_edge(v, g.vertex(getVertexIndex(row-1,0,numCols)))
            g.ep.edgeCost[e] = weightFunction(arr, (row, 0), (row-1, 0))
            e = g.add_edge(v, g.vertex(getVertexIndex(row-1,1,numCols)))
            g.ep.edgeCost[e] = weightFunction(arr, (row, 0), (row-1, 1))

            # Add first n-1 columns
            for col in range(1, numCols-1):
                v = g.add_vertex()
                e = g.add_edge(v, g.vertex(getVertexIndex(row, col-1,numCols)))
                g.ep.edgeCost[e] = weightFunction(arr, (row, col), (row, col-1))
                e = g.add_edge(v, g.vertex(getVertexIndex(row-1, col-1,numCols)))
                g.ep.edgeCost[e] = weightFunction(arr, (row, col), (row-1, col-1))
                e = g.add_edge(v, g.vertex(getVertexIndex(row-1, col,numCols)))
                g.ep.edgeCost[e] = weightFunction(arr, (row, col), (row-1, col))
                e = g.add_edge(v, g.vertex(getVertexIndex(row-1, col+1,numCols)))
                g.ep.edgeCost[e] = weightFunction(arr, (row, col), (row-1, col+1))

            # Add last column
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
   
    from graph_tool.draw import *
    a = np.arange(9)
    a = a.reshape(3,3)

    g = createGraph(a)

    print 'Neighbours of 4:'
    v = g.vertex(4)
    print [vert for vert in v.all_neighbours()]

    print 'Neighbours of 7:'
    v = g.vertex(7)
    print [vert for vert in v.all_neighbours()]

    print 'Neighbours of 5:'
    v = g.vertex(5)
    print [vert for vert in v.all_neighbours()]
    graph_draw(g, vorder=g.vertex_index, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(600,600), output='test.png')

    weights = 10*np.random.random(a.shape)
    print weights

    def weightFn(arr, v1index, v2index):
        return (weights[v1index] + weights[v2index])/2.

    g = createGraph(a, weightFunction=weightFn)

    graph_draw(g, vorder=g.vertex_index, vertex_text=g.vertex_index, vertex_font_size=18, edge_pen_width = g.ep.edgeCost,\
               output_size=(600,600), output='test2.png')

    vlist, elist = shortest_path(g, g.vertex(4), g.vertex(8), weights=g.ep.edgeCost)

    shortestPathFilter = g.new_edge_property("bool")
    shortestPathFilterV = g.new_vertex_property("bool")

    for edge in elist:
        shortestPathFilter[edge] = True


    for vertex in vlist:
        shortestPathFilterV[vertex] = True

    g.set_edge_filter(shortestPathFilter)
    g.set_vertex_filter(shortestPathFilterV)

    graph_draw(g, vorder=g.vertex_index, vertex_text=g.vertex_index, vertex_font_size=18, edge_pen_width = g.ep.edgeCost,\
               output_size=(600,600), output='test3.png')
