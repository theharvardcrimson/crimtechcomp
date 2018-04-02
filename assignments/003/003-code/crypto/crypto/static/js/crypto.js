var message, key, text;

$(document).ready(function() {
  $('#msg, #key').on('change paste keyup', function(){
    message = $('#msg').val();
    key = $('#key').val();
    if (window.location.pathname === '/encode/') {
      $('#local-text').text(code(message, key, "encode"));
    } else {
      $('#local-text').text(code(message, key, "decode"));
    }
  });
});

$(document).ready(function() {
    $('input[type=radio][name=optradio]').change(function() {
        if (this.value == 'false') {
            $('#local-text').css('display', 'none');
            $('#submit-btn').css('display', 'inherit');
        }
        else if (this.value == 'true') {
            $('#submit-btn').css('display', 'none');
            $('#local-text').css('display', 'inherit');
        }
    });
});

function code(msg, k, type) {
  const mod = (x, n) => (x % n + n) % n
  const ALPHABET_LENGTH = 26;
  const ORD_LOWER_A = 'a'.charCodeAt();

  var key_as_shift = Array.prototype.map.call(k, i => i.charCodeAt() - ORD_LOWER_A + 1);
  var res = "";
  var iterator = msg.split("").entries();

  for (let e of iterator) {
    if (e[1].match(/[a-z]/i)) {
      if (~~(e[0] / k.length) % 2 === 0) {
        var shift = key_as_shift[(e[0] % k.length)];
      }
      else {
        var shift_index = (-1 * ((e[0] % k.length) + 1));
        var shift = (shift_index === -1) ? key_as_shift.slice(-1)[0] : key_as_shift.slice(shift_index, shift_index + 1)[0];
      }
      type === "encode"
        ? res += String.fromCharCode(mod((e[1].charCodeAt() - ORD_LOWER_A + shift), ALPHABET_LENGTH) + ORD_LOWER_A)
        : res += String.fromCharCode(mod((e[1].charCodeAt() - ORD_LOWER_A - shift), ALPHABET_LENGTH) + ORD_LOWER_A);
    }
    else {
      res += e[1];
    }
  };

  return res
};
