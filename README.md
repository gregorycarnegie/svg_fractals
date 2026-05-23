# SVG Fractals

[![Python >=3.14](https://img.shields.io/badge/python-%3E%3D3.14-blue)](https://www.python.org/)
[![Built with uv](https://img.shields.io/badge/built%20with-uv-5C6BC0)](https://docs.astral.sh/uv/)
[![Output: SVG](https://img.shields.io/badge/output-SVG-brightgreen)](https://www.w3.org/Graphics/SVG/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Generate SVG artwork from classic space-filling fractals. Choose a pattern, colours, and iteration depth — or hit Randomise and let the generator decide.

![Example SVG fractal](svgs/example.svg)

## Patterns

- Hilbert curve
- Gosper curve
- Moore curve
- Peano curve

## Installation

```powershell
uv sync
```

## Usage

### Web UI (recommended)

```powershell
uv run python app.py
```

Then open `http://127.0.0.1:8000`. Pick a pattern, adjust colours and iterations, and preview the SVG in real time. Use **Randomise** to generate a random combination, or **Download SVG** to save the result.

### CLI

```powershell
uv run python main.py
```

Prompts for a file name and whether to use random mode. SVG files are written to `svgs/`.

### Tests

```powershell
uv run pytest
```

## Project structure

```
app.py                  Web UI (FastAPI)
main.py                 CLI entry point
fractals/
  data.py               Weighted colour and pattern tables
  fractal_funcs.py      Drawing logic and public API
  utils.py              L-system engine and geometry helpers
tests/
  test_fractal_funcs.py Tests for drawing helpers
  test_utils.py         Tests for L-system and fractal generators
svgs/
  example.svg           Example output
```

## License

MIT — see [LICENSE](LICENSE).
