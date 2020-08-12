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
inputShapes.fromFile('shorelines.shp')
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
proximityMetric.setRasterBounds(-180.0458321759259377,180.0458321759196281,-80.000000000000000,85.000000000000000)
proximityMetric.setRasterResolution(1000,900)
proximityMetric.setGradationParameters(15e3, 150e3, 2.0, 0.5)
proximityMetric.calculateLinearGradation()
proximityMetric.writeNetCDF('simplistic_earth_mesh_metric.nc')
#Create domain
domain = qmesh.mesh.Domain()
domain.setGeometry(loopShapes, polygonShapes)
domain.setMeshMetricField(proximityMetric)
domain.setTargetCoordRefSystem('PCC')
#Mesh the domain.
domain.gmsh(geoFilename = 'simplistic_earth.geo',
            fldFilename = 'simplistic_earth.fld',
            mshFilename = 'simplistic_earth.msh')

#Convert mesh into shapefile format, reprojecting the coords to EPSG4326
mesh = qmesh.mesh.Mesh()
mesh.readGmsh('simplistic_earth.msh', 'PCC')
mesh.reProjectVertices('EPSG:4326')
mesh.writeShapefile('simplistic_earth.shp')
