# Use the latest official Python image from the Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Install convenience packages
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    procps \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["bash"]