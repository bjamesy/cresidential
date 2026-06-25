import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    proxy: {
      '/plaid': process.env.BACKEND_URL ?? 'http://localhost:8000',
      '/transactions': process.env.BACKEND_URL ?? 'http://localhost:8000',
      '/jobs': process.env.BACKEND_URL ?? 'http://localhost:8000',
    },
  },
})
