#!/bin/bash

#We are running a janusgraph server from a docker

#Installation
#sudo docker pull janusgraph/janusgraph

#Activating docker and the janus server to listen in por 8182
sudo docker run -it -p 8182:8182 janusgraph/janusgraph





