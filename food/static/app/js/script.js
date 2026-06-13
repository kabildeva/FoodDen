// script.js — add automatic sliding (with simple pause/restart behavior)

const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");
const prev = document.getElementById("prev");
const next = document.getElementById("next");
const sliderEl = document.getElementById("slimg");

let index = 0;
const AUTOPLAY_MS = 1500; // change this to speed up/slow down
let autoplayId = null;

// Show slide function (keeps dots in sync)
function showSlide(i) {
  if (i < 0) index = slides.length - 1;
  else if (i >= slides.length) index = 0;
  else index = i;

  sliderEl.style.transform = `translateX(-${index * 100}%)`;
  dots.forEach(d => d.classList.remove("active"));
  if (dots[index]) dots[index].classList.add("active");
}

// Manual controls
prev.addEventListener("click", () => {
  showSlide(index - 1);
  restartAutoplay();
});
next.addEventListener("click", () => {
  showSlide(index + 1);
  restartAutoplay();
});
dots.forEach(dot => {
  dot.addEventListener("click", () => {
    showSlide(Number(dot.dataset.i));
    restartAutoplay();
  });
});

// Autoplay helpers
function startAutoplay() {
  stopAutoplay();
  autoplayId = setInterval(() => {
    showSlide(index + 1);
  }, AUTOPLAY_MS);
}
function stopAutoplay() {
  if (autoplayId !== null) {
    clearInterval(autoplayId);
    autoplayId = null;
  }
}
function restartAutoplay() {
  stopAutoplay();
  startAutoplay();
}

// Pause on hover (optional nice UX)
const mainContainer = document.getElementById("main");
if (mainContainer) {
  mainContainer.addEventListener("mouseenter", () => stopAutoplay());
  mainContainer.addEventListener("mouseleave", () => startAutoplay());
}

// Init
showSlide(0);
startAutoplay();
