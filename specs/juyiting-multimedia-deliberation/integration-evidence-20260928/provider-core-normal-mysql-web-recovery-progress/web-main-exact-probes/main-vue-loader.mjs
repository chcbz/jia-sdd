export async function resolve(specifier, context, nextResolve) {
  // Actual candidate imports resolve only the existing main Vue package; source unchanged.
  if (specifier === 'vue') return nextResolve('file:///home/isp/wsps/cyf/web/node_modules/vue/dist/vue.runtime.esm-bundler.js', context)
  return nextResolve(specifier, context)
}
