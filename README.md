# School Frontend Starter (React + Vite + Tailwind)

## Quick start

1. Install dependencies

```bash
npm install
```

2. Run dev server

```bash
npm run dev
```

3. Open your browser at `http://localhost:5173`

## Connect to your backend
Set the environment variable `VITE_API_BASE` for your backend API in a `.env` file (Vite uses `VITE_` prefix):

```
VITE_API_BASE=https://your-backend-url/api
```

## What is included
- Basic routing (Login, Register, Teacher, Student, Guardian dashboards)
- Axios config (src/api/axios.js)
- TailwindCSS configuration
- Simple components: Navbar, ExamCard, ResultCard

This is a starter scaffold — implement forms and secure auth flows (store JWT securely, refresh tokens, add role-based route guards) when wiring to the real backend.
