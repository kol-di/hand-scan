"""Blender add-on setup"""

bl_info = {
    "name" : "HandScan",
    "author" : "koldi",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


import bpy

from .addon.operators import HS_OT_CreateLeftHandMesh, HS_OT_CaptureHands
from .addon.panel import HS_PT_Panel

classes = (
    HS_OT_CreateLeftHandMesh, 
    HS_OT_CaptureHands,
    HS_PT_Panel,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


""" To run the addon you have to options

1) Install required packages into the directory with Blender python 
similiar to https://github.com/jkirsons/FacialMotionCapture_v2/blob/master/OpenCVAnimOperator.py

2) Create your own venv and specify path to site-packages folder in SITE_PACKAGES_PATH variable
"""

import sys
from pathlib import Path

addon_path = str(Path(bpy.path.abspath(__file__)).parent.absolute())
sys.path.append(addon_path)

SITE_PACKAGES_PATH = str(Path(__file__).parent / 'venv' / 'Lib' / 'site-packages')
sys.path.append(SITE_PACKAGES_PATH)
