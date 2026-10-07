import { pathToFileURL } from 'node:url'

const exactPackages = new Map([
  ['yauzl', pathToFileURL('/home/isp/wsps/cyf/.worktrees/juyiting-mmd-client-native-20260929/client/conf/codex-ws-agent/node_modules/yauzl/index.js').href],
  ['ws', pathToFileURL('/home/isp/wsps/cyf/.worktrees/juyiting-mmd-client-native-20260929/client/conf/codex-ws-agent/node_modules/ws/wrapper.mjs').href]
])

export async function resolve(specifier, context, nextResolve) {
  const exact = exactPackages.get(specifier)
  if (exact) return { url: exact, shortCircuit: true }
  return nextResolve(specifier, context)
}
