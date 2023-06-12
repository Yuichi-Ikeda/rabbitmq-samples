# Use Python 3.9 as base image
FROM python:3.9

# Install pika library
RUN pip install pika

# Set environment variable or use -e option when running docker run command
#ENV password=xxxx
#ENV hostname=host.docker.internal

# Copy program file to container
COPY receive.py .
#COPY 2.7gb.data .

# Run program
CMD ["python", "-u" ,"receive.py"]