// Chaque catégorie possède son rail : pas de dépendance, pas de déplacement global.
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const behavior = () => (reducedMotion.matches ? "instant" : "smooth");
const refreshRails = [];

document.querySelectorAll(".blog-row").forEach((row) => {
  const track = row.querySelector(".blog-track");
  if (!track) return;
  const prev = row.querySelector("[data-prev]");
  const next = row.querySelector("[data-next]");
  const step = () =>
    (track.querySelector(".article-card")?.getBoundingClientRect().width ||
      track.clientWidth) + (parseFloat(getComputedStyle(track).columnGap) || 0);
  const update = () => {
    const end = track.scrollWidth - track.clientWidth;
    prev.disabled = track.scrollLeft <= 2;
    next.disabled = end <= 2 || track.scrollLeft >= end - 2;
  };
  const move = (direction) =>
    track.scrollBy({ left: direction * step(), behavior: behavior() });
  prev.addEventListener("click", () => move(-1));
  next.addEventListener("click", () => move(1));
  track.addEventListener("scroll", update, { passive: true });
  track.addEventListener("keydown", (event) => {
    if (event.target !== track) return;
    if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
      event.preventDefault();
      move(event.key === "ArrowRight" ? 1 : -1);
    } else if (event.key === "Home" || event.key === "End") {
      event.preventDefault();
      track.scrollTo({
        left: event.key === "Home" ? 0 : track.scrollWidth,
        behavior: behavior(),
      });
    }
  });
  new ResizeObserver(update).observe(track);
  refreshRails.push(update);
  update();
});

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach((item) => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    document.querySelectorAll(".blog-row").forEach((row) => {
      row.hidden = filter !== "all" && row.dataset.category !== filter;
    });
    refreshRails.forEach((update) => update());
    (filter === "all"
      ? document.querySelector(".blog-listing")
      : document.querySelector(`.blog-row[data-category="${filter}"]`)
    )?.scrollIntoView({ behavior: behavior(), block: "start" });
  });
});
