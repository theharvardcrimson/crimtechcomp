function encode() {
    var box = document.getElementById("localBox")
    var key = document.getElementsByName("key")[0].value.toLowerCase()
    var text = document.getElementsByName("text")[0].value.toLowerCase()
    // Encrypting function
    var keyIndex = 0
    var forward = true
    var encoded = []
    for (var i = 0; i < text.length; i++) {
        if (String.charCodeAt(text.charAt(i)) >= String.charCodeAt('a') && String.charCodeAt(text.charAt(i)) <= String.charCodeAt('z')) {
            var t = String.charCodeAt(text.charAt(i)) - String.charCodeAt('a')
            var k = 0
            if (String.charCodeAt(key.charAt(keyIndex)) >= String.charCodeAt('a') && String.charCodeAt(key.charAt(keyIndex)) <= String.charCodeAt('z')) {
                k = String.charCodeAt(key.charAt(keyIndex)) - String.charCodeAt('a') + 1
            }
            else if (String.charCodeAt(key.charAt(keyIndex)) >= String.charCodeAt('0') && String.charCodeAt(key.charAt(keyIndex)) <= String.charCodeAt('9')) {
                k = String.charCodeAt(key.charAt(keyIndex)) - String.charCodeAt('0') + 10
            }
            encoded.push(String.fromCharCode((t + k) % 26 + String.charCodeAt('a')))
        }
        else {
            encoded.push(text.charAt(i))
        }
    }

        if (forward) {
            keyIndex += 1
        }
        else {
            keyIndex -= 1
        }
        if (keyIndex >= key.length) {
            forward = false
            keyIndex = key.length - 1
        }
        if (keyIndex <= -1) {
            forward = true
            keyIndex = 0
        }

    box.innerHTML = encoded.join('')
}

function decode() {
    var box = document.getElementById("localBox")
    var key = document.getElementsByName("key")[0].value.toLowerCase()
    var text = document.getElementsByName("text")[0].value.toLowerCase()
    // Encrypting function
    var keyIndex = 0
    var forward = true
    var decoded = []
    for (var i = 0; i < text.length; i++) {
        if (String.charCodeAt(text.charAt(i)) >= String.charCodeAt('a') && String.charCodeAt(text.charAt(i)) <= String.charCodeAt('z')) {
            var t = String.charCodeAt(text.charAt(i)) - String.charCodeAt('a')
            var k = 0
            if (String.charCodeAt(key.charAt(keyIndex)) >= String.charCodeAt('a') && String.charCodeAt(key.charAt(keyIndex)) <= String.charCodeAt('z')) {
                k = String.charCodeAt(key.charAt(keyIndex)) - String.charCodeAt('a') + 1
            }
            else if (String.charCodeAt(key.charAt(keyIndex)) >= String.charCodeAt('0') && String.charCodeAt(key.charAt(keyIndex)) <= String.charCodeAt('9')) {
                k = String.charCodeAt(key.charAt(keyIndex)) - String.charCodeAt('0') + 10
            }
            decoded.push(String.fromCharCode((t - k + 26) % 26 + String.charCodeAt('a')))
        }
        else {
            decoded.push(text.charAt(i))
        }
    }

        if (forward) {
            keyIndex += 1
        }
        else {
            keyIndex -= 1
        }
        if (keyIndex >= key.length) {
            forward = false
            keyIndex = key.length - 1
        }
        if (keyIndex <= -1) {
            forward = true
            keyIndex = 0
        }

    box.innerHTML = decoded.join('')
}
