"""Encryption for the private sponsor page.

The repo is public, so the sponsor deck is never committed in plain text:
  src/sponsors.html       plain-text source (gitignored, lives only on your machine)
  src/sponsors.html.enc   the same source, encrypted (committed)
  public/sponsors.html    a password page that decrypts the deck in the browser (committed)

Everything is AES-256-GCM with a key derived from the password by PBKDF2-SHA256,
which the browser's Web Crypto can undo. Set SPONSOR_PASSWORD before building.
"""
import base64, json, os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 600_000
b64 = lambda b: base64.b64encode(b).decode()


def _key(password, salt, iterations=ITERATIONS):
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations).derive(password.encode())


def seal(text, password):
    salt, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(_key(password, salt)).encrypt(iv, text.encode(), None)
    return {'v': 1, 'iter': ITERATIONS, 'salt': b64(salt), 'iv': b64(iv), 'ct': b64(ct)}


def unseal(blob, password):
    d = lambda k: base64.b64decode(blob[k])
    return AESGCM(_key(password, d('salt'), blob['iter'])).decrypt(d('iv'), d('ct'), None).decode()


def gate_page(blob):
    """A self-contained page: password form, then decrypt and swap in the deck."""
    return GATE.replace('/*BLOB*/null', json.dumps(blob, separators=(',', ':')))


GATE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Sponsors · BROKEN with Dr. G</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0B0B0B">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap">
<style>
:root{--ink:#0B0B0B;--bone:#F1ECE3;--mute:#9B968C;color-scheme:dark}
*{box-sizing:border-box}html,body{margin:0;background:var(--ink);color:var(--bone)}
body{font-family:Archivo,"Helvetica Neue",Arial,sans-serif;min-height:100vh;min-height:100dvh;display:grid;place-items:center;padding:24px 16px;-webkit-font-smoothing:antialiased}
main{width:min(100%,460px);display:grid;gap:22px}
.label{font-weight:600;font-size:.82rem;letter-spacing:.26em;text-transform:uppercase;color:var(--mute);margin:0}
h1{font-style:italic;font-weight:900;font-stretch:62%;text-transform:uppercase;line-height:.9;font-size:clamp(2.6rem,9vw,4rem);margin:0}
p{margin:0;line-height:1.55}
form{display:grid;gap:12px;margin-top:6px}
input{font:inherit;font-size:1.05rem;color:var(--bone);background:transparent;border:0;border-bottom:2px solid var(--bone);padding:12px 2px;border-radius:0}
input:focus{outline:none;box-shadow:0 2px 0 var(--bone)}
button{justify-self:start;font-family:inherit;font-style:italic;font-weight:900;font-stretch:75%;text-transform:uppercase;letter-spacing:.02em;font-size:1.05rem;line-height:1;padding:.75em 1.5em;background:var(--bone);color:var(--ink);border:0;cursor:pointer;clip-path:polygon(4% 0,100% 0,96% 100%,0 100%)}
button[disabled]{opacity:.6;cursor:progress}
:focus-visible{outline:2px solid var(--bone);outline-offset:3px}
.msg{color:var(--bone);font-weight:600;min-height:1.55em}
a{color:var(--bone)}
</style></head>
<body><main>
<p class="label">Sponsors · Private</p>
<h1>Different sports.<br>Same scars.</h1>
<p>The Season One sponsor deck. Enter the password you were given.</p>
<form id="f">
<label class="label" for="pw">Password</label>
<input id="pw" name="password" type="password" autocomplete="current-password" required autofocus>
<p class="msg" id="msg" role="alert"></p>
<button type="submit" id="go">Open the deck</button>
</form>
<noscript><p class="msg">This page needs JavaScript to unlock.</p></noscript>
<p class="label">No password? <a href="https://ig.me/m/brokenwithdrg">DM @brokenwithdrg</a></p>
</main>
<script>
(function () {
  var BLOB = /*BLOB*/null, KEY = 'bwdg-sponsor-pw';
  var bytes = function (s) { return Uint8Array.from(atob(s), function (c) { return c.charCodeAt(0); }); };
  function unlock(pw) {
    var enc = new TextEncoder();
    return crypto.subtle.importKey('raw', enc.encode(pw), 'PBKDF2', false, ['deriveKey'])
      .then(function (base) {
        return crypto.subtle.deriveKey({ name: 'PBKDF2', salt: bytes(BLOB.salt), iterations: BLOB.iter, hash: 'SHA-256' },
          base, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
      })
      .then(function (key) { return crypto.subtle.decrypt({ name: 'AES-GCM', iv: bytes(BLOB.iv) }, key, bytes(BLOB.ct)); })
      .then(function (buf) { return new TextDecoder().decode(buf); });
  }
  function show(html, pw) {
    try { localStorage.setItem(KEY, pw); } catch (e) {}
    document.open(); document.write(html); document.close();
  }
  var f = document.getElementById('f'), input = document.getElementById('pw'),
      msg = document.getElementById('msg'), go = document.getElementById('go');
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var pw = input.value; go.disabled = true; msg.textContent = 'Opening…';
    unlock(pw).then(function (html) { show(html, pw); })
      .catch(function () { go.disabled = false; msg.textContent = 'That’s not it. Try again.'; input.select(); });
  });
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (saved) {
    msg.textContent = 'Opening…';
    unlock(saved).then(function (html) { show(html, saved); })
      .catch(function () { msg.textContent = ''; try { localStorage.removeItem(KEY); } catch (e) {} });
  }
})();
</script>
</body></html>
'''
