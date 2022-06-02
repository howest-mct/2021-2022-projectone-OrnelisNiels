const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

let htmlInloggen,
  htmlRegistreren,
  htmlHome,
  htmlHistoriek,
  htmlNavHome,
  htmlNavMessage,
  htmlNavHistoriek;

//#region ***  Callback-Visualisation - show___         ***********
const showData = function (jsonObject) {
  try {
    console.log(jsonObject);
    let converted_labels = [];
    let converted_data = [];
    for (let data of jsonObject.historiek) {
      converted_labels.push(data.datum);
      converted_data.push(data.waarde);
    }
    drawChart(converted_labels, converted_data);
  } catch (error) {
    console.error(error);
  }
};

const showBerichten = function (jsonObject) {
  try {
    const htmlBerichtDisplay = document.querySelector('.js-berichten');

    console.log(jsonObject.berichten);
    let html = '';
    for (let bericht of jsonObject.berichten) {
      if (bericht.gebruiker_gebruikerid != 9) {
        html += `<div class="container">
            <p class="c-bericht js-berichten">${bericht.berichtinhoud}</p>
            <span class="time-right js-tijd">11:00</span>
            </div>`;
      } else {
        html += `<div class="container darker">
              <p class="c-bericht__darker js-berichten">${bericht.berichtinhoud}</p>
              <span class="time-left">karl</span>
            </div>`;
      }
    }
    htmlBerichtDisplay.innerHTML = html;
  } catch (error) {
    console.error(error);
  }
};
const showError = function (err) {
  console.error(err);
};

const drawChart = function (labels, data) {
  let options = {
    title: {
      text: 'Temperatuur',
      align: 'center',
      style: {
        fontSize: '16px',
        color: '#161B20',
      },
    },
    chart: {
      id: 'myChart',
      type: 'line',
      height: '550px',
    },
    stroke: {
      curve: 'straight',
    },
    grid: {
      borderColor: '#f1f1f1',
    },
    dataLabels: {
      enabled: false,
    },
    series: [
      {
        name: 'Temp sensor',
        data: data,
      },
    ],
    labels: labels,
    noData: {
      text: 'Loading...',
    },
  };
  let chart = new ApexCharts(document.querySelector('.js-chart'), options);
  chart.render();
};

//#endregion

//#region ***  Callback-No Visualisation - callback___  ***********

//#endregion

//#region ***  Data Access - get___                     ***********
const getBerichten = function () {
  let urlParams = new URLSearchParams(window.location.search);
  let idGebruiker = urlParams.get('id');
  const url = `http://${lanIP}/api/v1/berichten/${idGebruiker}/`;
  handleData(url, showBerichten, showError);
};

const getData = function () {
  const url = `http://${lanIP}/api/v1/historiek/`;
  handleData(url, showData, showError);
};

const gebruiker = function () {
  console.log('test');
  let urlParams = new URLSearchParams(window.location.search);
  let idGebruiker = urlParams.get('id');
  socketio.emit('F2B_gebruiker', {
    gebruiker: idGebruiker,
  });

  socketio.on('B2F_bestaande_gebruiker', function (jsonObject) {
    console.log(jsonObject.message);
    if (jsonObject.message == 'bestaand') {
      nieuweHome = `<a href="home.html?id=${idGebruiker}" class="c-nav__link js-nav">Home</a>`;
      nieweMessage = `<a href="bericht.html?id=${idGebruiker}" class="c-nav__link js-nav">Bericht</a>`;
      nieuweHistoriek = `<a href="historiek.html?id=${idGebruiker}" class="c-nav__link js-nav">Historiek</a>`;
      htmlNavHome.innerHTML = nieuweHome;
      htmlNavMessage.innerHTML = nieweMessage;
      htmlNavHistoriek.innerHTML = nieuweHistoriek;
      console.log(idGebruiker);
    } else if (jsonObject.message == 'niet-bestaand') {
      window.location.href = 'index.html';
    }
  });
};
//#endregion

//#region ***  Event Listeners - listenTo___            ***********
const listenToSocketHistoriek = function () {
  socketio.on('B2F_refresh_chart', function () {
    getData();
  });
};

