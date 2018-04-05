$(document).ready(
	$('#local').click(function() {
   		if($('#local').is(':checked')) {
   			document.getElementById('submit').style.display = 'none';
			document.getElementById('local-res').style.display = 'inline-block';
   		}
   	}))
 
$(document).ready(
	$('#remote').click(function() {
   		if($('#remote').is(':checked')) {
   			document.getElementById('local-res').style.display = 'none';
			document.getElementById('submit').style.display = 'inline-block';
   		}
   	}))

$(document).ready(
	function() {
	    $('#key, #msg').keyup(
		    function() {
		        k = $('#key').val();
		        m = $('#msg').val();
		        if (window.location.pathname === '/encode/') {
		        	document.getElementById('local-res').innerHTML = encode(m, k);
		        }
		        else document.getElementById('local-res').innerHTML = decode(m, k);
		    });
	})

function encode(msg, key) {
	x = "";
	key = key.toUpperCase();
	counter = 0;

	for (i = 0; i < msg.length; i++) {
		val = key.charCodeAt(counter) - 'A'.charCodeAt() + 1;

		if (msg[i] == msg[i].toLowerCase()) {
			x += String.fromCharCode(((msg.charCodeAt(i) - 'a'.charCodeAt() + val) % 26) + 'a'.charCodeAt());
		}
		else if (msg[i] == msg[i].toUpperCase()) {
			x += String.fromCharCode(((msg.charCodeAt(i) - 'A'.charCodeAt() + val) % 26) + 'A'.charCodeAt());
		}
		else {
			x += msg[i]
		}

		if (counter == key.length - 1) {
	    	key = key.split("").reverse().join("");
			counter = 0;
		}
		else {
			counter += 1;
		}
	}
	return x;
}

function decode(msg, key) {
	x = "";
	key = key.toUpperCase();
	counter = 0;

	for (i = 0; i < msg.length; i++) {
		val = key.charCodeAt(counter) - 'A'.charCodeAt() + 1;

		if (msg[i] == msg[i].toLowerCase()) {
			x += String.fromCharCode(((msg.charCodeAt(i) - 'a'.charCodeAt() - val) % 26) + 'a'.charCodeAt());
		}
		else if (msg[i] == msg[i].toUpperCase()) {
			x += String.fromCharCode(((msg.charCodeAt(i) - 'A'.charCodeAt() - val) % 26) + 'A'.charCodeAt());
		}
		else {
			x += msg[i]
		}

		if (counter == key.length - 1) {
	    	key = key.split("").reverse().join("");
			counter = 0;
		}
		else {
			counter += 1;
		}
	}
	return x;
}