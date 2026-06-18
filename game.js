const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

canvas.width = 1280;
canvas.height = 720;

const keys = {};

document.addEventListener("keydown", e => keys[e.key.toLowerCase()] = true);
document.addEventListener("keyup", e => keys[e.key.toLowerCase()] = false);

// ---------------- CONFIG ----------------
const ROAD_W = 260;
const LANE_COUNT = 4;

const LEFT_X = 320;
const RIGHT_X = 960;

const SPEED_MAX = 6;
const ACCEL = 0.15;
const STEER = 0.04;

// ---------------- STATE ----------------
let weather = "clear";
let day = true;
let trafficOn = false;

// ---------------- CAR ----------------
class Car {
  constructor(x, y, color="red") {
    this.x = x;
    this.y = y;
    this.angle = Math.PI / 2;
    this.speed = 0;
    this.color = color;
  }

  update() {
    // controls (player only)
    if (this === player) {
      if (keys["arrowup"] || keys["w"]) this.speed += ACCEL;
      if (keys["arrowdown"] || keys["s"]) this.speed -= ACCEL;
      if (keys["arrowleft"] || keys["a"]) this.angle -= STEER;
      if (keys["arrowright"] || keys["d"]) this.angle += STEER;
    }

    // clamp speed
    this.speed *= 0.98;
    this.speed = Math.max(-2, Math.min(SPEED_MAX, this.speed));

    this.x += Math.cos(this.angle) * this.speed;
    this.y += Math.sin(this.angle) * this.speed;

    // keep on screen vertically
    if (this.y < 0) this.y = 720;
    if (this.y > 720) this.y = 0;
  }

  draw() {
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.angle);

    ctx.fillStyle = this.color;
    ctx.fillRect(-10, -20, 20, 40);

    ctx.restore();
  }
}

// ---------------- ROADS ----------------
function drawRoad(x) {
  ctx.fillStyle = "#444";
  ctx.fillRect(x - ROAD_W/2, 0, ROAD_W, canvas.height);

  ctx.strokeStyle = "#fff";
  ctx.lineWidth = 2;

  for (let i = 1; i < LANE_COUNT; i++) {
    const lx = x - ROAD_W/2 + (ROAD_W / LANE_COUNT) * i;
    ctx.beginPath();
    ctx.moveTo(lx, 0);
    ctx.lineTo(lx, canvas.height);
    ctx.stroke();
  }
}

// ---------------- BUILDINGS ----------------
function drawBuildings() {
  ctx.fillStyle = "#2b2b55";

  for (let i = 0; i < 6; i++) {
    ctx.fillRect(50, i * 120, 100, 80);
    ctx.fillRect(1130, i * 120, 100, 80);
  }
}

// ---------------- TRAFFIC ----------------
function spawnTraffic() {
  let cars = [];
  for (let i = 0; i < 6; i++) {
    cars.push(new Car(
      RIGHT_X + (Math.random() - 0.5) * 100,
      Math.random() * 720,
      "blue"
    ));
  }
  return cars;
}

// ---------------- INIT ----------------
let player = new Car(LEFT_X, 360, "red");
let traffic = [];

// ---------------- INPUT EVENTS ----------------
document.addEventListener("keydown", e => {
  if (e.key === "t") {
    trafficOn = !trafficOn;
    traffic = trafficOn ? spawnTraffic() : [];
  }

  if (e.key === "e") day = !day;

  if (e.key === "q") {
    weather = weather === "clear"
      ? "rain"
      : weather === "rain"
        ? "fog"
        : "clear";
  }
});

// ---------------- LOOP ----------------
function loop() {
  // background
  ctx.fillStyle =
    !day ? "#0b0b1e" :
    weather === "clear" ? "#87ceeb" :
    weather === "rain" ? "#6f7a86" :
    "#cfcfcf";

  ctx.fillRect(0, 0, canvas.width, canvas.height);

  drawBuildings();
  drawRoad(LEFT_X);
  drawRoad(RIGHT_X);

  player.update();
  player.draw();

  traffic.forEach(c => {
    c.update();
    c.draw();
  });

  // UI
  ctx.fillStyle = "#fff";
  ctx.font = "18px Arial";
  ctx.fillText(
    `Weather: ${weather} | Day: ${day} | Traffic: ${trafficOn}`,
    20,
    30
  );

  requestAnimationFrame(loop);
}

loop();
