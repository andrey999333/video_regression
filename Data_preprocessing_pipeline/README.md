### Data preprocessing

In this folder there are files to make preprocessing and prepare the data for further use in training the models.

*) First step is to determine the numerical data for every video. And also split the video file into frames. This is done in 'extracting_frames_for_training_data' notebook.

*) For training the main objective is to create a very fast pipeline so we can feed data to the model as fast as possible to avoid GPUs to be idle waiting for new data batch. For that purpose I store the data in tfrecords format and use tf.dataset API while training. I store frames of the video compressed in jpg format, which is not the fastest since we need to decompress the frames before feeding into model. It's done to save space on the disk. In jpg format the whole training dataset is 20Gb, while stored as numbers (even in uint format) will take about 300Gb of space. It's appeared that this method is good enough for training as GPU was never idle during the training. 

*) There are two different cases for organizing data 1) stationary model where data sample consists of just one frame and corresponding labels. The dataset for this case is created in 'img_to_tfrecord' notebook. 2) in the case of dynamical model we need to feed sequence of time ordered frames and corresponding labels as one sample. The dataset for this case is created in 'img_to_tfrecord_sequence_chuncks_shuffle' notebook

