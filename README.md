# Wind prediction based on video analysis

### The general idea

The idea behind the project is following. For many athletes, doing some kind of wind related watersport activity (kitesurfing, windsurfing, sailing etc), it is important to know the strength of the wind before they go into the water. Depending on the wind strength they can be using different equipment. There are many special devices that measure the wind to solve this problem. But experienced athletes do not normally need these devices since they can very precisely guess the strength of the wind just by observing the beach, the water, the trees around. So the idea is to train a neural network to analyze visual information in order to predict the strength of the wind. It can then be realized as a mobile app. This project can be considered as a prove of concept for such a mobile application.

### Motivation and objectives

The basic motivation for me to start this project was to gain practical experience in doing end to end project, starting from just an idea and work through all the steps - finding the data in the internet, collecting it, preprocessing it and then finally creating, training and evaluating the tensorflow model. Most of the time Python 3.6 and Jupyter Notebook was used. The training of the models was performed on Google gloud platform using virtual machine with GPU support.

### Results

The resulting video produced by sliding model can bee seen here:

[![Prediction of wind strength based on visual information](https://img.youtube.com/vi/NcxbpOcWyI4/0.jpg)](https://www.youtube.com/watch?v=NcxbpOcWyI4)

On the video you can see predicted values, target values and self attention mask (the black areas). Attention mask shows the parts of the picture not contributing into the final prediction. This mask is learned together with other trainable parameters. More details about the video are in sec 5.

### Details of the project

The whole project is divided into several sections.

#### 1) Collecting data from the internet.

 The video data was collected from openly available webcams. For capturing video streamed in flash protocol I've used a ready php-script, which I wrapped up using Python.

 The numerical data are taken from weather related website [www.windfinder.com](www.windfinder.com), using selenium module. The data was hidden in some js array.

 The files for this part of the project are in the folder 'Data_collection'. The samples of data can be found in 'Data_samples' folder.


#### 2) Creating data set for training the model.

The frames can be extracted from the videos using openCV. For each video a corresponding numerical data can be obtained by extrapolation of numerical values of the wind strengths collected in the neighboring timepoints. The numerical data and corresponding frame (or frame sequence, in case of dynamical model) are combined into a sample of data, serialized and saved in tfrecords format for easy and fast access using tf.dataset API

The corresponding notebooks are in the folder "Data_preprocessing_pipeline"

#### 3) Creating simple static model that makes the prediction for a single random frame taken from the video.

As a convolutional base I've used MobiNetV2 architecture pretrained on Imnet dataset. I've chosen this model as a base, because of the small size, that allows to retrain the whole model with the limited computational resources. The convolutional base is FCN (fully convolutional network) allowing to use pictures of any size. The size of the pictures used in training is 448x704. This is pretty big size for deep vision problems. I've chosen this maximum size not to loose decisive features such as, for example, the textures of the water, that can be lost by lowering the resolution of the image.

In case of FCN, it's necessary to reduce dimension of the last convolutional block. This is normally done by GlobalAveraging, that is averaging along the special dimensions. Instead I used self attention mechanism. This is essentially the weighted averaging along the special dimensions with the weights of this averaging to be trained together with other trained parameters. This allows the model to decide which areas of the image are more important to look at for making prediction. Above in the video you can see this attention mask as a black areas - these are the areas of the frames that do not contribute into prediction.

The training was performed on google cloud platform using 1 GPUs. It was done in two stages: 1) the convolutional base got frozen and is used just as a feature extractor for the top layers. This can be done with relatively high learning rate. 2) second stage is to train all layers of the model including convolutional base.

The corresponding notebooks are in the folder 'Static_models'.

#### 4) Extending the model to take into account also dynamical features of the video information

Using the previously created and trained stationary model, the dynamical model was created. This dynamical model analyses sequence of frames, more precisely sequence of high level features that was generated by stationary model without the top layers. The attention weights were also trained in dynamical model.

To analyze sequential data I used different methods 1) 1D time convolution 2) GRU recurrent unit and 3) LSTM. The best result was achieved using 1D convolutional layer but all methods gave very similar precision.

The corresponding notebooks are in the folder 'dynamic_models'

#### 5) The sliding model for real time prediction.

For real time inference, I've constructed sliding model that slides along the video frames generating prediction on each time step. This sliding model takes one frame at a time from a (possibly infinite) video stream, as an input, also it take some features calculated on previous time steps. It then produces the prediction on each time step instead of taking the finite sequence as an input. The link to the video generated by this sliding model is given above. The inference time on normal CPU core i5 about 5 sec per frame, which is too slow to perform inference on the video in real time. The main problem is the big size of the frames.

### The conclusion.

The concept is feasible and it looks possible to train the model to predict the wind strength based on visual information. But in order to make it practical, one needs to overcome several problems. First one needs a better dataset - the data available in internet is not good enough for precise prediction, since visual information is a snapshot of a moment, but on the weather websites you can at best find the values for the wind every 5 min. Second, for real time prediction on mobile devices the inference time should be reduced. At the moment it's about 5 second per frame on core i5 CPU. This probably possible to be done by reducing the size of the picture in such a way that the important visual features are not destroyed.
