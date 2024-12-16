import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset, random_split
from transformers import BertTokenizer

if __name__ ==  "__main__":
     trainer = MTrainer()
     print("Init model!")
     trainer.load_model('seq2seq_model.pth')

     # test one sample
     new_message_stream = "User1: We need to discuss the new project plan. Can we meet at 3 PM?" 
     # Generate XML summary 
     xml_summary = trainer.predict(new_message_stream) 
     print("Generated XML Summary:", xml_summary) 
