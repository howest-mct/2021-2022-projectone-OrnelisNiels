const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

let htmlInloggen, htmlRegistreren;

const listenToRegistreren = function () {
  htmlRegistreren.addEventListener('click', function () {
    console.log(this);
  });
};

const listenToUI = function () {
  const knoppen = document.querySelectorAll('.js-btn');
  for (const knop of knoppen) {
    knop.addEventListener('click', function () {
      console.log(this);
      const id = this.getAttribute('knop-id');
      console.log(id);
      if (id == 1) {
        console.log('hoi');
        socketio.emit('F2B_toon_sensorwaarde', {
          knopid: id,
        });
      } else if (id == 2) {
        socketio.emit('F2B_toon_sensorwaarde', {
          knopid: id,
        });
      } else if (id == 3) {
        const bericht = document.querySelector('.js-bericht');
        socketio.emit('F2B_verstuur_bericht', {
          knopid: id,
          berichtinhoud: bericht.value,
        });
      }
    });
  }
};

const listenToSocket = function () {
  socketio.on('connected', function () {
    console.log('verbonden met socket webserver');
  });

  socketio.on('B2F_temperatuur_uitlezen', function (jsonObject) {
    console.log(jsonObject.temperatuur);
    const htmlTemp = document.querySelector('.js-temp');
    html = `<p>${jsonObject.temperatuur} ° C</p>`;
    htmlTemp.innerHTML = html;
  });

  socketio.on('B2F_licht_uitlezen', function (jsonObject) {
    console.log(jsonObject.licht);
    const htmlLdr = document.querySelector('.js-ldr');
    html = `<p>${jsonObject.licht} %</p>`;
    htmlLdr.innerHTML = html;
  });
};

const init = function () {
  console.info('DOM geladen');
  htmlRegistreren = document.querySelector('.js-registreren');
  htmlInloggen = document.querySelector('.js-login');
  if (htmlRegistreren) {
    console.log('Registreren');
    listenToRegistreren();
  } else if (htmlInloggen) {
    console.log('Inloggen');
  } else {
    listenToUI();
    listenToSocket();
  }
};

document.addEventListener('DOMContentLoaded', init);
