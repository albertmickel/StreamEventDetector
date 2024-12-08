import numpy as np
import os, random


"""
   This class aims to read in stream and split it into frames and output to input,txt and target,txt
"""

class MFeature(object):
    def __init__(self,windowSize=5, stepSize=2, featureFile="./input.txt", targetFile="./target.txt"):
       self.windowSize = windowSize
       self.stepSize = stepSize
       self.featureFile = featureFile
       self.targetFile = targetFile

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
    

    def split_stream(self, stream):
        """
         Split a stream into a frame sequence using a sliding window.
    
        Args:
            stream (list of str): List of messages from the stream.
        """
        num_messages = len(stream)
    
        for start_idx in range(0, num_messages - self.windowSize + 1, self.stepSize):
            frame = stream[start_idx:start_idx + self.windowSize]
            print(frame)
            self.process_frame(frame)

