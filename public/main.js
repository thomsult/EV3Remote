// @ts-ignore
class key {
  socket
  pressed = false;
  constructor(keyName) {
    this.key = keyName;
  }
  keyDown() {
    socket && !this.pressed && this.socket.emit('keyEvent', { keyEvent: this.key, type: 'keyDown' });
    this.pressed = true;
  }
  keyUp() {
    socket && this.pressed && this.socket.emit('keyEvent', { keyEvent: this.key, type: 'keyUp' });
    this.pressed = false;
  }
}

const keypad = (keyItems) => keyItems.map((el) => new key(el));

const keyPad = keypad([
  "ArrowUp",
  "ArrowDown",
  "ArrowLeft",
  "ArrowRight",
  "Escape",
]);

// @ts-ignore
const socket = io();
const ev3Dev = document.getElementById('ev3Dev');
const ev3DevConnected = document.createElement('H3');
socket.on('connect', function () {
  keyPad.forEach((el) => {
    el.socket = socket;
    const button = document.createElement('button');
    button.textContent = el.key;
    button.className = 'key ' + el.key;

    button.onmousedown = () => el.keyDown();
    button.onmouseup = () => el.keyUp();
    document.addEventListener('keydown', (e) => e.key === el.key && el.keyDown());
    document.addEventListener('keyup', (e) => e.key === el.key && el.keyUp());

    ev3Dev?.appendChild(button);
  });
  ev3DevConnected.textContent = 'EV3 disconnected';

  document.body.appendChild(ev3DevConnected);
  console.log('connected');
  socket.on('ev3', function (data) {
    console.log(data);
    
    if (data.message === 'EV3 connected') {
      ev3DevConnected.textContent = 'EV3 connected';
      document.getElementById('ev3Dev')?.classList.add('connected');
    }
    if (data.message === 'EV3 disconnected') {
      ev3DevConnected.textContent = 'EV3 disconnected';
      document.getElementById('ev3Dev')?.classList.remove('connected');
    }
  });
});
