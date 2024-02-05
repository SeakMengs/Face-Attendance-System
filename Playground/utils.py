import os

# Generate positives descriptor file for training
def generate_positives_txt():
    # Bounding box coordinates set equal to thumbnail dimensions
    bounding_rectangle = " 1 0 0 127 127"

    with open('positives2.txt', 'w') as f:
        for imageName in os.listdir('positives'):
            # Write image path followed by ROI coordinates
            f.write('positives2/' + imageName + bounding_rectangle + '\n')


# Generate negatives descriptor file for training
def generate_negatives_txt():
    with open('negatives2.txt', 'w') as f:
        for imageName in os.listdir('negatives'):
            # Write image path
            f.write('negatives2/' + imageName + '\n')

assert len(os.listdir('positives')) > 0, "Positives Directory has no images."
generate_positives_txt()

assert len(os.listdir('negatives')) > 0, "Negatives Directory has no images."
generate_negatives_txt()
