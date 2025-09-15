# HobbyRoom Frontend

Next.js + TypeScript frontend for the HobbyRoom application.

## 🚀 Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server (Next.js)
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Auto-fix ESLint issues
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting
- `npm run type-check` - Run TypeScript type checking

## 📁 Project Structure

```
app/                # Next.js 13+ App Router
├── layout.tsx     # Root layout component
├── page.tsx       # Homepage
└── providers.tsx  # React Query provider wrapper

src/
├── pages/         # Legacy page components (being migrated)
├── services/      # API services and utilities
├── types/         # TypeScript type definitions
└── styles/        # CSS files

public/            # Static assets
```

## 🛠️ Tech Stack

- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **React Query** - Server state management
- **Axios** - HTTP client
- **Zustand** - Client state management
- **ESLint** - Code linting
- **Prettier** - Code formatting

## 🔧 Configuration

### API Proxy
The Next.js configuration includes automatic API proxy setup:
- Frontend requests to `/api/*` are proxied to `http://localhost:8000/api/*`

### Code Quality
- **ESLint**: Configured with Next.js core web vitals rules
- **Prettier**: Consistent code formatting with single quotes, no semicolons
- **TypeScript**: Strict type checking enabled

## 🚀 Deployment

```bash
# Build the application
npm run build

# Start production server
npm run start
```
