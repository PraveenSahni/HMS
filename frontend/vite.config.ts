import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendUrl = env.VITE_TRYTON_URL || 'http://34.18.116.146'

  // /api/tryton/<database>/… → /<database>/… on Tryton (SAO-compatible multi-DB)
  const trytonProxy = {
    '/api/tryton': {
      target: backendUrl,
      changeOrigin: true,
      rewrite: (path: string) => path.replace(/^\/api\/tryton/, '') || '/',
    },
  }

  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: trytonProxy,
    },
    preview: {
      port: 3000,
      proxy: trytonProxy,
    },
  }
})
