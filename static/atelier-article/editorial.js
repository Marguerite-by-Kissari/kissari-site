/* M15: isolated global state, no article writes and no publication API. */
(() => {
  'use strict';
  const $=s=>document.querySelector(s), key='kissari-blog-editorial-draft-v1';
  const clone=o=>JSON.parse(JSON.stringify(o));
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fields=['title','enabled','article_paths'];
  let catalogue,base,working,pending;
  const status=(text,error=false)=>{const e=$('#m15-status');e.textContent=text;e.classList.toggle('error',error);};
  const normalized=()=>({...working,title:working.title.trim()});
  const dirty=()=>base&&fields.some(k=>JSON.stringify(normalized()[k])!==JSON.stringify(base[k]));
  function validateConfig(c){
    if(!c||c.schema_version!==1||Object.keys(c).sort().join('|')!=='article_paths|enabled|schema_version|title')throw Error('Configuration ou version inconnue.');
    if(typeof c.title!=='string'||/[\r\n]/.test(c.title)||![...c.title.trim()].length||[...c.title.trim()].length>100)throw Error('Titre : 1 à 100 caractères, sur une ligne.');
    if(typeof c.enabled!=='boolean'||!Array.isArray(c.article_paths)||c.article_paths.length>100||new Set(c.article_paths).size!==c.article_paths.length)throw Error('Sélection ou état d’affichage invalide.');
    for(const p of c.article_paths){if(typeof p!=='string'||!p.startsWith('/blog/')||!p.endsWith('/')||/[?#\\]/.test(p)||p.includes('//')||decodeURIComponent(p).split('/').some(x=>x==='.'||x==='..'))throw Error('Adresse d’article invalide.');}
    return {...clone(c),title:c.title.trim()};
  }
  function validateCatalogue(c){
    if(!c||c.schema_version!==1||typeof c.generated_at!=='string'||!Array.isArray(c.articles)||!/^\w{64}$/.test(c.base_config_sha256)||!/^[a-f0-9]{64}$/.test(c.base_config_sha256))throw Error('Fichier d’état du blog invalide.');
    validateConfig(c.config);
    const paths=new Set();
    for(const a of c.articles){if(!a||typeof a.title!=='string'||typeof a.path!=='string'||paths.has(a.path))throw Error('Catalogue d’articles invalide.');validateConfig({schema_version:1,title:'Validation',enabled:true,article_paths:[a.path]});paths.add(a.path);}
    return c;
  }
  function load(c,source){
    validateCatalogue(c);catalogue=clone(c);base=validateConfig(c.config);working=clone(base);pending=null;
    $('#m15-pending').hidden=true;$('#m15-source').textContent=`${source} · Génération : ${c.generated_at} · ${c.articles.length} articles publiables · Référence ${c.base_config_sha256.slice(0,12)}…`;
    $('#m15-title').value=working.title;$('#m15-enabled').checked=working.enabled;
    render();
  }
  function validTitle(){const n=[...working.title.trim()].length;const ok=n>=1&&n<=100&&!/[\r\n]/.test(working.title);$('#m15-counter').textContent=`${n} / 100 caractères${ok?'':' — titre à corriger'}`;$('#m15-counter').classList.toggle('is-invalid',!ok);$('#m15-title').setAttribute('aria-invalid',String(!ok));return ok;}
  function available(){
    const query=$('#m15-search').value.trim().toLocaleLowerCase();
    $('#m15-available').innerHTML=catalogue.articles.map((a,index)=>({a,index})).filter(({a})=>(a.title+' '+a.category).toLocaleLowerCase().includes(query)).map(({a,index})=>`<label class="m15-choice"><input type="checkbox" data-add="${index}" ${working.article_paths.includes(a.path)?'checked':''}><span>${esc(a.title)}<small>${esc(a.category)} · ${esc(a.date)}<br>${esc(a.path)}</small></span></label>`).join('')||'<p>Aucun article ne correspond à cette recherche.</p>';
  }
  function selected(){
    $('#m15-selected').innerHTML=working.article_paths.map((p,index)=>{const a=catalogue.articles.find(a=>a.path===p);return `<li><strong>${esc(a?.title||'Article indisponible : '+p)}</strong><div class="m15-order"><button type="button" data-action="up" data-index="${index}" ${index===0?'disabled':''} aria-label="Monter ${esc(a?.title||p)}">Monter</button><button type="button" data-action="down" data-index="${index}" ${index===working.article_paths.length-1?'disabled':''} aria-label="Descendre ${esc(a?.title||p)}">Descendre</button><button type="button" data-action="remove" data-index="${index}" aria-label="Retirer ${esc(a?.title||p)}">Retirer</button></div></li>`;}).join('')||'<li>Aucun article sélectionné. La rubrique sera masquée.</li>';
  }
  function preview(){
    validTitle();const articles=working.article_paths.map(p=>catalogue.articles.find(a=>a.path===p)).filter(Boolean);
    const show=working.enabled&&articles.length>0;
    $('#m15-preview-title').textContent=working.title.trim();$('#m15-preview-title').hidden=!show;
    $('#m15-preview-cards').innerHTML=show?articles.map(a=>`<article>${esc(a.title)}<small>${esc(a.category)} · ${esc(a.date)}</small></article>`).join(''):'';
    $('#m15-preview-empty').textContent=show?'Aperçu textuel : les images et styles des cartes sont vérifiables sur le blog après intégration.':(working.enabled?'La rubrique sera absente du blog : aucun article publiable sélectionné.':'La rubrique sera absente du blog : affichage désactivé.');
  }
  function render(){available();selected();preview();}
  function download(name,data){const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)+'\n'],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  function requestLoad(c,source){validateCatalogue(c);if(dirty()){pending={c,source};$('#m15-pending').hidden=false;status('État disponible ; vos modifications sont conservées.');}else{load(c,source);status('État chargé. Aucune publication.');}}
  async function refresh(){
    try{const r=await fetch('/blog/catalogue-editorial.json',{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);const c=await r.json();if(c.base_config_sha256!==catalogue.base_config_sha256||JSON.stringify(c.articles)!==JSON.stringify(catalogue.articles))requestLoad(c,'État du site (même origine)');else{$('#m15-source').textContent=`État du site (même origine) · Génération : ${c.generated_at} · ${c.articles.length} articles publiables · Référence ${c.base_config_sha256.slice(0,12)}…`;status('État actuel vérifié ; vos réglages locaux sont conservés.');}}
    catch(e){status('Chargement réseau impossible : instantané conservé. '+e.message,true);}
  }
  function tab(which,focus=false){const isRubric=which==='rubric';$('#article-panel').hidden=isRubric;$('#rubric-panel').hidden=!isRubric;for(const name of ['article','rubric']){const b=$('#tab-'+name);b.setAttribute('aria-selected',String(name===which));b.tabIndex=name===which?0:-1;}$('.topbar h1').textContent=isRubric?'Rubrique du blog':'Préparer un article';$('.topbar__hint').textContent=isRubric?'Réglages globaux. Export séparé. Aucune publication.':'Un dossier exporté. Un article prêt à intégrer.';if(focus)$('#tab-'+which).focus();}
  for(const name of ['article','rubric'])$('#tab-'+name).addEventListener('click',()=>tab(name));
  $('.m15-tabs').addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();tab(e.key==='Home'?'article':e.key==='End'?'rubric':$('#rubric-panel').hidden?'rubric':'article',true);}});
  $('#m15-title').addEventListener('input',e=>{working.title=e.target.value;preview();});
  $('#m15-enabled').addEventListener('change',e=>{working.enabled=e.target.checked;preview();});
  $('#m15-search').addEventListener('input',available);
  $('#m15-available').addEventListener('change',e=>{if(!e.target.matches('[data-add]'))return;const i=+e.target.dataset.add,p=catalogue.articles[i].path;if(e.target.checked){if(!working.article_paths.includes(p))working.article_paths.push(p);}else working.article_paths=working.article_paths.filter(x=>x!==p);render();$(`#m15-available [data-add="${i}"]`)?.focus();});
  $('#m15-selected').addEventListener('click',e=>{const b=e.target.closest('[data-action]');if(!b)return;const i=+b.dataset.index,action=b.dataset.action;let next=i;if(action==='remove'){working.article_paths.splice(i,1);next=Math.min(i,working.article_paths.length-1);}else{next=i+(action==='up'?-1:1);if(next<0||next>=working.article_paths.length)return;[working.article_paths[i],working.article_paths[next]]=[working.article_paths[next],working.article_paths[i]];}render();$(`#m15-selected [data-action="${action}"][data-index="${next}"]`)?.focus();});
  $('#m15-save').addEventListener('click',()=>{try{localStorage.setItem(key,JSON.stringify({catalogue,working}));$('#m15-saved-notice').hidden=false;status('Brouillon sauvegardé dans ce navigateur uniquement. Rien n’est publié.');}catch(e){status('Sauvegarde impossible : '+e.message,true);}});
  $('#m15-load').addEventListener('click',()=>{try{const raw=localStorage.getItem(key);if(!raw)throw Error('Aucun brouillon de rubrique trouvé.');const saved=JSON.parse(raw);validateCatalogue(saved.catalogue);if(typeof saved.working?.title!=='string')throw Error('Brouillon invalide.');validateConfig({...saved.working,title:'Brouillon'});if(dirty()&&!confirm('Remplacer les réglages en cours par le brouillon sauvegardé ?'))return;load(saved.catalogue,'Brouillon local — état de référence sauvegardé');working=clone(saved.working);$('#m15-title').value=working.title;$('#m15-enabled').checked=working.enabled;render();status('Brouillon rouvert. Un export basé sur un ancien état pourra être refusé à l’intégration.');}catch(e){status(e.message,true);}});
  $('#m15-use-current').addEventListener('click',()=>{if(pending&&confirm('Remplacer vos réglages locaux par cet état ?')){const p=pending;load(p.c,p.source);status('État chargé. Rien n’est publié.');}});
  $('#m15-refresh').addEventListener('click',refresh);
  $('#m15-download-state').addEventListener('click',()=>{download('kissari-etat-blog.json',catalogue);status('État de référence téléchargé ; il ne contient pas vos modifications locales non intégrées.');});
  $('#m15-import').addEventListener('change',async e=>{try{const f=e.target.files?.[0];if(!f)return;if(f.size>2*1024*1024)throw Error('Fichier trop volumineux.');requestLoad(JSON.parse(await f.text()),'État importé depuis '+f.name);}catch(err){status('Import refusé : '+err.message,true);}finally{e.target.value='';}});
  $('#m15-export').addEventListener('click',()=>{try{const c=validateConfig(working);const changes={};for(const k of fields)if(JSON.stringify(c[k])!==JSON.stringify(base[k]))changes[k]=c[k];if(!Object.keys(changes).length)throw Error('Aucune modification à exporter.');const missing=c.article_paths.filter(p=>!catalogue.articles.some(a=>a.path===p));if(missing.length&&changes.article_paths)throw Error('Retirez ou remplacez les références indisponibles.');download('kissari-reglages-rubrique-'+new Date().toISOString().slice(0,10)+'.json',{schema_version:1,base_config_sha256:catalogue.base_config_sha256,changes});status('Réglages exportés. À transmettre pour intégration ; rien n’est publié.'+(missing.length?' Références indisponibles conservées.':''));}catch(e){status(e.message,true);}});
  window.KISSARI_RUBRIC_TEST=()=>{const c=validateConfig(working),changes={};for(const k of fields)if(JSON.stringify(c[k])!==JSON.stringify(base[k]))changes[k]=c[k];if(!Object.keys(changes).length)changes.title=c.title;return {schema_version:1,base_config_sha256:catalogue.base_config_sha256,changes};};
  try{load(window.KISSARI_EDITORIAL_CATALOG,'Instantané embarqué');try{$('#m15-saved-notice').hidden=!localStorage.getItem(key);}catch{}if(location.protocol==='file:')document.querySelectorAll('.m15-online').forEach(e=>e.hidden=true);else refresh();tab(location.hash==='#article'?'article':'rubric');}catch(e){status('Initialisation refusée : '+e.message,true);}
})();
