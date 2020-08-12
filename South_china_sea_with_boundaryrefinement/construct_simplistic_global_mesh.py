#Copyright (C) 2018 Alexandros Avdis.
#This work is licensed under a Creative Commons Attribution 4.0 International License.
#https://creativecommons.org/licenses/by/4.0/
#
#This work is published under DOI 10.6084/m9.figshare.7130762
import qmesh
#Initialise qgis API.
qmesh.initialise()
#Read-in coastlines
inputShapes = qmesh.vector.Shapes()
inputShapes.fromFile('south_china_sea_mask.shp')
#Identify line-loops
loopShapes = qmesh.vector.identifyLoops(inputShapes,
                                        isGlobal = True,
                                        defaultPhysID = 3000, 
                                        fixOpenLoops = True)
#Identify Polygons
polygonShapes = qmesh.vector.identifyPolygons(loopShapes,
                                              isGlobal = True)
#Create mesh metric raster.
proximityMetric = qmesh.raster.gradationToShapes()
proximityMetric.setShapes(inputShapes)
proximityMetric.setRasterBounds(-103.0, 121.0, -3.0,25.0)
proximityMetric.setRasterResolution(1000,500)
proximityMetric.setGradationParameters(15e3, 150e3, 2.0, 0.5)
proximityMetric.calculateLinearGradation()
proximityMetric.writeNetCDF('south_china_sea_mesh.nc')
#Create domain
domain = qmesh.mesh.Domain()
domain.setGeometry(loopShapes, polygonShapes)
domain.setMeshMetricField(proximityMetric)
domain.setTargetCoordRefSystem('PCC')
#Mesh the domain.
domain.gmsh(geoFilename = 'south_china_sea_mesh.geo',
            fldFilename = 'south_china_sea_mesh.fld',
            mshFilename = 'south_china_sea_mesh.msh')

#Convert mesh into shapefile format, reprojecting the coords to EPSG4326
mesh = qmesh.mesh.Mesh()
mesh.readGmsh('south_china_sea_mesh.msh', 'PCC')
mesh.reProjectVertices('EPSG:4326')
mesh.writeShapefile('south_china_sea_mesh.shp')
