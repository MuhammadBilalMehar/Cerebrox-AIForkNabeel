// Client-side password strength hint on the register page (server still
// enforces real validation via Django's password validators).
function pwMeter(input, textId){
  const v = input.value;
  let n = 0;
  if (v.length >= 8) n++;
  if (/[A-Z]/.test(v)) n++;
  if (/[0-9]/.test(v)) n++;
  if (/[^A-Za-z0-9]/.test(v)) n++;
  const words = ['Too short','Getting there','Good','Strong'];
  const text = document.getElementById(textId);
  if (text) text.textContent = v ? words[Math.max(0,n-1)] : 'Use 8+ characters with a number.';
}
