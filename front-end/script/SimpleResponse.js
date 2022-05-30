const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

let htmlInloggen,
  htmlRegistreren,
  htmlHome,
  htmlHistoriek,
  htmlNavHome,
  htmlNavMessage,
  htmlNavHistoriek;

const listenToInloggen = function () {
  htmlInloggen.addEventListener('click', function () {
    const htmlGebruiker = document.querySelector('.js-gebruiker');
    console.log(htmlGebruiker.value);
    bestaandeGebruiker = htmlGebruiker.value;
    socketio.emit('F2B_login', { gebruikersnaam: bestaandeGebruiker });
  });

  socketio.on('B2F_log_in_succes', function (jsonObject) {
    console.log(jsonObject.id);
    html = `<a href="home.html?id=${jsonObject.id}" class="c-btn__link js-login">Login</a>`;
    htmlInloggen.innerHTML = html;
  });
};

const listenToRegistreren = function () {
  htmlRegistreren.addEventListener('click', function () {
    const htmlNieuweGebruiker = document.querySelector('.js-nieuweGebruiker');
    console.log(htmlNieuweGebruiker.value);
    gebruiker = htmlNieuweGebruiker.value;
    socketio.emit('F2B_maak_gebruiker', { gebruikersnaam: gebruiker });
  });
  socketio.on('B2F_toon_error', function (jsonObject) {
    console.log(jsonObject.error);
    const htmlMessage = document.querySelector('.js-message');
    html = `<p>${jsonObject.error}</p>`;
    htmlMessage.innerHTML = html;
  });

  socketio.on('B2F_toon_succes', function (jsonObject) {
    console.log(jsonObject.message);
    const htmlMessage = document.querySelector('.js-message');
    html = `<p>${jsonObject.message}${jsonObject.gebruiker}!</p>`;
    htmlMessage.innerHTML = html;
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
        let urlParams = new URLSearchParams(window.location.search);
        let idGebruiker = urlParams.get('id');
        socketio.emit('F2B_verstuur_bericht', {
          knopid: id,
          berichtinhoud: bericht.value,
          id: idGebruiker,
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

const gebruiker = function () {
  console.log('test');
  let urlParams = new URLSearchParams(window.location.search);
  let idGebruiker = urlParams.get('id');
  nieuweHome = `<a href="home.html?id=${idGebruiker}" class="c-nav__link js-nav">Home</a>`;
  nieweMessage = `<a href="bericht.html?id=${idGebruiker}" class="c-nav__link js-nav">Bericht</a>`;
  nieuweHistoriek = `<a href="historiek.html?id=${idGebruiker}" class="c-nav__link js-nav">Historiek</a>`;
  htmlNavHome.innerHTML = nieuweHome;
  htmlNavMessage.innerHTML = nieweMessage;
  htmlNavHistoriek.innerHTML = nieuweHistoriek;
};

const init = function () {
  console.info('DOM geladen');
  htmlRegistreren = document.querySelector('.js-registreren');
  htmlInloggen = document.querySelector('.js-login');
  htmlHome = document.querySelector('.js-home');
  htmlHistoriek = document.querySelector('.js-historiek');
  htmlNavHome = document.querySelector('.js-navHome');
  htmlNavMessage = document.querySelector('.js-navMessage');
  htmlNavHistoriek = document.querySelector('.js-navHistoriek');
  let urlParams = new URLSearchParams(window.location.search);
  let idGebruiker = urlParams.get('id');
  if (htmlRegistreren) {
    console.log('Registreren');
    listenToRegistreren();
  } else if (htmlInloggen) {
    console.log('Inloggen');
    listenToInloggen();
  } else {
    if (idGebruiker) {
      if (htmlHome) {
        console.log('Home');
        listenToUI();
        listenToSocket();
        gebruiker();
      } else if (htmlHistoriek) {
        console.log('Historiek');
      }
    } else {
      window.location.href = 'index.html';
    }
  }
};

document.addEventListener('DOMContentLoaded', init);
