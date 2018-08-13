n=1

jobname="Job_Flat_%s"%(n)


#NameOfFile="LE22_Path_Longt_%s_%s_%s_%s"%(M,MRad,MCoarse,MSides)
#NameOfFile2="LE11_Path_Longt_%s_%s_%s_%s"%(M,MRad,MCoarse,MSides)

#NameOfResultFile1="LE22"+modelname+".rpt"    
#NameOfResultFile2="LE11"+modelname+".rpt"

#XYPlotName="XY_Plot_Flat_LE22_%s"%(n)    
#XYPlotName2="XY_Plo_Flat_LE11_%s"%(n) 
#-----------------------------
writefile=r"C:\Users\eivinhug\NTNU\PhD\AbaqusModels\SplitDisk\MessAround"



f = open(writefile+"\\"+jobname+".inp", "r")
contents = f.readlines()
f.close()

f = open(writefile+"\\"+"UMATInsert"+".txt", "r")
Insertcontents = f.readlines()
f.close()

print(contents)
m=0
for line in contents:

    if line=="** MATERIALS\n":
        t=m+1
        break
    m=m+1

for i in range(0,(len(Insertcontents))):
    contents.insert(i+t,Insertcontents[i])

f = open(writefile+"\\"+jobname+"_UMAT"+".inp", "w")

for line in contents:
    f.write(str(line))
f.close()     