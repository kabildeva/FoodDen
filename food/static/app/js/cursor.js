(() => {
  const frameCount = 2;
  const fps = 10;
  const folder = "/static/app/images/cursor21";

  const frames = [];
  for (let i = 1; i <= frameCount; i++) {
    frames.push(`${folder}/frame${i}.png`);
  }

  let frameIndex = 0;

  setInterval(() => {
    document.documentElement.style.cursor =
      `url(${frames[frameIndex]}) 0 0, auto`;
    frameIndex = (frameIndex + 1) % frames.length;
  }, 1000 / fps);
})();
