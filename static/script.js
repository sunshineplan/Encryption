function Copy() {
    var textarea = $('#' + $("input[name='text']:checked").val());
    if (textarea.val().trim() !== '') {
        navigator.clipboard.writeText(textarea.val())
            .then(() => alert('Text has been copied to clipboard.'))
            .catch(() => alert('Unable to copy to clipboard.'));
    };
};

function Clear() {
    $('#unencrypted').val('');
    $('#encrypted').val('');
};

function waiting(on = true) {
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

function doEncrypt() {
    if ($('#unencrypted').val() == '') {
        alert('Empty unencrypted text!');
        return;
    };
    var key = $('#key').val().trim();
    if (key == '') {
        if (!confirm('Warning!\n\nNo key provided, only encode using base64.\n\nContinue?')) {
            return;
        };
    };
    if ($('#online').prop('checked')) {
        waiting();
        $.post('do', {
            mode: 'encrypt',
            key: key,
            content: $('#unencrypted').val(),
        }, function (data) {
            if (data.result != null) {
                $('#encrypted').val(data.result);
            } else {
                alert('Unknow error!');
            };
        }, 'json').fail(function () {
            alert('Network error!');
        }).always(function () {
            waiting(false);
        });
    } else {
        try {
            waiting();
            encrypt();
        } catch (e) {
            alert('Error!\n\n' + e.message);
        } finally {
            waiting(false);
        };
    };
};

function doDecrypt() {
    if ($('#encrypted').val() == '') {
        alert('Empty encrypted text!');
        return false;
    };
    if ($('#online').prop('checked')) {
        waiting();
        $.post('do', {
            mode: 'decrypt',
            key: $('#key').val().trim(),
            content: $('#encrypted').val(),
        }, function (data) {
            if (data.result != null) {
                $('#unencrypted').val(data.result);
            } else {
                alert('Incorrect key or malformed encrypted text!');
            };
        }, 'json').fail(function () {
            alert('Network error!');
        }).always(function () {
            waiting(false);
        });
    } else {
        try {
            waiting();
            decrypt();
        } catch (e) {
            alert('Incorrect key or malformed encrypted text!\n\n' + e.message);
        } finally { 
            waiting(false);
        };
    };
};

concat = sjcl.bitArray.concat;
base64 = sjcl.codec.base64

function encrypt() {
    var key = $('#key').val().trim();
    var content = $('#unencrypted').val();
    if (key == '') {
        $('#encrypted').val(btoa(unescape(encodeURIComponent(content))).replace(/=/g, ''));
        return;
    };
    sjcl.misc.pa = {};
    var plaintext = zlib(content);
    var data = sjcl.json.ja(key, plaintext.content);
    $('#encrypted').val(base64.fromBits(concat(concat(data.salt, data.iv), concat(data.ct, plaintext.compression))).replace(/=/g, ''));
};

function decrypt() {
    var key = $('#key').val().trim();
    if (key == '') {
        $('#unencrypted').val(decodeURIComponent(escape(atob($('#encrypted').val()))));
        return;
    };
    var cipher = BitsToUint8Array(base64.toBits($('#encrypted').val()));
    var data = {};
    data.salt = Uint8ArrayToBits(cipher.slice(0, 8));
    data.iv = Uint8ArrayToBits(cipher.slice(8, 24));
    data.ct = Uint8ArrayToBits(cipher.slice(24, cipher.length - 1));
    if (new TextDecoder().decode(cipher.slice(cipher.length - 1, cipher.length)) == 1) {
        $('#unencrypted').val(zlib(sjcl.json.ia(key, data, { raw: 1 })));
    } else {
        $('#unencrypted').val(sjcl.json.ia(key, data));
    }
};

function zlib(obj) {
    if (typeof obj == 'string') {
        var uint8array = new TextEncoder().encode(obj);
        var deflate = new Zlib.Deflate(uint8array).compress();
        if (uint8array.length > deflate.length) {
            return { content: Uint8ArrayToBits(deflate), compression: sjcl.codec.utf8String.toBits(1) };
        } else {
            return { content: Uint8ArrayToBits(uint8array), compression: sjcl.codec.utf8String.toBits(0) };
        };
    } else {
        var uint8array = BitsToUint8Array(obj);
        var inflate = new Zlib.Inflate(uint8array).decompress();
        return new TextDecoder().decode(inflate);
    };
};

function Uint8ArrayToBits(uint8array) {
    var hex = '';
    for (var i = 0; i < uint8array.length; i++) {
        hex += (uint8array[i] + 0xF00).toString(16).substr(1);
    };
    return sjcl.codec.hex.toBits(hex);
};

function BitsToUint8Array(bits) {
    var array = [], hex = sjcl.codec.hex.fromBits(bits);
    for (var i = 0; i < hex.length; i += 2) {
        array.push(parseInt(hex.substr(i, 2), 16));
    };
    return new Uint8Array(array);
};
