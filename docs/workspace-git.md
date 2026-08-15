# Workspace Git Notes

The workspace root is the `jia-sdd` coordinating repository. It records the SDD specifications, operational documentation, and pinned revisions of the independent implementation repositories.

- `api/` is the backend Git submodule (`https://gitee.com/chcbz/jia.git`, tracking `develop`).
- `web/` is the frontend Git submodule (`https://gitee.com/chcbz/cyf-web-kit.git`, tracking `develop`).
- The root remote is `https://gitee.com/chcbz/jia-sdd.git` on `master`.

Use the root repository to inspect or commit an integrated delivery baseline:

```bash
git status
git add specs docs api web
git commit -m "release: pin integrated feature baseline"
```

Use a submodule for implementation work:

```bash
git -C api status
git -C web status
./gitw all diff
./gitw web log --oneline -5
```

After cloning the coordination repository, initialize submodules with:

```bash
git submodule update --init --recursive
```
