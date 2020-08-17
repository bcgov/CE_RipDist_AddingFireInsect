#-------------------------------------------------------------------------------
# Name:         RiparianDisturbanceAssessment
# Purpose:      Calculates the percent of insect and fire disturbance within riparian area of each watershed feature.
#               Metadata concerning input layers: \\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis\RipDist_NS_Metadata
# Author:       nseguin
#
# Created:      08-08-2020
# Copyright:    BC Government
# Licence:      <your licence>
#-------------------------------------------------------------------------------

#Import system modules
import sys, string, os, time, win32com.client, datetime, win32api, arcpy, arcpy.mapping , csv

#Set environment settings
from arcpy import env
arcpy.env.overwriteOutput = True

#Set time stamp
time = time.strftime("%y%m%d")

#set a time year variable from current year
now = datetime.datetime.now()
#create a definition query variable that is 60 years old
FireYear = now.year - 60

#Location of BCGW w/Password embedded... You need to have a database called BCGW4Scripting.sde
BCGW = r'Database Connections\BCGW4Scripting.sde'

#Current Assessment Data with Assessment Units input
#au = arcpy.GetParameterAsText(0)
au = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\ESI_Data.gdb\CEF_2018\CEF_SSAF_Aquatics_2018_AU_Summary_200619"
#FWA Streams input
#streams = arcpy.GetParameterAsText(1)
streams = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\ESI_Data.gdb\Data\SSAF_fwaAU_FWA_Streams_200605"



#Insect Disturbance input
#insect = arcpy.GetParameterAsText(3)
insect_base = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\ESI_Data.gdb\CEF_2018\CEF_SSAF_Disturbance_Beetle_200715"

#Save Location Folder
#output_save = arcpy.GetParameterAsText(4)
output_save = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis"

#Unique Assessment Unit ID
au_ID = "WATERSHED_FEATURE_ID"
#au_ID = arcpy.GetParameterAsText(5)

#Human disturbance input
#Make sure that the disturbance feature includes roads and guard buffer
human_dist = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\ESI_Data.gdb\CEF_2018\CEF_ExtendedSSAF_Disturbance_RoadsGuardTrails_2018_200709"

#Create working geodatabase
save_gdb = "Working_RipDist_" + time
arcpy.CreateFileGDB_management(output_save, save_gdb)
output_gdb = output_save + r"\Working_RipDist_" + time + r".gdb"

#Fire Disturbance from past 60 years input
	#Jesse Fraser 2020/08/11 Doesn't need to be an input variable pull data from BCGW
#fires = arcpy.GetParameterAsText(2)
#fires_base = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Data\Values\Fish and Fish Habitat\Tier 1\Riparian Disturbance Analysis\RipDist_NS_200703.gdb\Fire_HmnErased_RipDistArea_200715"
hist_fire = 'WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP'
current_fire = 'WHSE_LAND_AND_NATURAL_RESOURCE.PROT_CURRENT_FIRE_POLYS_SP'

#Get the BCGW fire features
Input_current_fire = os.path.join(BCGW,hist_fire)
Input_hist_fire = os.path.join(BCGW,current_fire)

#create a query layer for the historic fires
arcpy.MakeFeatureLayer_management(Input_hist_fire,"histFire_lyr")
lyr_histFire = arcpy.mapping.Layer("histFire_lyr")

lyr_histFire.definitionQuery = r"FIRE_YEAR >= " +  str(FireYear)
SSAF_Current_Fire = output_gdb + r"\SSAF_Current_Fire_" + time
SSAF_Historic_Fire = output_gdb + r"\SSAF_Historic_Dist_Fire_" + time


arcpy.Clip_analysis(lyr_histFire, au, SSAF_Historic_Fire)
arcpy.Clip_analysis(Input_current_fire, au, SSAF_Current_Fire)

Dist_Fire = output_gdb + r"\SSAF_Dist_Fire_" + time
arcpy.Merge_management([SSAF_Current_Fire, SSAF_Historic_Fire], Dist_Fire)

#Jesse Fraser - 2020-08-11
#Need:
#code that takes base insect and then removes human and fire from insect
#Code that takes base fire and removes human

