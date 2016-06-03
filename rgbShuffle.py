import nuke
import nukescripts

#rgb hex value
#red value: 4278190081
#green value: 16711681
#blue value: 65281

def shuffle_R():
    node = nuke.createNode("Shuffle","name RED tile_color 4278190081")
    node['red'].setValue('red')
    node['green'].setValue('red')
    node['blue'].setValue('red')
    node['alpha'].setValue('red')

def shuffle_G():
    node = nuke.createNode("Shuffle","name GREEN tile_color 16711681")
    node['red'].setValue('green')
    node['green'].setValue('green')
    node['blue'].setValue('green')
    node['alpha'].setValue('green')

def shuffle_B():
    node = nuke.createNode("Shuffle","name BLUE tile_color 65281")
    node['red'].setValue('blue')
    node['green'].setValue('blue')
    node['blue'].setValue('blue')
    node['alpha'].setValue('blue')
