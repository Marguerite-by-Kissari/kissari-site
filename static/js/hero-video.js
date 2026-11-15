/* M07: supplied play artwork is a real control; native video controls remain available. */
const video = document.getElementById('hero-presentation');
const playButton = document.querySelector('.hero-media-badge');
const status = document.querySelector('.hero-video-status');
if (video && playButton) {
  const syncLabel = () => {
    playButton.setAttribute('aria-label', video.paused
      ? 'Lire la vidéo de présentation de KISSARI'
      : 'Mettre en pause la vidéo de présentation de KISSARI');
  };
  playButton.addEventListener('click', async () => {
    if (status) status.hidden = true;
    try {
      if (video.paused) await video.play();
      else video.pause();
    } catch {
      if (status) status.hidden = false;
    }
    syncLabel();
  });
  video.addEventListener('play', syncLabel);
  video.addEventListener('pause', syncLabel);
  video.addEventListener('ended', syncLabel);
}
