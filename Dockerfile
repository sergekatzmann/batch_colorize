FROM caffe:cpu

WORKDIR /work

RUN exec sh -c "ln /dev/null /dev/raw1394"

ADD colorization_deploy_v0.prototxt /work
RUN wget https://www.dropbox.com/s/8iq5wm4ton5gwe1/colorization_release_v0.caffemodel
#ADD colorization_release_v0.caffemodel /work
ADD colorize.py /work
RUN chmod u+x /work/colorize.py

VOLUME ["/images"]
ENTRYPOINT exec sh -c "/work/colorize.py -i /images/in/ -o /images/out/"