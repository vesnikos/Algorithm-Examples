# -*- coding: utf-8 -*-
__author__ = 'vesnikos'
__date__ = '24/10/2014'

import os
import arcpy


coord_list = [[
    [22.70583,41.39760],
    [25.42068,41.32526],
    [25.28676,39.24203],
    [22.65399,39.30926]
]]


# A list of features and coordinate pairs
feature_info = [[[1, 2], [2, 4], [3, 7]],
                [[6, 8], [5, 7], [7, 2], [9, 5]]]
cwd = os.path.dirname(__file__)
data_dir = os.path.join(cwd,"data")
outFC = os.path.join(data_dir,"test.shp")
# A list that will hold each of the Polygon objects
features = []

for feature in coord_list:
    # Create a Polygon object based on the array of points
    # Append to the list of Polygon objects
    features.append(
        arcpy.Polygon(
            arcpy.Array([arcpy.Point(*coords) for coords in feature])))

# Persist a copy of the Polyline objects using CopyFeatures
arcpy.CopyFeatures_management(features, outFC)