#from AbaFunctions.AbaFunctions import AbaFunctions as Af
#Af=Af()

#Af.Make_Flat_Specimen_Model()

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

#---- Make a part 3D solid ekstrusion ----

s = mdb.models['Flat_Specimen'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)

g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

#---- Edit sketch created above ------

s.setPrimaryObject(option=STANDALONE)

s.rectangle(point1=(0.0, 0.0), point2=(-50, 5.0))

#---- Make a part ----

p = mdb.models['Flat_Specimen'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)

p = mdb.models['Flat_Specimen'].parts['Part-1']

#---- Make an extrusion in p of s -----

p.BaseSolidExtrude(sketch=s, depth=200.0)

#----- Define faces on p, edges on p and datums on p and Datumplane for wires -----

f = p.faces

p.DatumPlaneByOffset(plane=f[4], flip=SIDE1, offset=10.0)

e, d1 = p.edges, p.datums

#------ Define sketch in datumplane called s1 and define all objects inside s1 -----

t = p.MakeSketchTransform(sketchPlane=d1[2], sketchUpEdge=e[7], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-25.0, 2.5, 
    210.0))

s1 = mdb.models['Flat_Specimen'].ConstrainedSketch(name='__profile__', 
    sheetSize=434.3, gridSpacing=10.85, transform=t)

g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints

#----- Draw lines -----#

s1.Line(point1=(-100, -1.5), point2=(
    100, -1.5))

s1.Line(point1=(-100, -0.5), point2=(
    100, -0.5))
    
s1.Line(point1=(-100, 0.5), point2=(100, 
    0.5))

s1.Line(point1=(-100, 1.5), point2=(100,
    1.5))

#----- Reset what p.datums is -------#

e, d2 = p.edges, p.datums

p.Wire(sketchPlane=d2[2], sketchUpEdge=e[7], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s1)

s1.unsetPrimaryObject()

#----- unsets the past profile from mdb -----

del mdb.models['Flat_Specimen'].sketches['__profile__']

p = mdb.models['Flat_Specimen'].parts['Part-1']

p.DatumCsysByThreePoints(name='Datum csys-1', coordSysType=CARTESIAN, origin=(
    0.0, 0.0, 0.0), line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))

#----- Lets Partition ---------

c = p.cells

pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
e1, d1 = p.edges, p.datums
pickedEdges =(e1[0], )
p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
    edges=pickedEdges, sense=REVERSE)

pickedCells = c.getSequenceFromMask(mask=('[#3 ]', ), )
e, d = p.edges, p.datums
pickedEdges =(e[3], )
p.PartitionCellByExtrudeEdge(line=d[4].axis3, cells=pickedCells, 
    edges=pickedEdges, sense=REVERSE)

pickedCells = c.getSequenceFromMask(mask=('[#7 ]', ), )
e1, d1 = p.edges, p.datums
pickedEdges =(e1[1], )
p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
    edges=pickedEdges, sense=REVERSE)

pickedCells = c.getSequenceFromMask(mask=('[#f ]', ), )
e, d = p.edges, p.datums
pickedEdges =(e[2], )
p.PartitionCellByExtrudeEdge(line=d[4].axis3, cells=pickedCells, 
    edges=pickedEdges, sense=REVERSE)

#----- Lets make hole ------

p = mdb.models['Flat_Specimen'].parts['Part-1']
f, e = p.faces, p.edges
p.HoleThruAllFromEdges(plane=f[21], edge1=e[44], edge2=e[45], planeSide=SIDE1, 
    diameter=20.0, distance1=100.0, distance2=25.0)

#----- Lets make mesh partitions -----



#----- Remove wire edges -----

e = p.edges
RemoveWireEdges = e.getSequenceFromMask(mask=('[#70 ]', ), )
p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)
RemoveWireEdges = e.getSequenceFromMask(mask=('[#f ]', ), )
p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)

#------ Make Material ------

mdb.models['Flat_Specimen'].Material(name='GFRP')
mdb.models['Flat_Specimen'].materials['GFRP'].Elastic(
    type=ENGINEERING_CONSTANTS, table=((40000.0, 5000.0, 5000.0, 0.3, 0.3, 
    0.3, 5000.0, 5000.0, 5000.0), ))

