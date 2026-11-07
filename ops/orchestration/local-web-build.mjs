// Keep the exact source Vite configuration; only avoid duplicating public assets
// on this almost-full host. The packager includes every public file unchanged.
import { pathToFileURL } from 'node:url'
const [source, output] = process.argv.slice(2)
const { build } = await import(pathToFileURL(`${source}/node_modules/vite/dist/node/index.js`))
await build({ root: source, build: { outDir: output, copyPublicDir: false, emptyOutDir: false } })
