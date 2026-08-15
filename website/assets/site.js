document.querySelectorAll(".motion-control").forEach((button) => {
  const figure = button.closest("figure");
  const animation = figure?.querySelector(".motion-demo");
  const poster = figure?.querySelector(".motion-fallback");

  if (!(animation instanceof HTMLImageElement) || !(poster instanceof HTMLImageElement)) {
    return;
  }

  const source = animation.currentSrc || animation.src;
  const duration = Number.parseInt(button.dataset.durationMs || "", 10);
  const playLabel = button.dataset.playLabel || "Play animation";
  const stopLabel = button.dataset.stopLabel || "Stop animation";
  const replayLabel = button.dataset.replayLabel || "Play again";
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let hasPlayed = false;
  let playbackGeneration = 0;
  let stopTimer;

  const showPoster = () => {
    playbackGeneration += 1;
    window.clearTimeout(stopTimer);
    figure.classList.remove("motion-playing");
    animation.hidden = true;
    poster.hidden = false;
    button.textContent = hasPlayed ? replayLabel : playLabel;
    button.dataset.playing = "false";
  };

  const play = () => {
    window.clearTimeout(stopTimer);
    hasPlayed = true;
    const generation = ++playbackGeneration;
    const replaySource = new URL(source);
    replaySource.searchParams.set("replay", Date.now().toString());
    const handleLoad = () => {
      animation.removeEventListener("error", handleError);
      if (generation === playbackGeneration && button.dataset.playing === "true") {
        stopTimer = window.setTimeout(showPoster, Number.isFinite(duration) ? duration : 0);
      }
    };
    const handleError = () => {
      animation.removeEventListener("load", handleLoad);
      if (generation === playbackGeneration) {
        showPoster();
      }
    };
    animation.addEventListener("load", handleLoad, { once: true });
    animation.addEventListener("error", handleError, { once: true });
    animation.src = replaySource.href;
    figure.classList.add("motion-playing");
    poster.hidden = true;
    animation.hidden = false;
    button.textContent = stopLabel;
    button.dataset.playing = "true";
  };

  button.hidden = false;
  reducedMotion.addEventListener("change", (event) => {
    if (event.matches) {
      showPoster();
    }
  });
  button.addEventListener("click", () => {
    if (button.dataset.playing === "true") {
      showPoster();
    } else {
      play();
    }
  });
});
