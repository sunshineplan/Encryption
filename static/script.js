function Copy() {
    textarea = $('#' + $("input[name='text']:checked").val());
    textarea.select();
    document.execCommand('Copy');
    textarea[0].setSelectionRange(textarea.val().length, textarea.val().length);
    if (textarea.val() !== '') {
        alert('Text has been copied to clipboard.');
    };
};

function Clear() {
    $('#unencrypted').val('');
    $('#encrypted').val('');
};

function getLevel() {
    if (0 < $('#level').val().length && $('#level').val().length < 6) {
        return $('#level').val();
    } else {
        return false;
    };
};
