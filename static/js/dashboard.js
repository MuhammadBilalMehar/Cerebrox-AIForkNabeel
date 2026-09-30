// Animates bar-fill widths in from 0 on load (purely cosmetic).
document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.bar-fill[data-w]').forEach(b=>{
    requestAnimationFrame(()=> b.style.width = b.dataset.w + '%');
  });
});
