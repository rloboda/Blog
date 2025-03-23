# Use Node base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy all frontend files
COPY . .

# Build the React app
RUN npm run build

# Use a simple server to serve React app
RUN npm install -g serve
CMD ["serve", "-s", "build"]

# Expose port for frontend
EXPOSE 3000
