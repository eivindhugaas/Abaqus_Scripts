from abaqus import *
from abaqusConstants import *
import __main__
import time
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
import os
#from abavariables import variables
#var=variables()

#---- Variables -----------


MeshOnCircumferenceN=[1,2,3,4,5,6,7,8,9,10] #Circum
MSideN=[1,2,3,4,5,6,7,8,9,10] #Outer side
MinMeshDensN=[9.90,4.,3.,2.,1.,0.9,0.7,0.6,0.4,0.3]
MaxMeshDensN=[10.1,6.,4.,3.,2.,1.9,1.7,1.3,1.0,0.7]
MeshCoarseN=[5,7,9,11,13,15,17,19,21,23] #Coarse 

MeshOnCircumference=10 #along holerim
MSide=10 #along side between hole and side of specimen.
MaxMeshDens=1. #Along hole rad max in mm
MinMeshDens=0.5 #Along hole rad min
MeshCoarse=20 #On back part of sample

M=MeshOnCircumference
MSide=MSide
MMax=MaxMeshDens
MMin=MinMeshDens
MCoarse=MeshCoarse

NameOfFile="LE22_Path_Longt_%s_%s_%s_%s_%s"%(M,MMax,MMin,MCoarse,MSide)
XYPlotName="XY_Plot_LE22_Path_Longt_%s_%s_%s_%s_%s"%(M,MMax,MMin,MCoarse,MSide)

