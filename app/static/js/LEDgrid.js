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

  // ===== Added Save to Account Functionality =====
  const saveBtn = document.getElementById('saveToAccount');
  if (saveBtn) {
    saveBtn.addEventListener('click', function() {
      // Get preset name
      const presetName = prompt("Name your preset:", 
          preset_name || "");
      
      if (!presetName || presetName.trim() === "") return; // User canceled or input is empty
      
      // Get RGB configuration data
      const rgbData = getCurrentRgbConfiguration();
      
      // Get public option
      const isPublic = document.getElementById('isPublic')?.checked || false;
      console.log("Is preset public:", isPublic);
      
      // Show loading state
      saveBtn.disabled = true;
      saveBtn.textContent = "Saving...";
      
      // Send data to server
      fetch('/save-preset', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              preset_name: presetName,
              preset_data: rgbData,
              is_public: isPublic,
              preset_id: preset_id || null
          })
      })
      .then(response => response.json())
      .then(data => {
          // Reset button
          saveBtn.disabled = false;
          saveBtn.textContent = "Save to Account";
          
          // Show feedback
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
            
            setTimeout(() => {
                messageEl.style.display = 'none';
            }, 3000);
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
            messageEl.textContent = "Error saving preset";
            
            setTimeout(() => {
                messageEl.style.display = 'none';
            }, 3000);
          }
      });
    });
  }
  
  // Helper function - Get current RGB configuration
  function getCurrentRgbConfiguration() {
      // Get all cells and their colors
      const cells = document.querySelectorAll('.cell');
      const cellsData = Array.from(cells).map(cell => {
          // Use existing dataset structure
          const colorData = cell.dataset.color ? JSON.parse(cell.dataset.color) : [0,0,0];
          const r = colorData[0];
          const g = colorData[1];
          const b = colorData[2];
          
          return {
              index: parseInt(cell.dataset.idx || 0),
              color: `rgb(${r},${g},${b})`,
              selected: cell.classList.contains('selected')
          };
      });
      
      // Get primary color from color picker
      const primaryColor = colorPicker ? colorPicker.value.substring(1) : 'ffffff'; // Remove #
      
      // Get brightness value
      const brightness = briSlider ? parseInt(briSlider.value) : 255;
      
      // Add WLED-specific data for restoring presets
      return {
          primary_color: primaryColor,
          brightness: brightness,
          cells: cellsData,
          wled_config: {
              segmentCount: segmentCount,
              segmentSize: segmentSize,
              totalLEDs: totalLEDs
          }
      };
  }

  // Apply preset data if available
  if (window.preset_data) {
    console.log("Loading preset data:", window.preset_data);
    
    // Skip setup phase, go directly to editor
    setupContainer.classList.add('hidden');
    editor.classList.remove('hidden');
    
    // Set grid dimensions based on saved preset or use defaults
    if (window.preset_data.wled_config) {
      segmentCount = window.preset_data.wled_config.segmentCount || 10;
      segmentSize = window.preset_data.wled_config.segmentSize || 1;
      totalLEDs = window.preset_data.wled_config.totalLEDs || 10;
    } else {
      // Default to debug mode (10 cells)
      segmentCount = 10;
      segmentSize = 1;
      totalLEDs = 10;
    }
    
    // Build grid
    grid.innerHTML = '';
    for (let i = 0; i < segmentCount; i++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.dataset.idx = i;
      cell.style.backgroundColor = '#000000'; // Default black
      cell.dataset.color = JSON.stringify([0,0,0]);
      cell.dataset.bri = '255';
      grid.appendChild(cell);
    }
    
    // Apply cell colors from preset data
    if (window.preset_data.cells && Array.isArray(window.preset_data.cells)) {
      window.preset_data.cells.forEach(cellData => {
        const cell = grid.querySelector(`.cell[data-idx="${cellData.index}"]`);
        if (cell) {
          // Apply color
          cell.style.backgroundColor = cellData.color;
          
          // Convert the RGB color to dataset format
          const rgbMatch = cellData.color.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
          if (rgbMatch) {
            const r = parseInt(rgbMatch[1]);
            const g = parseInt(rgbMatch[2]);
            const b = parseInt(rgbMatch[3]);
            cell.dataset.color = JSON.stringify([r, g, b]);
          }
          
          // // Add selection if in view mode
          // if (window.view_mode && cellData.selected) {
          //   cell.classList.add('selected');
          // }
        }
      });
    }
    
    // Apply primary color to color picker
    if (window.preset_data.primary_color && colorPicker) {
      colorPicker.value = '#' + window.preset_data.primary_color;
    }
    
    // Apply brightness to slider
    if (window.preset_data.brightness !== undefined && briSlider) {
      briSlider.value = window.preset_data.brightness;
      if (briValue) briValue.textContent = window.preset_data.brightness;
    }
    
    // If in view mode, disable interactions
    if (window.view_mode) {
      document.querySelectorAll('.cell').forEach(cell => {
        cell.style.pointerEvents = 'none';
      });
    }
    
    console.log("Preset data applied to grid");
  }
});