#Insect w/ human disturbance removed
insect_hmn_remove = output_gdb + r"\insect_hmn_remove_" + time

#Insect w/ all other disturbance removed
insect_dist_no_Overlap = output_gdb + r"\Insect_Dist_" + time

#Fire w/all other disturbance removed
fire_dist_no_Overlap = output_gdb + r"\Fire_Dist_" + time

#Erase the human disturbance from the fire disturbance
arcpy.Erase_analysis(Dist_Fire, human_dist, fire_dist_no_Overlap)

#Erase the human disturbance from insect disturbance
arcpy.Erase_analysis(insect_base, human_dist, insect_hmn_remove)

#Erase the fire disturbance from the insect disturbance
arcpy.Erase_analysis(insect_hmn_remove, fire_dist_no_Overlap, insect_dist_no_Overlap)

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
arcpy.AddField_management(working_au, "Rip_Tot_All_Dstrb_CLS", "TEXT")
arcpy.AddField_management(working_au, "Rip_Tot_All_Dstrb_NUM", "SHORT")

''' Not necessary if the assessment is by fire and insect
#Merge fire and insect disturbance layers
arcpy.Merge_management(["working_fires", "working_insect"], "output_gdb/disturbances_merged_" + time)




#List feature classes in new geodatabase
datasetList = arcpy.ListDatasets("*", "Feature")
for dataset in datasetList:
    print dataset
'''

#Create buffer disturbance features
Buff_Dist_Fire = output_gdb + r"\Buff_Dist_Fire_" + time
Buff_Dist_Insect = output_gdb + r"\Buff_Dist_Insect_" + time

#Buffer disturbance features
arcpy.Buffer_analysis(insect_dist_no_Overlap, Buff_Dist_Insect, "30 Meters")
arcpy.Buffer_analysis(fire_dist_no_Overlap, Buff_Dist_Fire, "30 Meters")

#Clip streams
Stream_Dist_Insect = output_gdb + r"\Streams_Dist_Insect_" + time
Stream_Dist_Fire = output_gdb + r"\Streams_Dist_Fire_" + time

arcpy.Clip_analysis(streams, Buff_Dist_Fire, Stream_Dist_Fire)
arcpy.Clip_analysis(streams, Buff_Dist_Insect, Stream_Dist_Insect)

#create a query layer for the assessment units
arcpy.MakeFeatureLayer_management(working_au,"au_lyr")
lyr_au = arcpy.mapping.Layer("au_lyr")
#Iterate through each assessment unit
with arcpy.da.UpdateCursor(working_au, [au_ID, "Rip_Fire_Dstrb_KM", "Rip_Insect_Dstrb_KM"]) as cursor:
	for test in cursor:

		#query the au layer to make sure that we are only working on an assessment unit
		lyr_au.definitionQuery = au_ID + r" = " + test[0]

		#Clip by AU
		#Fire
		au_Stream_Fire_Dist = output_gdb + r"\Streams_Dist_Fire_AU" + str(test[0]) + "_" + time
		arcpy.Clip_analysis(Stream_Dist_Fire, lyr_au, au_Stream_Fire_Dist)

		#Insect
		au_Stream_Insect_Dist = output_gdb + r"\Streams_Dist_Insect_AU" + str(test[0]) + "_" + time
		arcpy.Clip_analysis(Stream_Dist_Insect, lyr_au, au_Stream_Insect_Dist)

		#get the areafield name to avoid geometry vs shape issue (Thanks you Carol Mahood)
		desc = arcpy.Describe(au_Stream_Insect_Dist)
		geomField = desc.shapeFieldName
		insect_areaFieldName = str(geomField) + "_Area"

		#get the areafield name to avoid geometry vs shape issue (Thanks you Carol Mahood)
		desc = arcpy.Describe(au_Stream_Fire_Dist)
		geomField = desc.shapeFieldName
		Fire_areaFieldName = str(geomField) + "_Area"

		#Output stats tables
		au_Stream_Fire_sum = output_gdb + r"\SUM_Streams_Dist_Fire_AU" + str(test[0]) + "_" + time
		au_Stream_Insect_sum = output_gdb + r"\SUM_Streams_Dist_Insect_AU" + str(test[0]) + "_" + time

		#Get the total area for each
		arcpy.Statistics_analysis(au_Stream_Fire_Dist, au_Stream_Fire_sum, [Fire_areaFieldName, "SUM"])
		arcpy.Statistics_analysis(au_Stream_Insect_Dist, au_Stream_Insect_sum, [insect_areaFieldName, "SUM"])

		#Iterate through to get the sum of the lines for fire
		cursor = arcpy.SearchCursor(au_Stream_Fire_sum)
		fire_sum = 0
		for sum_fun in cursor:
			fire_sum = sum_fun2.getValue(Fire_areaFieldName) + fire_sum

		#set the total value into the output feature
		test[1] = fire_sum/1000

		#Iterate through to get the sum of the lines for insect
		cursor2 = arcpy.SearchCursor(au_Stream_Insect_sum)
		insect_sum = 0
		for sum_fun2 in cursor2:
			insect_sum = sum_fun2.getValue(insect_areaFieldName) + insect_sum

		test[2] = insect_sum/1000

		cursor.updateRow(test)


