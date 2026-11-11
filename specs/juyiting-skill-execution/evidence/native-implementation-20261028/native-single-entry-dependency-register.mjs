import { registerHooks } from 'node:module'
import { pathToFileURL } from 'node:url'
const root = '/home/isp/apps/cyf-agent-runtime-v1/app/codex-bridge/node_modules/@imagemagick/magick-wasm/dist/'
const files = new Map([['@imagemagick/magick-wasm', 'index.js'], ['@imagemagick/magick-wasm/magick.wasm', 'x86/magick.wasm']])
registerHooks({ resolve(specifier, context, next) {
  if (files.has(specifier)) return { url: pathToFileURL(root + files.get(specifier)).href, shortCircuit: true }
  return next(specifier, context)
} })
