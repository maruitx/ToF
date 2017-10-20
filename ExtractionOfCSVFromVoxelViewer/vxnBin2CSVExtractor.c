/*====================================================================================================================
This is example code that helps extract csv file from .bin files generated from .vxl files using voxel viewer. 
  Author     : Karthik Rajagopal (krthik@ti.com)
  Date       : 28-Mar-2016
  Version    : v1.0
  Compatible Voxel viewer version: v0.4.0 
  Change Log : Initial version creation 
====================================================================================================================
*/

// Standard Includes for file I/O 
#include<stdio.h>
#include<stdlib.h>
 
#define NROWS     60   // Set this to 60 for OPT8320. In case of OPT8241 choose 240
#define NCOLS     80   // Set this to 80 for OPT8320. In case of OPT8241 choose 320
#define NFRAMES   175  // Set this based on how many frames are captured in the .vxl/.bin file. This information is shown while exporting .bin file from .vlx file


void vxlBin2CSV(void){ // Function to read all streams (except PointCloud) file and create csv
 
    FILE *inFile,*csvFile;   // File Pointer declaration 
    char fileName[30];       // Generic file name container strings. Re-allocate more memory based on file name length/path
	char csvFileName[30];    // Generic file name container strings. Re-allocate more memory based on file name length/path
	char frame[NFRAMES][NCOLS][NROWS]; // Set this data type as follows 
/*  Please refer to Table 1 in Extration of csv files from voxel viewer document 
	---------------
	Stream:datatype
	---------------
	Ambient:char
	Amplitude:unsigned short int
	AmplitudeAvg:unsigned short int
	AmplitudeStd:unsigned short int
    
	Depth:float
	DepthAvg:float
	DepthStd:float
	
	Distance:float
	
	Phase:unsigned short int
	PhaseAvg:unsigned short int
	PhaseStd:unsigned short int
*/	
	int i,j,k; // generic pointers
    
	sprintf(fileName,"Ambient.bin");           // Assign file name as per file name given while exporting
	
	inFile=fopen(fileName, "rb");              // Opening .bin file    
 
    fread(frame, sizeof(char), NFRAMES*NCOLS*NROWS, inFile);  // Reading all binary values all at once
	fclose(inFile);                                           // Closing .bin file since all lines are read already                                     
/*
	sizeof(char) needs to be replaced with sizeof(unsigned short int) or sizeof(float) as per the stream extracted mentioned above
*/
 
    for (i=0;i<NFRAMES;i++) {                              // Loop to iterate over number of frames 
		sprintf(csvFileName,"%s_frame:%04d.csv",fileName,i);     // File names for each frame 
		csvFile=fopen(csvFileName,"w");                    // opening CSV file to dump frame 
		for (j=0;j<NROWS;j++)                              // Loop to iterate over rows 
		{
			for (k=0;k<NCOLS;k++)                          // Loop to iterate over columns 
					fprintf(csvFile,"%d,",frame[i][k][j]); // printing each pixel value to the csv file 
/*
			replace %d with %f or %g if data type is float. This depends on the stream extracted  

*/
			fprintf(csvFile,"\n");                         // printing newline separator for reach row
		}
		fclose(csvFile);                                   // closing CSV file 
	}
	return; // void return 
}


void pointCloudBin2CSV(void){ // Function to read  PointCloud stream (.bin) file and create csv
 
    FILE *inFile,*csvFile;   // File Pointer declaration 
    char fileName[60];       // Generic file name container strings. Re-allocate more memory based on file name length/path
	char csvFileName[60];    // Generic file name container strings. Re-allocate more memory based on file name length/path
	char quantitiesList[] = {'x','y','z','i'}; // Generatation of list of quantities in order which is stored 
	float frame[NFRAMES][NROWS][NCOLS][4]; 
	int i,j,k,m; // generic pointers
    
	sprintf(fileName,"PointCloud.bin");           // Assign file name as per file name given while exporting
	
	inFile=fopen(fileName, "rb");              // Opening .bin file    
 
    fread(frame, sizeof(float), NFRAMES*NROWS*NCOLS*4, inFile);  // Reading all binary values all at once
	fclose(inFile);                                           // Closing .bin file since all lines are read already                                     
 
    for (i=0;i<NFRAMES;i++) {                              // Loop to iterate over number of frames 
		for(m=0;m<4;m++){                                  // Loop to iterate over quantities per pixel 
			sprintf(csvFileName,"%s_q:%c_frame:%04d.csv",fileName,quantitiesList[m],i);     // File names for each frame 
			csvFile=fopen(csvFileName,"w");                    // opening CSV file to dump frame 
			for (j=0;j<NROWS;j++)                              // Loop to iterate over rows 
			{
				for (k=0;k<NCOLS;k++)                          // Loop to iterate over columns 
						fprintf(csvFile,"%f,",frame[i][j][k][m]); // printing each pixel value to the csv file 
				fprintf(csvFile,"\n");                         // printing newline separator for reach row
			}
			fclose(csvFile);                                   // closing CSV file 
		}
	}
	return; // void return 
}

int main()
{
    vxlBin2CSV();
	pointCloudBin2CSV();
	return 0;
}
