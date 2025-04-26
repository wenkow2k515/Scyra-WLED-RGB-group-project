document.addEventListener('DOMContentLoaded', () => {
    const show = (id) => {
        document.querySelectorAll('.step').forEach((s) => s.classList.remove('active'));
        const element = document.getElementById(id);
        if (element) {
            element.classList.add('active');
        } else {
            console.error(`Element with ID "${id}" not found.`);
        }
    };

    // This takes the total number of LEDs from the WLED JSON package
    const addrInput = document.getElementById('wledAddress');
    const checkBtn = document.getElementById('checkBtn');
    const checkMsg = document.getElementById('checkMsg');

    addrInput.addEventListener('input', () => {
        checkBtn.disabled = !addrInput.value.trim();
        checkMsg.textContent = '';
    });

    checkBtn.onclick = async () => {
        // Reminder: WLED uses HTTP protocol, not HTTPS
        let addr = addrInput.value.trim();
        if (!/^https?:\/\//i.test(addr)) addr = 'http://' + addr;

        //comment this part of code to test without real WLED
        checkMsg.textContent = '';
        try {
            const res = await fetch(`${addr}/json`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const data = await res.json();
            const total = data.info?.leds?.count;

            if (!Number.isInteger(total) || total <= 0) {
                throw new Error('Invalid LED count');
            }

            window.totalLEDs = total;
            window.baseUrl = addr;
            show('step2');
        } catch (e) {
            checkMsg.textContent = `Cannot connect (${e.message}).`;
        }
        //comment this part of code to test without real WLED
        
        window.totalLEDs = 300; // Set a mock total LED count for testing
        window.baseUrl = addr; // Use the entered address as-is
        show('step2');
    };

    // Bugfix: The group size must be able to divide the number of LEDs
    const groupSize = document.getElementById('groupSize');
    const toStep3 = document.getElementById('toStep3');
    const divMsg = document.getElementById('divMsg');

    groupSize.addEventListener('input', () => {
        divMsg.textContent = '';
        const g = Number(groupSize.value);

        if (!g || g < 1) {
            toStep3.disabled = true;
        } else if (window.totalLEDs % g !== 0) {
            toStep3.disabled = true;
            divMsg.textContent = `Group size must divide ${window.totalLEDs} exactly.`;
        } else {
            toStep3.disabled = false;
        }
    });

    let pixelCount, grpSize;

    toStep3.onclick = () => {
        grpSize = Number(groupSize.value);
        pixelCount = window.totalLEDs / grpSize;
    
        // Redirect to Step 3
        window.location.href = `/step3?wled_address=${encodeURIComponent(window.baseUrl)}&group_size=${grpSize}`;
    };
});