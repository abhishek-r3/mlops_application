#step 1 - specify host operating system
#This will install linux os with python3
FROM python:3.7

#create a working directory with name app
WORKDIR /app

#copy the files of current folder to the app folder inside the container
COPY . /app

#install the libraries
RUN pip install -r requirements.txt
RUN ls 
EXPOSE 5000 
ENTRYPOINT ["python"]
CMD ["api_main.py"]