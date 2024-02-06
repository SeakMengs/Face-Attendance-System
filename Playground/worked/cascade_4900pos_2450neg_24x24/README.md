# Train time 3-4 Hours

opencv_traincascade -data cascade5k/ -vec positives5k.vec -bg negatives5k.txt -w 24 -h 24 -numPos 4900 -numNeg 2450 -numStages 10 -maxFalseAlarmRate 0.3 -minHitRate 0.999