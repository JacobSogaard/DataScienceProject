FROM bde2020/hadoop-base

LABEL Name=pysparkExampleImage Version=0.0.1 

# Updating package manager
RUN apt-get update

# installing packages needed and pip packages
RUN DEBIAN_FRONTEND=noninteractive apt-get -yq install python3 python3-pip locales
RUN python3 -m pip install pyspark

# cleanup
RUN apt-get autoremove -y
RUN apt-get clean

# making sure python and python 3 is the same - symlinks dont seem to work
RUN cp /usr/bin/python3 /usr/bin/python
# RUN ln -s /usr/bin/python3 python

# Setting up Locale for python
RUN touch /usr/share/locale/locale.alias
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

# adding files to the container
WORKDIR /app
ADD . /app

# running the python file at container startup
CMD ["python3 example.py"]