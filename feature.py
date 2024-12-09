import numpy as np
import os, random


"""
   This class aims to read in stream and split it into frames and output to input,txt and target,txt
     + do prediction
"""

class MFeature(object):
    def __init__(self,windowSize=5, stepSize=2, featureFile="./input.txt", targetFile="./target.txt"):
       self.windowSize = windowSize
       self.stepSize = stepSize
       self.featureFile = featureFile
       self.targetFile = targetFile
       self.str_padding_len = 4

       # delete the files if exist
       if os.path.exists(self.featureFile): 
          os.remove(self.featureFile)
       if os.path.exists(self.targetFile): 
          os.remove(self.targetFile)


    def process_frame(self, segment):
        """
	   Process a frame. Output it into two files:
                input.txt 
                target.txt
        """
        frame = ''.join(segment)
        with open(self.featureFile, 'a') as foutFea:
           with open(self.targetFile, 'a') as foutTarget:
              foutFea.write(frame + "\n")
              target = random.randint(0, 1)
              if target == 0: 
                 foutTarget.write("<UNK>N/A</UNK>\n")
              else:
                 foutTarget.write("<event><type>meeting</type><time>10 AM</time><date>tomorrow</date><participants><user>User1</user><user>User2</user><user>User3</user></participants></event>\n")
    
    def count_files_in_folder(folder_path): 
        # List all the files in the folder 
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))] 
        # Count the number of files 
        num_files = len(files) 
        return num_files

    def predict(self, segment, trainer):
       
       xml_summary = trainer.predict(segment)
       if "<UNK>" not in xml_summary: 
           print("Detect an event: ", xml_summary)
           cur_dir = "./results/" 
           i = count_files_in_folder(cur_dir)
           i += 1
           add_file_path = cur_dir + "event_" + str(i).zfill(self.str_padding_len)
           with open(add_file_path, 'w') as fout:
                fout.write(xml_summary)

    def split_stream(self, stream, trainer=None):
        """
         Split a stream into a frame sequence using a sliding window.
    
        Args:
            stream (list of str): List of messages from the stream.
        """
        num_messages = len(stream)
    
        for start_idx in range(0, num_messages - self.windowSize + 1, self.stepSize):
            frame = stream[start_idx:start_idx + self.windowSize]
            print(frame)
            if not predict:
                # dump features 
                self.process_frame(frame)
            else:
                # do prediction
                self.predict(frame, trainer)

