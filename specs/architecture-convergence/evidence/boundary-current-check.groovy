class ArchitectureBoundaryScanner extends com.sun.source.util.TreeScanner<Void, Void> {
    String sourcePath
    String sourceDomain
    String className = '<unit>'
    String methodName = '<class>'
    Map<String, Map> sourceIndex
    Set<Map> findings
    boolean scopedNewSource

    void finding(String rule, String symbol) {
        findings.add([rule: rule, sourcePath: sourcePath, symbol: symbol])
    }

    @Override Void visitClass(com.sun.source.tree.ClassTree node, Void unused) {
        String previous = className
        className = previous == '<unit>' ? node.simpleName.toString() : previous + '.' + node.simpleName
        try { return super.visitClass(node, unused) } finally { className = previous }
    }

    @Override Void visitMethod(com.sun.source.tree.MethodTree node, Void unused) {
        String previous = methodName
        methodName = node.name.toString() + '(' + node.parameters.collect { it.type.toString() }.join(',') + ')'
        try { return super.visitMethod(node, unused) } finally { methodName = previous }
    }

    @Override Void visitImport(com.sun.source.tree.ImportTree node, Void unused) {
        String target = node.qualifiedIdentifier.toString()
        def targets = []
        if (target.endsWith('.*') && !node.isStatic()) {
            String pkg = target.substring(0, target.length() - 2)
            targets = sourceIndex.values().findAll { it.pkg == pkg }
        } else {
            String candidate = target
            while (candidate.contains('.')) {
                if (sourceIndex.containsKey(candidate)) { targets = [sourceIndex[candidate]]; break }
                candidate = candidate.substring(0, candidate.lastIndexOf('.'))
            }
        }
        if (targets.any { it.domain != sourceDomain && it.domain != 'common' &&
                (it.path.contains('-service/src/main/java/') || it.path.contains('/mapper/') || it.path.contains('/dao/impl/')) }) {
            finding('G1', target)
        }
        return null // imports are not uses of SecurityContextHolder in a method
    }

    void checkIdentity(String name) {
        if (sourcePath.contains('/service/') && (name == 'SecurityContextHolder' ||
                name == 'org.springframework.security.core.context.SecurityContextHolder')) {
            finding('G2', className + '#' + methodName + ':SecurityContextHolder')
        }
    }
    @Override Void visitIdentifier(com.sun.source.tree.IdentifierTree node, Void unused) {
        checkIdentity(node.name.toString())
        return super.visitIdentifier(node, unused)
    }
    @Override Void visitMemberSelect(com.sun.source.tree.MemberSelectTree node, Void unused) {
        checkIdentity(node.toString())
        return super.visitMemberSelect(node, unused)
    }
    @Override Void visitLiteral(com.sun.source.tree.LiteralTree node, Void unused) {
        if (node.value instanceof String) {
            String value = node.value
            if (sourceDomain == 'chat') {
                def tables = value =~ /(?i)\bagent_personal_workspace_(?:task_file_link|file_version|file)\b/
                tables.each { table -> finding('G3', className + '#' + methodName + ':' + table.toLowerCase(Locale.ROOT)) }
            }
            if (scopedNewSource && (value =~ /(?i)\b(?:create|alter|drop|truncate)\s+table\b/).find()) {
                finding('G4', className + '#' + methodName + ':schema-write')
            }
        }
        return super.visitLiteral(node, unused)
    }
    @Override Void visitAnnotation(com.sun.source.tree.AnnotationTree node, Void unused) {
        String name = node.annotationType.toString().tokenize('.').last()
        if (scopedNewSource && name in ['Controller', 'RestController', 'RequestMapping', 'GetMapping',
                'PostMapping', 'PutMapping', 'DeleteMapping', 'PatchMapping']) finding('G4', 'HTTP:' + name)
        return super.visitAnnotation(node, unused)
    }
}

def collectArchitectureBoundaries = { File sourceRoot, Collection<File> sourceFiles, Set<String> scopedNewSources ->
    def compiler = javax.tools.ToolProvider.systemJavaCompiler
    if (compiler == null) throw new IllegalStateException('validateLayering requires the configured JDK compiler')
    def diagnostics = new javax.tools.DiagnosticCollector<javax.tools.JavaFileObject>()
    def manager = compiler.getStandardFileManager(diagnostics, Locale.ROOT, java.nio.charset.StandardCharsets.UTF_8)
    try {
        def task = compiler.getTask(null, manager, diagnostics, ['-proc:none'], null,
                manager.getJavaFileObjectsFromFiles(sourceFiles))
        def units = task.parse().toList()
        def errors = diagnostics.diagnostics.findAll { it.kind == javax.tools.Diagnostic.Kind.ERROR }
        if (errors) throw new IllegalStateException('Architecture source parse failed: ' + errors.join('\n'))
        Map<String, Map> index = [:]
        def paths = [:]
        units.each { unit ->
            String path = sourceRoot.toPath().relativize(new File(unit.sourceFile.toUri()).toPath()).toString().replace('\\', '/')
            String domain = path.tokenize('/')[0]
            if (domain == 'mat') domain = 'material'
            String pkg = unit.packageName?.toString() ?: ''
            paths[unit] = [path: path, domain: domain]
            unit.typeDecls.findAll { it instanceof com.sun.source.tree.ClassTree }.each { type ->
                index[pkg + '.' + type.simpleName] = [path: path, domain: domain, pkg: pkg]
            }
        }
        Set<Map> findings = new LinkedHashSet<>()
        units.each { unit ->
            def entry = paths[unit]
            // Starter composition and common infrastructure are not business-domain consumers.
            if (entry.domain in ['common', 'starter', 'plugin'] || entry.path.contains('-starter/')) return
            new ArchitectureBoundaryScanner(sourcePath: entry.path, sourceDomain: entry.domain,
                    sourceIndex: index, findings: findings, scopedNewSource: scopedNewSources.contains(entry.path)).scan(unit, null)
        }
        return findings.toList().sort { a, b -> (a.rule + a.sourcePath + a.symbol) <=> (b.rule + b.sourcePath + b.symbol) }
    } finally { manager.close() }
}


def root = new File(args[0]).canonicalFile
 def sources = new File(args[1]).readLines().collect { new File(root,it) }
 def baseline = new groovy.json.JsonSlurper().parse(new File(root, 'docs/architecture-boundary-baseline.json'))
 def result = collectArchitectureBoundaries(root,sources,baseline.scopedNewSources as Set)
 def key = { x -> [x.rule,x.sourcePath,x.symbol] }
 def allowed = baseline.exceptions.collect { key(it) }.toSet()
 def violations = result.findAll { !allowed.contains(key(it)) }
 assert violations.empty : violations
 println "PASS: syntax-only source scan; ${sources.size()} Java files, ${result.size()} exact historical edges, zero new edges"
