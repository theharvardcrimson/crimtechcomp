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
		val = key.charCodeAt(counter) - 64;
    
		if (msg.charCodeAt(i) >= 97 && msg.charCodeAt(i) <= 122) {     
			x += String.fromCharCode((Math.abs(msg.charCodeAt(i) - 97 + val) % 26 + 97));
		}
		else if (msg.charCodeAt(i) >= 65 && msg.charCodeAt(i) <= 90) {
			x += String.fromCharCode((Math.abs(msg.charCodeAt(i) - 65 + val) % 26 + 65));
		}
		else {
			x += msg[i];
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
  
		val = key.charCodeAt(counter) - 64;
    
		if (msg.charCodeAt(i) >= 97 && msg.charCodeAt(i) <= 122) {     
			x += String.fromCharCode((Math.abs(msg.charCodeAt(i) - 97 - val) % 26 + 97));
		}
		else if (msg.charCodeAt(i) >= 65 && msg.charCodeAt(i) <= 90) {
			x += String.fromCharCode((Math.abs(msg.charCodeAt(i) - 65 - val) % 26 + 65));
		}
		else {
			x += msg[i];
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