document.querySelectorAll(".motion-replay").forEach((button) => {
  const figure = button.closest("figure");
  const animation = figure?.querySelector(".motion-demo");

  if (!(animation instanceof HTMLImageElement)) {
    button.hidden = true;
    return;
  }

  const source = animation.currentSrc || animation.src;
  button.hidden = false;

  button.addEventListener("click", () => {
    const replaySource = new URL(source);
    replaySource.searchParams.set("replay", Date.now().toString());
    animation.src = replaySource.href;
  });
});
