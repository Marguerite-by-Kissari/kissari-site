/* Disclosure natif : reste utilisable au clic / clavier sans JavaScript.
   Le survol n'envoie rien et ne charge aucun service tiers. */
(() => {
  'use strict';
  const info = document.querySelector('#contact-privacy-info');
  if (!info) return;
  const trigger = info.querySelector('summary');
  let pinned = false;
  let timer;
  const cancel = () => clearTimeout(timer);
  const close = () => { cancel(); pinned = false; info.open = false; };
  info.addEventListener('pointerenter', (event) => {
    cancel();
    if (event.pointerType === 'mouse') info.open = true;
  });
  info.addEventListener('pointerleave', () => {
    cancel();
    if (!pinned) timer = setTimeout(() => {
      if (!info.matches(':hover') && !info.contains(document.activeElement)) close();
    }, 200);
  });
  trigger.addEventListener('click', (event) => {
    event.preventDefault();
    cancel();
    pinned = !pinned;
    info.open = pinned;
  });
  info.addEventListener('focusout', () => {
    setTimeout(() => {
      if (!pinned && !info.contains(document.activeElement) && !info.matches(':hover')) close();
    }, 0);
  });
  document.addEventListener('pointerdown', (event) => {
    if (!info.contains(event.target)) close();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && info.open) {
      event.preventDefault();
      if (info.contains(document.activeElement)) trigger.focus();
      close();
    }
  });
})();
