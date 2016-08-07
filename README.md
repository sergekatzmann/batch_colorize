# Batch process implementation for the grayscale image colorization

Objective
------------
The purpose of this project is to create a batch process implementation of the graysace image colorization process created by Richard Zhang, Phillip Isola and Alexei A. Efros (http://richzhang.github.io/colorization/).
The Colorful Image Colorization project is using Caffe to colorize images using a trained network. The installation of Caffe and dependencies is a complex process and cannot be always done on every environment easily.
This project is using docker to simplify the process and make it work on any environment (tested on Centos 7) with docker installed.

Prerequisites
------------
For the process to work docker is needed.
You can install Docker and configure it to start on boot on Centos 7 using folowing commands:

```
sudo yum install docker -y
sudo chkconfig docker on
```

To do it on other Linux flavours you have to use specific commands for the version you are running.


Installation
------------

Clone this repository to a local folder. For example in the home folder.

```
cd ~
git clone -b master --single-branch https://github.com/sergekatzmann/batch_colorize.git
```

_Optional_

To prepare the docker image you can pull the image from the docker repository or build it yourself.

To build the image perform the following command:

```
cd ~/batch_colorize
sudo bash build.sh
```

To pull from docker repo use this command:

```
sudo docker pull sergekatzmann/batch_colorize:latest
```

Image preparation
------------

Switch into the project folder and then go to images/in folder and place your grayscale images in this location.
Thats it for this part.

You can perform the copy by omthing similar to the following lines:

Replace [image location] with the source location of your images.
```
cd ~/batch_colorize/images/in
cp [image location] .
```

Run the batch colorization
------------
Perform the folllwing command to colorize all the images from the images/in folder:


```
sudo bash batch_colorize.sh

```

The results
------------
After the successful execution you will find the colorized images in the images/out folder.


Thanks
------------
Thanks to Richard Zhang, Phillip Isola and Alexei A. Efros for the great project making alot of people happy. At least my family is very happy to see the old photos in the new colorful version.







