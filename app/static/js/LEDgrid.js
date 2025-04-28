document.addEventListener('DOMContentLoaded', () => {
    // Visibility management
    function show(id) {
        document.querySelectorAll('.setup-pane, #editor').forEach(el => {
            el.classList.add('hidden');
        });
        const target = document.getElementById(id);
        if (target) target.classList.remove('hidden');
        if (id === 'editor') {
            document.getElementById('setup').classList.add('hidden');
        }
    }

    // Initial state
    show('step1');

    // Step 1: WLED Address Validation
    const addrInput = document.getElementById('wledAddress');
    const checkBtn = document.getElementById('checkBtn');
    const checkMsg = document.getElementById('checkMsg');

    addrInput.addEventListener('input', () => {
        checkBtn.disabled = !addrInput.value.trim();
    });

    checkBtn.addEventListener('click', async () => {
        let addr = addrInput.value.trim();
        if (!/^https?:\/\//i.test(addr)) addr = 'http://' + addr;
        checkMsg.textContent = 'Checking...';
        
        try {
            const response = await fetch(`${addr}/json`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            
            if (!data.info?.leds?.count) throw new Error('Invalid LED count');
            window.totalLEDs = data.info.leds.count;
            window.baseUrl = addr;
            
            document.getElementById('groupSize').disabled = false;
            show('step2');
            checkMsg.textContent = '';
        } catch (error) {
            checkMsg.textContent = `Error: ${error.message}`;
        }
    });

    // Step 2: Group Size Validation
    const groupSizeInput = document.getElementById('groupSize');
    const toEditorBtn = document.getElementById('toEditor');
    const divMsg = document.getElementById('divMsg');

    groupSizeInput.addEventListener('input', () => {
        const value = parseInt(groupSizeInput.value);
        divMsg.textContent = '';
        
        if (!value || value < 1 || window.totalLEDs % value !== 0) {
            toEditorBtn.disabled = true;
            if (value) divMsg.textContent = `Must divide ${window.totalLEDs} exactly`;
        } else {
            toEditorBtn.disabled = false;
        }
    });

    // Step 3: Editor Initialization
    toEditorBtn.addEventListener('click', () => {
        const groupSize = parseInt(groupSizeInput.value);
        const pixelCount = window.totalLEDs / groupSize;
        const grid = document.getElementById('grid');
        
        grid.innerHTML = '';
        for (let i = 0; i < pixelCount; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.idx = i;
            cell.style.backgroundColor = '#ffffff';
            cell.dataset.color = JSON.stringify([255, 255, 255]);
            cell.dataset.bri = 255;
            grid.appendChild(cell);
        }
        show('editor');
    });

    // Editor Functionality
    const briSlider = document.getElementById('briSlider');
    const briValue = document.getElementById('briValue');
    const colorPicker = document.getElementById('colorPicker');
    const applyColorBtn = document.getElementById('applyColor');
    const defaultBtn = document.getElementById('defaultBtn');
    const createBtn = document.getElementById('createBtn');
    const outputEl = document.getElementById('output');

    // Brightness Slider
    briSlider.addEventListener('input', () => {
        briValue.textContent = briSlider.value;
    });

    // Color Application
    applyColorBtn.addEventListener('click', () => {
        const hex = colorPicker.value;
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        const bri = parseInt(briSlider.value);
        
        document.querySelectorAll('.cell.selected').forEach(cell => {
            cell.style.backgroundColor = hex;
            cell.dataset.color = JSON.stringify([r, g, b]);
            cell.dataset.bri = bri;
        });
    });

    // Default Button
    defaultBtn.addEventListener('click', () => {
        briSlider.value = 128;
        briValue.textContent = 128;
        document.querySelectorAll('.cell').forEach(cell => {
            cell.classList.add('selected');
            cell.style.backgroundColor = '#0000ff';
            cell.dataset.color = JSON.stringify([0, 0, 255]);
            cell.dataset.bri = 128;
        });
    });

    // Cell Selection
    document.getElementById('grid').addEventListener('click', (e) => {
        if (e.target.classList.contains('cell')) {
            e.target.classList.toggle('selected');
        }
    });

    // JSON Generation
    createBtn.addEventListener('click', () => {
        const groupSize = parseInt(document.getElementById('groupSize').value);
        const segments = [];
        
        document.querySelectorAll('.cell').forEach(cell => {
            const idx = parseInt(cell.dataset.idx);
            const color = JSON.parse(cell.dataset.color);
            const bri = parseInt(cell.dataset.bri);
            
            segments.push({
                start: idx * groupSize,
                stop: (idx + 1) * groupSize,
                col: [color],
                bri: bri,
                grp: groupSize
            });
        });

        const preset = {
            on: true,
            seg: segments
        };

        outputEl.textContent = JSON.stringify(preset, null, 2);
    });

    // Output JSON to Text Box
    const outputToTextBoxBtn = document.getElementById('outputToTextBoxBtn');
    const jsonTextBox = document.getElementById('jsonTextBox');

    outputToTextBoxBtn.addEventListener('click', () => {
        const groupSize = parseInt(document.getElementById('groupSize').value);
        const segments = [];
        
        document.querySelectorAll('.cell').forEach(cell => {
            const idx = parseInt(cell.dataset.idx);
            const color = JSON.parse(cell.dataset.color);
            const bri = parseInt(cell.dataset.bri);
            
            segments.push({
                start: idx * groupSize,
                stop: (idx + 1) * groupSize,
                col: [color],
                bri: bri,
                grp: groupSize
            });
        });

        const preset = {
            on: true,
            seg: segments
        };

        // Output JSON to the text box
        jsonTextBox.value = JSON.stringify(preset, null, 2); // Pretty print
    });
});

