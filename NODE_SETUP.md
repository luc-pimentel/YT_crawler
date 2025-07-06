# Node.js Server Setup

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run the server:**
   ```bash
   npm start
   ```

   Or for development with auto-reload:
   ```bash
   npm run dev
   ```

3. **Visit your server:**
   - Main endpoint: http://localhost:3000
   - Health check: http://localhost:3000/health

## Project Structure

- `server.js` - Main server file
- `package.json` - Dependencies and scripts
- `.env.example` - Example environment variables

## Environment Variables

Copy `.env.example` to `.env` and customize if needed:
```bash
cp .env.example .env
```

## Development

- The server runs on port 3000 by default
- Use `npm run dev` for development with nodemon (auto-restart on file changes)
- Add new routes in `server.js`

That's it! You now have a basic Node.js server running.