FROM pytorch/pytorch-binary-docker-image-ubuntu16.04

WORKDIR /GreenhouseModMod
COPY . .
RUN apt-get install -y nano
RUN pip3 install xlrd==1.2.0
RUN pip3 install chime
RUN pip3 install reportlab==3.5.59
RUN pip3 install git+https://github.com/jdmolinam/ModMod_Programming_environment.git 
RUN pip3 install matplotlib==3.4.2
RUN pip3 install numpy==1.18.5
RUN pip3 install sympy==1.6.2
RUN pip3 install pandas==1.1.0
RUN pip3 install scipy==1.5.2
RUN pip install torch===1.5.1 -f https://download.pytorch.org/whl/torch_stable.html
CMD python3 try_climate_only.py
