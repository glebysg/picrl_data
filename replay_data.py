import cv2
import pickle
import numpy as np

def frames_to_video(FILE_NAME, fps=10, processing="color"):
    """Code to stitch a video based on frames saved in a pickle file"""
    
    print("stiching colour frames into video")
    
    #Load first colour frame, to get colour frame properties
    datafile = open("data\\COLOUR." + FILE_NAME + ".pickle", "rb")
    datafile_depth = open("data\\DEPTH." + FILE_NAME + ".pickle", "rb")
    if processing == "color":
        filename = 'data\\COLOUR.'  + FILE_NAME + '.avi'
        frame = pickle.load(datafile)
        height, width, channels = frame.shape
    else:
        filename = 'data\\DEPTH.'  + FILE_NAME + '.avi'
        frame = pickle.load(datafile_depth)
        height, width, channels = ( 424, 512, 1)
    
    #define video properties
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), fps, (int(width), int(height))) 
    
    #display first frame on a screen for progress (some duplication of later code as first frame needs to be loaded seperately to the rest so we can get the frame dimensions from it)
    # out.write(frame)
    # cv2.imshow('Stiching Video',frame)

    #Cycle through the rest of the colour frames, stiching them together
    while True:
        try:
            if processing=="color":
                frame = pickle.load(datafile)
                out.write(frame)
                cv2.imshow('Stiching Video',frame)
                if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
                    break

            else:
                frame = pickle.load(datafile_depth)
                cut_down_depth_frame = frame.astype(np.uint8)
                cut_down_depth_frame = np.reshape(cut_down_depth_frame, (424, 512))
                cut_down_depth_frame = cv2.cvtColor(cut_down_depth_frame, cv2.COLOR_GRAY2RGB)
                out.write(cut_down_depth_frame)
                cv2.imshow('Stiching Video',cut_down_depth_frame)
                if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
                    break

        except EOFError:
            print("Video Stiching Finished")
            break

    # Release everything if job is finished
    out.release()
    cv2.destroyAllWindows()
if __name__ == '__main__': 
    
    #replace name below with the corresponding section of the name of your saved depth data (for reference, the full name of my saved colour data file was COLOUR.test.1.29.13.17.pickle)
    frames_to_video('S1.28.4.4.26',30,"depth")    