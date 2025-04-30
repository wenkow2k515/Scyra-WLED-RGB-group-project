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
            window.location.href = "{{ url_for('delete_preset', preset_id=0) }}".replace('0', presetToDelete);
        }
    });