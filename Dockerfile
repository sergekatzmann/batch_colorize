FROM ubuntu:14.04
MAINTAINER Serge Katzmann serge.katzmann@gmail.com

#Caffe:cpu image from https://github.com/BVLC/caffe/blob/master/docker/standalone/cpu/Dockerfile
#Start
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-pip \
        python-scipy && \
    rm -rf /var/lib/apt/lists/*

ENV CAFFE_ROOT=/opt/caffe
WORKDIR $CAFFE_ROOT

ENV CLONE_TAG=master

RUN git clone -b ${CLONE_TAG} --depth 1 https://github.com/BVLC/caffe.git . && \
    for req in $(cat python/requirements.txt) pydot; do pip install $req; done && \
    mkdir build && cd build && \
    cmake -DCPU_ONLY=1 .. && \
    make -j"$(nproc)"

ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

#End

WORKDIR /work

RUN exec sh -c "ln /dev/null /dev/raw1394"

ADD colorization_deploy_v0.prototxt /work
RUN wget https://www.dropbox.com/s/8iq5wm4ton5gwe1/colorization_release_v0.caffemodel
#ADD colorization_release_v0.caffemodel /work
ADD colorize.py /work
RUN chmod u+x /work/colorize.py

VOLUME ["/images"]
ENTRYPOINT exec sh -c "/work/colorize.py -i /images/in/ -o /images/out/"