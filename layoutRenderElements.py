import nuke
import nukescripts

#define group names
beauty_grp = 'Beauty'
lightSelect_grp = 'Light Selects'
lightingPass_grp = 'Lighting Passes'
lightingPassSecond_grp = 'Lighting Passes Secondary'
utility_grp = 'Utility'
id_grp = 'ID'
undefined_grp = 'Undefined'

#create group list
groupList = [
    beauty_grp,
    lightSelect_grp,
    lightingPass_grp,
    lightingPassSecond_grp,
    utility_grp,
    id_grp,
    undefined_grp
    ]

#vray hardcoded render names.
renderNamesLookupDict = dict()
renderNamesSearchDict = dict()
#beauty
renderNamesLookupDict[beauty_grp] = ["BEAUTY"]
#light selects
renderNamesSearchDict[lightSelect_grp] = ["LS"]
#lighting passses
renderNamesLookupDict[lightingPass_grp] = [
    "ATMOSPHERE",
    "DIFFUSE",
    "GI",
    "LIGHTING",
    "REFLECTION",
    "REFRACTION",
    "SELFILLUM",
    "SHADOW",
    "SPECULAR",
    "SSS"]
#lighting passses secondary
renderNamesLookupDict[lightingPassSecond_grp] = [
    "RAWGI",
    "RAWLIGHTING",
    "RAWREFLECTION",
    "RAWREFRACTION",
    "RAWSHADOW",
    "REFLECTIONFILTER",
    "REFRACTIONFILTER"]
#utilities
renderNamesLookupDict[utility_grp] = [
    "BUMPNORMALS",
    "POBJECT",
    "MATERIALID",
    "MATTESHADOW",
    "NORMALS",
    "PWORLD",
    "SAMPLERATE",
    "ZDEPTH"]
#IDs
renderNamesSearchDict[id_grp] = ["ID"]

#define backdrop colors
bgColorDict = {
    beauty_grp: 2241641985,
    lightSelect_grp: 3803559681, 
    lightingPass_grp: 2694310657,
    lightingPassSecond_grp: 1180666113,
    utility_grp: 2211297025,
    id_grp: 3248919041,
    undefined_grp: 2374606337
}

def selectedList():
    #return selected nodes
    nodes = nuke.selectedNodes()
    return nodes

def getCenterPos(inputNodes):
    #get center postion of all selected nodes 
    centerPos = []
    nodes = inputNodes
    amount = len(nodes)
    if amount == 0:
        return 0
    else:
        allX = sum( [ n.xpos()+n.screenWidth()/2 for n in nodes ] )  # SUM OF ALL X VALUES
        allY = sum( [ n.ypos()+n.screenHeight()/2 for n in nodes ] ) # SUM OF ALL Y VALUES
        centerX = allX / amount
        centerY = allY / amount
        centerPos.append(centerX)
        centerPos.append(centerY)
        return centerPos

def pStamp(nodes,posX,posY):
    #create postage stamp
    inputNodes = []
    inputNodes.append(nodes)
    for a in inputNodes:
        if a.Class()=='Read':
            namer = a.knob('file').getValue()
            col=2570627072
        else:
            namer=a.knob('name').getValue()
            col=2993684480
        namer= namer.split('/')[-1].split('.')[0]
        namer=namer+'_001'
        nukescripts.clear_selection_recursive()
        nuke.createNode('PostageStamp').setXYpos(posX,posY)
        for i in nuke.selectedNodes():
            i.setInput(0,a)
            i['tile_color'].setValue(col)
            verList=[]
            for i in nuke.allNodes():
                    if i.Class()=='PostageStamp':
                        if i.knob('name').getValue()[:-2]==namer[:-2]:
                            nVer = i.knob('name').getValue()[-1]
                            verList.append(nVer)
                            while namer[-1] in verList:
                                ver=int(namer[-1])
                                ver=str(int(ver)+1)
                                namer=namer[:-1]+ver
            for a in nuke.selectedNodes():
                if a.Class()=='PostageStamp':
                    a.knob('hide_input').setValue(True)
                    a.knob('name').setValue(namer)
                    nukescripts.clear_selection_recursive()
    return namer    

def isID(label):
    #is it a ID passe?
    if len(label.split('ID')) > 1:
        return True

def isLightSelect(label):
    #is it a light select?
    if label.split("_")[0] in renderNamesSearchDict[lightSelect_grp]:
        return True

