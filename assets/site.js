const buttons=document.querySelectorAll('[data-lang]');
const menu=document.querySelector('.menu');
const links=document.querySelector('.links');
let lang=localStorage.getItem('streamverse-language')||(navigator.language.startsWith('es')?'es':'en');
function setLanguage(next){lang=next==='es'?'es':'en';document.documentElement.lang=lang;document.querySelectorAll('[data-en][data-es]').forEach(el=>{el.textContent=el.dataset[lang]});buttons.forEach(btn=>{const active=btn.dataset.lang===lang;btn.classList.toggle('active',active);btn.setAttribute('aria-pressed',active)});const title=document.querySelector('[data-title-en]');if(title)document.title=title.dataset['title'+(lang==='es'?'Es':'En')];localStorage.setItem('streamverse-language',lang)}
buttons.forEach(btn=>btn.addEventListener('click',()=>setLanguage(btn.dataset.lang)));
if(menu){menu.addEventListener('click',()=>{const open=links.classList.toggle('open');menu.textContent=open?'×':'☰';menu.setAttribute('aria-expanded',open)});links.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{links.classList.remove('open');menu.textContent='☰'}))}

const normalizePath=path=>{let cleaned=path.replace(/\/$/, '')||'/';if(cleaned==='/index.html')cleaned='/';if(cleaned.endsWith('/index.html'))cleaned=cleaned.replace(/\/index\.html$/,'');return cleaned};
const currentPath=normalizePath(window.location.pathname);
document.querySelectorAll('.links a').forEach(link=>{const linkPath=normalizePath(new URL(link.href,window.location.origin).pathname);const isNewsLink=linkPath==='/news'&&currentPath.startsWith('/news');if(linkPath===currentPath||isNewsLink){link.classList.add('active');link.setAttribute('aria-current','page')}});

document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
document.querySelectorAll('[data-demo-form]').forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();alert(lang==='es'?'Formulario listo para conectar con tu servicio de correo.':'Form ready to connect to your email service.')}));

setLanguage(lang);

// Inject a homepage-only nav link to the IPVanish landing page if not present
(function(){
	try{
		const links = document.querySelector('.links');
		if(!links) return;
		const has = Array.from(links.querySelectorAll('a')).some(a=>a.getAttribute('href')==='ipvanish.html');
		const cleaned = normalizePath(window.location.pathname);
		const isIndex = cleaned === '/';
		if(!has && isIndex){
			const li = document.createElement('li');
			const a = document.createElement('a');
			a.setAttribute('href','ipvanish.html');
			a.dataset.en = 'IPVanish';
			a.dataset.es = 'IPVanish';
			a.textContent = 'IPVanish';
			li.appendChild(a);
			// insert before About/Contact if possible, otherwise append
			const aboutIdx = Array.from(links.children).findIndex(ch=>ch.textContent.trim().toLowerCase()==='about');
			if(aboutIdx> -1) links.insertBefore(li, links.children[aboutIdx]); else links.appendChild(li);
		}
	}catch(e){}
})();
