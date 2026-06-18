document.addEventListener('DOMContentLoaded', function(){
  const input = document.getElementById('newsSearch');
  const grid = document.getElementById('newsGrid');
  if(!input || !grid) return;
  const cards = Array.from(grid.children);
  function filter(q){
    const term = q.trim().toLowerCase();
    cards.forEach(card=>{
      const t = (card.dataset.title||'') + ' ' + (card.dataset.source||'');
      const show = term === '' || t.indexOf(term) !== -1;
      card.style.display = show ? '' : 'none';
      if(show){ card.animate([{opacity:0,transform:'translateY(6px)'},{opacity:1,transform:'translateY(0)'}],{duration:220,fill:'both'}); }
    });
  }
  let timeout = null;
  input.addEventListener('input', (e)=>{
    clearTimeout(timeout);
    timeout = setTimeout(()=>filter(e.target.value),120);
  });
});