const listenToInloggen = function () {
  htmlInloggen.addEventListener('click', function () {
    const htmlGebruiker = document.querySelector('.js-gebruiker');
    console.log(htmlGebruiker.value);
    bestaandeGebruiker = htmlGebruiker.value;
    socketio.emit('F2B_login', { gebruikersnaam: bestaandeGebruiker });
  });
  const htmlGebruiker = document.querySelector('.js-gebruiker');
  htmlGebruiker.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
      console.log('test');
      console.log(htmlGebruiker.value);
      bestaandeGebruiker = htmlGebruiker.value;
      socketio.emit('F2B_login', { gebruikersnaam: bestaandeGebruiker });
    }
  });

  socketio.on('B2F_log_in_succes', function (jsonObject) {
    console.log(jsonObject.id);
    window.location.href = `home.html?id=${jsonObject.id}`;
  });

  const htmlRegistratie = document.querySelector('.js-registratie');
  htmlRegistratie.addEventListener('click', function () {
    window.location.href = `registreren.html`;
  });
};

const listenToRegistreren = function () {
  htmlRegistreren.addEventListener('click', function () {
    const htmlNieuweGebruiker = document.querySelector('.js-nieuweGebruiker');
    console.log(htmlNieuweGebruiker.value);
    let gebruikersnaam = htmlNieuweGebruiker.value;
    socketio.emit('F2B_maak_gebruiker', { gebruikersnaam: gebruikersnaam });
  });

  const htmlNieuweGebruiker = document.querySelector('.js-nieuweGebruiker');
  htmlNieuweGebruiker.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
      console.log('test');
      console.log(htmlNieuweGebruiker.value);
      nieuweGebruiker = htmlNieuweGebruiker.value;
      socketio.emit('F2B_maak_gebruiker', {
        gebruikersnaam: nieuweGebruiker,
      });
    }
  });

  socketio.on('B2F_toon_error', function (jsonObject) {
    console.log(jsonObject.error);
    const htmlMessage = document.querySelector('.js-message');
    html = `<p>${jsonObject.error}</p>`;
    htmlMessage.innerHTML = html;
  });

  socketio.on('B2F_toon_succes', function (jsonObject) {
    window.location.href = `home.html?id=${jsonObject.id}`;
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
        // } else if (id == 3) {
        //   const bericht = document.querySelector('.js-bericht');
        //   let urlParams = new URLSearchParams(window.location.search);
        //   let idGebruiker = urlParams.get('id');
        //   socketio.emit('F2B_verstuur_bericht', {
        //     knopid: id,
        //     berichtinhoud: bericht.value,
        //     id: idGebruiker,
        //   });
      } else if (id == 4) {
        socketio.emit('F2B_verander_led', {
          knopid: id,
          actie: 'rood',
        });
      } else if (id == 5) {
        socketio.emit('F2B_verander_led', {
          knopid: id,
          actie: 'groen',
        });
      } else if (id == 6) {
        socketio.emit('F2B_verander_led', {
          knopid: id,
          actie: 'blauw',
        });
      } else if (id == 7) {
        socketio.emit('F2B_verander_led', {
          knopid: id,
          actie: 'cycle',
        });
      } else if (id == 8) {
        socketio.emit('F2B_verander_led', {
          knopid: id,
          actie: 'aan',
        });
      } else if (id == 9) {
        socketio.emit('F2B_verander_led', {
          knopid: id,
          actie: 'uit',
        });
      } else if (id == 10) {
        socketio.emit('F2B_verander_ventilator', {
          knopid: id,
          actie: 'aan',
        });
      } else if (id == 11) {
        socketio.emit('F2B_verander_ventilator', {
          knopid: id,
          actie: 'uitt',
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

  socketio.on('B2F_historiek_data', function (jsonObject) {
    console.log(jsonObject);
  });
};

const listenToSocketBericht = function () {
  const verstuurKnop = document.querySelector('.js-send');
  verstuurKnop.addEventListener('click', function () {
    const bericht = document.querySelector('.js-bericht');
    let urlParams = new URLSearchParams(window.location.search);
    let idGebruiker = urlParams.get('id');
    if (bericht.value != '')
      socketio.emit('F2B_verstuur_bericht', {
        berichtinhoud: bericht.value,
        id: idGebruiker,
      });
  });
};
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  console.info('DOM geladen');
  htmlRegistreren = document.querySelector('.js-registreren');
  htmlInloggen = document.querySelector('.js-login');
  htmlHome = document.querySelector('.js-home');
  htmlHistoriek = document.querySelector('.js-historiek');
  htmlBericht = document.querySelector('.js-bericht');
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
        gebruiker();
        getData();
        listenToSocketHistoriek();
      } else if (htmlBericht) {
        console.log('Bericht');
        listenToSocketBericht();
        getBerichten();
        gebruiker();
      }
    } else {
      window.location.href = 'index.html';
    }
  }
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
