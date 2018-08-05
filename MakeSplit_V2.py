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
import numpy as np
from distutils.dir_util import copy_tree
import shutil as shutil

#---- Variables -----------

MeshOnCircumferenceN=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18] #Circum
MeshRadN=   [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
MeshSidesN= [1,2,2,3,3,3, 3, 4, 4, 5, 5, 6, 7, 8, 9]
MeshCoarseN=[2,3,5,7,9,11,13,15,17,19,20,21,22,23,24] #Coarse 

Friction=np.arange(0.01,0.51,0.01)
ID=140.
Thickness=5.
T=Thickness
L4=(ID/2)+((T/5)*4.)
L3=(ID/2)+((T/5)*3.)
L2=(ID/2)+((T/5)*2.)
L1=(ID/2)+((T/5)*1.)

writefile=r"C:\Users\eivinhug\NTNU\PhD\AbaqusModels\SplitDisk\Split_Friciton_study" #Work directory
UMATdir=r'C:\Users\eivinhug\Documents\GitHub\CompDam_DGD\for'
EnvFile=r'C:\Users\eivinhug\Documents\GitHub\CompDam_DGD\examples\abaqus_v6.env'

if not os.path.exists(writefile):
    os.makedirs(writefile)    

n=0

UMAT=False

if UMAT:
    
    copy_tree(UMATdir, writefile+"\\for")
    
    shutil.copy(EnvFile, writefile)    

for i in range(0,len(Friction)):
    
    M=MeshOnCircumferenceN[-1]
    MRad=MeshRadN[-1]
    MSides=MeshSidesN[-1]
    MCoarse=MeshCoarseN[-1]
    Fric=Friction[i]
    n=n+1

    #--------- Initiate ----------
    modelname="SplitDisk_%s"%(n)
    jobname="Job_SplitDisk_%s"%(n)
    
    NameOfFile="LE22_Path_Longt_%s_%s_%s_%s"%(M,MRad,MCoarse,MSides)
    NameOfFile2="LE11_Path_Longt_%s_%s_%s_%s"%(M,MRad,MCoarse,MSides)
    
    NameOfResultFile1="LE22"+modelname+".rpt"    
    NameOfResultFile2="LE11"+modelname+".rpt"
    
    XYPlotName="XY_Plot_Split_LE22_%s"%(n)    
    XYPlotName2="XY_Plot_Split_LE11_%s"%(n) 
    #-----------------------------
    


    jobfolder=(writefile+"\\%s.odb")%(jobname)

    joblogname=(writefile+"\\%s.log")%(jobname)    
    
    os.chdir(writefile)
    mdb.Model(name=modelname, modelType=STANDARD_EXPLICIT)
    mdb.saveAs(pathName=writefile+"\\SplitModel.cae")    
    
    #-------- Make sketch ---------
    
    s = mdb.models[modelname].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(-ID/2., 0.0), point2=(0.0, ID/2.), 
        direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(-((ID/2.)+T), 0.0), point2=(0.0, ((ID/2.)+T)), 
        direction=CLOCKWISE)
    s.Line(point1=(-(ID/2.), 0.0), point2=(-((ID/2)+T), 0.0))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(0.0, (ID/2.)), point2=(0.0, (ID/2.)+T))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[5], addUndoState=False)
    p = mdb.models[modelname].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[modelname].parts['Part-1']
    p.BaseSolidExtrude(sketch=s, depth=25.0)
    
    p = mdb.models[modelname].parts['Part-1']

    del mdb.models[modelname].sketches['__profile__']
        
    #------ Make Datum plane --------
    
    f = p.faces
    p.DatumPlaneByOffset(plane=f[5], flip=SIDE1, offset=10.0)
    
    #------ Make layers -----------
    
    e, d = p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=d[2], sketchUpEdge=e[11], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-37.5, 37.5, 
        -10.0))
    s = mdb.models[modelname].ConstrainedSketch(name='__profile__', 
        sheetSize=243.61, gridSpacing=6.09, transform=t)
    g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints

    p = mdb.models[modelname].parts['Part-1']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)

    p = mdb.models[modelname].parts['Part-1']
    e1, p1 = p.edges, p.elemEdges

    s.ArcByCenterEnds(center=(37.5, -37.5), point1=(-35.0175, -48.72), point2=(
        51.765, 33.495), direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(37.5, -37.5), point1=(-27.405, -50.2425), point2=(
        50.2425, 25.8825), direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(37.5, -37.5), point1=(-21.315, -50.2425), point2=(
        45.675, 21.315), direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(37.5, -37.5), point1=(-15.225, -47.1975), point2=(
        47.1975, 15.225), direction=CLOCKWISE)
    s.RadialDimension(curve=g[2], textPoint=(37.5, -37.5), 
        radius=L4)
    s.RadialDimension(curve=g[3], textPoint=(37.5, -37.5), 
        radius=L3)
    s.RadialDimension(curve=g[4], textPoint=(37.5, -37.5), 
        radius=L2)
    s.RadialDimension(curve=g[5], textPoint=(37.5, -37.5), 
        radius=L1)   
    
    p = mdb.models[modelname].parts['Part-1']
    e, d2 = p.edges, p.datums
    p.Wire(sketchPlane=d2[2], sketchUpEdge=e[11], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s)

    del mdb.models[modelname].sketches['__profile__']

    p = mdb.models[modelname].parts['Part-1']
    s1 = p.features['Wire-1'].sketch
    mdb.models[modelname].ConstrainedSketch(name='__edit__', objectToCopy=s1)

    del mdb.models[modelname].sketches['__edit__']
    p = mdb.models[modelname].parts['Part-1']

    
    #----- Make global coord copy -----
    
    p = mdb.models[modelname].parts['Part-1']
    p.DatumCsysByThreePoints(name='CSYS_Glob', coordSysType=CYLINDRICAL, origin=(
        0.0, 0.0, 0.0), line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))
       
    #----- Section layers --------
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, d = p.edges, p.datums
    pickedEdges =(e[3], )
    p.PartitionCellByExtrudeEdge(line=d[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=FORWARD)
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[1], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=FORWARD)

    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#7 ]', ), )
    e, d = p.edges, p.datums
    pickedEdges =(e[2], )
    p.PartitionCellByExtrudeEdge(line=d[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=FORWARD)

    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#f ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[0], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis3, cells=pickedCells, 
        edges=pickedEdges, sense=FORWARD)    

    #-------- Make plane -----------
    
    p = mdb.models[modelname].parts['Part-1']
    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=10.0)    
    
    #---------- Make Hole ------------
    
    p = mdb.models[modelname].parts['Part-1']
    d = p.datums
    t = p.MakeSketchTransform(sketchPlane=d[9], sketchUpEdge=d[4].axis2, 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(10.0, 30.21128, 
        7.5))
    s = mdb.models[modelname].ConstrainedSketch(name='__profile__', 
        sheetSize=290.14, gridSpacing=7.25, transform=t)
    g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints

    p = mdb.models[modelname].parts['Part-1']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    
    p = mdb.models[modelname].parts['Part-1']
    e, p1 = p.edges, p.elemEdges
    p.projectEdgesOntoSketch(sketch=s, edges=(e[43], ))

    s.setAsConstruction(objectList=(g[2], ))

    s.CircleByCenterPerimeter(center=(7.5, -30.21128), point1=(3.625, -18.125))
    s.RadialDimension(curve=g[3], textPoint=(36.6058120727539, -17.5263892529297), 
        radius=10.0)
    p = mdb.models[modelname].parts['Part-1']
    d2 = p.datums
    p.CutExtrude(sketchPlane=d2[9], sketchUpEdge=d2[4].axis2, 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, 
        flipExtrudeDirection=OFF)

    del mdb.models[modelname].sketches['__profile__']

    #--------- Make mesh partitons sketch --------

    p = mdb.models[modelname].parts['Part-1']
    d = p.datums
    
    t = p.MakeSketchTransform(sketchPlane=d[9], sketchUpEdge=d[4].axis2, 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(10.0, 30.21128, 
        7.5))
    s = mdb.models[modelname].ConstrainedSketch(name='__profile__', 
        sheetSize=290.14, gridSpacing=7.25, transform=t)
    g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
    
    s.ArcByCenterEnds(center=(7.5, -30.21128), point1=(-12.5, -30.21128), point2=(
        -6.64213562373095, -16.069144376269), direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(7.5, -30.21128), point1=(-6.64213562373095, 
        -16.069144376269), point2=(7.5, -10.21128), direction=CLOCKWISE)
    s.Line(point1=(7.5, -5.21128), point2=(-17.5, -5.21128))
    s.Line(point1=(-17.5, -5.21128), point2=(-6.64213562373095, -16.069144376269))
    s.Line(point1=(-6.64213562373095, -16.069144376269), point2=(7.5, -30.21128))
    mdb.save()
    d2 = p.datums
    p.Wire(sketchPlane=d2[9], sketchUpEdge=d2[4].axis2, sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s)

    mdb.save()
    del mdb.models[modelname].sketches['__profile__']    
    
    #-------- Partition mesh lines -----------
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    
    pickedCells = c.getSequenceFromMask(mask=('[#1f ]', ), )
    e, d = p.edges, p.datums
    pickedEdges =(e[9], )
    p.PartitionCellByExtrudeEdge(line=d[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)

    pickedCells = c.getSequenceFromMask(mask=('[#1f ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[8], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)

    pickedCells = c.getSequenceFromMask(mask=('[#3ff ]', ), )
    e, d = p.edges, p.datums
    pickedEdges =(e[11], )
    p.PartitionCellByExtrudeEdge(line=d[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)

    pickedCells = c.getSequenceFromMask(mask=('[#7fff ]', ), )
    e1, d1 = p.edges, p.datums
    pickedEdges =(e1[9], )
    p.PartitionCellByExtrudeEdge(line=d1[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)

    pickedCells = c.getSequenceFromMask(mask=('[#fffff ]', ), )
    e, d = p.edges, p.datums
    pickedEdges =(e[12], )
    p.PartitionCellByExtrudeEdge(line=d[4].axis1, cells=pickedCells, 
        edges=pickedEdges, sense=REVERSE)    

    #------- Remove edges and fix geometry ---------
    
    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    RemoveWireEdges = e.getSequenceFromMask(mask=('[#1f55 ]', ), )
    p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)
    RemoveWireEdges = e.getSequenceFromMask(mask=('[#f ]', ), )
    p.RemoveWireEdges(wireEdgeList=RemoveWireEdges)    
    
    
    p = mdb.models[modelname].parts['Part-1']
    v = p.vertices
    p.RemoveRedundantEntities(vertexList = v[50:51]+v[53:54]+v[57:58]+v[66:67]+\
        v[69:71])
    mdb.models[modelname].parts['Part-1'].checkGeometry()        
    
    #------ Make Materials ------
    
    mdb.models[modelname].Material(name='GFRP')
    mdb.models[modelname].materials['GFRP'].Elastic(
        type=ENGINEERING_CONSTANTS, table=((34092.0, 11000.0, 11000.0, 0.3, 0.3, 
        0.49, 3070.0, 3070.0, 3070.0), ))
    
    mdb.models[modelname].Material(name='GFRP_UMAT')
    mdb.models[modelname].materials['GFRP_UMAT'].UserMaterial(
        mechanicalConstants=(0.0, ))
    mdb.models[modelname].materials['GFRP_UMAT'].Depvar(
        n=19)
    mdb.models[modelname].materials['GFRP_UMAT'].userMaterial.setValues(
        mechanicalConstants=(101000, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 34092.0, 
        11000.0, 3070.0, 0.3, 0.096796902, 39.0, 42.0, 0.277, 0.788, 1.634, 
        112.0, 0.925, 11000.0, 1000.0, 3070.0, 0.3, 0.0, 0.0, 4.412e-10, 5.934, 
        755.15, 0.5, 133.3, 0.5, 365.65, 0.5, 47.5, 0.5))    
    
    Mat='GFRP'
    if UMAT:
        Mat='GFRP_UMAT'
        
    #------ Make Section -------
    
    sectionLayer1 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=90.0, numIntPts=1, plyName='Ply_1')
    sectionLayer2 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=90.0, numIntPts=1, plyName='Ply_2')
    sectionLayer3 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=90.0, numIntPts=1, plyName='Ply_3')
    sectionLayer4 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=90.0, numIntPts=1, plyName='Ply_4')
    
    mdb.models[modelname].CompositeSolidSection(name='Sect_Hoop', layupName='', 
        symmetric=False, layup=(sectionLayer1, sectionLayer2, 
                                              sectionLayer3, sectionLayer4,))    
    
    sectionLayer1 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=8.3, numIntPts=1, plyName='Ply_1')
    sectionLayer2 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=-8.3, numIntPts=1, plyName='Ply_2')
    sectionLayer3 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=8.3, numIntPts=1, plyName='Ply_3')    
    sectionLayer4 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=-8.3, numIntPts=1, plyName='Ply_4')
    sectionLayer5 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=8.3, numIntPts=1, plyName='Ply_5')
    sectionLayer6 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=-8.3, numIntPts=1, plyName='Ply_6')
    sectionLayer7 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=8.3, numIntPts=1, plyName='Ply_7')
    sectionLayer8 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=-8.3, numIntPts=1, plyName='Ply_8')    
    sectionLayer9 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=8.3, numIntPts=1, plyName='Ply_9')    
    sectionLayer10 = section.SectionLayer(material=Mat, thickness=1.0, 
        orientAngle=-8.3, numIntPts=1, plyName='Ply_10')    
    mdb.models[modelname].CompositeSolidSection(name='Sect_8_3_deg', 
        layupName='', symmetric=False, layup=(sectionLayer1, sectionLayer2, 
                                              sectionLayer3, sectionLayer4, 
                                              sectionLayer5, sectionLayer6, 
                                              sectionLayer7, sectionLayer8,
                                              sectionLayer9, sectionLayer10))  
    
    #----- Make material orientations and assign sections -----
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1d554bb ]', ), )
    region = regionToolset.Region(cells=cells)
    orientation = mdb.models[modelname].parts['Part-1'].datums[4]
    mdb.models[modelname].parts['Part-1'].MaterialOrientation(region=region, 
        orientationType=SYSTEM, axis=AXIS_2, localCsys=orientation, 
        fieldName='', additionalRotationType=ROTATION_ANGLE, 
        additionalRotationField='', angle=90.0, stackDirection=STACK_3)
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2aab44 ]', ), )
    region = regionToolset.Region(cells=cells)
    orientation = mdb.models[modelname].parts['Part-1'].datums[4]
    mdb.models[modelname].parts['Part-1'].MaterialOrientation(region=region, 
        orientationType=SYSTEM, axis=AXIS_2, localCsys=orientation, 
        fieldName='', additionalRotationType=ROTATION_ANGLE, 
        additionalRotationField='', angle=90.0, stackDirection=STACK_3)
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1d554bb ]', ), )
    region = p.Set(cells=cells, name='Set_Sect_8_3')
    p = mdb.models[modelname].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Sect_8_3_deg', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#28ab44 ]', ), )
    region = p.Set(cells=cells, name='Set_Sect_Hoop')
    p = mdb.models[modelname].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Sect_Hoop', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)    
   
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2aab44 ]', ), )
    p.Set(cells=cells, name='Set_Sect_Hoop')
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2aab44 ]', ), )
    p.Set(cells=cells, name='Set_Sect_Hoop')    
   
    #------ Make BC's----
    
    a = mdb.models[modelname].rootAssembly

    a = mdb.models[modelname].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelname].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    
    mdb.models[modelname].StaticStep(name='Step-1', previous='Initial', 
        maxNumInc=1000, initialInc=0.01, nlgeom=ON)

    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#2ac00000 #0 #88800000 #104 ]', ), )
    region = a.Set(faces=faces1, name='Set_BC_ZSym')
    datum = mdb.models[modelname].rootAssembly.instances['Part-1-1'].datums[4]
    mdb.models[modelname].ZsymmBC(name='BC_ZSym', createStepName='Step-1', 
        region=region, localCsys=datum)

    faces1 = f1.getSequenceFromMask(mask=('[#0:2 #4a83e0 #20 ]', ), )
    region = a.Set(faces=faces1, name='Set_TanSymBot')
    mdb.models[modelname].YsymmBC(name='BC_TanSymBot', createStepName='Step-1', 
        region=region, localCsys=None)
    datum = mdb.models[modelname].rootAssembly.instances['Part-1-1'].datums[4]
    mdb.models[modelname].boundaryConditions['BC_TanSymBot'].setValues(
        localCsys=datum)

    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#0:2 #45000000 #88 ]', ), )
    region = a.Set(faces=faces1, name='Set_BC_TanSymTop')
    datum = mdb.models[modelname].rootAssembly.instances['Part-1-1'].datums[4]
    mdb.models[modelname].YsymmBC(name='BC_TanSymTop', 
        createStepName='Step-1', region=region, localCsys=datum)    
    
    #-------- Make disk -------------

    p1 = mdb.models[modelname].parts['Part-1']

    s = mdb.models[modelname].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(-((ID/2.)**2-(3.5**2))**0.5, 3.5), point2=(0.0, 70.0), 
        direction=CLOCKWISE)
    p = mdb.models[modelname].Part(name='Part-2', dimensionality=THREE_D, 
        type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[modelname].parts['Part-2']
    p.AnalyticRigidSurfExtrude(sketch=s, depth=25.0)

    p = mdb.models[modelname].parts['Part-2']

    del mdb.models[modelname].sketches['__profile__']
        
    a = mdb.models[modelname].rootAssembly
    a1 = mdb.models[modelname].rootAssembly
    p = mdb.models[modelname].parts['Part-2']
    a1.Instance(name='Part-2-1', part=p, dependent=ON)
    
    a1 = mdb.models[modelname].rootAssembly
    a1.translate(instanceList=('Part-2-1', ), vector=(0.0, 0.0, 12.5))

    #---- Make interaction properties -------
    
    mdb.models[modelname].ContactProperty('IntProp_Fric')
    mdb.models[modelname].interactionProperties['IntProp_Fric'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
        table=((Fric, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models[modelname].interactionProperties['IntProp_Fric'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, contactStiffness=1000.0, 
        contactStiffnessScaleFactor=1.0, clearanceAtZeroContactPressure=0.0, 
        stiffnessBehavior=LINEAR, constraintEnforcementMethod=PENALTY)
    a = mdb.models[modelname].rootAssembly
    s1 = a.instances['Part-2-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    region1=a.Surface(side1Faces=side1Faces1, name='Set_Surf_Disk')
    
    a = mdb.models[modelname].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#200020 #200100 #10000 ]', ), )
    region2=a.Surface(side1Faces=side1Faces1, name='Set_Surf_Pipe')
    mdb.models[modelname].SurfaceToSurfaceContactStd(name='SurfToSurf', 
        createStepName='Step-1', master=region1, slave=region2, sliding=FINITE, 
        enforcement=NODE_TO_SURFACE, thickness=OFF, 
        interactionProperty='IntProp_Fric', surfaceSmoothing=NONE, 
        adjustMethod=NONE, smooth=0.2, initialClearance=OMIT, datumAxis=None, 
        clearanceRegion=None)
    
    #------- Make ref point ----------
    
    a = mdb.models[modelname].rootAssembly
    a.ReferencePoint(point=(0.0, 0.0, 0.0))
    a = mdb.models[modelname].rootAssembly
    region5=a.surfaces['Set_Surf_Disk']
    a = mdb.models[modelname].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[11], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    mdb.models[modelname].RigidBody(name='Constr_RefP', refPointRegion=region1, 
        surfaceRegion=region5)    

    #---------- Make Disp BC on ref point ----------
    
    a = mdb.models[modelname].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[11], )
    region = a.Set(referencePoints=refPoints1, name='Set_RP-1')
    mdb.models[modelname].DisplacementBC(name='BC_Disp', 
        createStepName='Step-1', region=region, u1=0.0, u2=1.0, u3=0.0, 
        ur1=0.0, ur2=0.0, ur3=0.0, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)

    #----ZEEEEDing----   
    
    #---- Hole Sides -----

    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    pickedEdges1 = e.getSequenceFromMask(mask=('[#40000 #15a00 #0 #800000 ]', ), )
    pickedEdges2 = e.getSequenceFromMask(mask=(
        '[#10000 #44000000 #144 #780000 #80 ]', ), )
    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
        end2Edges=pickedEdges2, ratio=1.25, number=MSides, constraint=FINER)
    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#50000 #44015a00 #144 #f80000 #80 ]', ), 
        )
    p.Set(edges=edges, name='Set_Seed_HoleSides')

    #-------- Radial ------------

    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    pickedEdges1 = e.getSequenceFromMask(mask=('[#0:2 #50216a00 #20040120 #4000 ]', 
        ), )
    pickedEdges2 = e.getSequenceFromMask(mask=('[#0:2 #40000 #10 #8900 ]', ), )
    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
        end2Edges=pickedEdges2, ratio=2.0, number=MRad, constraint=FINER)
    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#0:2 #50256a00 #20040130 #c900 ]', ), )
    p.Set(edges=edges, name='Set_Seed_Radial')

    #----------- Circumferential ----------

    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=(
        '[#22495 #aad00000 #ad5000aa #1544a #35 ]', ), )
    p.seedEdgeByNumber(edges=pickedEdges, number=M, constraint=FIXED)
    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#22495 #aad00000 #ad5000aa #1544a #35 ]', 
        ), )
    p.Set(edges=edges, name='Set_Seed_Circumferential')

    #-------- Coarse ------------

    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#55680000 #80055 ]', ), )
    p.seedEdgeByNumber(edges=pickedEdges, number=MCoarse, constraint=FIXED)
    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#55680000 #80055 ]', ), )
    p.Set(edges=edges, name='Set_Seed_Coarse')

    #--------- Vertical ----------

    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=(
        '[#8890db6a #1122a508 #28a9411 #df02aa85 #1364a ]', ), )
    p.seedEdgeByNumber(edges=pickedEdges, number=1, constraint=FIXED)
    p = mdb.models[modelname].parts['Part-1']
    e = p.edges
    edges = e.getSequenceFromMask(mask=(
        '[#8890db6a #1122a508 #28a9411 #df02aa85 #1364a ]', ), )
    p.Set(edges=edges, name='Set_Seed_Vertical')  
    
    #----- Assign stack direction -----

    a = mdb.models[modelname].rootAssembly
    a.regenerate()
    p = mdb.models[modelname].parts['Part-1']

    elemType1 = mesh.ElemType(elemCode=C3D8, elemLibrary=STANDARD, 
        secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
    
    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1ffffff ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models[modelname].parts['Part-1']
    p.generateMesh()

    p = mdb.models[modelname].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1ffffff ]', ), )
    f = p.faces
    p.assignStackDirection(referenceRegion=f[15], cells=pickedCells)
    
    #----- The Gnaaaaaaaarrrrr!!! arrrrggghhhh!!!!-----
    
    if UMAT:
        mdb.Job(name=jobname, model=modelname, description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine=writefile+"\\for\\UMAT.for", 
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
            numGPUs=0)
    
    if not UMAT:
        mdb.Job(name=jobname, model=modelname, description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
            numGPUs=0)        
    
    mdb.save()
    mdb.jobs[jobname].submit(consistencyChecking=OFF)
        
    #----- Result section LE22 -----
    cont=False
    time.sleep(15)    
    for i in range(0,10000):
        time.sleep(5)
        if 'COMPLETED' in open(joblogname).read():
            cont=True
            break
        if 'Abaqus/Analysis exited with errors' in open(joblogname).read():
            break
        
    if not cont:
        print('Analysis for %s not ran')%(jobname)
        
    if cont:
        
        #--------- Paths -----------
        
        a = mdb.models[modelname].rootAssembly
        
        o3 = session.openOdb(
            name=jobfolder)
        
        session.viewports['Viewport: 1'].setValues(displayedObject=o3)
        a = mdb.models['Model-1'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.mdbData.summary()
        session.viewports['Viewport: 1'].setValues(
            displayedObject=session.odbs[jobfolder])
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(
            optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
        session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=100)        
        
        session.Path(name='Path_Circumferential', type=CIRCUMFERENTIAL, expression=((0, 0, 0), (0, 0, 
            10), (0, 75, 10)), circleDefinition=ORIGIN_AXIS, numSegments=100, 
            startAngle=0, endAngle=90, radius=CIRCLE_RADIUS)   
        
        session.Path(name='Path_Transverse', type=POINT_LIST, expression=((-75.0, 0.0, 
            10.0), (-75.0, 0.0, 25.0)))        
        
        #----- Result section LE22 -----
        

        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
            variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
            COMPONENT, 'LE22'))
        session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
            sectionResults=USE_TOP)

        xyp = session.XYPlot(XYPlotName)
        chartName = xyp.charts.keys()[0]
        chart = xyp.charts[chartName]
        pth = session.paths['Path_Circumferential']
        xy1 = xyPlot.XYDataFromPath(path=pth, includeIntersections=True, 
            projectOntoMesh=True, pathStyle=PATH_POINTS, numIntervals=100, 
            projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE)
        c1 = session.Curve(xyData=xy1)
        chart.setValues(curvesToPlot=(c1, ), )
        session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
        session.XYDataFromPath(name=NameOfFile, path=pth, includeIntersections=True,
            projectOntoMesh=True, pathStyle=PATH_POINTS, numIntervals=100, 
            projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE)        
        
        #------- Make report, reset visual ---------
        
        session.mdbData.summary()
        xyp = session.xyPlots[XYPlotName]
        session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
        odb = session.odbs[jobfolder]
        session.viewports['Viewport: 1'].setValues(displayedObject=odb)
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            CONTOURS_ON_DEF, ))
        x0 = session.xyDataObjects[NameOfFile]
        session.writeXYReport(fileName=NameOfResultFile1, xyData=(x0, ))
    
        #--------- Make LE11 --------------#

        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
            variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
            COMPONENT, 'LE11'))
        session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
            sectionResults=USE_TOP)

        xyp = session.XYPlot(XYPlotName2)
        chartName = xyp.charts.keys()[0]
        chart = xyp.charts[chartName]
        pth = session.paths['Path_Transverse']
        xy1 = xyPlot.XYDataFromPath(path=pth, includeIntersections=True, 
            projectOntoMesh=True, pathStyle=PATH_POINTS, numIntervals=100, 
            projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE)
        c1 = session.Curve(xyData=xy1)
        chart.setValues(curvesToPlot=(c1, ), )
        session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
        session.XYDataFromPath(name=NameOfFile2, path=pth, includeIntersections=True,
            projectOntoMesh=True, pathStyle=PATH_POINTS, numIntervals=100, 
            projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE)        
        
        #------- Make report, reset visual ---------
        
        session.mdbData.summary()
        xyp = session.xyPlots[XYPlotName2]
        session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
        odb = session.odbs[jobfolder]
        session.viewports['Viewport: 1'].setValues(displayedObject=odb)
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            CONTOURS_ON_DEF, ))
        x0 = session.xyDataObjects[NameOfFile2]
        session.writeXYReport(fileName=NameOfResultFile2, xyData=(x0, ))
