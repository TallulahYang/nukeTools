import nuke
import nukescripts

#print all node knobs(attributes)
def printKnobs():
    print '\n'.join(sorted(nuke.selectedNode().knobs()))

def test():
    print "hello world"

#convert rgb to hex value
def getHexColor():
    print "hello world" 
    """
    r = red
    g = green
    b = blue
    hexColor = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16)
    return hexColor
    """