def resultDict():
    #create result dict
    result = dict()
    #create selected node list
    nodes = selectedList()
    for n in nodes:
        nodeLabel = n.knob("label").value()
        nodeLabel = nodeLabel.upper()
        #matching primary elements
        if nodeLabel in renderNamesLookupDict[beauty_grp]:
            try:
                result[beauty_grp].append(n)
            except:
                result[beauty_grp] = [n]
            #print "beauty render: ", n.name(), nodeLabel
            continue
        elif isLightSelect(nodeLabel):
            try:
                result[lightSelect_grp].append(n)
            except:
                result[lightSelect_grp] = [n]
            #print "light select: ", n.name(), nodeLabel
            continue
        elif nodeLabel in renderNamesLookupDict[lightingPass_grp]:
            try:
                result[lightingPass_grp].append(n)
            except:
                result[lightingPass_grp] = [n]
            #print "lighting passes: ", n.name(), nodeLabel
            continue
        elif nodeLabel in renderNamesLookupDict[lightingPassSecond_grp]:
            try:
                result[lightingPassSecond_grp].append(n)
            except:
                result[lightingPassSecond_grp] = [n]
            #print "secondary lighting passes: ", n.name(), nodeLabel
            continue
        elif nodeLabel in renderNamesLookupDict[utility_grp]:
            try:
                result[utility_grp].append(n)
            except:
                result[utility_grp] = [n]
            #print "utility: ", n.name(), nodeLabel
            continue
        elif isID(nodeLabel):
            try:
                result[id_grp].append(n)
            except:
                result[id_grp] = [n]
            #print "id: ", n.name(), nodeLabel
            continue
        else:
            try:
                result[undefined_grp].append(n)
            except:
                result[undefined_grp] = [n]
            #print "undefined: ", n.name(), nodeLabel
    return result

def layoutDict():
    layoutNodes = dict()
    result = resultDict()
    requiredPasses = ["GI","REFLECTION","REFRACTION","SSS"]
    if beauty_grp in result.keys():
        for n in result[beauty_grp]:
            try:
                layoutNodes[beauty_grp].append(n)
            except:
                layoutNodes[beauty_grp] = [n]

    if lightSelect_grp in result.keys():
        for s in result[lightSelect_grp]:
            try:
                layoutNodes[lightSelect_grp].append(s)
            except:
                layoutNodes[lightSelect_grp] = [s]

    if lightingPass_grp in result.keys():
        for t in sorted(result[lightingPass_grp], key = lambda t:t.knob("label").value()):
            nodeLabel = t.knob("label").value()
            nodeLabel = nodeLabel.upper()
            if nodeLabel == "LIGHTING":
                try:
                    layoutNodes["Lighting"].insert(0,t)
                except:
                    layoutNodes["Lighting"] = [t]
            elif nodeLabel == "SPECULAR":
                try:
                    layoutNodes["Lighting"].append(t)
                except:
                    layoutNodes["Lighting"] = [t]
            elif nodeLabel in requiredPasses:    
                try:
                    layoutNodes[lightingPass_grp].append(t)
                except:
                    layoutNodes[lightingPass_grp] = [t]
            else:
                pass
    return layoutNodes
    
def organizeRenders():
    nodes = selectedList()
    result = resultDict()
    #define nodes position
    centerPos = getCenterPos(nodes)
    originX = centerPos[0]
    originY = centerPos[1]
    setX = originX
    setY = originY
    xOffset = 120
    yOffset = 200
    nodeUnitX =120
    nodeUnitY =180
    #for key in result.keys():
    for key in groupList:
        if key in sorted(result):
            nodes = result[key]
            for n in nodes:
                n.setXpos(setX)
                n.setYpos(setY)
                setX+=xOffset
            setX=originX
            #backdrop
            bgColor = int( bgColorDict[key])
            backdrop = nuke.nodes.BackdropNode(xpos = setX-20, ypos = setY-80, 
                        bdwidth=nodeUnitX*len(result[key]), bdheight = nodeUnitY,
                        tile_color = bgColor, note_font_size=50)
            backdrop.knob("label").setValue(key)
            setY+=yOffset

