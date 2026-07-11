# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# AnimeMangaDB Frontend

The AnimeMangaDB frontend is a thin React client that consumes the FastAPI REST API.

## Technology

- React
- React Router
- Vite
- JavaScript
- ESLint

## Architecture

```text
Browser
  ↓
React Frontend
  ↓
FastAPI REST API
  ↓
AnimeMangaDB Database
```

Business logic, scraping, comparison, repair, and metadata resolution remain in Python. The frontend only collects input, calls the API, and displays results.

## Requirements

- Node.js
- npm
- Running AnimeMangaDB API

## Install

From the `frontend` directory:

```bash
npm install
```

## Configure the API

The frontend reads the API address from:

```text
VITE_API_BASE_URL
```

Copy the example configuration when a custom API URL is needed:

```bash
copy .env.example .env
```

Default local API:

```text
http://127.0.0.1:8000
```

## Run the Backend

From the repository root:

```bash
uvicorn scraper.api.app:app --reload
```

## Run the Frontend

From the `frontend` directory:

```bash
npm run dev
```

Open the local URL printed by Vite, normally:

```text
http://localhost:5173
```

## Production Build

```bash
npm run build
```

## Lint

```bash
npm run lint
```

## Scope v2 Features

- Browse supported anime
- View series episode counts
- Browse episodes for a series
- Search episodes by number or title
- View episode titles and anime arcs
- View episode-to-chapter mappings
- Find episodes adapting a manga chapter
- Search anime, episodes, and chapter numbers
- Navigate to series and episode detail pages

## Current Scope Limitation

Scope v2 stores manga chapter numbers only.

Chapter-title and manga-arc search will be added as part of Scope v3.

## Admin UI

A protected Admin UI is planned for a future release. It will call approved backend operations through an admin API rather than execute arbitrary shell commands.