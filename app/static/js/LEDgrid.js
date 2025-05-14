// LEDgrid.js
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
        cell.className   = 'cell selected';
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
        cell.className   = 'cell selected';
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
  if (defaultBtn) {
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
  }

  // Generate JSON (solid fx:0)
  createBtn.addEventListener('click', () => {
    const segments = [];
    for (let i = 0; i < segmentCount; i++) {
      const start = i * segmentSize;
      let stop    = start + segmentSize;
      if (i === segmentCount - 1) stop = start + remainder;

      const cell  = grid.querySelector(`.cell[data-idx="${i}"]`);
      const color = JSON.parse(cell.dataset.color);
      const bri   = parseInt(cell.dataset.bri, 10);

      segments.push({
        start,
        stop,
        col: [color],
        bri,
        fx: 0
      });
    }

    const preset     = { on: true, seg: segments };
    const jsonString = JSON.stringify(preset, null, 2);

    // still set the output text so copy/send work,
    // but the <pre> is hidden via CSS
    output.textContent = jsonString;

    // un-hide the container so the buttons (and heading) appear
    outputContainer.classList.remove('hidden');

    // show only the two JSON action buttons
    document.querySelector('.json-controls').style.display = 'flex';

    // show the save-to-account & public-toggle UI
    document.querySelector('.save-preset-container').style.display = 'flex';
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

  // ===== Added Save to Account Functionality =====
  const saveBtn = document.getElementById('saveToAccount');
  if (saveBtn) {
    saveBtn.addEventListener('click', function() {
      // First, make sure to generate the JSON (if it hasn't been generated already)
      if (outputContainer.classList.contains('hidden')) {
        createBtn.click();
      }
      
      // Get preset name
      const presetName = prompt("Name your preset:", preset_name || "");
      if (!presetName || presetName.trim() === "") return;
      
      // Get RGB configuration data
      const rgbData = getCurrentRgbConfiguration();
      
      // Get public option
      const isPublic = document.getElementById('isPublic')?.checked || false;
      
      // Show loading state
      saveBtn.disabled = true;
      saveBtn.textContent = "Saving...";
      
      // Get CSRF token from meta tag
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
      
      // Send data to server
      fetch('/save-preset', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          preset_name: presetName,
          preset_data: rgbData,
          is_public: isPublic,
          preset_id: preset_id || null
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        saveBtn.disabled = false;
        saveBtn.textContent = "Save to Account";
        const messageEl = document.getElementById('saveMessage');
        if (messageEl) {
          messageEl.style.display = 'block';
          if (data.success) {
            messageEl.className = 'feedback-message success-message';
            messageEl.textContent = data.message || "Preset saved successfully!";
          } else {
            messageEl.className = 'feedback-message error-message';
            messageEl.textContent = data.error || "Error saving preset";
          }
          setTimeout(() => messageEl.style.display = 'none', 3000);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        saveBtn.disabled = false;
        saveBtn.textContent = "Save to Account";
        const messageEl = document.getElementById('saveMessage');
        if (messageEl) {
          messageEl.style.display = 'block';
          messageEl.className = 'feedback-message error-message';
          messageEl.textContent = "Error saving preset: " + error.message;
          setTimeout(() => messageEl.style.display = 'none', 3000);
        }
        alert('An error occurred while saving the preset.');
      });
    });
  }
  
  // Helper function - Get current RGB configuration
  function getCurrentRgbConfiguration() {
    const cells = document.querySelectorAll('.cell');
    const cellsData = Array.from(cells).map(cell => {
      const colorData = cell.dataset.color ? JSON.parse(cell.dataset.color) : [0,0,0];
      const [r, g, b] = colorData;
      return {
        index: parseInt(cell.dataset.idx || 0),
        color: `rgb(${r},${g},${b})`,
        selected: cell.classList.contains('selected')
      };
    });
    const primaryColor = colorPicker.value.substring(1);
    const brightness = parseInt(briSlider.value);
    return {
      primary_color: primaryColor,
      brightness,
      cells: cellsData,
      wled_config: { segmentCount, segmentSize, totalLEDs }
    };
  }

  // Apply preset data if available
  if (window.preset_data) {
    setupContainer.classList.add('hidden');
    editor.classList.remove('hidden');

    if (window.preset_data.wled_config) {
      segmentCount = window.preset_data.wled_config.segmentCount || 10;
      segmentSize = window.preset_data.wled_config.segmentSize || 1;
      totalLEDs = window.preset_data.wled_config.totalLEDs || 10;
    } else {
      segmentCount = 10;
      segmentSize = 1;
      totalLEDs = 10;
    }

    grid.innerHTML = '';
    for (let i = 0; i < segmentCount; i++) {
      const cell = document.createElement('div');
      cell.className   = 'cell';
      cell.dataset.idx = i;
      cell.style.backgroundColor = '#000000';
      cell.dataset.color = JSON.stringify([0,0,0]);
      cell.dataset.bri   = '255';
      grid.appendChild(cell);
    }

    if (window.preset_data.cells && Array.isArray(window.preset_data.cells)) {
      window.preset_data.cells.forEach(cellData => {
        const cell = grid.querySelector(`.cell[data-idx="${cellData.index}"]`);
        if (!cell) return;
        cell.style.backgroundColor = cellData.color;
        const rgbMatch = cellData.color.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
        if (rgbMatch) {
          const [_, r, g, b] = rgbMatch.map(Number);
          cell.dataset.color = JSON.stringify([r, g, b]);
        }
        if (window.view_mode && cellData.selected) {
          cell.classList.add('selected');
        }
      });
    }

    if (window.preset_data.primary_color && colorPicker) {
      colorPicker.value = '#' + window.preset_data.primary_color;
    }
    if (window.preset_data.brightness !== undefined && briSlider) {
      briSlider.value = window.preset_data.brightness;
      briValue.textContent = window.preset_data.brightness;
    }
    if (window.view_mode) {
      document.querySelectorAll('.cell').forEach(cell => {
        cell.style.pointerEvents = 'none';
      });
    }
  }
});
