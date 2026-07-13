import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  base: '/car-driver-test-jp/',
  plugins: [
    vue(),
    VitePWA({
      registerType: 'prompt',
      includeAssets: ['favicon.svg', 'favicon-48x48.png', 'apple-touch-icon.png'],
      manifest: {
        name: '日本驾照笔试真题 (Offline)',
        short_name: 'JPDriverTest',
        description: '日本驾照笔试真题离线训练系统',
        lang: 'zh-CN',
        theme_color: '#182848',
        background_color: '#f5f7fa',
        display: 'standalone',
        start_url: './',
        scope: './',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: 'pwa-maskable-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ]
      },
      workbox: {
        // Cache all static assets including our JSON database
        globPatterns: ['**/*.{js,css,html,ico,png,svg,json,jpg}']
      }
    })
  ],
})
