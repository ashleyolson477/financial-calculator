#Base image
FROM python:3.13-slim

#Working directory in the container
WORKDIR /app

#Copies current director into the container
COPY . /app

#Installs the requried python packages
RUN pip install -r requirements.txt

#Listen to port 8080
EXPOSE 8080

#Run flask app
CMD ["python", "app.py"]