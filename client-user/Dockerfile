# Base image
FROM node:15.12.0-alpine3.10

# Set working directory
WORKDIR /app

# Add node_modules .bin to path
ENV PATH /app/node_modules.bin:$PATH

# Install dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm config set strict-ssl false
RUN npm install

# Add app
COPY . ./
RUN chmod +rwx ./*

# Start client
CMD ["npm", "start"]
