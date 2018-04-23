var alphabet = 'abcdefghijklmnopqrstuvwxzy';

function encode(msg, k) {

	var output = '';

	var counter = 0;

	var key = k;

	for (i in msg) {

		key += k[::-1] + k;
	}
	for (i in msg) {

		if (i.isdigit() == true) {

			output += i;
		}
			counter += 1;
	}
		} else if (i.isalpha() == false) {

			output += i;

			counter +=1;

		} else if (i.isalpha() == true) {

			if (msg.index(i) == 0) {

				output += alphabet[alphabet.index(i)+alphabet.index(key[counter])+1];
			}
				counter += 1;

			} else {

				if ((alphabet.index(i)+alphabet.index(key[msg.index(i)])+1) > 25) {

					output += alphabet[alphabet.index(i)+alphabet.index(key[msg.index(i)])-24];
				}
					counter += 1;

				} else {

					output += alphabet[alphabet.index(i)+alphabet.index(key[msg.index(i)])+1];

					counter += 1;

	return output;
}

function decode(msg, k) {

	var output = '';

	var counter = 0;

	var key = k;

	for (i in msg) {

		key += k[::-1] + k;
	}
	for (i in msg) {

		if (i.isdigit() == true) {

			output += i;
		}
			counter += 1;
	}
		} else if (i.isalpha() == false) {

			output += i;

			counter +=1;

		} else if (i.isalpha() == true) {

			if (msg.index(i) == 0) {

				output += alphabet[alphabet.index(i)-alphabet.index(key[counter])-1];
			}
				counter += 1;

			} else {

				if ((alphabet.index(i)-alphabet.index(key[msg.index(i)])-1) < 0) {

					output += alphabet[alphabet.index(i)-alphabet.index(key[msg.index(i)]) + 24];
				}
					counter += 1;

				} else {

					output += alphabet[alphabet.index(i)-alphabet.index(key[msg.index(i)])-1];

					counter += 1;

	return output;
}
