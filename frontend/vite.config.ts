import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react({
      // Configure Emotion for MUI
      jsxImportSource: '@emotion/react',
      babel: {
        plugins: ['@emotion/babel-plugin'],
      },
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    // Enable tree-shaking optimizations
    rollupOptions: {
      output: {
        manualChunks: {
          // Separate MUI components into their own chunk for better caching
          mui: ['@mui/material', '@mui/system', '@emotion/react', '@emotion/styled'],
        },
      },
    },
  },
  optimizeDeps: {
    // Pre-bundle MUI dependencies for better performance
    include: [
      '@mui/material',
      '@mui/system',
      '@emotion/react',
      '@emotion/styled',
      '@mui/material/styles',
      '@mui/material/utils',
    ],
  },
});
