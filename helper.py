# CIFAR - 10

import pickle
import numpy as np
from keras.utils import np_utils
from matplotlib import pyplot as plt




#constants

path = "data/"  # Path to data 

# Height or width of the images (32 x 32)
size = 32 
# 3 channels: Red, Green, Blue (RGB)
channels = 3  
# Size of flattened image
size_flat = size * size * channels

num_classes = 10 

# Each file contains 10000 images
image_batch = 10000 
# 5 training files
num_files_train = 5  

# Total number of training images
images_train = image_batch * num_files_train




def unpickle(file):  
    
    # Convert byte stream to object
    with open(path + file,'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
        
    return dict




def convert_images(raw_images):
    
    # Convert images to numpy arrays
    
    # Convert raw images to numpy array and normalize it
    raw = np.array(raw_images, dtype = float) / 255.0
    
    # Reshape to 4-dimensions - [image_number, channel, height, width]
    images = raw.reshape([-1, channels, size, size])

    images = images.transpose([0, 2, 3, 1])

    # 4D array - [image_number, height, width, channel]
    return images




def load_data(file):
    # Load file, unpickle it and return images with their labels
    
    data = unpickle(file)
    
    # Get raw images
    images_array = data[b'data']
    
    # Convert image
    images = convert_images(images_array)
    # Convert class number to numpy array
    labels = np.array(data[b'labels'])
        
    
    return images, labels




def get_test_data():
    # Load all test data
    
    images, labels = load_data(file = "test_batch")
    
    return images, labels, np_utils.to_categorical(labels,num_classes)




def get_train_data():
    # Load all training data in 5 files
    
    # Pre-allocate arrays
    images = np.zeros(shape = [images_train, size, size, channels], dtype = float)
    labels = np.zeros(shape=[images_train],dtype = int)
    
    # Starting index of training dataset
    start = 0
    
    # For all 5 files
    for i in range(num_files_train):
        
        # Load images and labels
        images_batch, labels_batch = load_data(file = "data_batch_" + str(i+1))
        
        # Calculate end index for current batch
        end = start + image_batch
        
        # Store data to corresponding arrays
        images[start:end,:] = images_batch        
        labels[start:end] = labels_batch
        
        # Update starting index of next batch
        start = end
    
    return images, labels, np_utils.to_categorical(labels,num_classes)
        


def get_class_names():

    # Load class names
    raw = unpickle("batches.meta")[b'label_names']

    # Convert from binary strings
    names = [x.decode('utf-8') for x in raw]

    return names



def plot_images(images, labels_true, class_names, labels_pred=None):

    assert len(images) == len(labels_true)

    # Create a figure with sub-plots
    fig, axes = plt.subplots(3, 3, figsize = (8,8))

    # Adjust the vertical spacing
    if labels_pred is None:
        hspace = 0.2
    else:
        hspace = 0.5
    fig.subplots_adjust(hspace=hspace, wspace=0.3)

    for i, ax in enumerate(axes.flat):
        # Fix crash when less than 9 images
        if i < len(images):
            # Plot the image
            ax.imshow(images[i], interpolation='spline16')

            # Name of the true class
            labels_true_name = class_names[labels_true[i]]

            # Show true and predicted classes
            if labels_pred is None:
                xlabel = "True: "+labels_true_name
            else:
                # Name of the predicted class
                labels_pred_name = class_names[labels_pred[i]]

                xlabel = "True: "+labels_true_name+"\nPredicted: "+ labels_pred_name

            # Show the class on the x-axis
            ax.set_xlabel(xlabel)
        
        # Remove ticks from the plot
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Show the plot
    plt.show()