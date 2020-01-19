function Copy() {
    result = document.getElementById('output');
    result.select();
    document.execCommand('Copy');
    result.setSelectionRange(0, 0);
    if (result.value !== '') {
        alert('Output has been copied to clipboard.');
    };
};

function Clear() {
    $('#content').val('');
    $('#output').val('');
};