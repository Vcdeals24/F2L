# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any dependencies in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your bot may use (optional, if you want to run a web service)
# EXPOSE 8080

# Command to run the bot
CMD ["python", "bot.py"]