Thickness=5.
T=Thickness
L4=((T/5)*1)+((T/5)/2)
L3=((T/5)/2)
L2=-((T/5)/2)
L1=-(((T/5)*1)+((T/5)/2))
n=1
for i in range(0,10):
    
    M=MeshOnCircumferenceN[i]
    MSide=MSideN[i]
    MMax=MaxMeshDensN[i]
    MMin=MinMeshDensN[i]
    MCoarse=MeshCoarseN[i]
    
    n=n+1

    #--------- Initiate ----------
    modelname="Flat_%s"%(n)
    
    NameOfFile="LE22_Path_Longt_%s_%s_%s_%s_%s"%(M,MMin,MMax,MCoarse,MSide)
    NameOfFile2="LE11_Path_Longt_%s_%s_%s_%s_%s"%(M,MMin,MMax,MCoarse,MSide)
    
    XYPlotName="XY_Plot_LE22_%s"%(n)    
    XYPlotName2="XY_Plot_LE11_%s"%(n) 
    #-----------------------------
    
    os.chdir(r"C:\Users\eivinhug\NTNU\PhD\AbaqusModels\SplitDisk")
    mdb.Model(name=modelname, modelType=STANDARD_EXPLICIT)
    mdb.saveAs(pathName=r"C:\Users\eivinhug\NTNU\PhD\AbaqusModels\SplitDisk\FlatModel.cae")
    #-------- Make sketch ---------
    
    s = mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(-10.0, 0.0), point2=(0.0, 10.0), 
        direction=CLOCKWISE)
    s.Line(point1=(0.0, 10.0), point2=(0.0, 25.0))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s.Line(point1=(0.0, 25.0), point2=(-100.0, 25.0))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(-100.0, 25.0), point2=(-100.0, 0.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s.Line(point1=(-100.0, 0.0), point2=(-10.0, 0.0))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
    p = mdb.models[modelname].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[modelname].parts['Part-1']
    p.BaseSolidExtrude(sketch=s, depth=Thickness)
    
    del mdb.models[modelname].sketches['__profile__']
    
    
    #------ Make Datum plane --------
    
    f = p.faces
    p.DatumPlaneByOffset(plane=f[2], flip=SIDE1, offset=10.0)
    
    #------ Make layers -----------
    
    e1, d1 = p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=d1[2], sketchUpEdge=e1[5], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(10.0, 12.5, 
        2.5))
    s1 = mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=227.03, 
        gridSpacing=5.67, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.Line(point1=(-25.0, -1.5), point2=(50.0, L1))
    s1.HorizontalConstraint(entity=g[2], addUndoState=False)
    s1.Line(point1=(-25.0, -0.5), point2=(50.0, L2))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.Line(point1=(-25.0, 0.5), point2=(50.0, L3))
    s1.HorizontalConstraint(entity=g[4], addUndoState=False)
    s1.Line(point1=(-25.0, 1.5), point2=(-50.0, L4))
    s1.HorizontalConstraint(entity=g[5], addUndoState=False)
    s1.delete(objectList=(g[5], ))
    s1.Line(point1=(-25.0, 1.5), point2=(50.0, L4))
    s1.HorizontalConstraint(entity=g[6], addUndoState=False)
    e, d2 = p.edges, p.datums
    p.Wire(sketchPlane=d2[2], sketchUpEdge=e[5], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1)
    del mdb.models[modelname].sketches['__profile__']
    
    #----- Make global coord copy -----
    
    p.DatumCsysByThreePoints(name='CSYS_GlobCopy', coordSysType=CARTESIAN, origin=(
        0.0, 0.0, 0.0), line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))
    
    #----- Section layers --------
    
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[0], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    e, d2 = p.edges, p.datums
    pickedEdges =(e[3], )
    p.PartitionCellByExtrudeEdge(line=d2[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#7 ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[1], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#f ]', ), )
    e, d2 = p.edges, p.datums
    pickedEdges =(e[2], )
    p.PartitionCellByExtrudeEdge(line=d2[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    
    
    #----- Make Mesh partition sketch --------
    
    f1 = p.faces
    p.DatumPlaneByOffset(plane=f1[29], flip=SIDE1, offset=10.0)
    e1, d1 = p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=d1[9], sketchUpEdge=e1[48], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-45.0, 25.0, 
        15.0))
    s = mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=294.48, 
        gridSpacing=7.36, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.ArcByCenterEnds(center=(45.0, -25.0), point1=(25.0, -25.0), point2=(45.0, 
        -5.0), direction=CLOCKWISE)
    s.Line(point1=(20.0, -30.0), point2=(20.0, 10.0))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.Line(point1=(45.0, -25.0), point2=(20.0, 0.0))
    e, d2 = p.edges, p.datums
    p.Wire(sketchPlane=d2[9], sketchUpEdge=e[48], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s)
    
    del mdb.models[modelname].sketches['__profile__']
    
    #----- Make Mesh partitions --------
    
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1f ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[4], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    
    pickedCells = c.getSequenceFromMask(mask=('[#1f ]', ), )
    e, d2 = p.edges, p.datums
    pickedEdges =(e[4], )
    p.PartitionCellByExtrudeEdge(line=d2[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    
    pickedCells = c.getSequenceFromMask(mask=('[#3ff ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[4], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    
    pickedCells = c.getSequenceFromMask(mask=('[#7fff ]', ), )
    e, d2 = p.edges, p.datums
    pickedEdges =(e[7], )
    p.PartitionCellByExtrudeEdge(line=d2[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    
    pickedCells = c.getSequenceFromMask(mask=('[#fffff ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[8], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)
    
    
    #------- Remove edges ---------
    
    e = p.edges
    RemoveWireEdges = e.getSequenceFromMask(mask=('[#3ff ]', ), )
    p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)
    
    #------ Make Material ------
    
    mdb.models[modelname].Material(name='GFRP')
    mdb.models[modelname].materials['GFRP'].Elastic(
        type=ENGINEERING_CONSTANTS, table=((40000.0, 5000.0, 5000.0, 0.3, 0.3, 
        0.3, 5000.0, 5000.0, 5000.0), ))
    
    #------ Make Section -------
    
    sectionLayer1 = section.SectionLayer(material='GFRP', thickness=1.0, 
        orientAngle=0.0, numIntPts=1, plyName='Layer')
    mdb.models[modelname].CompositeSolidSection(name='Sect_VacInf', 
        layupName='', symmetric=False, layup=(sectionLayer1, ))
    
    #----- Make material orientations and assign sections -----
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1820011 ]', ), )
    region = p.Set(cells=cells, name='Set_Layer_1')
    p = mdb.models[modelname].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    cells = c.getSequenceFromMask(mask=('[#442300 ]', ), )
    region = p.Set(cells=cells, name='Set_Layer_2')
    p = mdb.models[modelname].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    cells = c.getSequenceFromMask(mask=('[#84422 ]', ), )
    region = p.Set(cells=cells, name='Set_Layer_3')
    p = mdb.models[modelname].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    cells = c.getSequenceFromMask(mask=('[#108844 ]', ), )
    region = p.Set(cells=cells, name='Set_Layer_4')
    p = mdb.models[modelname].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    cells = c.getSequenceFromMask(mask=('[#211088 ]', ), )
    region = p.Set(cells=cells, name='Set_Layer_5')
    p = mdb.models[modelname].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Sect_VacInf', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    cells = c.getSequenceFromMask(mask=('[#1820011 ]', ), )
    region = regionToolset.Region(cells=cells)
    orientation = mdb.models[modelname].parts['Part-1'].datums[4]
    mdb.models[modelname].parts['Part-1'].MaterialOrientation(region=region, 
        orientationType=SYSTEM, axis=AXIS_3, localCsys=orientation, 
        fieldName='', additionalRotationType=ROTATION_ANGLE, 
        additionalRotationField='', angle=90.0, stackDirection=STACK_3)
    
    cells = c.getSequenceFromMask(mask=('[#442300 ]', ), )
    region = regionToolset.Region(cells=cells)
    orientation = mdb.models[modelname].parts['Part-1'].datums[4]
    mdb.models[modelname].parts['Part-1'].MaterialOrientation(region=region, 
        orientationType=SYSTEM, axis=AXIS_3, localCsys=orientation, 
        fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', stackDirection=STACK_3)
    
    cells = c.getSequenceFromMask(mask=('[#84422 ]', ), )
    region = regionToolset.Region(cells=cells)
    orientation = mdb.models[modelname].parts['Part-1'].datums[4]
    mdb.models[modelname].parts['Part-1'].MaterialOrientation(region=region, 
        orientationType=SYSTEM, axis=AXIS_3, localCsys=orientation, 
        fieldName='', additionalRotationType=ROTATION_ANGLE, 
        additionalRotationField='', angle=90.0, stackDirection=STACK_3)
    
    cells = c.getSequenceFromMask(mask=('[#108844 ]', ), )
    region = regionToolset.Region(cells=cells)
    orientation = mdb.models[modelname].parts['Part-1'].datums[4]
    mdb.models[modelname].parts['Part-1'].MaterialOrientation(region=region, 
        orientationType=SYSTEM, axis=AXIS_3, localCsys=orientation, 
        fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', stackDirection=STACK_3)
    
    cells = c.getSequenceFromMask(mask=('[#211088 ]', ), )
    region = regionToolset.Region(cells=cells)
    orientation = mdb.models[modelname].parts['Part-1'].datums[4]
    mdb.models[modelname].parts['Part-1'].MaterialOrientation(region=region, 
        orientationType=SYSTEM, axis=AXIS_3, localCsys=orientation, 
        fieldName='', additionalRotationType=ROTATION_ANGLE, 
        additionalRotationField='', angle=90.0, stackDirection=STACK_3)
    
    
    #------ Make BC's----
    
    a = mdb.models[modelname].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models[modelname].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelname].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    mdb.models[modelname].StaticStep(name='Step-1', previous='Initial', 
        timeIncrementationMethod=FIXED, initialInc=0.01, noStop=OFF, nlgeom=ON)
    
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#2ac0 #5540 #84028000 #40 ]', ), )
    region = a.Set(faces=faces1, name='Set_Symmetry_Y')
    mdb.models[modelname].YsymmBC(name='Symmetry_Y', createStepName='Step-1', 
        region=region, localCsys=None)
    
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#2ac00000 #0 #42100800 #10 ]', ), )
    region = a.Set(faces=faces1, name='Set-2')
    mdb.models[modelname].XsymmBC(name='BC_Symmetry_X', createStepName='Step-1', 
        region=region, localCsys=None)
    
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#0:2 #1084000 #6 ]', ), )
    region = a.Set(faces=faces1, name='Set-3')
    mdb.models[modelname].DisplacementBC(name='BC_Displacement', 
        createStepName='Step-1', region=region, u1=-1.0, u2=UNSET, u3=UNSET, 
        ur1=0.0, ur2=0.0, ur3=0.0, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#200020 #200800 #0 #100 ]', ), )
    region = a.Set(faces=faces1, name='Set_Bottom')
    mdb.models[modelname].DisplacementBC(name='BC_Z', createStepName='Step-1', 
        region=region, u1=UNSET, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, 
        ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, 
        fieldName='', localCsys=None)
    
    #----ZEEEEDing----
    
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderStyle=HIDDEN)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        renderStyle=WIREFRAME)
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    session.viewports['Viewport: 1'].partDisplay.setValues(renderStyle=HIDDEN)
    session.viewports['Viewport: 1'].partDisplay.setValues(renderStyle=WIREFRAME)
    e = p.edges
    
    pickedEdges = e.getSequenceFromMask(mask=(
        '[#50000 #2000000 #0 #9210f840 #14a01 ]', ), )
    p.seedEdgeByNumber(edges=pickedEdges, number=MSide, constraint=FIXED)
    edges = e.getSequenceFromMask(mask=(
         '[#50000 #2000000 #0 #9210f840 #14a01 ]', ), )
    p.Set(edges=edges, name='Set_Seed_HoleSides')
    
    #-----------------
    
    pickedEdges = e.getSequenceFromMask(mask=(
        '[#22495 #1249500 #24aad111 #24a40491 #100 ]', ), )
    p.seedEdgeByNumber(edges=pickedEdges, number=M, constraint=FIXED)
    edges = e.getSequenceFromMask(mask=(
        '[#22495 #1249500 #24aad111 #24a40491 #100 ]', ), )
    p.Set(edges=edges, name='Set_Seed_Circumferential')
    
    #----------------
    
    pickedEdges1 = e.getSequenceFromMask(mask=('[#0:2 #48000200 #12a ]', ), )
    pickedEdges2 = e.getSequenceFromMask(mask=('[#0 #b4000000 #20028aa ]', ), )
    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
        end2Edges=pickedEdges2, minSize=MMin, maxSize=MMax, constraint=FIXED)
    
    pickedEdges1 = e.getSequenceFromMask(mask=('[#0 #b4000000 #20028aa ]', ), )
    pickedEdges2 = e.getSequenceFromMask(mask=('[#0:2 #48000200 #12a ]', ), )
    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
        end2Edges=pickedEdges2, minSize=MMin, maxSize=MMax, constraint=FIXED)
    
    edges = e.getSequenceFromMask(mask=('[#0 #b4000000 #4a002aaa #12a ]', ), )
    p.Set(edges=edges, name='Set_Seed_Radial')
    
    #------------------
    
    session.viewports['Viewport: 1'].partDisplay.setValues(renderStyle=SHADED)
    mdb.save()
    
    pickedEdges = e.getSequenceFromMask(mask=('[#55680000 #55 #0 #20000 ]', ), )
    p.seedEdgeByNumber(edges=pickedEdges, number=MCoarse, constraint=FIXED)
    
    edges = e.getSequenceFromMask(mask=('[#55680000 #55 #0 #20000 ]', ), )
    p.Set(edges=edges, name='Set_Seed_Coarse')
    
    #--------------------
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1ffffff ]', ), )
    f = p.faces
    p.assignStackDirection(referenceRegion=f[15], cells=pickedCells)
    
    #---- ZEND EEEEEEEEEEEEEETTTTT!!!!! -----
    
    p.generateMesh()
    mdb.save()
    #----- The Gnaaaaaaaarrrrr!!! arrrrggghhhh!!!!------
    
    mdb.Job(name='Job_Flat', model=modelname, description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['Job_Flat'].submit(consistencyChecking=OFF)
    
    mdb.save()
    
    #----- Result section LE22 -----
    
    time.sleep(120)  
    
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    
    o3 = session.openOdb(
        name='C:/Users/eivinhug/NTNU/PhD/AbaqusModels/SplitDisk/Job_Flat.odb')
    
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    
    a = mdb.models[modelname].rootAssembly
    
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    
    session.mdbData.summary()
    
    session.viewports['Viewport: 1'].setValues(
        displayedObject=session.odbs['C:/Users/eivinhug/NTNU/PhD/AbaqusModels/SplitDisk/Job_Flat.odb'])
    
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(
        plotState=CONTOURS_ON_DEF)
    
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
        COMPONENT, 'LE22'), )
    
    session.Path(name='Path_Longitudinal', type=POINT_LIST, expression=((0.0, 10.0, 
        5.0), (-100.0, 10.0, 5.0)))
    
    session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
        sectionResults=USE_TOP)
    
    xyp = session.XYPlot(XYPlotName)
    
    session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
    
    xyp = session.xyPlots[XYPlotName]
    chartName = xyp.charts.keys()[0]
    chart = xyp.charts[chartName]
    pth = session.paths['Path_Longitudinal']
    xy1 = xyPlot.XYDataFromPath(path=pth, includeIntersections=True, 
        projectOntoMesh=True, pathStyle=UNIFORM_SPACING, numIntervals=100, 
        projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE)
    c1 = session.Curve(xyData=xy1)
    chart.setValues(curvesToPlot=(c1, ), )
    
    pth = session.paths['Path_Longitudinal']
    
    session.XYDataFromPath(name=NameOfFile, path=pth, 
        includeIntersections=True, projectOntoMesh=True, 
        pathStyle=UNIFORM_SPACING, numIntervals=100, projectionTolerance=0, 
        shape=UNDEFORMED, labelType=TRUE_DISTANCE)
    
    #------- Make report, reset visual ---------
    
    session.mdbData.summary()
    xyp = session.xyPlots[XYPlotName]
    session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
    odb = session.odbs['C:/Users/eivinhug/NTNU/PhD/AbaqusModels/SplitDisk/Job_Flat.odb']
    session.viewports['Viewport: 1'].setValues(displayedObject=odb)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF, ))
    x0 = session.xyDataObjects[NameOfFile]
    session.writeXYReport(fileName='abaqus.rpt', xyData=(x0, ))

    #--------- Make LE11 --------------#

    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
        COMPONENT, 'LE11'), )
    
    session.Path(name='Path_Transverse', type=POINT_LIST, expression=((0.0, 10.0, 
        5.0), (0.0, 25.0, 5.0)))
    
    session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
        sectionResults=USE_TOP)
    
    xyp = session.XYPlot(XYPlotName2)
    
    session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
    
    xyp = session.xyPlots[XYPlotName2]
    chartName = xyp.charts.keys()[0]
    chart = xyp.charts[chartName]
    pth = session.paths['Path_Transverse']
    xy1 = xyPlot.XYDataFromPath(path=pth, includeIntersections=True, 
        projectOntoMesh=True, pathStyle=UNIFORM_SPACING, numIntervals=100, 
        projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE)
    c1 = session.Curve(xyData=xy1)
    chart.setValues(curvesToPlot=(c1, ), )
    
    pth = session.paths['Path_Transverse']
    
    session.XYDataFromPath(name=NameOfFile2, path=pth, 
        includeIntersections=True, projectOntoMesh=True, 
        pathStyle=UNIFORM_SPACING, numIntervals=100, projectionTolerance=0, 
        shape=UNDEFORMED, labelType=TRUE_DISTANCE)
    
    #------- Make report, reset visual ---------
    
    session.mdbData.summary()
    xyp = session.xyPlots[XYPlotName2]
    session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
    odb = session.odbs['C:/Users/eivinhug/NTNU/PhD/AbaqusModels/SplitDisk/Job_Flat.odb']
    session.viewports['Viewport: 1'].setValues(displayedObject=odb)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF, ))
    x0 = session.xyDataObjects[NameOfFile2]
    session.writeXYReport(fileName='abaqus.rpt', xyData=(x0, ))