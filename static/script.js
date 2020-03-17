function Copy() {
    var textarea = $('#' + $("input[name='text']:checked").val());
    textarea.select();
    document.execCommand('Copy');
    textarea[0].setSelectionRange(textarea.val().length, textarea.val().length);
    $('#copy').focus();
    if (textarea.val() !== '') {
        alert('Text has been copied to clipboard.');
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

concat = sjcl.bitArray.concat;

function encrypt() {
    var key = $('#key').val().trim();
    var plaintext = $('#unencrypted').val();
    if (key == '') {
        if (confirm('Warning!\n\nNo key provided, only encode using base64.\n\nContinue?')) {
            $('#encrypted').val(btoa(unescape(encodeURIComponent(plaintext))).replace(/=/g, ''));
        };
        return;
    };
    sjcl.misc.pa = {};
    var content = zlib(plaintext)
    var data = sjcl.json.ja(key, content.content);
    $('#encrypted').val(base64(concat(concat(data.salt, data.iv), concat(data.ct, content.compression))).replace(/=/g, ''));
};

function decrypt() {
    var key = $('#key').val().trim();
    if (key == '') {
        $('#unencrypted').val(decodeURIComponent(escape(atob($('#encrypted').val()))));
        return;
    };
    var cipher = BitsToUint8Array(base64($('#encrypted').val(), encode = false));
    var data = {}
    data.ct = Uint8ArrayToBits(cipher.slice(24, cipher.length - 1))
    data.salt = Uint8ArrayToBits(cipher.slice(0, 8))
    data.iv = Uint8ArrayToBits(cipher.slice(8, 24))
    if (Uint8ArrayToString(cipher.slice(cipher.length - 1, cipher.length)) == 1) {
        $('#unencrypted').val(zlib(sjcl.json.ia(key, data, { raw: 1 }), compress = false));
    } else {
        $('#unencrypted').val(sjcl.json.ia(key, data));
    }
};

function zlib(obj, compress = true) {
    if (compress) {
        var uint8Array = StringToUint8Array(obj);
        var deflate = new Zlib.Deflate(uint8Array).compress();
        if (uint8Array.length > deflate.length) {
            return { content: Uint8ArrayToBits(deflate), compression: sjcl.codec.utf8String.toBits(1) };
        } else {
            return { content: Uint8ArrayToBits(uint8Array), compression: sjcl.codec.utf8String.toBits(0) };
        };
    } else {
        var uint8Array = BitsToUint8Array(obj);
        var inflate = new Zlib.Inflate(uint8Array).decompress();
        return Uint8ArrayToString(inflate);
    };
};

function base64(obj, encode = true) {
    if (encode) {
        return sjcl.codec.base64.fromBits(obj);
    } else {
        return sjcl.codec.base64.toBits(obj);
    };
};

function Uint8ArrayToBits(array) {
    var hex = '', i;
    for (i = 0; i < array.length; i++) {
        hex += ((array[i] | 0) + 0xF00).toString(16).substr(1);
    };
    return sjcl.codec.hex.toBits(hex);
};

function BitsToUint8Array(bitArray) {
    hex = sjcl.codec.hex.fromBits(bitArray);
    var array = [], i;
    for (i = 0; i < hex.length; i += 2) {
        array.push(parseInt(hex.substr(i, 2), 16));
    };
    return array;
};

function StringToUint8Array(e) {
    var a = []
        , d = 0;
    for (var b = 0; b < e.length; b++) {
        var f = e.charCodeAt(b);
        if (f < 128) {
            a[d++] = f
        } else {
            if (f < 2048) {
                a[d++] = (f >> 6) | 192;
                a[d++] = (f & 63) | 128
            } else {
                if (((f & 64512) == 55296) && (b + 1) < e.length && ((e.charCodeAt(b + 1) & 64512) == 56320)) {
                    f = 65536 + ((f & 1023) << 10) + (e.charCodeAt(++b) & 1023);
                    a[d++] = (f >> 18) | 240;
                    a[d++] = ((f >> 12) & 63) | 128;
                    a[d++] = ((f >> 6) & 63) | 128;
                    a[d++] = (f & 63) | 128
                } else {
                    a[d++] = (f >> 12) | 224;
                    a[d++] = ((f >> 6) & 63) | 128;
                    a[d++] = (f & 63) | 128
                }
            }
        }
    }
    return a
};

function Uint8ArrayToString(j) {
    var e = []
        , h = 0
        , g = 0;
    while (h < j.length) {
        var f = j[h++];
        if (f < 0) {
            f += 256
        }
        if (f < 128) {
            e[g++] = String.fromCharCode(f)
        } else {
            if (f > 191 && f < 224) {
                var d = j[h++];
                e[g++] = String.fromCharCode((f & 31) << 6 | d & 63)
            } else {
                if (f > 239 && f < 365) {
                    var d = j[h++];
                    var b = j[h++];
                    var a = j[h++];
                    var i = ((f & 7) << 18 | (d & 63) << 12 | (b & 63) << 6 | a & 63) - 65536;
                    e[g++] = String.fromCharCode(55296 + (i >> 10));
                    e[g++] = String.fromCharCode(56320 + (i & 1023))
                } else {
                    var d = j[h++];
                    var b = j[h++];
                    e[g++] = String.fromCharCode((f & 15) << 12 | (d & 63) << 6 | b & 63)
                }
            }
        }
    }
    return e.join('')
};
