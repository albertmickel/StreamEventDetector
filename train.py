import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset, random_split
from transformers import BertTokenizer


class Seq2Seq(nn.Module):
    def __init__(self, input_dim, output_dim, emb_dim, hid_dim, num_layers=1):
        super(Seq2Seq, self).__init__()
        self.encoder = nn.LSTM(emb_dim, hid_dim, num_layers=num_layers, batch_first=True)
        self.decoder = nn.LSTM(emb_dim, hid_dim, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hid_dim, output_dim)
        self.embedding = nn.Embedding(input_dim, emb_dim)
    
    def forward(self, src, trg):
        # Encode
        embedded_src = self.embedding(src)
        encoder_outputs, (hidden, cell) = self.encoder(embedded_src)
        
        # Decode
        embedded_trg = self.embedding(trg)
        decoder_outputs, _ = self.decoder(embedded_trg, (hidden, cell))
        
        # Output
        output = self.fc(decoder_outputs)
        return output


class MMsgDataset(Dataset):
    def __init__(self, message_sequences, decoder_input_sequences, decoder_target_sequences):
        self.message_sequences = message_sequences
        self.decoder_input_sequences = decoder_input_sequences
        self.decoder_target_sequences = decoder_target_sequences

    def __len__(self):
        return len(self.message_sequences)

    def __getitem__(self, idx):
        return (self.message_sequences[idx],
                self.decoder_input_sequences[idx],
                self.decoder_target_sequences[idx])




class MTrainer(object):
    def __init__(self, vocab_size = 30522, embedding_dim = 256, hidden_units = 512, num_layers=1):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_units = hidden_units
        self.num_layers = num_layers

        # read messages
        self.message_streams = self.read_samples("input.txt")
        self.xml_summaries = self.read_samples("target.txt") 

    def read_samples(self, fileName):
        samples = []
        with open(fileName, 'r') as fp:
           for sample in fp:
               samples.append(sample)
        return samples
    

    def init_model(self):
        # Initialize the tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        # Tokenize the data
        message_sequences = [self.tokenizer.encode(m, add_special_tokens=True) for m in self.message_streams]
        summary_sequences = [self.tokenizer.encode(s, add_special_tokens=True) for s in self.xml_summaries]

        # Pad the sequences
        message_sequences = pad_sequence([torch.tensor(seq) for seq in message_sequences], batch_first=True, padding_value=0)
        summary_sequences = pad_sequence([torch.tensor(seq) for seq in summary_sequences], batch_first=True, padding_value=0)

        # Split input and target sequences
        decoder_input_sequences = summary_sequences[:, :-1]
        decoder_target_sequences = summary_sequences[:, 1:]

        self.dataset = MMsgDataset(message_sequences, decoder_input_sequences, decoder_target_sequences)

        # Split dataset into training and dev sets
        self.train_size = int(0.8 * len(self.dataset))
        self.dev_size = len(self.dataset) - self.train_size
        self.train_dataset, self.dev_dataset = random_split(self.dataset, [self.train_size, self.dev_size])

        self.train_dataloader = DataLoader(self.train_dataset, batch_size=2, shuffle=True)
        self.dev_dataloader = DataLoader(self.dev_dataset, batch_size=2, shuffle=True)

        # Instantiate the model
        self.model = Seq2Seq(self.vocab_size, self.vocab_size, self.embedding_dim, self.hidden_units, self.num_layers)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters())

    def train(self):
      # Train the model
      num_epochs = 10
      for epoch in range(num_epochs):
         self.model.train()
         train_loss = 0
         for message_seq, dec_input_seq, dec_target_seq in self.train_dataloader:
            self.optimizer.zero_grad()
            output = self.model(message_seq, dec_input_seq)
            loss = self.criterion(output.view(-1, self.vocab_size), dec_target_seq.view(-1))
            loss.backward()
            self.optimizer.step()
            train_loss += loss.item()
         avg_train_loss = train_loss / len(self.train_dataloader)
    
         # Evaluate on the dev set
         self.model.eval()
         dev_loss = 0
         with torch.no_grad():
            for message_seq, dec_input_seq, dec_target_seq in self.dev_dataloader:
                output = self.model(message_seq, dec_input_seq)
                loss = self.criterion(output.view(-1, self.vocab_size), dec_target_seq.view(-1))
                dev_loss += loss.item()
         avg_dev_loss = dev_loss / len(self.dev_dataloader)
    
         print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {avg_train_loss}, Dev Loss: {avg_dev_loss}")

         # save it on the disk
         self.model_save_path = 'seq2seq_model.pth' 
         # Save the model's state dictionary 
         torch.save(self.model.state_dict(), self.model_save_path)

         # test one sample
         new_message_stream = "User1: We need to discuss the new project plan. Can we meet at 3 PM?"
         # Generate XML summary
         xml_summary = self.predict(new_message_stream)
         print("Generated XML Summary:", xml_summary)

    def load_model(self, model_save_path='seq2seq_model.pth'):
        # Initialize the tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = Seq2Seq(self.vocab_size, self.vocab_size, self.embedding_dim, self.hidden_units, self.num_layers) 
        # Load the model's state dictionary from the saved file 
        self.model.load_state_dict(torch.load(model_save_path)) 
        # Set the model to evaluation mode 
        self.model.eval()

    def predict(self, message_stream):
        self.model.eval()  # Set the model to evaluation mode
    
        # Tokenize and pad the message stream
        message_sequence = self.tokenizer.encode(message_stream, add_special_tokens=True)
        message_sequence = torch.tensor([message_sequence])
        message_sequence = message_sequence.long()

        with torch.no_grad(): 
            # Initialize the decoder input with the start token 
            decoder_input = torch.tensor([[self.tokenizer.cls_token_id]]) 
            # Encode the message sequence 
            embedded_src = self.model.embedding(message_sequence) 
            encoder_outputs, (hidden, cell) = self.model.encoder(embedded_src) 
            summary_tokens = [] 
            for _ in range(100): # Limit the maximum length of the summary to 100 tokens 
               embedded_trg = self.model.embedding(decoder_input) 
               decoder_outputs, (hidden, cell) = self.model.decoder(embedded_trg, (hidden, cell)) 
               output =self.model.fc(decoder_outputs[:, -1, :]) 
               # Get the predicted token 
               _, predicted_token = torch.max(output, dim=1) 
               # Append the predicted token to the summary 
               summary_tokens.append(predicted_token.item()) 
               # Stop if the end token is generated 
               if predicted_token.item() == self.tokenizer.sep_token_id: 
                  break 
               # Prepare the next decoder input 
               decoder_input = torch.cat([decoder_input, predicted_token.unsqueeze(0)], dim=1) 

        # Decode the summary tokens to text 
        summary = self.tokenizer.decode(summary_tokens, skip_special_tokens=True) 
        return summary       



if __name__ == "__main__":
     trainer = MTrainer()
     print("Init model!")
     trainer.init_model()
     print("Start training...")
     trainer.train()
     print("Done!")