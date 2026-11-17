/* Native button + ordinary navigation, not a modal or ARIA application menu.
   Without JS the mobile links stay visible and usable. */
(() => {
  const header = document.querySelector('.site-header');
  const button = header?.querySelector('.mobile-nav-toggle');
  const nav = header?.querySelector('#primary-navigation');
  if (!button || !nav) return;
  const mobile = window.matchMedia('(max-width: 799px)');
  const close = (returnFocus = false) => {
    header.dataset.menuOpen = 'false';
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-label', 'Ouvrir le menu');
    if (returnFocus && mobile.matches) button.focus();
  };
  button.hidden = false;
  close();
  header.dataset.mobileReady = 'true';
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    header.dataset.menuOpen = String(open);
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
  });
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) close();
  });
  document.addEventListener('click', (event) => {
    if (!header.contains(event.target)) close();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') close(true);
  });
  header.addEventListener('focusout', (event) => {
    if (event.relatedTarget && !header.contains(event.relatedTarget)) close();
  });
  mobile.addEventListener('change', () => close());
})();