#------ Make Section -------

sectionLayer1 = section.SectionLayer(material='GFRP', thickness=1.0, 
    orientAngle=0.0, numIntPts=1, plyName='Layer')
mdb.models['Flat_Specimen'].CompositeSolidSection(name='Sect_VacInf', 
    layupName='', symmetric=False, layup=(sectionLayer1, ))

#------ Assign Sections --------

p = mdb.models['Flat_Specimen'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#80700 ]', ), )
region = p.Set(cells=cells, name='Set_Layer_1')
p = mdb.models['Flat_Specimen'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

cells = c.getSequenceFromMask(mask=('[#40888 ]', ), )
region = p.Set(cells=cells, name='Set_Layer_2')
p = mdb.models['Flat_Specimen'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

cells = c.getSequenceFromMask(mask=('[#21044 ]', ), )
region = p.Set(cells=cells, name='Set_Layer_3')
p = mdb.models['Flat_Specimen'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

cells = c.getSequenceFromMask(mask=('[#12022 ]', ), )
region = p.Set(cells=cells, name='Set_Layer_4')
p = mdb.models['Flat_Specimen'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

cells = c.getSequenceFromMask(mask=('[#c011 ]', ), )
region = p.Set(cells=cells, name='Set_Layer_5')
p = mdb.models['Flat_Specimen'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

#------ Make material orientation coordinate systems ------

p = mdb.models['Flat_Specimen'].parts['Part-1']
d2 = p.datums
p.DatumCsysByTwoLines(CARTESIAN, line1=d2[4].axis3, line2=d2[4].axis1, 
    name='CSYS_0deg')

p = mdb.models['Flat_Specimen'].parts['Part-1']
d = p.datums
p.DatumCsysByTwoLines(CARTESIAN, line1=d[4].axis1, line2=d[4].axis3, 
    name='CSYS_90deg')

#------ Assign material orientations -------

p = mdb.models['Flat_Specimen'].parts['Part-1']
region = p.sets['Set_Layer_1']
orientation = mdb.models['Flat_Specimen'].parts['Part-1'].datums[23]
mdb.models['Flat_Specimen'].parts['Part-1'].MaterialOrientation(region=region, 
    orientationType=SYSTEM, axis=AXIS_1, localCsys=orientation, 
    fieldName='', additionalRotationType=ROTATION_ANGLE, 
    additionalRotationField='', angle=180.0, stackDirection=STACK_3)

p = mdb.models['Flat_Specimen'].parts['Part-1']
region = p.sets['Set_Layer_2']
orientation = mdb.models['Flat_Specimen'].parts['Part-1'].datums[22]
mdb.models['Flat_Specimen'].parts['Part-1'].MaterialOrientation(region=region, 
    orientationType=SYSTEM, axis=AXIS_1, localCsys=orientation, 
    fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, 
    additionalRotationField='', stackDirection=STACK_3)

p = mdb.models['Flat_Specimen'].parts['Part-1']
region = p.sets['Set_Layer_3']
orientation = mdb.models['Flat_Specimen'].parts['Part-1'].datums[23]
mdb.models['Flat_Specimen'].parts['Part-1'].MaterialOrientation(region=region, 
    orientationType=SYSTEM, axis=AXIS_1, localCsys=orientation, 
    fieldName='', additionalRotationType=ROTATION_ANGLE, 
    additionalRotationField='', angle=180.0, stackDirection=STACK_3)

p = mdb.models['Flat_Specimen'].parts['Part-1']
region = p.sets['Set_Layer_4']
orientation = mdb.models['Flat_Specimen'].parts['Part-1'].datums[22]
mdb.models['Flat_Specimen'].parts['Part-1'].MaterialOrientation(region=region, 
    orientationType=SYSTEM, axis=AXIS_1, localCsys=orientation, 
    fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, 
    additionalRotationField='', stackDirection=STACK_3)

p = mdb.models['Flat_Specimen'].parts['Part-1']
region = p.sets['Set_Layer_5']
orientation = mdb.models['Flat_Specimen'].parts['Part-1'].datums[23]
mdb.models['Flat_Specimen'].parts['Part-1'].MaterialOrientation(region=region, 
    orientationType=SYSTEM, axis=AXIS_1, localCsys=orientation, 
    fieldName='', additionalRotationType=ROTATION_ANGLE, 
    additionalRotationField='', angle=180.0, stackDirection=STACK_3)

#------ Cut out quarter piece ------

f, e, d2 = p.faces, p.edges, p.datums

t = p.MakeSketchTransform(sketchPlane=d2[10], sketchUpEdge=e[111], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-25.0, 35.0, 
    100.0))
s = mdb.models['Flat_Specimen'].ConstrainedSketch(name='__profile__', 
    sheetSize=641.88, gridSpacing=16.04, transform=t)

g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)

p = mdb.models['Flat_Specimen'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)

s.Line(point1=(96.24, 0.0), point2=(96.24, -112.28))
s.VerticalConstraint(entity=g[2], addUndoState=False)
s.Line(point1=(96.24, -112.28), point2=(-64.16, -112.28))
s.HorizontalConstraint(entity=g[3], addUndoState=False)
s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
s.Line(point1=(-64.16, -112.28), point2=(-64.16, 0.0))
s.VerticalConstraint(entity=g[4], addUndoState=False)
s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
s.Line(point1=(-64.16, 0.0), point2=(0.0, 0.0))
s.HorizontalConstraint(entity=g[5], addUndoState=False)
s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
s.Line(point1=(0.0, 0.0), point2=(0.0, 112.28))
s.VerticalConstraint(entity=g[6], addUndoState=False)
s.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
s.Line(point1=(0.0, 112.28), point2=(96.24, 112.28))
s.HorizontalConstraint(entity=g[7], addUndoState=False)
s.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
s.Line(point1=(96.24, 112.28), point2=(96.24, 0.0))
s.VerticalConstraint(entity=g[8], addUndoState=False)
s.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)

p = mdb.models['Flat_Specimen'].parts['Part-1']
f1, e1, d1 = p.faces, p.edges, p.datums

p.CutExtrude(sketchPlane=d1[10], sketchUpEdge=e1[111], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=OFF)
s.unsetPrimaryObject()
del mdb.models['Flat_Specimen'].sketches['__profile__']

#------ Assembly ------

a = mdb.models['Flat_Specimen'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Flat_Specimen'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Flat_Specimen'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)

#------ Step ------

mdb.models['Flat_Specimen'].StaticStep(name='Step-1', previous='Initial', 
    timeIncrementationMethod=FIXED, initialInc=0.01, noStop=OFF, nlgeom=ON)
a = mdb.models['Flat_Specimen'].rootAssembly

#------ Boundary Conds. ------

f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#803fff ]', ), )
region = a.Set(faces=faces1, name='Set_BC_Sym_Mid')
mdb.models['Flat_Specimen'].XsymmBC(name='BC-1', createStepName='Step-1', 
    region=region, localCsys=None)

a = mdb.models['Flat_Specimen'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#17fc000 ]', ), )
region = a.Set(faces=faces1, name='Set_BC_Sym_Hole')
mdb.models['Flat_Specimen'].ZsymmBC(name='BC-2', createStepName='Step-1', 
    region=region, localCsys=None)

a = mdb.models['Flat_Specimen'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#4000000 #0 #6c ]', ), )
region = a.Set(faces=faces1, name='Set_BC_Disp')

mdb.models['Flat_Specimen'].DisplacementBC(name='BC-3', 
    createStepName='Step-1', region=region, u1=UNSET, u2=UNSET, u3=-0.1, 
    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

#------- Seed and mesh ---------

#------- Hole End --------

#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#pickedEdges = e.getSequenceFromMask(mask=('[#400400a #510004a2 #1 ]', ), )
#p.seedEdgeByNumber(edges=pickedEdges, number=5)

#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#edges = e.getSequenceFromMask(mask=('[#400400a #510004a2 #1 ]', ), )
#p.Set(edges=edges, name='Set_Seed_HoleEnd')


#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#edges = e.getSequenceFromMask(mask=('[#400400a #510004a2 #1 ]', ), )
#p.Set(edges=edges, name='Set_Seed_HoleEnd')

#------- Set Seed Hole Side ------

p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
pickedEdges1 = e.getSequenceFromMask(mask=('[#20000 #24d000 ]', ), )
pickedEdges2 = e.getSequenceFromMask(mask=('[#81248000 #4000000 ]', ), )
p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
    end2Edges=pickedEdges2, minSize=0.7, maxSize=1.3)

p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#81268000 #424d000 ]', ), )
p.Set(edges=edges, name='Set_Seed_Hole')

p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
pickedEdges1 = e.getSequenceFromMask(mask=('[#81248000 #4000000 ]', ), )
pickedEdges2 = e.getSequenceFromMask(mask=('[#20000 #24d000 ]', ), )
p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
    end2Edges=pickedEdges2, minSize=0.7, maxSize=1.3)
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#81268000 #424d000 ]', ), )
p.Set(edges=edges, name='Edge Seeds-1')
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#81268000 #424d000 ]', ), )
p.Set(edges=edges, name='Set_Seed_Hole')

p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#81268000 #424d000 ]', ), )
p.Set(edges=edges, name='Set_Seed_Hole')

#------- Set Seed Hole perimeter ------

session.viewports['Viewport: 1'].partDisplay.setValues(renderStyle=WIREFRAME)
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#0:2 #1e66780 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=16, constraint=FIXED)
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#0:2 #1e66780 ]', ), )
p.Set(edges=edges, name='Set_Seed_HolePerimeter')
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#0:2 #1e66780 ]', ), )
p.Set(edges=edges, name='Set_Seed_HolePerimeter')

#------- Set Seed Hole Side outside hole ------

p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#400400a #510004a2 #1 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FIXED)
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#400400a #510004a2 #1 ]', ), )
p.Set(edges=edges, name='Set_Seed_HoleSides')

p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#400400a #510004a2 #1 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FIXED)
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#400400a #510004a2 #1 ]', ), )
p.Set(edges=edges, name='Set_Seed_HoleSides')


#------- Set Seed Hole straight corners ------

p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#0:2 #7a199802 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=8, constraint=FIXED)
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#0:2 #7a199802 ]', ), )
p.Set(edges=edges, name='Set_Seed_HoleCorners')

#------- Set Seed thickness ----------

p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=(
    '[#72d936a5 #aadb2b4d #84000020 #7807 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=1, constraint=FIXED)
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#72d936a5 #aadb2b4d #84000020 #7807 ]', 
    ), )
p.Set(edges=edges, name='Set_Seed_VertEdges')
p = mdb.models['Flat_Specimen'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#72d936a5 #aadb2b4d #84000020 #7807 ]', 
    ), )
p.Set(edges=edges, name='Set_Seed_VertEdges')



#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#pickedEdges = e.getSequenceFromMask(mask=('[#0:2 #7a19985a #2a0 ]', ), )
#p.seedEdgeByNumber(edges=pickedEdges, number=19)
#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#edges = e.getSequenceFromMask(mask=('[#0:2 #7a19985a #2a0 ]', ), )
#p.Set(edges=edges, name='Set_Seed_Sides')
#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#edges = e.getSequenceFromMask(mask=('[#0:2 #7a19985a #2a0 ]', ), )
#p.Set(edges=edges, name='Set_Seed_Sides')

#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#pickedEdges = e.getSequenceFromMask(mask=('[#8000950 #10 #4 #558 ]', ), )
#p.seedEdgeByNumber(edges=pickedEdges, number=15)
#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#edges = e.getSequenceFromMask(mask=('[#8000950 #10 #4 #558 ]', ), )
#p.Set(edges=edges, name='Set_Seed_CoarseSides')
#p = mdb.models['Flat_Specimen'].parts['Part-1']
#e = p.edges
#edges = e.getSequenceFromMask(mask=('[#8000950 #10 #4 #558 ]', ), )
#p.Set(edges=edges, name='Set_Seed_CoarseSides')
