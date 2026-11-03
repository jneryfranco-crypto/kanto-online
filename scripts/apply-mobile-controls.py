from pathlib import Path
import sys

engine = Path(sys.argv[1])
input_file = engine / "src/core/Input.ts"
source = input_file.read_text(encoding="utf-8")

if "createTouchControls()" not in source:
    source = source.replace(
        "  private callbacks = new Map<string, Array<() => void>>();",
        "  private callbacks = new Map<string, Array<() => void>>();\n  private touchKeys = new Set<string>();"
    )
    source = source.replace(
        "    });\n  }\n\n  isDown(key: string): boolean {",
        "    });\n    this.createTouchControls();\n  }\n\n  isDown(key: string): boolean {",
        1
    )
    source = source.replace(
        "if (this.keys.has(key)) return dir;",
        "if (this.keys.has(key) || this.touchKeys.has(key)) return dir;"
    )
    source = source.replace(
        "return this.keys.has('Shift');",
        "return this.keys.has('Shift') || this.touchKeys.has('Shift');"
    )
    source = source.replace(
        "if (this.keys.has(key)) return true;",
        "if (this.keys.has(key) || this.touchKeys.has(key)) return true;"
    )
    method = r'''
  /** Touch controls for phones/tablets; keyboard controls remain available. */
  private createTouchControls(): void {
    if (document.getElementById('kanto-touch-controls')) return;
    const root = document.createElement('div');
    root.id = 'kanto-touch-controls';
    root.setAttribute('aria-label', 'Controles do jogo');
    root.innerHTML = `
      <div class="kanto-touch-left">
        <div class="kanto-joystick" role="group" aria-label="Direcional">
          <div class="kanto-joystick-knob"></div>
        </div>
      </div>
      <div class="kanto-touch-right">
        <button class="kanto-touch-key kanto-key-b" data-key="Escape" aria-label="B">B</button>
        <button class="kanto-touch-key kanto-key-a" data-key="Enter" aria-label="A">A</button>
        <div class="kanto-touch-utility">
          <button class="kanto-touch-small" data-key="Shift" aria-label="Correr">RUN</button>
          <button class="kanto-touch-small" data-key="e" aria-label="Interagir">E</button>
        </div>
      </div>`;
    document.body.appendChild(root);
    const joystick = root.querySelector<HTMLElement>('.kanto-joystick')!;
    const knob = root.querySelector<HTMLElement>('.kanto-joystick-knob')!;
    let pointerId: number | null = null;
    const release = () => {
      for (const key of ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight']) this.touchKeys.delete(key);
      pointerId = null;
      knob.style.transform = 'translate(-50%, -50%)';
    };
    const updateDirection = (event: PointerEvent) => {
      const rect = joystick.getBoundingClientRect();
      const dx = event.clientX - (rect.left + rect.width / 2);
      const dy = event.clientY - (rect.top + rect.height / 2);
      const limit = rect.width * 0.28;
      const length = Math.hypot(dx, dy) || 1;
      const scale = Math.min(1, limit / length);
      knob.style.transform = `translate(calc(-50% + ${dx * scale}px), calc(-50% + ${dy * scale}px))`;
      for (const key of ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight']) this.touchKeys.delete(key);
      if (Math.max(Math.abs(dx), Math.abs(dy)) > rect.width * 0.12) {
        if (Math.abs(dx) > Math.abs(dy)) this.touchKeys.add(dx < 0 ? 'ArrowLeft' : 'ArrowRight');
        else this.touchKeys.add(dy < 0 ? 'ArrowUp' : 'ArrowDown');
      }
    };
    joystick.addEventListener('pointerdown', event => {
      event.preventDefault(); pointerId = event.pointerId;
      joystick.setPointerCapture(pointerId); updateDirection(event);
    });
    joystick.addEventListener('pointermove', event => {
      if (pointerId === event.pointerId) updateDirection(event);
    });
    joystick.addEventListener('pointerup', release);
    joystick.addEventListener('pointercancel', release);
    joystick.addEventListener('lostpointercapture', release);
    root.querySelectorAll<HTMLButtonElement>('[data-key]').forEach(button => {
      const key = button.dataset.key!;
      const down = (event: PointerEvent) => {
        event.preventDefault(); button.setPointerCapture(event.pointerId); this.touchKeys.add(key);
      };
      const up = () => { this.touchKeys.delete(key); };
      button.addEventListener('pointerdown', down);
      button.addEventListener('pointerup', up);
      button.addEventListener('pointercancel', up);
      button.addEventListener('lostpointercapture', up);
      button.addEventListener('contextmenu', event => event.preventDefault());
    });
  }

'''
    marker = "  onKeyDown(key: string, callback: () => void): void {"
    if marker not in source:
        raise SystemExit("Could not locate Input.onKeyDown insertion point")
    source = source.replace(marker, method + marker, 1)
    input_file.write_text(source, encoding="utf-8")

