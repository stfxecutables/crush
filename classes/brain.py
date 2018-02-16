import re

class Brain:

    def __init__(self):
        #self.segments=['3002','3003','1234']
        
        self.Segments = {"3002":"wm-lh-caudalanteriorcingulate ",
                         "3003":"wm-lh-caudalmiddlefrontal",
                         "3007":"wm-lh-fusiform"
                        }

        
class Measurement:
        
    def IntersectAndTerminate(self,data):
        #TODO -roi_end and -roi2
        #
        return
        
    def IntersectBoth(self,data):
        #TODO -roi and roi2
        return
        
    def NaturallyTerminate(self,data):
        #-roi_end and -roi_end2            
            #Number of tracks: 1078274
            #Number of tracks to render: 0
            #Number of line segments to render: 0
            #Mean track length: 0.00 +/- 0.00 mm
            #
            #Volume dimension: 256 256 256
            #Voxel size: 1.000 1.000 1.000

        ############
        m = re.search(r'Number of tracks: (\d+)', data)
        if m:
            self.Number_of_Tracks = m.group(1)
        else:
            self.Number_of_Tracks = 0
        ############
        m = re.search(r'Number of tracks to render: (\d+)', data)
        if m:
            self.Number_of_Tracks_to_Render = m.group(1)
        else:
            self.Number_of_Tracks_to_Render = 0
        ############
        m = re.search(r'Number of line segments to render: (\d+)', data)
        if m:
            self.Number_of_Line_Segments_to_Render = m.group(1)
        else:
            self.Number_of_Line_Segments_to_Render = 0
        ############
        m = re.search(r'Mean track length: (\d+.\d+) +/- (\d+.\d+)', data)
        if m:
            self.Mean_Track_Length = m.group(1)
            self.Mean_Track_Length_ErrBar = m.group(2)
        else:
            self.Mean_Track_Length = 0
            self.Mean_Track_Length_ErrBar = 0
        ############
        m = re.search(r'Volume dimension: (\d+) (\d+) (\d+)', data)
        if m:
            self.Volume_Dimension_X = m.group(1)
            self.Volume_Dimension_Y = m.group(2)
            self.Volume_Dimension_Z = m.group(3)
        else:
            self.Volume_Dimension_X = 0
            self.Volume_Dimension_Y = 0
            self.Volume_Dimension_Z = 0
            
        ############
        m = re.search(r'Voxel Size: (\d*[.,]?\d*) (\d*[.,]?\d*) (\d*[.,]?\d*)', data)
        if m:
            self.Voxel_Size_X = m.group(1)
            self.Voxel_Size_Y = m.group(2)
            self.Voxel_Size_Z = m.group(3)
        else:
            self.Voxel_Size_X = 0
            self.Voxel_Size_Y = 0
            self.Voxel_Size_Z = 0
                 
