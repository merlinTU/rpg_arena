
# Documentation

## Overview

To install the necessary dependencies, please run

```bash
pip install -e .[docs]
```

in the root directory of the project.

## Build Process

This section describes the goals and setup of the documentation build system.

## Building the Documentation

### Standard HTML Build

Run:

```bash
make html
```

This executes:

```bash
sphinx-build -b html . _build/html
```

After completion, open:

```bash
_build/html/index.html
```

in your browser.

---

### Clean Build

If you encounter issues, delete old build files first:

```bash
make clean
make html
```

---

