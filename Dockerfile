# Use Node.js 18
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files from bulk-link-generator
COPY bulk-link-generator/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the entire bulk-link-generator app
COPY bulk-link-generator/ ./

# Expose port
EXPOSE 3300

# Start the application
CMD ["node", "enhanced-tracker.js"]
