# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Expose port for Flask
EXPOSE 4000

# Command to run the app
CMD [ "flask" , "run", "--host=0.0.0.0", "--port=4000" ]