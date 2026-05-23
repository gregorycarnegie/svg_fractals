import json

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from fractals.fractal_funcs import (
    ITERATION_RANGES,
    generate,
    random_settings,
)

app = FastAPI()


class GenerateRequest(BaseModel):
    pattern: str
    background: str
    colour: str
    iterations: int


@app.get('/', response_class=HTMLResponse)
def index():
    return HTML


@app.post('/generate')
def api_generate(req: GenerateRequest):
    return {'svg': generate(req.pattern, req.background, req.colour, req.iterations)}


@app.get('/randomise')
def api_randomise():
    s = random_settings()
    return {**s, 'svg': generate(s['pattern'], s['background'], s['colour'], s['iterations'])}


# Iteration ranges as JSON for the JS side
_ITER_RANGES_JSON = json.dumps(ITERATION_RANGES)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SVG Fractal Generator</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: system-ui, -apple-system, sans-serif;
      background: #111;
      color: #ddd;
      height: 100dvh;
      display: flex;
      flex-direction: column;
    }}

    header {{
      padding: .75rem 1.25rem;
      background: #1a1a1a;
      border-bottom: 1px solid #2a2a2a;
      font-weight: 600;
      font-size: .95rem;
      letter-spacing: .02em;
      color: #eee;
    }}

    main {{
      display: flex;
      flex: 1;
      min-height: 0;
    }}

    /* ── Controls ── */
    .panel {{
      width: 240px;
      flex-shrink: 0;
      background: #1a1a1a;
      border-right: 1px solid #2a2a2a;
      padding: 1.25rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 1.1rem;
      overflow-y: auto;
    }}

    .field {{ display: flex; flex-direction: column; gap: .4rem; }}

    label {{
      font-size: .7rem;
      text-transform: uppercase;
      letter-spacing: .07em;
      color: #888;
    }}

    select {{
      background: #252525;
      border: 1px solid #333;
      border-radius: 5px;
      color: #eee;
      font-size: .88rem;
      padding: .45rem .5rem;
      cursor: pointer;
      width: 100%;
    }}
    select:focus {{ outline: none; border-color: #555; }}

    .slider-row {{
      display: flex;
      align-items: center;
      gap: .6rem;
    }}

    input[type=range] {{
      flex: 1;
      accent-color: #5b8dee;
      cursor: pointer;
    }}

    .iter-val {{
      font-size: .85rem;
      font-variant-numeric: tabular-nums;
      color: #bbb;
      min-width: 1.2rem;
      text-align: right;
    }}

    .colour-row {{
      display: flex;
      align-items: center;
      gap: .6rem;
    }}

    input[type=color] {{
      width: 36px;
      height: 30px;
      border: 1px solid #333;
      border-radius: 5px;
      background: none;
      cursor: pointer;
      padding: 2px;
      flex-shrink: 0;
    }}

    .hex-label {{
      font-size: .8rem;
      color: #aaa;
      font-variant-numeric: tabular-nums;
    }}

    .divider {{ border: none; border-top: 1px solid #2a2a2a; }}

    button {{
      width: 100%;
      padding: .55rem;
      border: none;
      border-radius: 5px;
      font-size: .88rem;
      font-weight: 600;
      cursor: pointer;
      transition: opacity .15s;
    }}
    button:hover {{ opacity: .85; }}
    button:active {{ opacity: .7; }}

    .btn-generate  {{ background: #5b8dee; color: #fff; }}
    .btn-randomise {{ background: #252525; color: #ddd; border: 1px solid #333; }}
    .btn-download  {{ background: #2d6a4f; color: #fff; }}
    .btn-download:disabled {{ opacity: .35; cursor: not-allowed; }}

    /* ── Preview ── */
    .preview {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #161616;
      position: relative;
      overflow: hidden;
    }}

    #svg-wrap {{
      width: 90%;
      height: 90%;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    #svg-wrap svg {{
      max-width: 100%;
      max-height: 100%;
      border-radius: 4px;
      box-shadow: 0 4px 32px rgba(0,0,0,.6);
    }}

    #placeholder {{
      color: #444;
      font-size: .9rem;
    }}

    #spinner {{
      display: none;
      position: absolute;
      inset: 0;
      align-items: center;
      justify-content: center;
      background: rgba(0,0,0,.45);
      font-size: .85rem;
      color: #aaa;
    }}
    #spinner.active {{ display: flex; }}
  </style>
</head>
<body>

<header>SVG Fractal Generator</header>

<main>
  <div class="panel">

    <div class="field">
      <label for="pattern">Pattern</label>
      <select id="pattern">
        <option value="hilbert">Hilbert</option>
        <option value="gosper">Gosper</option>
        <option value="peano">Peano</option>
        <option value="moore">Moore</option>
        <option value="sierpinski">Sierpinski</option>
        <option value="dragon">Dragon</option>
      </select>
    </div>

    <div class="field">
      <label>Iterations</label>
      <div class="slider-row">
        <input type="range" id="iterations" min="1" max="6" value="2">
        <span class="iter-val" id="iter-display">2</span>
      </div>
    </div>

    <div class="field">
      <label>Background</label>
      <div class="colour-row">
        <input type="color" id="background" value="#1a1a2e">
        <span class="hex-label" id="bg-hex">#1a1a2e</span>
      </div>
    </div>

    <div class="field">
      <label>Pattern colour</label>
      <div class="colour-row">
        <input type="color" id="colour" value="#5b8dee">
        <span class="hex-label" id="col-hex">#5b8dee</span>
      </div>
    </div>

    <hr class="divider">

    <button class="btn-generate" onclick="generate()">Generate</button>
    <button class="btn-randomise" onclick="randomise()">Randomise</button>
    <button class="btn-download" id="btn-dl" onclick="download()" disabled>Download SVG</button>

  </div>

  <div class="preview">
    <div id="svg-wrap">
      <span id="placeholder">Click Generate to preview</span>
    </div>
    <div id="spinner">Generating&hellip;</div>
  </div>
</main>

<script>
  const ITER_RANGES = {_ITER_RANGES_JSON};
  let currentSvg = '';

  // ── helpers ──────────────────────────────────────────────────

  function cssToHex(name) {{
    const c = document.createElement('canvas');
    c.width = c.height = 1;
    const ctx = c.getContext('2d');
    ctx.fillStyle = name;
    return ctx.fillStyle;   // always returns #rrggbb
  }}

  function setColour(inputId, hexLabelId, value) {{
    const hex = value.startsWith('#') ? value : cssToHex(value);
    document.getElementById(inputId).value = hex;
    document.getElementById(hexLabelId).textContent = hex;
  }}

  function setPattern(pattern) {{
    document.getElementById('pattern').value = pattern;
    const [lo, hi] = ITER_RANGES[pattern];
    const slider = document.getElementById('iterations');
    slider.min = lo;
    slider.max = hi;
    slider.value = Math.min(Math.max(parseInt(slider.value), lo), hi);
    document.getElementById('iter-display').textContent = slider.value;
  }}

  function showSvg(svg) {{
    currentSvg = svg;
    const wrap = document.getElementById('svg-wrap');
    wrap.innerHTML = svg;
    document.getElementById('placeholder')?.remove();
    document.getElementById('btn-dl').disabled = false;
  }}

  function setLoading(on) {{
    document.getElementById('spinner').classList.toggle('active', on);
  }}

  // ── API calls ─────────────────────────────────────────────────

  async function generate() {{
    setLoading(true);
    try {{
      const res = await fetch('/generate', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{
          pattern:    document.getElementById('pattern').value,
          background: document.getElementById('background').value,
          colour:     document.getElementById('colour').value,
          iterations: parseInt(document.getElementById('iterations').value),
        }}),
      }});
      const data = await res.json();
      showSvg(data.svg);
    }} finally {{
      setLoading(false);
    }}
  }}

  async function randomise() {{
    setLoading(true);
    try {{
      const data = await (await fetch('/randomise')).json();
      setPattern(data.pattern);
      document.getElementById('iterations').value = data.iterations;
      document.getElementById('iter-display').textContent = data.iterations;
      setColour('background', 'bg-hex', data.background);
      setColour('colour', 'col-hex', data.colour);
      showSvg(data.svg);
    }} finally {{
      setLoading(false);
    }}
  }}

  function download() {{
    if (!currentSvg) return;
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([currentSvg], {{type: 'image/svg+xml'}}));
    a.download = 'fractal.svg';
    a.click();
  }}

  // ── Live controls ─────────────────────────────────────────────

  document.getElementById('pattern').addEventListener('change', () => {{
    setPattern(document.getElementById('pattern').value);
    generate();
  }});

  // Show value while dragging; generate only on release
  document.getElementById('iterations').addEventListener('input', e =>
    document.getElementById('iter-display').textContent = e.target.value
  );
  document.getElementById('iterations').addEventListener('change', generate);

  let colTimer;
  function debouncedGenerate() {{
    clearTimeout(colTimer);
    colTimer = setTimeout(generate, 350);
  }}

  document.getElementById('background').addEventListener('input', e => {{
    document.getElementById('bg-hex').textContent = e.target.value;
    debouncedGenerate();
  }});

  document.getElementById('colour').addEventListener('input', e => {{
    document.getElementById('col-hex').textContent = e.target.value;
    debouncedGenerate();
  }});
</script>

</body>
</html>
"""

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=False)
