"""====================================================================================================================
This is example code that helps extract csv file from .bin files generated from .vxl files using voxel viewer. 
  Author	 : Karthik Rajagopal (krthik@ti.com)
  Date	   : 28-Mar-2016
  Version	: v1.0
  Compatible Voxel viewer version: v0.4.0 
  Change Log : Initial version creation 
====================================================================================================================
"""

# coding: utf-8

# # This program Extracts CSV files from Volxe viewer generated .bin files (convered from .vxl) files

# In[61]:

# This section imports the packages needed for extraction
import os
import sys
import numpy as np


# In[62]:

# This section defines all the necessary steps required
#dataDir="D:/docs/3DTOF/OPT8320/CDK/binExtracts/"		# Change to required dir
dataDir="D:/ToF/data/"

# In[78]:

# This section defines all the necessary LUTs

deviceResolution=dict()
deviceResolution['OPT8320']=(60,80)
deviceResolution['OPT8241']=(240,320)


# This is the list of all possible extraction from .vxl file
#fileList=['Ambient','Amplitude','AmplitudeAvg','AmplitudeStd','Depth','DepthAvg','DepthStd','Distance','Phase','PhaseAvg','PhaseStd','PointCloud']
fileList=['PointCloud']
#fileList=['Depth']

fileDetails=dict()										# Creating Empty dictionary to be filled up based on file name

for fileT in fileList:
	fileDetails[fileT]=dict()							 # Creating Empty Dictionary entries to be filled up
#fileDetails['Ambient']['dtype']=np.uint8				  # C/C++ Equivalent of char data type
#fileDetails['Ambient']['nQuantities']=1				   # Only 1 Quantity per pixel stored
#fileDetails['Ambient']['quantityNames']=np.array(['raw']) # This is just for file naming
#fileDetails['Ambient']['reverseRowCols']=False			# This is to indicate whether the row and col order is reversed or not
#
#
#fileDetails['Amplitude']['dtype']=np.uint16
#fileDetails['Amplitude']['nQuantities']=1
#fileDetails['Amplitude']['quantityNames']=np.array(['raw'])
#fileDetails['Amplitude']['reverseRowCols']=False
#
#fileDetails['AmplitudeAvg']['dtype']=np.uint16
#fileDetails['AmplitudeAvg']['nQuantities']=1
#fileDetails['AmplitudeAvg']['quantityNames']=np.array(['avg'])
#fileDetails['AmplitudeAvg']['reverseRowCols']=False
#
#
#fileDetails['AmplitudeStd']['dtype']=np.uint16
#fileDetails['AmplitudeStd']['nQuantities']=1
#fileDetails['AmplitudeStd']['quantityNames']=np.array(['std'])
#fileDetails['AmplitudeStd']['reverseRowCols']=False
#
#
#
#fileDetails['Depth']['dtype']=np.float32
#fileDetails['Depth']['nQuantities']=1
#fileDetails['Depth']['quantityNames']=np.array(['raw'])
#fileDetails['Depth']['reverseRowCols']=False

#
#fileDetails['DepthAvg']['dtype']=np.float32
#fileDetails['DepthAvg']['nQuantities']=1
#fileDetails['DepthAvg']['quantityNames']=np.array(['avg'])
#fileDetails['DepthAvg']['reverseRowCols']=False
#
#
#fileDetails['DepthStd']['dtype']=np.float32
#fileDetails['DepthStd']['nQuantities']=1
#fileDetails['DepthStd']['quantityNames']=np.array(['std'])
#fileDetails['DepthStd']['reverseRowCols']=False
#
#
#fileDetails['Distance']['dtype']=np.float32
#fileDetails['Distance']['nQuantities']=1
#fileDetails['Distance']['quantityNames']=np.array(['raw'])
#fileDetails['Distance']['reverseRowCols']=False
#
#
#fileDetails['Phase']['dtype']=np.uint16
#fileDetails['Phase']['nQuantities']=1
#fileDetails['Phase']['quantityNames']=np.array(['raw'])
#fileDetails['Phase']['reverseRowCols']=False
#
#
#fileDetails['PhaseAvg']['dtype']=np.uint16
#fileDetails['PhaseAvg']['nQuantities']=1
#fileDetails['PhaseAvg']['quantityNames']=np.array(['avg'])
#fileDetails['PhaseAvg']['reverseRowCols']=False
#
#
#fileDetails['PhaseStd']['dtype']=np.uint16
#fileDetails['PhaseStd']['nQuantities']=1
#fileDetails['PhaseStd']['quantityNames']=np.array(['std'])
#fileDetails['PhaseStd']['reverseRowCols']=False


fileDetails['PointCloud']['dtype']=np.float32
fileDetails['PointCloud']['nQuantities']=4
fileDetails['PointCloud']['quantityNames']=np.array(['x','y','z','i'])
fileDetails['PointCloud']['reverseRowCols']=True


# In[79]:

# Use OPT8241 or OPT8320 according to file format
#device='OPT8320'
device='OPT8241'
fileSizeQ=np.product(deviceResolution[device]) # Quantized File Size


# In[81]:

# This section iterates though all file types and converts then to csv file. Creates 1 CSV file for each frame-quantity
for fileT in fileList:
	fileName=fileT+".bin"								# Adds .bin to the file extension 
	dtype=fileDetails[fileT]['dtype']					# datatype defined based on dictionary
	nQuantities=fileDetails[fileT]['nQuantities']		# Number of quantities per pixel defined based on dictionary
	quantityName=fileDetails[fileT]['quantityNames']	 # This is used to just name csv files
	filePath=dataDir+fileName
	if(os.path.exists(filePath)):						# Checking if file path exisits
		data=np.fromfile(filePath,dtype=dtype)		   # Loading Raw binary file from disk 
		if(np.size(data)%(fileSizeQ*nQuantities)==0):	# Checking if file size is quantied to whole frames
			nFrames=np.size(data)/(fileSizeQ*nQuantities)# Calculating number of frames in .bin file  
			print "INFO: %04d Frames in file [%s]"%(nFrames,filePath)
		else:
			print "ERROR: File size [%d] for file [%s] not a multiple of frame size [%d] X nQuantities [%d]"%(np.size(data),filePath,fileSizeQ,nQuantities)
	else:
		print "ERROR: Unable to open file [%s]"%(filePath)

	csvDir=dataDir+fileName.replace('.','_')			 # Directory where CSV files will be saved
	if(not os.path.exists(csvDir)):					  # Checking for existance of directory if not will be created
		os.makedirs(csvDir)							  # Creation of directory
	if(fileDetails[fileT]['reverseRowCols']):
		data=data.reshape(nFrames,deviceResolution[device][0],deviceResolution[device][1],nQuantities).swapaxes(-1,-2).swapaxes(-2,-3)
	else:
		data=data.reshape(nFrames,deviceResolution[device][1],deviceResolution[device][0],nQuantities).swapaxes(-1,-3)
		
	for c0 in np.arange(nFrames):						# Loop for each frame
		for c1 in np.arange(nQuantities):				# Loop for each quantity per pixel 
			dataSave=data[c0,c1]						 # Extracted data selected only for 1 frame and 1 quantity
			csvFileName=csvDir+'/frame%04d_%s.csv'%(c0,quantityName[c1])
			np.savetxt(csvFileName,dataSave,delimiter=',',newline='\n') # Saving in CSV format


