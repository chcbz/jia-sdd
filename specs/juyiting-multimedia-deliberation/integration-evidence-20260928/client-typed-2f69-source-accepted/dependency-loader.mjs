const packages = new Map([
  ['yauzl', 'file:///home/isp/wsps/cyf/.worktrees/juyiting-mmd-client-native-20260929/client/conf/codex-ws-agent/node_modules/yauzl/index.js'],
  ['ws', 'file:///home/isp/wsps/cyf/.worktrees/juyiting-mmd-client-native-20260929/client/conf/codex-ws-agent/node_modules/ws/wrapper.mjs']
])
export async function resolve(specifier, context, nextResolve) {
  const url = packages.get(specifier)
  if (url) return { url, shortCircuit: true }
  return nextResolve(specifier, context)
}
