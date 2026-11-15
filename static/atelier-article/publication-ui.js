/* Publication uses a local connector; no key or token is stored in the browser. */
(() => {
 'use strict';
 const buttons=[];let csrf='',busy=false;
 const encode=bytes=>{let s='';for(let i=0;i<bytes.length;i+=32768)s+=String.fromCharCode(...bytes.subarray(i,i+32768));return btoa(s);};
 const status=document.createElement('p');status.id='publication-service-status';status.setAttribute('role','status');status.textContent='Publication : connexion au connecteur local…';
 document.querySelector('.m15-prototype').append(status);
 async function request(url,payload){const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json','X-Atelier-CSRF':csrf},body:JSON.stringify(payload)});const data=await r.json();if(!r.ok)throw Error(data.error||'Action refusée.');return data;}
 async function publish(kind){
  if(busy||!csrf)return;
  busy=true;buttons.forEach(b=>b.disabled=true);
  try{
   const payload=kind==='article'?{kind,zip_base64:encode(window.KISSARI_ARTICLE_TEST())}:{kind,patch:window.KISSARI_RUBRIC_TEST()};
   status.textContent='Préparation Git et vérification de la version distante…';
   const candidate=await request('/api/publication/prepare',payload);
   if(!confirm('Publier sur le site ?\n\nDépôt : Marguerite-by-Kissari/kissari-site\nBranche : main\nFichiers :\n'+candidate.files.join('\n')+'\n\nLa mise en ligne dépend des contrôles GitHub et de la date. Aucun accord webmaster ne sera demandé.')){status.textContent='Publication annulée. Aucun envoi sur GitHub.';return;}
   status.textContent='Envoi SSH de la version confirmée…';
   const receipt=await request('/api/publication/publish',{token:candidate.token});
   status.replaceChildren(document.createTextNode(receipt.message+' Révision '+receipt.commit.slice(0,12)+' · '));
   const a=document.createElement('a');a.href='https://github.com/Marguerite-by-Kissari/kissari-site/commit/'+receipt.commit;a.textContent='Voir le commit et ses contrôles GitHub';a.target='_blank';a.rel='noopener';status.append(a);
  }catch(e){status.textContent='Publication non confirmée : '+e.message+' Votre brouillon est conservé. En cas de coupure après envoi, vérifiez GitHub avant de réessayer.';}
  finally{busy=false;buttons.forEach(b=>b.disabled=!csrf);}
 }
 for(const [kind,anchor] of [['article','#article-test'],['rubric','#m15-test']]){
  const b=document.createElement('button');b.type='button';b.id=kind==='article'?'article-publish':'m15-publish';b.className='button button--primary m15-primary';b.textContent='Publier sur le site';b.disabled=true;b.addEventListener('click',()=>publish(kind));document.querySelector(anchor).after(b);buttons.push(b);
 }
 async function connect(){
  if(location.protocol==='file:'){status.textContent='Publier sur le site : utilisez le lanceur du package local pour connecter Git et votre clé SSH. Les exports restent disponibles hors ligne.';return;}
  try{const r=await fetch('/api/publication/session',{cache:'no-store'});if(!r.ok)throw Error('Connecteur absent');const s=await r.json();if(!s.csrf||!s.configured)throw Error('Profil à configurer avec le lanceur du package');csrf=s.csrf;buttons.forEach(b=>b.disabled=false);status.textContent='Publication connectée pour '+s.name+' · Dépôt unique · Confirmation requise avant chaque envoi.';}
  catch(e){status.textContent='Publication disponible avec le package connecté : '+e.message+'. Aucun envoi possible depuis cette session.';}
 }
 connect();
})();
