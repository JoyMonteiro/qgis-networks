import rasterio
import fiona

def readFeature(shapeFile, feature='Point'):
    """Read all the points and their properties from a vector shape file
    
    :param shapeFile: name of a file to read from
    :param feature: either 'Point', 'Linestring' or 'Polygon' for now
    :returns: a list of feature coordinates and their names
    
    """
    
    with fiona.open(shapeFile) as shpFile:
        allFeatures = list(shpFile)
    
    coordinates = []
    names = []
    
    print 'Number of features: ', len(allFeatures)
    for p in allFeatures:
        if p['geometry']['type'] == feature:
            
            if feature is 'Polygon':
                coords = p['geometry']['coordinates'][0]
                coordinates.append(coords)
            elif feature is 'MultiPolygon':
                coords = p['geometry']['coordinates'][0][0]
                coordinates.append(coords)
            else:
                coords = p['geometry']['coordinates']
                coordinates.append(coords)
            
            if 'Name' in p['properties'].keys(): 
                names.append(p['properties']['Name'])
    
    return names, coordinates
    

def writeRasterFile(outputArray, outputFilename, refRaster):
    
    with rasterio.open(refRaster) as src:
        kwargs = src.meta
        
    with rasterio.open(outputFilename, 'w', **kwargs) as dst:
        dst.write_band(1, outputArray.astype(kwargs['dtype']))


def writeShapeFile(fileName, featureList, propertyDict, featureType='LineString', **kwargs):
    """ Write a shapefile containing all features in list.

    :param featureList: a list of vector features to write
    :param featureType: what kind of feature is contained
    :param propertyDict: dict containing properties available in kwargs and their types
    :param kwargs: set of key-value pairs, which contain the properties for the
    corresponding feature

    """

    #setup basic metadata

    meta = {}
    meta['crs'] = {'init' : u'epsg:4326'}
    meta['driver'] = u'ESRI Shapefile'

    #setup schema
    schema = {}
    schema['geometry'] = featureType
    schema['properties'] = propertyDict

    meta['schema'] = schema

    shapefile = fiona.open(fileName, 'w', **meta)

    for index in range(len(featureList)):

        record = {}
        geom = {}

        feature = featureList[index]
        geom['coordinates'] = feature
        geom['type'] = featureType
        record['geometry'] = geom
    
        props = {}

        for key in kwargs.keys():
            props[key] = kwargs[key][index]

        record['properties'] = props

        shapefile.write(record)

    shapefile.close()


