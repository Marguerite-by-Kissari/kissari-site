/* Same-origin connection to the loopback test service. Never applies or publishes. */
(() => {
  'use strict';
  const $=s=>document.querySelector(s),buttons=[...document.querySelectorAll('.m15-test-action')];
  let csrf='',busy=false;
  const result=$('#test-result'),message=$('#test-message'),checks=$('#test-checks'),links=$('#test-links');
  function plan(){
    const node=$('#publication-plan');if(!node)return;
    if($('#publication-status').value==='draft'){node.textContent='Brouillon : jamais publié automatiquement.';return;}
    try{const date=window.KissariPublication.toISO($('#publication-date').value,$('#publication-time').value||'09:00');
      node.textContent=(new Date(date).getTime()>Date.now()?'Programmé pour le ':'Publiable depuis le ')+$('#publication-date').value+' à '+($('#publication-time').value||'09:00')+' (Paris).';
    }catch(e){node.textContent='Choisissez une date et une heure valides : '+e.message;}
  }
  for(const id of ['publication-status','publication-date','publication-time'])$('#'+id).addEventListener('change',plan);
  $('#load').addEventListener('click',plan);plan();
  const encode=bytes=>{let out='';for(let i=0;i<bytes.length;i+=32768)out+=String.fromCharCode(...bytes.subarray(i,i+32768));return btoa(out);};
  async function run(kind){
    if(busy||!csrf)return;
    result.hidden=false;message.textContent='Préparation du test…';checks.replaceChildren();links.replaceChildren();
    result.focus();result.scrollIntoView({behavior:'smooth',block:'start'});
    busy=true;buttons.forEach(b=>b.disabled=true);result.setAttribute('aria-busy','true');
    try{
      let payload;
      if(kind==='rubric')payload={kind,patch:window.KISSARI_RUBRIC_TEST()};
      else{const bytes=window.KISSARI_ARTICLE_TEST();if(bytes.length>16*1024*1024)throw Error('ZIP limité à 16 Mio pour le test.');payload={kind,zip_base64:encode(bytes)};}
      message.textContent='Construction Hugo et contrôles dans une copie isolée… Rien n’est publié.';
      const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),180000);
      let response;
      try{response=await fetch('/api/test',{method:'POST',headers:{'Content-Type':'application/json','X-Atelier-CSRF':csrf},body:JSON.stringify(payload),signal:controller.signal});}
      finally{clearTimeout(timer);}
      const report=await response.json();
      if(!response.ok||report.status!=='success')throw Error(report.error||'Le test a échoué.');
      window.KISSARI_LAST_TEST_REPORT=report;
      message.textContent=report.message+(report.publication_state==='scheduled'?' Article futur : absence vérifiée dans le build public actuel, présence après échéance simulée.':report.publication_state==='draft'?' Le brouillon reste exclu du build public.':'');
      for(const item of report.checks){const li=document.createElement('li');li.textContent='✓ '+item.name;checks.append(li);}
      for(const [text,url] of [['Ouvrir la prévisualisation',report.preview_url],['Voir le blog de ce test',report.blog_url]]){
        const parsed=new URL(url);if(parsed.protocol!=='http:'||parsed.hostname!=='127.0.0.1')throw Error('Adresse de prévisualisation inattendue.');
        const a=document.createElement('a');a.textContent=text;a.href=url;a.target='_blank';a.rel='noopener';links.append(a);
      }
      const note=document.createElement('p');note.textContent='Rapport '+report.id+' · '+report.at;links.append(note);
    }catch(e){message.textContent='Test refusé ou interrompu — rien n’est publié. '+(e.name==='AbortError'?'Délai dépassé ; le service peut encore terminer le test.':e.message);}
    finally{busy=false;buttons.forEach(b=>b.disabled=!csrf);result.setAttribute('aria-busy','false');}
  }
  $('#m15-test').addEventListener('click',()=>run('rubric'));
  $('#article-test').addEventListener('click',()=>run('article'));
  async function connect(){
    const node=$('#test-service-status');
    if(location.protocol==='file:'){
      node.textContent='Édition hors ligne disponible. Le test Hugo nécessite l’atelier connecté : ';
      const a=document.createElement('a');a.href='http://127.0.0.1:1335/atelier-article/';a.textContent='Ouvrir l’atelier de test local';node.append(a);return;
    }
    try{const r=await fetch('/api/test-session',{cache:'no-store'});if(!r.ok)throw Error('Service absent');const s=await r.json();
      if(!s.csrf||!s.capabilities.includes('rubric')||!s.capabilities.includes('article'))throw Error('Service incompatible');
      csrf=s.csrf;buttons.forEach(b=>b.disabled=false);node.textContent='Service local connecté · Tests Hugo disponibles dans les deux onglets · Aucune publication.';
    }catch{node.textContent='Service de test indisponible. Démarrez scripts/serve-editorial-preview.py ; les sauvegardes et exports restent disponibles.';}
  }
  connect();
})();
