alert( "ready!" );

// var isAlpha = function(ch){
//   return /^[A-Z]$/i.test(ch);
// }

// $('#message, #key').on('input propertychange paste', function() {
//   var msg = $("#message").val();
//   var key = $("#key").val();
//   var msgl = msg.length;
//   var keyl = key.length;
//   var res = "";
//   var counter = 0;
//   var forward = true;
//   for (i = 0; i < msgl; i++) {
//     var msgc = msg.charCodeAt(i) - (msg.charAt(i).toUpperCase() == msg.charAt(i) ? 65 : 97);
//     var keyc = key.charCodeAt(counter) - (ket.charAt(counter).toUpperCase() == key.charAt(counter) ? 64 : 96);
//     res += String.fromCharCode(isAlpha(msg.charAt(i)) ? (msgc + keyc) % 26 + 97 : msg.charAt(i));
//     counter += forward ? 1 : -1;
//     if (counter > keyl - 1) {
//       counter = keyl - 1;
//       forward = False;
//     }
//     else if (counter < 0) {
//       counter = 0;
//       forward = True;
//     }
//   }
//   $('#realtime').html(res);
// });

