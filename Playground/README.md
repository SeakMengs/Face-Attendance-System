# Install opencv

Use version 3.4.16 because it has opencv_createsamples.exe
```
https://sourceforge.net/projects/opencvlibrary/files/3.4.16/
```
Set up and put bin folder into environment path
example E:\opencv\build\x64\vc15\bin

# Docs for more usage

https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html

# Create Opencv Samples

Create positive samples from images for training
```
opencv_createsamples -info positives.txt -w 24 -h 24 -num 1000 -vec positives.vec
```

# Train Cascade

-numPos: number of positive samples, must be less than or equal to the number of samples in positives.vec

In this case we created sample 1000 positives vec and we use 900 for training

-numNeg: number of negative samples, can be any number

advice: put numNeg = numPos / 2 or numNeg = numPos * 2

numStages: number of stages, the more stages the more accurate but also the more time it takes to train

- maxFalseAlarmRate: the lower the better, but it will take longer to train

- minHitRate: the higher the better, but it will take longer to train
```
opencv_traincascade -data cascade/ -vec positives.vec -bg negatives.txt -w 24 -h 24 -numPos 900 -numNeg 450 -numStages 10 -maxFalseAlarmRate 0.3 -minHitRate 0.999 
```

train and specify ram usage
```
opencv_traincascade -data cascade/ -vec positives.vec -bg negatives.txt -w 24 -h 24 -numPos 900 -numNeg 450 -numStages 10 -maxFalseAlarmRate 0.3 -minHitRate 0.999 -precalcValBufSize 6144 -precalcIdxBufSize 6144
```

## Note For Train Cascade
 
- FA = False Alarm
- HR = Hit Rate
- We want the false alarm rate to be as low as possible and the hit rate to be as high as possible
- If the FA is too high, we can increase the number of negative samples
- If the HR is too low, we can increase the number of positive samples
- HR is % of positive samples that are correctly classified as positive
- FA is % of negative samples that are incorrectly classified as positive

## How to perfect train cascade

https://stackoverflow.com/questions/16058080/how-to-train-cascade-properly

First you need a couple of original samples (don't use one and multiply it with create samples). I have used 10 different photos of beer bottles, for each I have created 200 hundred samples, then I have combined all samples in one vector file with 2000 samples.
-w 20 -h 35 should match aspect ratio of your original image
Relation of positive samples to negative should be around 2:1 (there should be more positive samples)
Number of stages you should chose by yourself (for me it is 12-13). The more stages you set the more precisely will be your cascade, but you can also overtrain your cascade and it won't find anything. The precision of your cascade is shown by acceptanceRatio on the last stage it should be around this value 0.000412662 or less.
But if you get acceptanceRatio like this 7.83885e-07 your cascade is probably overtrained and it wont find anything, try to set less stages.

!!! And one more important thing, when you train your cascade you should have more than one feature on your stage beginning from 2 or 3 stage. If you have only one feature you wont get good cascade. You should work on your training images (negative and positive samples). Normal training will look like this:


## 5k Train

Create 5k positive samples
```
opencv_createsamples -info positives5k.txt -w 28 -h 28 -num 5000 -vec positives5k.vec
```

Train 5k
```
opencv_traincascade -data cascade5k/ -vec positives5k.vec -bg negatives5k.txt -w 28 -h 28 -numPos 5000 -numNeg 2500 -numStages 10 -maxFalseAlarmRate 0.3 -minHitRate 0.999
```

## Resource

Positive: https://drive.google.com/drive/folders/1tg-Ur7d4vk1T8Bn0pPpUSQPxlPGBlGfv
Negative data set: https://github.com/handaga/tutorial-haartraining/tree/master/data/negatives