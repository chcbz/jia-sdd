import { ESLint } from '/home/isp/wsps/cyf/web/node_modules/eslint/lib/api.js'
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
const cwd = '/home/isp/wsps/cyf/web', filePath = 'src/components/juyiting/HallMaterialPicker.vue'
process.chdir(cwd)
const lint = new ESLint({ cwd }), result = {}
for (const [name, source] of [['baseline', execFileSync('git', ['show', `HEAD:${filePath}`], { cwd, encoding: 'utf8' })], ['candidate', readFileSync(`${cwd}/${filePath}`, 'utf8')]]) {
 const [r] = await lint.lintText(source, { filePath: `${cwd}/${filePath}` })
 result[name] = { errors: r.errorCount, warnings: r.warningCount, messages: r.messages }
}
console.log(JSON.stringify(result, null, 2))
