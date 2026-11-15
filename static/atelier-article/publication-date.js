/* Europe/Paris scheduling, including explicit DST gap/overlap rejection. */
(function(root){
  'use strict';
  function toISO(day,time){
    if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||!/^\d{2}:\d{2}$/.test(time))throw Error('Date ou heure invalide.');
    const [y,m,d]=day.split('-').map(Number),[h,min]=time.split(':').map(Number);
    if(y<2000||y>9998||h>23||min>59)throw Error('Date ou heure invalide.');
    const naive=Date.UTC(y,m-1,d,h,min),check=new Date(naive);
    if(check.toISOString().slice(0,10)!==day)throw Error('Date invalide.');
    const fmt=new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Paris',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'});
    const matches=[60,120].filter(offset=>{
      const parts=Object.fromEntries(fmt.formatToParts(new Date(naive-offset*60000)).map(p=>[p.type,p.value]));
      return `${parts.year}-${parts.month}-${parts.day}`===day&&`${parts.hour}:${parts.minute}`===time;
    });
    if(matches.length!==1)throw Error('Heure inexistante ou ambiguë lors du changement d’heure. Choisissez une autre heure.');
    return `${day}T${time}:00+${matches[0]===60?'01':'02'}:00`;
  }
  const api={toISO};
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.KissariPublication=api;
})(globalThis);
