# Brewery Explorer Frontend

A modern Vue.js application for exploring breweries, built with Vue 3, Vite, and TailwindCSS.

## Features

- 🍺 Browse and search breweries
- 📍 View brewery locations and details
- 🔍 Advanced filtering and search capabilities
- 📱 Responsive design for all devices
- 🎨 Modern UI with TailwindCSS
- 📊 Interactive data visualization with D3.js
- 🔄 Real-time search and filtering
- 📋 Table view with sorting and pagination
- 🎯 Random brewery discovery
- 📈 Data grouping and visualization

## Prerequisites

- Node.js (v22 or higher)
- npm or yarn
- Backend API running (see backend README for setup)

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/chrisdamba/brewery-explorer.git
cd brewery-explorer/frontend
```

2. Install dependencies:

```bash
npm install
# or
yarn install
```

3. Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000/api
```

4. Start the development server:

```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests
- `npm run test:coverage` - Run tests with coverage report
- `npm run lint` - Lint code
- `npm run format` - Format code with Prettier

## Project Structure

```
frontend/
├── src/
│   ├── components/    # Vue components
│   │   ├── BreweryExplorer.vue  # Main component
│   │   └── __tests__/          # Component tests
│   ├── assets/        # Static assets
│   ├── router/        # Vue Router configuration
│   ├── stores/        # Pinia stores
│   ├── views/         # Page components
│   ├── App.vue        # Root component
│   └── main.js        # Application entry point
├── public/            # Public static files
├── .env               # Environment variables
├── .eslintrc.js      # ESLint configuration
├── .prettierrc       # Prettier configuration
├── index.html        # HTML template
├── package.json      # Project dependencies
├── tailwind.config.js # TailwindCSS configuration
├── vite.config.js    # Vite configuration
└── vitest.config.js  # Vitest configuration
```

## Testing

The project uses Vitest for testing. Tests are located in the `src/components/__tests__` directory.

```bash
# Run tests
npm run test

# Run tests with coverage
npm run test:coverage
```

### Test Structure

- `BreweryExplorer.spec.js`: Tests for the main component
  - Component rendering
  - Data fetching
  - Filtering functionality
  - Search functionality
  - Random brewery feature
  - Data grouping

## Code Quality

The project uses ESLint and Prettier for code quality and formatting.

```bash
# Lint code
npm run lint

# Format code
npm run format
```

## Key Dependencies

- Vue 3 - Progressive JavaScript framework
- Vite - Next generation frontend tooling
- TailwindCSS - Utility-first CSS framework
- D3.js - Data visualization library
- Axios - HTTP client
- Vitest - Testing framework
- ESLint - Code linting
- Prettier - Code formatting

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and ensure they pass
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
