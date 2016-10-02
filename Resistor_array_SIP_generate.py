#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory

from KicadModTree import *  # NOQA

def roundG(x, g):
    if (x>0):
        return math.ceil(x/g)*g
    else:
        return math.floor(x/g)*g


def roundCrt(x):
    return roundG(x, 0.05)



if __name__ == '__main__':
    for pins in range(5, 11):
        print(pins)
        rm=2.54
        h=0.5
        leftw=1.29
        ddrill=0.8
        padx=1.2
        pady=1.4
        crt_offset=0.25
        slk_offset=0.15
        lw_fab=0.1
        lw_crt=0.05
        lw_slk=0.15
        txt_offset=1

        w=(pins-1)*rm+2*leftw
        left=-leftw
        top=-h/2
        h_slk=max(h,pady)+2*slk_offset
        w_slk=w+2*slk_offset
        l_slk=-leftw-slk_offset
        r_slk=l_slk+w_slk
        t_slk=-h_slk/2
        w_crt=w_slk+2*crt_offset
        h_crt=max(h_slk, pady)+2*crt_offset
        l_crt=min(l_slk, -padx/2)-crt_offset
        t_crt=min(t_slk, -pady/2)-crt_offset
        
        
        footprint_name = "Resistor_Array_SIP%d" % (pins-1)
        lib_name = "Resistors_ThroughHole"

        print(footprint_name)

        # init kicad footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription("{0}-pin Resistor SIP pack, {1} resistors".format(pins, pins-1))
        kicad_mod.setTags("R")

        # set general values
        kicad_mod.append(Text(type='reference', text='REF**', at=[pins/2*rm, t_slk-txt_offset], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text=footprint_name, at=[pins/2*rm, h_slk/2+txt_offset], layer='F.Fab'))

        # create FAB-layer
        kicad_mod.append(RectLine(start=[left, top], end=[left+w, top+h], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[0.5*rm, top], end=[0.5*rm, top+h], layer='F.Fab', width=lw_fab))

        # create SILKSCREEN-layer
        kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk+h_slk], layer='F.SilkS'))
        kicad_mod.append(Line(start=[0.5*rm, t_slk], end=[0.5*rm, t_slk+h_slk], layer='F.SilkS'))

        # create courtyard
        kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

        # create pads 
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[0, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))
        for x in range(2,pins+1):
            kicad_mod.append(Pad(number=x, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[(x-1)*rm, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))

        # add model
        kicad_mod.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl",
                               at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

        # print render tree
        # print(kicad_mod.getRenderTree())
        # print(kicad_mod.getCompleteRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(footprint_name+'.kicad_mod')