def createLayout():
    nodes = selectedList()
    if not nodes:
        print "There is nothing selected!"
    else:
        #organize render elements and creat backdrops
        organizeRenders()
        #get result dictionary
        result = resultDict()
        #get dictionary for layout
        layoutNodes = layoutDict()
        if beauty_grp in layoutNodes.keys():
            if lightingPass_grp in layoutNodes.keys():
                #create lighting passes for building layout 
                layoutNodesList = []
                if lightSelect_grp in result.keys():
                    layoutNodesList = layoutNodes[lightSelect_grp] + layoutNodes[lightingPass_grp]
                    print "Layout Completed. Built with:\nBEAUTY"
                    for node in layoutNodesList:
                        print node.knob("label").value()
                else:
                    if 'Lighting' in layoutNodes.keys():
                        layoutNodesList = layoutNodes['Lighting'] + layoutNodes[lightingPass_grp]
                        print "Layout completed. Built with:\nBEAUTY"
                        for node in layoutNodesList:
                            print node.knob("label").value()
                    else:
                        print "Error building layout: Missing both " + lightSelect_grp + " and Lighting Pass"
                #get initial position
                centerPos = getCenterPos(nodes)
                offsetOriginY = 600
                originX = result[beauty_grp][0].xpos()
                originY = centerPos[1] + offsetOriginY
                offsetX = 0
                #store beauty postageStamp node
                pStamp_beauty = []
                #store all unpremultBy nodes
                unpremultNodeList = []
                #store all unpremultBy dot nodes
                unpremultNodeDotList = []
                #store all merge nodes
                mergeNodeList = []
                for node in layoutNodes[beauty_grp]:
                    posX = originX
                    posY = originY
                    pStampName = pStamp(node,posX,posY)
                    pStamp_beauty.append(nuke.toNode(pStampName))
                #create and connect light select postageStamp nodes
                for node in layoutNodesList:
                    #define offset value for each postageStamp
                    offsetX += 200
                    #define postageStamp position
                    posX = originX + offsetX
                    posY = originY + 100
                    #create postageStamp
                    pStampName = pStamp(node,posX,posY)
                    pStampNode = nuke.toNode(pStampName)
                    #create unpremultBy node and connect inputs
                    unpremultNode = nuke.createNode("UnpremultBy")
                    unpremultNode['xpos'].setValue(posX-75)
                    unpremultNode['ypos'].setValue(posY+100)
                    unpremultNodeDot = nuke.nodes.Dot()
                    unpremultNodeDot['xpos'].setValue(unpremultNode.xpos() + 34)
                    unpremultNodeDot['ypos'].setValue(pStamp_beauty[0].ypos() + 27)
                    unpremultNode.setInput(0,pStampNode)
                    unpremultNode.setInput(1,unpremultNodeDot)
                    unpremultNodeList.append(unpremultNode)
                    unpremultNodeDotList.append(unpremultNodeDot)
                    #create merge nodes
                    if len(unpremultNodeList) > 1:
                        mergeNode = nuke.nodes.Merge()
                        mergeNode['xpos'].setValue(posX-75)
                        mergeNode['ypos'].setValue(posY+300)
                        mergeNode['operation'].setValue('plus')
                        mergeNode.setInput(1,unpremultNode)
                        mergeNodeList.append(mergeNode)
                #connect merge nodes
                for i in range(0,len(mergeNodeList)):
                    if i == 0:
                        mergeNodeDot = nuke.nodes.Dot()
                        mergeNodeDot['xpos'].setValue(unpremultNodeList[0].xpos() + 34)
                        mergeNodeDot['ypos'].setValue(mergeNodeList[0].ypos() + 4)
                        mergeNodeDot.setInput(0,unpremultNodeList[0])
                        mergeNodeList[i].setInput(0,mergeNodeDot)
                    else:
                        mergeNodeList[i].setInput(0,mergeNodeList[i-1])
                #connect unpremultBy dots to beauty
                for d in range(0,len(unpremultNodeDotList)):
                    if d == 0:
                        unpremultNodeDotList[d].setInput(0,pStamp_beauty[0])
                    else:
                        unpremultNodeDotList[d].setInput(0,unpremultNodeDotList[d-1])
                #create copy node 
                copyNode = nuke.nodes.Copy()
                copyNode['from0'].setValue('rgba.alpha')
                copyNode['to0'].setValue('rgba.alpha')
                copyNode['xpos'].setValue(mergeNodeList[-1].xpos())
                copyNode['ypos'].setValue(mergeNodeList[-1].ypos() + 200)
                copyNodeDot = nuke.nodes.Dot()
                copyNodeDot['xpos'].setValue(pStamp_beauty[0].xpos() + 34)
                copyNodeDot['ypos'].setValue(copyNode.ypos() + 10)
                copyNodeDot.setInput(0,pStamp_beauty[0])
                copyNode.setInput(1,copyNodeDot)
                copyNode.setInput(0,mergeNodeList[-1])
                #create copyBBox node
                copyBBoxNode = nuke.nodes.CopyBBox()
                copyBBoxNode['xpos'].setValue(mergeNodeList[-1].xpos())
                copyBBoxNode['ypos'].setValue(mergeNodeList[-1].ypos() + 238)
                copyBBoxDot = nuke.nodes.Dot()
                copyBBoxDot['xpos'].setValue(pStamp_beauty[0].xpos() + 34)
                copyBBoxDot['ypos'].setValue(copyBBoxNode.ypos() + 4)
                copyBBoxDot.setInput(0,copyNodeDot)
                copyBBoxNode.setInput(1,copyBBoxDot)
                copyBBoxNode.setInput(0,copyNode)
                #create premult node
                premultNode = nuke.nodes.Premult()
                premultNode['xpos'].setValue(mergeNodeList[-1].xpos())
                premultNode['ypos'].setValue(mergeNodeList[-1].ypos() + 300)
                premultNode.setInput(0,copyBBoxNode)
            else:
                print "Error building layout: Missing lighting passes."
        else:
            print "Error building layout: Missing beayty pass."





    
