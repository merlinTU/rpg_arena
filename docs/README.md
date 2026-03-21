# Documentation

After cloning the repository into a local directory, you can generate the HTML documentation by following these steps.

## 1. Install documentation dependencies

First, install the required dependencies:

```bash
pip install ".[docs]"
```

## 2. Build the documentation

Next, run the following command inside the rpg_arena/docs directory:

```bash
make html
```

## 3. View the documentation

Once the build process is complete, the generated HTML documentation can be found at:

```
docs/build/index.html
```

Open this file in your browser to view the documentation.
