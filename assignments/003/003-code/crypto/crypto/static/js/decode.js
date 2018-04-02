$(function() {
	$(document).on('click', '[name="evaloption"]', function(event) {
		if ($(event.target).val() == "local") {
			$('#remote_submit').hide();
			$('#local_submit').show();
		}
		else {
			$('#remote_submit').show();
			$('#local_submit').hide();
		}
	});

	$(document).on('click', '#local_submit', function(event) {
		var msg = $('[name="msg"]').val().split("");
		var key = $('[name="key"]').val().split("");

		for (var i = 0; i < msg.length; i++) {
			if (i > 0 && i % key.length == 0) {
				key.reverse();
			}

			let k = key[i % key.length].charCodeAt(0);

			let kVal = 0;

			if (k >= 97 && k <= 122) {
				kVal = k - 97;
			} else if (k >= 65 && k <= 90) {
				kVal = k - 65;
			}

			let m = msg[i].charCodeAt(0);

			if (m >= 65 && m <= 90) {
				msg[i] = String.fromCharCode(65 + (m - kVal - 65) % 26);
			}
			else if (m >= 97 && m <= 122) {
				msg[i] = String.fromCharCode(97 + (m - kVal - 97) % 26);
			}
		}

		var plaintext = msg.join("");

		console.log(plaintext);

		$('#local_result').text(plaintext);
		$('#local_result').show();
	});
});