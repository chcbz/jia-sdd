# JIA SDD Workspace

This repository coordinates the JIA system through Spec-Driven Development (SDD). It stores cross-repository specifications, operational documentation, and the tested revision pair of the backend and frontend submodules.

## Repositories

| Path | Repository | Responsibility |
| --- | --- | --- |
| `api/` | `chcbz/jia` | Java/Gradle backend |
| `web/` | `chcbz/cyf-web-kit` | Vue frontend |
| `specs/` | This repository | Feature specifications, design, tasks, and acceptance |

## Clone

```bash
git clone --recurse-submodules https://gitee.com/chcbz/jia-sdd.git
```

For an existing checkout:

```bash
git submodule update --init --recursive
```

## Delivery workflow

1. Define or update the feature under `specs/`.
2. Implement and commit independently in `api/` and/or `web/`.
3. Verify the integrated feature.
4. Commit the updated submodule pointers and SDD records in this repository.

The root commit is the reproducible, integrated delivery baseline; it does not replace the independent histories of the two implementation repositories.
