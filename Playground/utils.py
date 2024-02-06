import os

# default
# POSITIVE_PATH = 'positives'
# NEGATIVE_PATH = 'negatives'

# POSITIVE_OUTPUT = 'positives'
# NEGATIVE_OUTPUT = 'negatives'

POSITIVE_PATH = 'Dataset/Positive'
NEGATIVE_PATH = 'Dataset/Negative'

POSITIVE_OUTPUT = 'positives5k'
NEGATIVE_OUTPUT = 'negatives5k'

# Generate positives descriptor file for training
def generate_positives_txt():
    # Bounding box coordinates set equal to thumbnail dimensions
    bounding_rectangle = " 1 0 0 127 127"

    with open(f'{POSITIVE_OUTPUT}.txt', 'w') as f:
        for imageName in os.listdir(POSITIVE_PATH):
            # Write image path followed by ROI coordinates
            f.write(f'{POSITIVE_PATH}/' + imageName + bounding_rectangle + '\n')


# Generate negatives descriptor file for training
def generate_negatives_txt():
    with open(f'{NEGATIVE_OUTPUT}.txt', 'w') as f:
        for imageName in os.listdir(NEGATIVE_PATH):
            # Write image path
            f.write(f'{NEGATIVE_PATH}/' + imageName + '\n')

assert len(os.listdir(f'{POSITIVE_PATH}')) > 0, "Positives Directory has no images."
generate_positives_txt()

assert len(os.listdir(f'{NEGATIVE_PATH}')) > 0, "Negatives Directory has no images."
generate_negatives_txt()
