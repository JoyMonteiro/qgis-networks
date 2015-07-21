from rasterGraphCreate import *
import matplotlib

from matplotlib import pyplot

if __name__ == "__main__":
    
    arraySize = 100

    startNode = 4
    destNode = 8080

    startNode1 = 90
    destNode1 = 8008

    startNode2 = 390
    destNode2 = 9080

    startNode3 = 450
    destNode3 = 9000

    raster = np.zeros((arraySize,arraySize))

    measureX = np.linspace(0,5, arraySize)
    measureY = measureX.copy()
    kx,ky = np.meshgrid(measureX, measureY)

    raster += np.exp(-pow(kx-0.5, 2)/.5  - pow(ky-2.5,2)/2.)
    raster += np.exp(-pow(kx-2.5, 2)/.5  - pow(ky-2.5,2)/2.)
    raster += np.exp(-pow(kx-4.5, 2)/.5  - pow(ky-2.5,2)/2.)
    #raster += np.exp(-pow(measureX-0.5, 2)/5.  - pow(measureY-0.7,2)/5.)

    raster += 0.1*np.random.random(raster.shape)

    pyplot.ion()
    pyplot.imshow(raster.transpose(),cmap=pyplot.cm.coolwarm)

    def weightFn(arr, v1index, v2index):
        return (raster[v1index] + raster[v2index])/2.

    g = createGraph(raster, weightFunction=weightFn)


    vlist, elist = shortest_path(g, g.vertex(startNode), g.vertex(destNode), weights=g.ep.edgeCost)
    print g.vertex(4)
    print [vert for vert in g.vertex(destNode).out_neighbours()]

    xs = []
    ys = []
    for vertex in vlist:
        index = g.vertex_index[vertex]
        row,col = getRowCol(index, arraySize)

        xs.append(row)
        ys.append(col)

    pyplot.hold(True)

    pyplot.plot(xs, ys,'white',linewidth=2)

    vlist, elist = shortest_path(g, g.vertex(startNode1), g.vertex(destNode1), weights=g.ep.edgeCost)
    print g.vertex(4)
    
    print [vert for vert in g.vertex(destNode).out_neighbours()]

    xs = []
    ys = []
    for vertex in vlist:
        index = g.vertex_index[vertex]
        row,col = getRowCol(index, arraySize)

        xs.append(row)
        ys.append(col)

    pyplot.hold(True)

    pyplot.plot(xs, ys,'red',linewidth=2)


    vlist, elist = shortest_path(g, g.vertex(startNode3), g.vertex(destNode3), weights=g.ep.edgeCost)
    
    xs = []
    ys = []
    for vertex in vlist:
        index = g.vertex_index[vertex]
        row,col = getRowCol(index, arraySize)

        xs.append(row)
        ys.append(col)

    pyplot.hold(True)

    pyplot.plot(xs, ys,'g',linewidth=2)




    vlist, elist = shortest_path(g, g.vertex(startNode2), g.vertex(destNode2), weights=g.ep.edgeCost)
    
    xs = []
    ys = []
    for vertex in vlist:
        index = g.vertex_index[vertex]
        row,col = getRowCol(index, arraySize)

        xs.append(row)
        ys.append(col)

    pyplot.hold(True)

    pyplot.plot(xs, ys,'k',linewidth=2)


    pyplot.xlim(-1,arraySize)
    pyplot.ylim(0,arraySize)
    pyplot.show()
