const buttons=document.querySelectorAll('[data-lang]');
const menu=document.querySelector('.menu');
const links=document.querySelector('.links');
let lang=localStorage.getItem('streamverse-language')||(navigator.language.startsWith('es')?'es':'en');
function setLanguage(next){lang=next==='es'?'es':'en';document.documentElement.lang=lang;document.querySelectorAll('[data-en][data-es]').forEach(el=>{el.textContent=el.dataset[lang]});buttons.forEach(btn=>{const active=btn.dataset.lang===lang;btn.classList.toggle('active',active);btn.setAttribute('aria-pressed',active)});const title=document.querySelector('[data-title-en]');if(title)document.title=title.dataset['title'+(lang==='es'?'Es':'En')];localStorage.setItem('streamverse-language',lang)}
buttons.forEach(btn=>btn.addEventListener('click',()=>setLanguage(btn.dataset.lang)));
if(menu){menu.addEventListener('click',()=>{const open=links.classList.toggle('open');menu.textContent=open?'×':'☰';menu.setAttribute('aria-expanded',open)});links.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{links.classList.remove('open');menu.textContent='☰'}))}
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
document.querySelectorAll('[data-demo-form]').forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();alert(lang==='es'?'Formulario listo para conectar con tu servicio de correo.':'Form ready to connect to your email service.')}));
setLanguage(lang);