index_file = engine / "index.html"
html = index_file.read_text(encoding="utf-8")
if "kanto-touch-controls" not in html:
    style = r'''
    #kanto-touch-controls { display:none; }
    @media (pointer: coarse), (max-width: 900px) {
      html, body { width:100%; height:100%; height:100dvh; overscroll-behavior:none; }
      body { touch-action:none; user-select:none; -webkit-user-select:none; }
      #game-container { width:100%; height:100%; height:100dvh; overflow:hidden; }
      #game-container canvas { max-width:100%; max-height:100%; touch-action:none; }
      #kanto-touch-controls {
        position:fixed; inset:0; z-index:20; display:flex; justify-content:space-between;
        align-items:flex-end; padding: max(22px, env(safe-area-inset-top)) max(22px, env(safe-area-inset-right))
          max(42px, env(safe-area-inset-bottom)) max(22px, env(safe-area-inset-left));
        pointer-events:none; color:#fff; font-family:Arial,sans-serif;
      }
      .kanto-touch-left,.kanto-touch-right { display:flex; align-items:flex-end; pointer-events:none; }
      .kanto-joystick {
        width:min(34vw,156px); height:min(34vw,156px); min-width:112px; min-height:112px;
        border-radius:50%; position:relative; background:rgba(120,135,155,.28);
        border:2px solid rgba(210,225,255,.18); box-shadow:inset 0 0 18px #0008,0 4px 18px #0008;
        pointer-events:auto; touch-action:none;
      }
      .kanto-joystick-knob {
        position:absolute; left:50%; top:50%; width:43%; height:43%; border-radius:50%;
        transform:translate(-50%,-50%); background:radial-gradient(circle at 35% 28%,#d9efff,#5e9ed8 58%,#244b82);
        border:3px solid #a9d5ff; box-shadow:0 3px 10px #0009;
      }
      .kanto-touch-right { position:relative; width:min(42vw,190px); height:min(34vw,150px); min-height:132px; }
      .kanto-touch-key {
        position:absolute; width:clamp(66px,18vw,94px); height:clamp(66px,18vw,94px); border-radius:50%;
        border:3px solid #9bd4ff; color:white; font-weight:900; font-size:clamp(27px,7vw,40px);
        text-shadow:0 2px 4px #123; box-shadow:inset 0 3px 8px #fff8,0 5px 12px #0009;
        pointer-events:auto; touch-action:none;
      }
      .kanto-key-a { right:0; top:0; background:radial-gradient(circle at 35% 25%,#8ceaff,#1684e9 62%,#0750b7); }
      .kanto-key-b { left:0; bottom:0; background:radial-gradient(circle at 35% 25%,#8ceaff,#1684e9 62%,#0750b7); }
      .kanto-touch-utility { position:absolute; right:0; bottom:100%; display:flex; gap:10px; margin-bottom:12px; }
      .kanto-touch-small {
        width:48px; height:48px; border-radius:50%; border:2px solid #ddd; color:white; font-weight:bold;
        background:linear-gradient(#59616c,#171b22); box-shadow:0 3px 10px #0009; pointer-events:auto; touch-action:none;
      }
    }
'''
    html = html.replace("</style>", style + "\n  </style>", 1)
    html = html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, maximum-scale=1.0, user-scalable=no">'
    )
    index_file.write_text(html, encoding="utf-8")
print("Mobile controls patch applied.")
