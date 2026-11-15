/* Return to the reading line, not the shifted box of its superscript marker. */
(() => {
  const readingLineRect = (call) => {
    const block = call.closest('p, li, .article-callout__body') || call.parentElement;
    const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
    let node;
    let previous;
    while ((node = walker.nextNode())) {
      if (call.contains(node)) break;
      if (node.textContent.trim()) previous = node;
    }
    if (!previous) return call.getBoundingClientRect();
    const end = previous.textContent.trimEnd().length;
    const range = document.createRange();
    range.setStart(previous, end - 1);
    range.setEnd(previous, end);
    return range.getBoundingClientRect();
  };

  document.addEventListener('click', (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest?.('.footnote-backref, .footnote-number');
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin || url.pathname !== location.pathname) return;
    const call = document.getElementById(decodeURIComponent(url.hash.slice(1)));
    if (!call?.matches('sup[id^="fnref"]')) return;
    const line = readingLineRect(call);
    const header = document.querySelector('.site-header');
    const headerBottom = Math.max(0, header?.getBoundingClientRect().bottom || 0);
    const top = Math.max(0, window.scrollY + line.top - headerBottom - 16);
    event.preventDefault();
    if (location.hash !== url.hash) history.pushState(null, '', url.hash);
    call.focus({preventScroll: true});
    window.scrollTo({top, behavior: 'instant'});
  });
})();
