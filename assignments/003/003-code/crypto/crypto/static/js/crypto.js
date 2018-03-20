function encode(msg, k) {
  const ALPHABET_LENGTH = 26;
  const ORD_LOWER_A = 'a'.charCodeAt();

  var key_as_shift = Array.prototype.map.call(k, i => i.charCodeAt() - ORD_LOWER_A + 1);
  var ciphertext = "";
  var iterator = msg.split("").entries();

  for (let e of iterator) {
    if (e[1].match(/[a-z]/i)) {
      if (~~(e[0] / k.length) % 2 === 0) {
        var shift = key_as_shift[(e[0] % k.length)];
      }
      else {
        var shift_index = (-1 * ((e[0] % k.length) + 1));
        var shift = (shift_index === -1) ? key_as_shift.slice(-1) : key_as_shift.slice(shift_index, shift_index + 1);
      }
      ciphertext += String.fromCharCode(((e[1].charCodeAt() - ORD_LOWER_A + shift) % ALPHABET_LENGTH) + ORD_LOWER_A);
    }
    else {
      ciphertext += e[1];
    }
  };

  return ciphertext
};

function decode(msg, k) {
  const mod = (x, n) => (x % n + n) % n
  const ALPHABET_LENGTH = 26;
  const ORD_LOWER_A = 'a'.charCodeAt();

  var key_as_shift = Array.prototype.map.call(k, i => i.charCodeAt() - ORD_LOWER_A + 1);
  var plaintext = "";
  var iterator = msg.split("").entries();

  for (let e of iterator) {
    if (e[1].match(/[a-z]/i)) {
      if (~~(e[0] / k.length) % 2 === 0) {
        var shift = key_as_shift[(e[0] % k.length)];
      }
      else {
        var shift_index = (-1 * ((e[0] % k.length) + 1));
        var shift = (shift_index === -1) ? key_as_shift.slice(-1) : key_as_shift.slice(shift_index, shift_index + 1);
      }
      plaintext += String.fromCharCode(mod((e[1].charCodeAt() - ORD_LOWER_A - shift), ALPHABET_LENGTH) + ORD_LOWER_A);
    }
    else {
      plaintext += e[1];
    }
  };

  return plaintext
};

