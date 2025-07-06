# Basic Node.js Server

A barebones Node.js server scaffold built with Express.js for local development.

## Features

- Simple Express.js server setup
- Basic routing with JSON responses
- Health check endpoint
- Error handling middleware
- Environment variable support
- Development mode with auto-restart

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
npm install
```

## Running the Server

### Development mode (with auto-restart):
```bash
npm run dev
```

### Production mode:
```bash
npm start
```

The server will start on `http://localhost:3000` by default.

## Environment Variables

You can customize the server behavior using environment variables:

- `PORT`: Server port (default: 3000)
- `NODE_ENV`: Environment mode (development/production)

Example:
```bash
PORT=8080 NODE_ENV=production npm start
```

## API Endpoints

### GET /
- **Description**: Basic welcome endpoint
- **Response**: JSON message with timestamp

### GET /health
- **Description**: Health check endpoint
- **Response**: Server status and uptime information

### 404 Handler
- **Description**: Handles all undefined routes
- **Response**: 404 error message

## Project Structure

```
├── server.js          # Main server file
├── package.json       # Dependencies and scripts
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Development

The server includes:
- JSON parsing middleware
- URL-encoded body parsing
- Basic error handling
- Development-friendly error messages
- CORS support (can be added if needed)

## Adding New Routes

To add new routes, edit `server.js` and add them before the 404 handler:

```javascript
app.get('/api/users', (req, res) => {
  res.json({ users: [] });
});

app.post('/api/users', (req, res) => {
  // Handle user creation
  res.json({ message: 'User created' });
});
```

## Testing

You can test the server using curl or any HTTP client:

```bash
# Test the main endpoint
curl http://localhost:3000/

# Test the health endpoint
curl http://localhost:3000/health

# Test 404 handling
curl http://localhost:3000/nonexistent
```

## License

MIT License - feel free to use this scaffold for your projects.