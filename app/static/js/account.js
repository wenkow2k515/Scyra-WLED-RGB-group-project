let presetToDelete = null;
    
function confirmDelete(presetId) {
    presetToDelete = presetId;
    document.getElementById('deleteModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('deleteModal').style.display = 'none';
}

document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
    if (presetToDelete) {
        window.location.href = `/presets/${presetToDelete}/delete`;
    }
});