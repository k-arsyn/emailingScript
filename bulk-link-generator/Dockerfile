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

# Ensure public/images directory exists (should already be copied above)
RUN mkdir -p public/images

# Create user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Expose port (will be overridden by hosting platform)
EXPOSE $PORT

# Start the application
CMD ["node", "enhanced-tracker.js"]
