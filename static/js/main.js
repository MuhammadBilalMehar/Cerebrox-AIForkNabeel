// theme toggle + small global UI behaviours (kept deliberately light —
// all real logic lives server-side in Django views)
const THEME_KEY = 'cerebrox-theme';
function applyTheme(t){
  document.documentElement.setAttribute('data-theme', t);
  try { localStorage.setItem(THEME_KEY, t); } catch(e){}
}
document.addEventListener('click', e=>{
  if (e.target.closest('[data-theme-toggle]')) {
    const cur = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    applyTheme(cur);
  }
});
(function initTheme(){
  let saved = null;
  try { saved = localStorage.getItem(THEME_KEY); } catch(e){}
  if (saved) applyTheme(saved);
})();
