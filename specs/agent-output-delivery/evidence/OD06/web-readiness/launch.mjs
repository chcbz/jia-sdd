import { createServer } from '/home/chc/wsps/cyf-worktrees/output-web/node_modules/vite/dist/node/index.js'
const server = await createServer({
  root: '/home/chc/wsps/cyf-worktrees/output-web',
  configFile: '/home/chc/wsps/cyf-worktrees/output-web/vite.config.js',
  server: { host: '127.0.0.1', port: 15173, strictPort: true, https: false },
  logLevel: 'warn'
})
await server.listen()
console.log('OD06_WEB_READY http://127.0.0.1:15173')
const stop = async () => { await server.close(); process.exit(0) }
process.on('SIGTERM', stop)
process.on('SIGINT', stop)
