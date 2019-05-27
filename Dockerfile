# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app/

# Make port 80 available to the world outside this container
EXPOSE 80

# Copy the current directory contents into the container at /app
ADD . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# REDIS
ENV REDIS_HOST=host.docker.internal
ENV REDIS_PORT=6379
ENV REDIS_DB=0

# Run app.py when the container launches
ENTRYPOINT ["python", "NobodyExpects.py"]