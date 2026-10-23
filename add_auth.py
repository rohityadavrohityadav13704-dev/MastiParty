from pathlib import Path

p = Path("www/index.html")
s = p.read_text()

old = '''<button onclick="toast('रजिस्ट्रेशन और सुरक्षित लॉगिन अभी सेट करना बाकी है।')">लॉगिन / रजिस्टर</button>'''
new = '''<button onclick="page('auth')">लॉगिन / रजिस्टर</button>'''
if old in s:
    s = s.replace(old, new, 1)

auth_section = """
<section id="auth">
<h2>🔐 MastiParty Login / Register</h2>
<div class="room">
<label>ईमेल</label>
<input id="authEmail" type="email" placeholder="अपना ईमेल लिखें"
style="width:100%;padding:13px;margin-top:8px;border-radius:10px;border:0">
<label style="display:block;margin-top:15px">पासवर्ड</label>
<input id="authPassword" type="password" placeholder="कम से कम 6 अक्षर"
style="width:100%;padding:13px;margin-top:8px;border-radius:10px;border:0">
<button onclick="registerUser()">नया अकाउंट बनाएँ</button>
<button onclick="loginUser()">लॉगिन करें</button>
<p id="authStatus">ईमेल और पासवर्ड से अकाउंट बनाएँ या लॉगिन करें।</p>
<button onclick="logoutUser()">लॉगआउट</button>
</div>
</section>
"""

if 'id="auth"' not in s:
    s = s.replace('<div class="bottom">', auth_section + '\\n<div class="bottom">', 1)

firebase_scripts = """
<script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js"></script>
"""
if 'firebase-app-compat.js' not in s:
    s = s.replace('<script>', firebase_scripts + '\\n<script>', 1)

firebase_code = """
const firebaseConfig = {
  apiKey: "AIzaSyCT9uKIpurWEwnI9OasaVDEvXIiB7P34B0",
  authDomain: "mastiparty-a7732.firebaseapp.com",
  projectId: "mastiparty-a7732",
  appId: "1:302990440757:web:52263bd2b22a2bc2b7f47c"
};
if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

function authMessage(msg) {
  const el = document.getElementById('authStatus');
  if (el) el.textContent = msg;
  else toast(msg);
}
function registerUser() {
  const email = document.getElementById('authEmail').value.trim();
  const password = document.getElementById('authPassword').value;
  if (!email || password.length < 6) {
    authMessage('सही ईमेल और कम से कम 6 अक्षर का पासवर्ड लिखें।');
    return;
  }
  auth.createUserWithEmailAndPassword(email, password)
    .then(() => authMessage('अकाउंट बन गया! आप लॉगिन हैं।'))
    .catch(e => authMessage('त्रुटि: ' + e.message));
}
function loginUser() {
  const email = document.getElementById('authEmail').value.trim();
  const password = document.getElementById('authPassword').value;
  auth.signInWithEmailAndPassword(email, password)
    .then(() => authMessage('लॉगिन सफल!'))
    .catch(e => authMessage('लॉगिन नहीं हुआ: ' + e.message));
}
function logoutUser() {
  auth.signOut()
    .then(() => authMessage('लॉगआउट हो गया।'))
    .catch(e => authMessage(e.message));
}
auth.onAuthStateChanged(user => {
  const status = document.getElementById('authStatus');
  if (status && user) status.textContent = 'लॉगिन: ' + user.email;
});
"""
if 'function registerUser()' not in s:
    s = s.replace('</script>', firebase_code + '\\n</script>', 1)

p.write_text(s)
print("Login/Register code added.")
