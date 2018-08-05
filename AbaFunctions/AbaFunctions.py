# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior


def Make_Flat_Specimen_Model():

    s = mdb.models['Flat_Specimen'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(0.0, 0.0), point2=(-50, 5.0))
    s.FixedConstraint(entity=v[0])
    
    p = mdb.models['Flat_Specimen'].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    
    p.BaseSolidExtrude(sketch=s, depth=200.0)

    f = p.faces
    
    p.DatumPlaneByOffset(plane=f[4], flip=SIDE1, offset=10.0)
    
    e, d1 = p.edges, p.datums
    
    t = p.MakeSketchTransform(sketchPlane=d1[2], sketchUpEdge=e[7], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-25.0, 2.5, 
        210.0))
    
    s1 = mdb.models['Flat_Specimen'].ConstrainedSketch(name='__profile__', 
        sheetSize=434.3, gridSpacing=10.85, transform=t)
    
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    
    s1.setPrimaryObject(option=SUPERIMPOSE)
    
    e1, p1 = p.edges, p.elemEdges
    
    s1.Line(point1=(-100, -1.5), point2=(
        100, -1.5))

    s1.Line(point1=(-100, -0.5), point2=(
        100, -0.5))
        
    s1.Line(point1=(-100, 0.5), point2=(100, 
        0.5))
    
    s1.Line(point1=(-100, 1.5), point2=(100,
        1.5))
    
    e, d2 = p.edges, p.datums
    
    p.Wire(sketchPlane=d2[2], sketchUpEdge=e[7], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1)
    
    s1.unsetPrimaryObject()
    
    del mdb.models['Flat_Specimen'].sketches['__profile__']

    p = mdb.models['Flat_Specimen'].parts['Part-1']
    p.DatumCsysByThreePoints(name='Datum csys-1', coordSysType=CARTESIAN, origin=(
        0.0, 0.0, 0.0), line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))

    p = mdb.models['Flat_Specimen'].parts['Part-1']
    c = p.cells

    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )

    e1, d1 = p.edges, p.datums

    pickedEdges =(e1[0], )

    p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    
    c = p.cells
    
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e, d2 = p.edges, p.datums
    
    pickedEdges =(e[3], )
    p.PartitionCellByExtrudeEdge(line=d2[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, d1 = p.edges, p.datums
    
    pickedEdges =(e1[1], )
    
    p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)

    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e, d2 = p.edges, p.datums
    pickedEdges =(e[4], )
    p.PartitionCellByExtrudeEdge(line=d2[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)

def material():

    mdb.models['Flat_Specimen'].Material(name='GFRP_Vacuum')
    mdb.models['Flat_Specimen'].materials['GFRP_Vacuum'].Elastic(
        type=ENGINEERING_CONSTANTS, table=((44800.0, 12000.0, 12000.0, 0.3, 
        0.3, 0.1, 5000.0, 5000.0, 5000.0), ))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=353.179, 
        farPlane=540.333, width=60.4153, height=33.8254, viewOffsetX=59.1911, 
        viewOffsetY=25.8288)
    layupOrientation = mdb.models['Flat_Specimen'].parts['Part-1'].datums[4]
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
    region1=regionToolset.Region(cells=cells)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
    region2=regionToolset.Region(cells=cells)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    region3=regionToolset.Region(cells=cells)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    region4=regionToolset.Region(cells=cells)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region5=regionToolset.Region(cells=cells)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#200000 ]', ), )
    normalAxisRegion = p.Surface(side1Faces=side1Faces, name='Set_Surf_Top')
    primaryAxisDatum=mdb.models['Flat_Specimen'].parts['Part-1'].datums[4].axis3
    
def MakeComposite():

    compositeLayup = mdb.models['Flat_Specimen'].parts['Part-1'].CompositeLayup(
        name='VacuumInfused', description='', elementType=SOLID, 
        symmetric=False, thicknessAssignment=FROM_SECTION)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-1', region=region1, 
        material='GFRP_Vacuum', thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=1)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-2', region=region2, 
        material='GFRP_Vacuum', thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=90.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=1)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-3', region=region3, 
        material='GFRP_Vacuum', thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=1)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-4', region=region4, 
        material='GFRP_Vacuum', thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=90.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=1)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-5', region=region5, 
        material='GFRP_Vacuum', thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=1)
    compositeLayup.ReferenceOrientation(orientationType=DISCRETE, localCsys=None, 
        additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', axis=AXIS_3, stackDirection=STACK_3, 
        normalAxisDefinition=SURFACE, normalAxisRegion=normalAxisRegion, 
        normalAxisDirection=AXIS_3, flipNormalDirection=False, 
        primaryAxisDefinition=DATUM, primaryAxisDatum=primaryAxisDatum, 
        primaryAxisDirection=AXIS_1, flipPrimaryDirection=False)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    a = mdb.models['Flat_Specimen'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models['Flat_Specimen'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=336.921, 
        farPlane=556.592, width=193.847, height=108.531, viewOffsetX=-15.5067, 
        viewOffsetY=-16.2523)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e = p.edges
    RemoveWireEdges = e.getSequenceFromMask(mask=('[#10 ]', ), )
    p.RemoveWireEdges(wireEdgeList=RemoveWireedges)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=348.156, 
        farPlane=544.559, width=95.3321, height=53.3745, viewOffsetX=-39.7874, 
        viewOffsetY=-24.9527)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e = p.edges
    RemoveWireEdges = e.getSequenceFromMask(mask=('[#2 ]', ), )
    p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e = p.edges
    RemoveWireEdges = e.getSequenceFromMask(mask=('[#4 ]', ), )
    p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e = p.edges
    RemoveWireEdges = e.getSequenceFromMask(mask=('[#1 ]', ), )
    p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e = p.edges
    RemoveWireEdges = e.getSequenceFromMask(mask=('[#1 ]', ), )
    p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=334.04, 
        farPlane=559.125, width=266.338, height=149.118, viewOffsetX=18.366, 
        viewOffsetY=-1.95097)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    f1 = p.faces
    p.DatumPlaneByOffset(plane=f1[21], flip=SIDE1, offset=20.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=339.518, 
        farPlane=548.019, width=121.104, height=67.8038, viewOffsetX=-7.80943, 
        viewOffsetY=-16.9339)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e1, d1 = p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=d1[20], sketchUpEdge=e1[5], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-25.0, 25.0, 
        100.0))
    s = mdb.models['Flat_Specimen'].ConstrainedSketch(name='__profile__', 
        sheetSize=456.34, gridSpacing=11.4, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=407.105, 
        farPlane=505.584, width=251.501, height=140.81, cameraPosition=(
        -10.0224, 468.719, 147.01), cameraTarget=(-10.0224, 12.375, 147.01))
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e, p2 = p.edges, p.elemEdges
    p.projectEdgesOntoSketch(sketch=s, edges=(e[5], ))
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e1, p1 = p.edges, p.elemEdges
    p.projectEdgesOntoSketch(sketch=s, edges=(e1[21], ))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=409.302, 
        farPlane=503.387, width=236.411, height=132.362, cameraPosition=(
        1.43311, 468.719, 102.328), cameraTarget=(1.43311, 12.375, 102.328))
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(-8.55, 5.7))
    s.DistanceDimension(entity1=v[3], entity2=g[2], textPoint=(16.7442102432251, 
        16.7571029663086), value=25.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=378.994, 
        farPlane=533.695, width=503.157, height=281.708, cameraPosition=(
        32.8297, 468.719, 101.411), cameraTarget=(32.8297, 12.375, 101.411))
    s.DistanceDimension(entity1=v[3], entity2=g[3], textPoint=(-72.1155700683594, 
        -78.3894348144531), value=100.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=404.265, 
        farPlane=508.424, width=271.008, height=151.732, cameraPosition=(
        16.6741, 468.719, 84.223), cameraTarget=(16.6741, 12.375, 84.223))
    s.RadialDimension(curve=g[4], textPoint=(47.3156471252441, -5.57136535644531), 
        radius=10.0)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e, d2 = p.edges, p.datums
    p.Wire(sketchPlane=d2[20], sketchUpEdge=e[5], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models['Flat_Specimen'].sketches['__profile__']
    session.viewports['Viewport: 1'].view.setValues(nearPlane=324.763, 
        farPlane=562.629, width=244.401, height=136.835, viewOffsetX=60.5205, 
        viewOffsetY=33.9913)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    del p.features['Wire-2']
    session.viewports['Viewport: 1'].view.setValues(nearPlane=339.381, 
        farPlane=548.155, width=122.048, height=68.3323, viewOffsetX=-5.84335, 
        viewOffsetY=-5.10329)
    p = mdb.models['Flat_Specimen'].parts['Part-1']
    e1, d1 = p.edges, p.datums
    p.HoleThruAllFromEdges(plane=d1[20], edge1=e1[21], edge2=e1[5], 
        planeSide=SIDE1, diameter=20.0, distance1=100.0, distance2=25.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=328.724, 
        farPlane=558.812, width=219.481, height=122.883, viewOffsetX=18.8129, 
        viewOffsetY=9.52637)
    mdb.save()


