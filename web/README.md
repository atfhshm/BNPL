# BNPL Web Application

A modern, production-ready web application for Buy Now Pay Later services built with React and React Router.

## Features

- 🚀 Server-side rendering with React Router
- ⚡️ Hot Module Replacement (HMR) for rapid development
- 📦 Optimized asset bundling with Vite
- 🎨 Modern UI components with Radix UI
- 📊 Data visualization with Recharts
- 🔄 State management with Zustand
- 📝 Form handling with React Hook Form and Zod validation
- 🔒 TypeScript for type safety
- 🎨 TailwindCSS for styling
- 📱 Responsive design
- 🌙 Dark mode support with next-themes

## Tech Stack

- **Frontend Framework**: React 19 with React Router 7
- **UI Components**: Radix UI
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Form Handling**: React Hook Form with Zod validation
- **HTTP Client**: Axios
- **Build Tool**: Vite
- **Type Checking**: TypeScript

## Getting Started

### Prerequisites

- Node.js (Latest LTS version recommended)
- pnpm (Package manager)

### Installation

Install the dependencies:

```bash
pnpm install
```

### Development

Start the development server:

```bash
pnpm dev
```

Your application will be available at `http://localhost:5173`.

## Building for Production

Create a production build:

```bash
pnpm build
```

## Docker Deployment

Build and run using Docker:

```bash
docker build -t bnpl-web .

# Run the container
docker run -p 3000:3000 bnpl-web
```

The containerized application can be deployed to any platform that supports Docker, including:

- AWS ECS
- Google Cloud Run
- Azure Container Apps
- Digital Ocean App Platform
- Fly.io
- Railway

## Project Structure

```sh
├── package.json
├── package-lock.json (or pnpm-lock.yaml, or bun.lockb)
├── build/
│   ├── client/    # Static assets
│   └── server/    # Server-side code
```

## Styling

This template comes with [Tailwind CSS](https://tailwindcss.com/) already configured for a simple default starting experience. You can use whatever CSS framework you prefer.

---

Built with ❤️
