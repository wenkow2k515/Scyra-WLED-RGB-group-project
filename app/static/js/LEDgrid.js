document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const groupSize = Number(urlParams.get('group_size'));
    const totalLEDs = 300; // Replace with actual total LEDs if available
    const pixelCount = totalLEDs / groupSize;

    const grid = document.getElementById('grid');
    grid.innerHTML = '';

    // Initialize the grid
    for (let i = 0; i < pixelCount; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.idx = i;
        cell.dataset.color = '[255,255,255]';
        cell.dataset.bri = 255;
        grid.appendChild(cell);
    }

    // Add event listeners for grid interactions
    grid.addEventListener('click', (e) => {
        if (e.target.classList.contains('cell')) {
            e.target.classList.toggle('selected');
        }
    });

    // Brightness slider
    const briSlider = document.getElementById('briSlider');
    const briValue = document.getElementById('briValue');
    briSlider.addEventListener('input', () => {
        briValue.textContent = briSlider.value;
    });

    // Applying colors to the selection
    document.getElementById('applyColor').onclick = () => {
        const hex = document.getElementById('colorPicker').value;
        const r = parseInt(hex.slice(1, 3), 16),
            g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16);
        const bri = Number(briSlider.value);
        document.querySelectorAll('.cell.selected').forEach((c) => {
            c.style.background = hex;
            c.dataset.color = JSON.stringify([r, g, b]);
            c.dataset.bri = bri;
        });
    };

    // Default color: 50% blue
    document.getElementById('defaultBtn').onclick = () => {
        briSlider.value = 128;
        briValue.textContent = 128;
        document.querySelectorAll('.cell').forEach((c) => {
            c.classList.add('selected');
            c.style.background = '#0000ff';
            c.dataset.color = JSON.stringify([0, 0, 255]);
            c.dataset.bri = 128;
        });
    };
    
    // Select All
    document.getElementById('selectAllBtn').onclick = () => {
      document.querySelectorAll('.cell').forEach((c) => {
          c.classList.add('selected');
      });
  };

  // Cancel All
  document.getElementById('cancelAllBtn').onclick = () => {
      document.querySelectorAll('.cell').forEach((c) => {
          c.classList.remove('selected');
      });
  };

    // Create JSON
    document.getElementById('createBtn').onclick = () => {
        const cells = Array.from(document.querySelectorAll('.cell.selected'));
        if (!cells.length) {
            alert('Please select at least one segment.');
            return;
        }

        // Build array of { idx, color, bri }
        const segsRaw = cells
            .map((c) => ({
                idx: Number(c.dataset.idx),
                color: c.dataset.color,
                bri: Number(c.dataset.bri),
            }))
            .sort((a, b) => a.idx - b.idx);

        // Merge same properties
        const merged = [];
        let run = null;
        segsRaw.forEach((item) => {
            if (
                run &&
                item.idx === run.end + 1 &&
                item.color === run.color &&
                item.bri === run.bri
            ) {
                run.end = item.idx;
            } else {
                if (run) merged.push(run);
                run = { startIdx: item.idx, end: item.idx, color: item.color, bri: item.bri };
            }
        });
        if (run) merged.push(run);

        // Converts JSON segments to WLED-parsable code
        const segs = merged.map((r) => ({
            start: r.startIdx * groupSize,
            stop: (r.end + 1) * groupSize,
            bri: r.bri,
            col: [JSON.parse(r.color)],
            grp: groupSize,
        }));

        const payload = { on: true, seg: segs };
        document.getElementById('output').textContent = JSON.stringify(payload, null, 2);
    };

    document.getElementById('outputToTextBoxBtn').onclick = () => {
        const cells = Array.from(document.querySelectorAll('.cell.selected'));
        if (!cells.length) {
            alert('Please select at least one segment.');
            return;
        }

        // Build array of { idx, color, bri }
        const segsRaw = cells
            .map((c) => ({
                idx: Number(c.dataset.idx),
                color: c.dataset.color,
                bri: Number(c.dataset.bri),
            }))
            .sort((a, b) => a.idx - b.idx);

        // Merge same properties
        const merged = [];
        let run = null;
        segsRaw.forEach((item) => {
            if (
                run &&
                item.idx === run.end + 1 &&
                item.color === run.color &&
                item.bri === run.bri
            ) {
                run.end = item.idx;
            } else {
                if (run) merged.push(run);
                run = { startIdx: item.idx, end: item.idx, color: item.color, bri: item.bri };
            }
        });
        if (run) merged.push(run);

        // Converts JSON segments to WLED-parsable code
        const segs = merged.map((r) => ({
            start: r.startIdx * groupSize,
            stop: (r.end + 1) * groupSize,
            bri: r.bri,
            col: [JSON.parse(r.color)],
            grp: groupSize,
        }));

        const payload = { on: true, seg: segs };

        // Output JSON to <textarea>
        const textBox = document.getElementById('jsonTextBox');
        textBox.value = JSON.stringify(payload, null, 2); // Pretty-print JSON
    };
});