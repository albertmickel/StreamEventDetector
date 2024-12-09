# StreamEventDetector

##Several comments:

- This demo aims at testing my goal to see how much I can finish in 4 ~ 6 hours: one day at maximium (Sunday)
- Programming started from 11:am, Sunday, 12/08/2024 and ended at 8:52pm, Sunday, 12/08/2024
- Monday: write up the documentation only (in one hr) and then commit!!
- So what we have done so far:
  - feature.py: for feature generation and do online prediction 
  - trainer.py: the essential component
  - inference.py: a wrapper tool to test inference example
  - client.py: modify it to support feature dumping and online inference 

- no time to do:
  - need bugging for online inference within client.py
  - manually label data (currently use fixed values to fill up the fields for some samples randomly selected)
  - fine tune some important paramters to achieve higher performance
  - no time to create a dcoker and a local env to run train.py locally (the client.py was run locally to generate input.txt and target.txt). We ran it on colab to product the results (cf. the results given below)

- The code is not perfect, but it should be a working solution, when we manually labelled some data. The expected accuracy could reach 80% or a bit higher. However, for advanced performance, we must have more resoruces and time (cf. the comment below on this) 


## below were some of my thought I wrote in my working/thinking process (not deleted for just reference)

- This demo show a simple solution for event detection based on a given stream.
- The target time dedicated to this project is 4~6 hrs, the maximum is 8 hrs.
- Since we have limited time (4~6 hrs) and have no powerful gpus, except for using free service gpu, like colab, we will have to select a solution as simple as possible in this demo.
- The performance of this solution would be OK, or say, medium, which should roughly solve the problem. The expected accuracy would be around 80% or higher, if we manually label a big dataset. In fact, the bigger, the better! (see below the comment for labelling the data)
- If I had more GPUs, I would go for other more complicated solutions, e.g, using the pretrained model. However, it would surely require multiples GPUs and more stable GPU service (colab is not the stable one!)
- we need to manually label a dataset for training/dev/testing. This part of work would require a plenty of time. The basic idea is that the more labelled data, the better. However, for demo purpose, a small example set with several labelled samples would be enough! Please more focus on the methodology, but not the accuracy.
- Due to the limitted 4-6 hrs, the manual work has been skipped. Instead, we randomly chose some samples to label them as event being found and filled the feilds with the fixed values (for simulation only). In reality, we should have people to label the data manually.

- The whole structure of the codes is organized by three components whose names are self-explained: 
  -- feature.py: 
  -- train.py
  -- inference.py


- training curve:
  ```Init model!
  Start training...
  Epoch 1/10, Train Loss: 6.064892117793743, Dev Loss: 1.2988142222166061

  Epoch 2/10, Train Loss: 1.3353360891342163, Dev Loss: 0.8007514625787735

  Epoch 3/10, Train Loss: 0.8786612336452191, Dev Loss: 0.5996354594826698

  Epoch 4/10, Train Loss: 0.602766364812851, Dev Loss: 0.4177117720246315

  Epoch 5/10, Train Loss: 0.4098215275085889, Dev Loss: 0.28012335672974586

  Epoch 6/10, Train Loss: 0.2847662310187633, Dev Loss: 0.16099568456411362

  Epoch 7/10, Train Loss: 0.19452546995419723, Dev Loss: 0.13503759168088436

  Epoch 8/10, Train Loss: 0.13819390821915406, Dev Loss: 0.09735275711864233

  Epoch 9/10, Train Loss: 0.09944753004954411, Dev Loss: 0.06827877461910248

  Epoch 10/10, Train Loss: 0.07387460854191047, Dev Loss: 0.05415740702301264

Done!
  ```

- example inference outputs with respect to iterations:
  Init model!
```Start training...

Epoch 1/10, Train Loss: 6.180439215440017, Dev Loss: 1.6596072018146515

Generated XML Summary: < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < > < >

Epoch 2/10, Train Loss: 1.3400157873447125, Dev Loss: 1.1493702232837677

Generated XML Summary: < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > < / > <

Epoch 3/10, Train Loss: 0.8848875440084017, Dev Loss: 0.8143899440765381

Generated XML Summary: < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user > < / user >

Epoch 4/10, Train Loss: 0.6546788376111251, Dev Loss: 0.5249920152127743

Generated XML Summary: < / type > < / user > < / user > < / user > < / user > < / user > < user > user3 < / user > < / user > < user > user3 < / user > < / user > < user > user3 < / user > < / user > < user > user3 < / user > < / user > < user > user3 < / user > < / user > < user > user3 < / user > < /

Epoch 5/10, Train Loss: 0.4617459120658728, Dev Loss: 0.4145588092505932

Generated XML Summary: < / type > < / participants > < / user > < user > user3 < / user > < user > user3 < / user > < user > user3 < / user > < user > user3 < / user > < user > user3 < / user > < user > user3 < / user > < user > user3 < / user > < user > user3 < / user > < user > user3 < / user > < user > user3 < /

Epoch 6/10, Train Loss: 0.3212673927728946, Dev Loss: 0.28497982397675514

Generated XML Summary: < / type > < date > tomorrow < / user > < user > user1 < / user > < user > user3 < / user > < user > user3 < / user > < / user > < user > user3 < / user > < user > user3 < / user > < / user > < user > user3 < / user > < user > user3 < / user > < / user > < user > user3 < / user > < user > user

Epoch 7/10, Train Loss: 0.22522267928490272, Dev Loss: 0.21180029399693012

Generated XML Summary: < / type > < time > 10 am < / time > < date > tomorrow < / date > < participants > < user > user1 < / user > < user > user3 < / user > < / participants > < / event >

Epoch 8/10, Train Loss: 0.1645104753283354, Dev Loss: 0.1302384166046977

Generated XML Summary: < / type > < time > 10 am < / time > < date > tomorrow < / date > < participants > < user > user1 < / user > < user > user3 < / user > < / participants > < / event >

Epoch 9/10, Train Loss: 0.12452367750497964, Dev Loss: 0.12512813974171877

Generated XML Summary: < / type > < time > 10 am < / time > < date > tomorrow < / user > < user > user1 < / user > < user > user2 < / user > < user > user3 < / user > < / participants > < / event >

Epoch 10/10, Train Loss: 0.09711187734053685, Dev Loss: 0.0813563046976924

Generated XML Summary: < / type > < time > 10 am < / time > < date > tomorrow < / date > < participants > < user > user1 < / user > < user > user2 < / user > < user > user3 < / user > < / participants > < / event >

Done!
```



