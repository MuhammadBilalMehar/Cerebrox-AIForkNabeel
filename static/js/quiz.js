// Countdown timer for the quiz-taking page. The server is authoritative for
// scoring; this only warns the student and auto-submits on timeout.
function startQuizTimer(totalSeconds, formId){
  let left = totalSeconds;
  const el = document.getElementById('time');
  const timer = setInterval(()=>{
    left--;
    const m = String(Math.floor(left/60)).padStart(2,'0');
    const s = String(left%60).padStart(2,'0');
    if (el) el.textContent = `${m}:${s}`;
    if (left <= 60 && el) el.style.color = 'var(--bad)';
    if (left <= 0){
      clearInterval(timer);
      document.getElementById(formId)?.submit();
    }
  }, 1000);
}
