# Use Node.js 18
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy app source
COPY . .

# Create public/images directory and copy pixel
RUN mkdir -p public/images
COPY public/images/pixel.svg public/images/

# Expose port
EXPOSE 3300

# Start the application
CMD ["node", "enhanced-tracker.js"]
