# Train time 3-4 Hours

opencv_traincascade -data cascade5k/ -vec positives5k.vec -bg negatives5k.txt -w 28 -h 28 -numPos 3000 -numNeg 1500 -numStages 9 -maxFalseAlarmRate 0.3 -minHitRate 0.999