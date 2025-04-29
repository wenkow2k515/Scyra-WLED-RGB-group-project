document.addEventListener('DOMContentLoaded', () => {
  // State
  let wledAddress = '';
  let totalLEDs   = 0;
  let segmentCount= 0;
  let segmentSize = 0;
  let remainder   = 0;

  // DOM
  const setupContainer   = document.getElementById('setup');
  const editor           = document.getElementById('editor');
  const outputContainer  = document.getElementById('output-container');

  const addrInput        = document.getElementById('wledAddress');
  const checkBtn         = document.getElementById('checkBtn');
  const checkMsg         = document.getElementById('checkMsg');

  const grid             = document.getElementById('grid');
  const colorPicker      = document.getElementById('colorPicker');
  const briSlider        = document.getElementById('briSlider');
  const briValue         = document.getElementById('briValue');
  const applyColorBtn    = document.getElementById('applyColor');
  const defaultBtn       = document.getElementById('defaultBtn');
  const createBtn        = document.getElementById('createBtn');
  const output           = document.getElementById('output');
  const copyJsonBtn      = document.getElementById('copyJson');
  const sendToWledBtn    = document.getElementById('sendToWled');

  // Enable Connect button only when there's input
  addrInput.addEventListener('input', () => {
    checkBtn.disabled = !addrInput.value.trim();
    checkMsg.textContent = '';
  });

  // Connect & build grid
  checkBtn.addEventListener('click', async () => {
    let addr = addrInput.value.trim();
    if (!addr) return;
    if (!/^https?:\/\//i.test(addr)) addr = 'http://' + addr;

    // --- DEBUG MODE: IP "000" → show 10 test squares ---
    if (addr === '000' || addr === 'http://000') {
      wledAddress   = addr;
      totalLEDs     = 10;
      segmentCount  = 10;
      segmentSize   = 1;
      remainder     = 0;
      checkMsg.textContent = 'Debug mode: 10 test segments';
      // build grid
      grid.innerHTML = '';
      for (let i = 0; i < segmentCount; i++) {
        const cell = document.createElement('div');
        cell.className   = 'cell';
        cell.dataset.idx = i;
        cell.style.backgroundColor = '#ffffff';
        cell.dataset.color = JSON.stringify([255,255,255]);
        cell.dataset.bri   = '255';
        grid.appendChild(cell);
      }
      setupContainer.classList.add('hidden');
      editor.classList.remove('hidden');
      return;
    }
    // --------------------------------------

    checkMsg.textContent = 'Connecting…';

    try {
      const resp = await fetch(`${addr}/json`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      if (!data.info?.leds?.count) throw new Error('Invalid LED count');

      totalLEDs   = data.info.leds.count;
      wledAddress = addr;
      checkMsg.textContent = `Connected! ${totalLEDs} LEDs detected.`;

      // --- SEGMENTATION: ensure ≤16 segments ---
      const grp = Math.ceil(totalLEDs / 16);
      segmentSize  = grp;
      segmentCount = Math.ceil(totalLEDs / grp);
      remainder    = totalLEDs - (segmentSize * (segmentCount - 1));
      // --------------------------------------

      // Build one cell per segment
      grid.innerHTML = '';
      for (let i = 0; i < segmentCount; i++) {
        const cell = document.createElement('div');
        cell.className   = 'cell';
        cell.dataset.idx = i;
        cell.style.backgroundColor = '#ffffff';
        cell.dataset.color = JSON.stringify([255,255,255]);
        cell.dataset.bri   = '255';
        grid.appendChild(cell);
      }

      setupContainer.classList.add('hidden');
      editor.classList.remove('hidden');
    } catch (err) {
      checkMsg.textContent = `Error: ${err.message}`;
    }
  });

  // Brightness slider feedback
  briSlider.addEventListener('input', () => {
    briValue.textContent = briSlider.value;
  });

  // Select/deselect cells
  grid.addEventListener('click', e => {
    if (e.target.classList.contains('cell')) {
      e.target.classList.toggle('selected');
    }
  });

  // Apply color + brightness to selected cells
  applyColorBtn.addEventListener('click', () => {
    const hex = colorPicker.value;
    const r   = parseInt(hex.slice(1,3),16);
    const g   = parseInt(hex.slice(3,5),16);
    const b   = parseInt(hex.slice(5,7),16);
    const bri = parseInt(briSlider.value,10);

    document.querySelectorAll('.cell.selected').forEach(cell => {
      cell.style.backgroundColor = hex;
      cell.dataset.color = JSON.stringify([r,g,b]);
      cell.dataset.bri   = bri.toString();
    });
  });

  // Default: select all, 50% blue
  defaultBtn.addEventListener('click', () => {
    briSlider.value = 128;
    briValue.textContent = '128';
    document.querySelectorAll('.cell').forEach(cell => {
      cell.classList.add('selected');
      cell.style.backgroundColor = '#0000ff';
      cell.dataset.color = JSON.stringify([0,0,255]);
      cell.dataset.bri   = '128';
    });
  });

  // Generate JSON (solid fx:0)
  createBtn.addEventListener('click', () => {
    const segments = [];
    for (let i = 0; i < segmentCount; i++) {
      const start = i * segmentSize;
      let stop    = start + segmentSize;
      if (i === segmentCount - 1) stop = start + remainder;

      const cell  = grid.querySelector(`.cell[data-idx="${i}"]`);
      const color = JSON.parse(cell.dataset.color);
      const bri   = parseInt(cell.dataset.bri,10);

      segments.push({
        start,
        stop,
        col: [color],
        bri,
        fx: 0
      });
    }

    const preset = { on: true, seg: segments };
    output.textContent = JSON.stringify(preset, null, 2);
    outputContainer.classList.remove('hidden');
  });

  // Copy JSON
  copyJsonBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(output.textContent)
      .then(() => alert('Copied to clipboard!'))
      .catch(err => console.error('Copy failed:', err));
  });

  // Send to WLED
  sendToWledBtn.addEventListener('click', async () => {
    if (!wledAddress) {
      alert('No WLED address configured');
      return;
    }
    try {
      const resp = await fetch(`${wledAddress}/json/state`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: output.textContent
      });
      if (resp.ok) {
        alert('Successfully sent to WLED!');
      } else {
        throw new Error(`HTTP ${resp.status}`);
      }
    } catch (err) {
      alert(`Failed to send: ${err.message}`);
    }
  });
});
