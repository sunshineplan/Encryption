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
    if (0 < $('#level').val() && $('#level').val() < 101) {
        return $('#level').val();
    } else {
        return false;
    };
};

function waiting(on=true) {
    if (on == true) {
        $('.btn').attr('disabled', true);
        $('body').addClass('wait');
        $('.navbar').css('pointer-events', 'none');
        $('.row').css('pointer-events', 'none');
    } else {
        $('.btn').attr('disabled', false);
        $('body').removeClass('wait');
        $('.navbar').css('pointer-events', 'auto');
        $('.row').css('pointer-events', 'auto');
    };
};
