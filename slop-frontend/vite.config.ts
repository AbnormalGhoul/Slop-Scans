import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import fs from 'fs'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), copyManifest()],
  build: {
    rollupOptions: {
      input: {
        popup: resolve(__dirname, 'popup.html'),
        content: resolve(__dirname, 'src/content.ts'),
        background: resolve(__dirname, 'src/background.ts'),
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: 'chunks/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash][extname]',
        dir: resolve(__dirname, 'dist'),
      },
    },
    outDir: 'dist',
    emptyOutDir: true,
  },
})

function copyManifest() {
  return {
    name: 'copy-manifest',
    writeBundle() {
      const manifest = fs.readFileSync('./manifest.json', 'utf-8')
      fs.mkdirSync('./dist', { recursive: true })
      fs.writeFileSync('./dist/manifest.json', manifest)
    },
  }
}
