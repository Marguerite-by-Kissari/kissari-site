/* First visual contact draft: no sending endpoint and no simulated delivery. */
(() => {
  'use strict';
  const wordCount = value => (String(value || '').trim().match(/\S+/gu) || []).length;
  if (typeof module === 'object' && module.exports) module.exports = { wordCount };
  if (typeof document === 'undefined') return;
  const form = document.querySelector('#contact-form');
  if (!form) return;
  const message = document.querySelector('#contact-message');
  const counter = document.querySelector('#contact-word-count');
  const status = document.querySelector('#contact-availability');
  const button = document.querySelector('#contact-send');
  function update() {
    const words = wordCount(message.value);
    counter.value = `${words} / 600 mots`;
    message.setCustomValidity(words > 600 ? 'Votre message dépasse 600 mots. Raccourcissez-le avant de continuer.' : '');
    if (words <= 600) message.removeAttribute('aria-invalid');
    return words;
  }
  message.addEventListener('input', update);
  form.addEventListener('submit', event => {
    event.preventDefault();
    update();
    if (!form.checkValidity()) {
      const invalid = form.querySelector(':invalid');
      if (invalid) { invalid.setAttribute('aria-invalid', 'true'); invalid.focus(); invalid.reportValidity(); }
      return;
    }
    status.textContent = 'Envoi non activé : aucun message n’a été envoyé. Votre texte est conservé. La configuration du service de contact reste à fournir.';
    status.classList.add('is-error');
    status.scrollIntoView({ block: 'nearest' });
  });
  form.addEventListener('invalid', event => event.target.setAttribute('aria-invalid', 'true'), true);
  form.addEventListener('input', event => { if (event.target.validity.valid) event.target.removeAttribute('aria-invalid'); });
  // Enable only after installing the guard; without JavaScript the submit stays disabled.
  button.disabled = false;
  update();
  if (new URLSearchParams(location.search).get('apercu') === 'confirmation') {
    form.hidden = true;
    document.querySelector('#contact-confirmation-preview').hidden = false;
  }
})();
