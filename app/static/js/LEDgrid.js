document.addEventListener("DOMContentLoaded", function () {
  const grid = document.getElementById("ledGrid");

  for (let i = 0; i < 256; i++) {
    const cell = document.createElement("div");
    cell.className = "color-cell";

    const colorInput = document.createElement("input");
    colorInput.type = "color";
    colorInput.className = "color-input";
    colorInput.addEventListener("input", () => {
      cell.style.backgroundColor = colorInput.value;
    });

    cell.appendChild(colorInput);
    grid.appendChild(cell);
  }
});


function exportColors() {
    const cells = document.querySelectorAll('.color-cell');
    const colors = [];
  
    cells.forEach(cell => {
      // get the color of the grid and the default value is  #ffffff
      let bg = window.getComputedStyle(cell).backgroundColor;
      let hex = rgbToHex(bg).trim();
      colors.push(hex);
    });
  
    // display the JSON output in the div
    const jsonOutput = JSON.stringify(colors, null, 2); // pretty print
    // document.getElementById('output').textContent = jsonOutput;
  
    downloadJSON(jsonOutput, "led_colors.json");
  }
  
  // RGB turn to HEX
  function rgbToHex(rgb) {
    const result = rgb.match(/\d+/g);
    if (!result) return "#ffffff";
    return (
      "#" +
      result.slice(0, 3).map(x => {
        const hex = parseInt(x).toString(16);
        return hex.length === 1 ? "0" + hex : hex;
      }).join("")
    );
  }
  
  // download JSON 
  function downloadJSON(content, fileName) {
    const blob = new Blob([content], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = fileName;
    a.click();
  }
  