lyr_au.definition = ""
#Calculate Fields

#Calc Percents
form1 = r"(!Rip_Fire_Dstrb_KM!/!AU_TOT_strLngth_km!)*100"
form2 = r"(!Rip_Insect_Dstrb_KM!/!AU_TOT_strLngth_km!)*100"

arcpy.CalculateField_management(lyr_au, "Rip_Fire_Dstrb_PCNT", form1, "PYTHON_9.3")
arcpy.CalculateField_management(lyr_au, "Rip_Insect_Dstrb_PCNT", form2, "PYTHON_9.3")

#Calc New Total Disturbance
form3 = r"!Rip_Fire_Dstrb_KM!+!Rip_Insect_Dstrb_KM!+!Rip_Tot_Human_Dstrb_KM!"
arcpy.CalculateField_management(lyr_au, "Rip_Tot_All_Dstrb_KM", form3, "PYTHON_9.3")

#Calc Total Rip Dist
form4 = r"(!Rip_Tot_All_Dstrb_KM!/!AU_TOT_strLngth_km!)*100"
arcpy.CalculateField_management(lyr_au, "Rip_Tot_All_Dstrb_PCNT", form3, "PYTHON_9.3")

#Create, and calc the class and class num

#Low
#definition query to only have Low Risk Watersehds
lyr_au.definitionQuery = "Rip_Tot_All_Dstrb_PCNT <=5 OR Rip_Tot_All_Dstrb_PCNT IS NULL"

#Populate Appropriate fields
arcpy.CalculateField_management(lyr_au, "Rip_Tot_All_Dstrb_CLS", "Low", "PYTHON_9.3")
arcpy.CalculateField_management(lyr_au, "Rip_Tot_All_Dstrb_NUM", "0", "PYTHON_9.3")

lyr_au.definitionQuery = ""

#Medium
#definition query to only have Medium Risk Watershed
lyr_au.definitionQuery = "Rip_Tot_All_Dstrb_PCNT >5 AND Rip_Tot_All_Dstrb_PCNT <=15"

#Populate Appropriate fields
arcpy.CalculateField_management(lyr_au, "Rip_Tot_All_Dstrb_CLS", "Medium", "PYTHON_9.3")
arcpy.CalculateField_management(lyr_au, "Rip_Tot_All_Dstrb_NUM", "1", "PYTHON_9.3")

lyr_au.definitionQuery = ""

#High
#definition query to only have High Risk Watershed
lyr_au.definitionQuery = "Rip_Tot_All_Dstrb_PCNT >15 "

#Populate Appropriate fields
arcpy.CalculateField_management(lyr_au, "Rip_Tot_All_Dstrb_CLS", "High", "PYTHON_9.3")
arcpy.CalculateField_management(lyr_au, "Rip_Tot_All_Dstrb_NUM", "2", "PYTHON_9.3")

lyr_au.definitionQuery = ""
