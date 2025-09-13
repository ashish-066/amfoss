const canvas = document.getElementById("circle");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("score");
const bestScoree = document.getElementById("bestScore");
const messagee = document.getElementById("message");
const drawSound = document.getElementById("drawSound");

let isDrawing = false;
let points = [];
let score = 0;
let bestScore = sessionStorage.getItem("bestScore") || 0;
let difficulty = "medium";
let startTime = 0;
const center = { x: canvas.width / 2, y: canvas.height / 2 };

bestScoree.textContent = `${bestScore}%`;

function setDifficulty(level) {
  difficulty = level;
  messagee.textContent = `Difficulty: ${level}`;
  clearCanvas();
}

function toggleDark() {
  document.body.dataset.dark =
    document.body.dataset.dark === "true" ? "false" : "true";
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawDot();
  score = 0;
  scoreDisplay.textContent = "0%";
  messagee.textContent = "";
  points = [];
}

function drawDot() {
  ctx.fillStyle = "blue";
  let radius = 5;
  if (difficulty === "easy") radius = 10;
  if (difficulty === "hard") radius = 3;
  ctx.beginPath();
  ctx.arc(center.x, center.y, radius, 0, Math.PI * 2);
  ctx.fill();
}

function startDrawing(e) {
  isDrawing = true;
  points = [];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawDot();
  ctx.beginPath();
  ctx.moveTo(e.offsetX, e.offsetY);
  points.push({ x: e.offsetX, y: e.offsetY });
  startTime = Date.now();
  playSound();
}

function draw(e) {
  if (!isDrawing) return;
  ctx.lineTo(e.offsetX, e.offsetY);
  ctx.stroke();
  points.push({ x: e.offsetX, y: e.offsetY });
}

function stopDrawing() {
  if (!isDrawing) return;
  isDrawing = false;
  stopSound();

  if (!isCircleComplete()) {
    score = 0;
    scoreDisplay.textContent = "0%";
    messagee.textContent = "Circle not complete";
    return;
  }

  if (!enclosesCenter(points)) {
    score = 0;
    scoreDisplay.textContent = "0%";
    messagee.textContent = " The center dot is not inside your circle";
    return;
  }

  calculateScore();

  if (score > bestScore) {
    bestScore = score;
    sessionStorage.setItem("bestScore", bestScore);
    messagee.textContent = ` New High Score: ${bestScore.toFixed(1)}% `;
  } else {
    messagee.textContent = `Final Score: ${score.toFixed(1)}%`;
  }

  bestScoree.textContent = `${Number(bestScore).toFixed(1)}%`;
}

function isCircleComplete() {
  if (points.length < 10) return false;
  const dx = points[0].x - points[points.length - 1].x;
  const dy = points[0].y - points[points.length - 1].y;
  return Math.sqrt(dx * dx + dy * dy) < 20;
}

function enclosesCenter(points) {
  let inside = false;
  for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
    const xi = points[i].x,
      yi = points[i].y;
    const xj = points[j].x,
      yj = points[j].y;
    const intersect =
      yi > center.y !== yj > center.y &&
      center.x < ((xj - xi) * (center.y - yi)) / (yj - yi) + xi;
    if (intersect) inside = !inside;
  }
  return inside;
}

function calculateScore() {
  let sumX = 0,
    sumY = 0;
  points.forEach((p) => {
    sumX += p.x;
    sumY += p.y;
  });
  const cx = sumX / points.length;
  const cy = sumY / points.length;
  const avgRadius =
    points.reduce(
      (acc, p) => acc + Math.hypot(p.x - cx, p.y - cy),
      0
    ) / points.length;
  const variance =
    points.reduce(
      (acc, p) =>
        acc + Math.abs(Math.hypot(p.x - cx, p.y - cy) - avgRadius),
      0
    ) / points.length;

  let penaltyFactor = 1;
  if (difficulty === "medium") penaltyFactor = 1.2;
  if (difficulty === "hard") penaltyFactor = 1.6;

  let accuracy = Math.max(0, 100 - variance * penaltyFactor);

  const elapsed = (Date.now() - startTime) / 1000; 
  const timeBonus = Math.max(0, 20 - elapsed); 
  accuracy += timeBonus;

  score = Math.min(100, accuracy);
  scoreDisplay.textContent = `${score.toFixed(1)}%`;
}

function playSound() {
  drawSound.loop = true;
  drawSound.play().catch(() => {});
}

function stopSound() {
  drawSound.pause();
  drawSound.currentTime = 0;
}

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseleave", stopDrawing);

clearCanvas(); 
