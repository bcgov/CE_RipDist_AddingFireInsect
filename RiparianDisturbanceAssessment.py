#-------------------------------------------------------------------------------
# Name:         RiparianDisturbanceAssessment
# Purpose:      Calculates the percent of insect and fire disturbance within riparian area of each watershed feature.
#               Metadata concerning input layers: \\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis\RipDist_NS_Metadata
# Author:       nseguin
#
# Created:      08-08-2020
# Copyright:    (c) nseguin 2020
# Licence:      <your licence>
#-------------------------------------------------------------------------------

#Import system modules
import sys, string, os, time, win32com.client, datetime, win32api, arcpy, arcpy.mapping , csv

#Set environment settings
from arcpy import env
arcpy.env.overwriteOutput = True

#Current Assessment Data with Assessment Units input
#au = arcpy.GetParameterAsText(0)
au = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis\RipDist_NS_200703.gdb\CEF_SSAF_Aquatics_2018_AU_Summary_200619"

#FWA Streams input
#streams = arcpy.GetParameterAsText(1)
streams = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis\RipDist_NS_200703.gdb\SSAF_fwaAU_FWA_Streams_200605"

#Fire Disturbance from past 60 years input
#fires = arcpy.GetParameterAsText(2)
fires = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis\RipDist_NS_200703.gdb\Fire_HmnErased_RipDistArea_200715"

#Insect Disturbance input
#insect = arcpy.GetParameterAsText(3)
insect = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis\RipDist_NS_200703.gdb\Insect_AllErased_RipDistArea_200715"

#Jesse Fraser - 2020-08-11
#Need:
#code that takes base insect and then removes human and fire from insect
#Code that takes base fire and removes human



#Save Location Folder
#output_save = arcpy.GetParameterAsText(4)
output_save = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis"

#Set time stamp
time = time.strftime("%y%m%d")

#Create working geodatabase
save_gdb = "Working_RipDist_" + time
arcpy.CreateFileGDB_management(output_save, save_gdb)
output_gdb = output_save + r"\Working_RipDist_" + time + r".gdb"


#Copy Watershed Assessment Units to new geodatabase
working_au = output_gdb + r"\au_" + time
arcpy.CopyFeatures_management(au, working_au)

''' Don't need to copy over features that aren't going to be changed - Jesse Fraser
#Copy FWA Streams to new geodatabase
working_streams = output_gdb + r"\streams_" + time
arcpy.CopyFeatures_management(streams, working_streams)

#Copy Fire Disturbance to new geodatabase
working_fires = output_gdb + r"\fires_" + time
arcpy.CopyFeatures_management(fires, working_fires)

#Copy Insect Disturbance to new geodatabse
working_insect = output_gdb + r"\insect_" + time
arcpy.CopyFeatures_management(insect, working_insect)
'''

#Add fields to Watershed Assessment Units feature that are necessary
arcpy.AddField_management(working_au, "Rip_Fire_Dstrb_KM", "DOUBLE")
arcpy.AddField_management(working_au, "Rip_Insect_Dstrb_KM", "DOUBLE")
arcpy.AddField_management(working_au, "Rip_Fire_Dstrb_PCNT", "DOUBLE")
arcpy.AddField_management(working_au, "Rip_Insect_Dstrb_PCNT", "DOUBLE")
arcpy.AddField_management(working_au, "Rip_Tot_All_Dstrb_KM", "DOUBLE")
arcpy.AddField_management(working_au, "Rip_Tot_All_Dstrb_PCNT", "DOUBLE")

''' Not necessary if the assessment is by fire and insect
#Merge fire and insect disturbance layers
arcpy.Merge_management(["working_fires", "working_insect"], "output_gdb/disturbances_merged_" + time)

'''


#List feature classes in new geodatabase
datasetList = arcpy.ListDatasets("*", "Feature")
for dataset in datasetList:
    print dataset


#Iterate through each assessment unit
for 

#Buffer fire disturbance

#Buffer insect disturbance

#Clip stream line features by fire buffer

#Clip stream line features by insect buffer

