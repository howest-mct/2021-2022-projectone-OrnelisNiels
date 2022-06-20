const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

let htmlInloggen,
  htmlRegistreren,
  htmlHome,
  htmlHistoriek,
  htmlNavHome,
  htmlNavMessage,
  htmlNavHistoriek,
  htmlNavHomeMobile,
  htmlNavMessageMobile,
  htmlNavHistoriekMobile,
  chartStat = false,
  chart,
  dag = false,
  week = false,
  all = false,
  grafTemp = false,
  grafBer = true,
  weekBer = true,
  allBer = false,
  vorigeBer = '';

//#region ***  Callback-Visualisation - show___         ***********
function toggleNav() {
  let toggleTrigger = document.querySelectorAll('.js-toggle-nav');
  for (let i = 0; i < toggleTrigger.length; i++) {
    toggleTrigger[i].addEventListener('click', function () {
      console.log('test');
      document.querySelector('body').classList.toggle('has-mobile-nav');
    });
  }
}

const showData = function (jsonObject) {
  try {
    console.log(jsonObject);
    console.log(grafBer);
    console.log(grafTemp);
    console.log(chartStat);
    let converted_labels = [];
    let converted_data = [];
    if (grafBer == true) {
      for (let data of jsonObject.historiek) {
        converted_labels.push(data.datum);
        converted_data.push(data.aantal);
      }
      console.log('Data', converted_data, '\nLabels', converted_labels);
      if (chartStat == false) {
        drawChart(converted_labels, converted_data);
        chartStat = true;
      } else {
        if (weekBer == true) {
          chart.updateOptions({
            labels: converted_labels,
            series: [
              {
                data: converted_data,
                type: 'bar',
                color: '#F4A950',
              },
            ],
            chart: {
              id: 'myChart',
              type: 'bar',
              height: '550px',
              // colors: 'F4A950',
              // forecolor: 'F4A950',
              toolbar: {
                show: false,
              },
              zoom: {
                enabled: false,
              },
            },
            dataLabels: {
              enabled: true,
            },
            title: {
              text: 'Aantal berichten laatste week',
              align: 'center',
              style: {
                fontSize: '16px',
                color: '#161B20',
              },
            },
          });
        } else if (allBer == true) {
          console.log('all ber');
          chart.updateOptions({
            labels: converted_labels,
            series: [
              {
                data: converted_data,
                type: 'bar',
                color: '#F4A950',
              },
            ],
            chart: {
              id: 'myChart',
              type: 'bar',
              height: '550px',
              toolbar: {
                show: false,
              },
              zoom: {
                enabled: false,
              },
            },
            title: {
              text: 'Aantal berichten all time',
              align: 'center',
              style: {
                fontSize: '16px',
                color: '#161B20',
              },
            },
            dataLabels: {
              enabled: true,
            },
          });
        }
      }
    } else if (grafTemp == true) {
      for (let data of jsonObject.historiek) {
        converted_labels.push(data.datum);
        converted_data.push(data.waarde);
      }
      console.log('Data', converted_data, '\nLabels', converted_labels);
      if (chartStat == false) {
        drawChart(converted_labels, converted_data);
        chartStat = true;
      } else {
        if (dag == true) {
          chart.updateOptions({
            title: {
              text: 'Temperatuur laatste 24u',
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
              toolbar: {
                show: false,
              },
              zoom: {
                enabled: false,
              },
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
            // xaxis: {
            //   type: 'datetime',
            //   labels: {
            //     datetimeFormatter: {
            //       year: 'yyyy',
            //       month: "MMM 'yy",
            //       day: 'dd MMM',
            //       hour: 'HH:mm',
            //     },
            //   },
            // },
            series: [
              {
                type: 'line',
                name: 'Aantal berichten',
                data: converted_data,
                color: '#F47550',
              },
            ],
            labels: converted_labels,
            // noData: {
            //   text: 'Loading...',
            // },
            tooltip: {
              enabled: true,
              // formatter: 'HH:mm:ss',
              offsetY: 0,
              x: {
                show: true,
                format: 'dd MMM',
              },
              style: {
                fontSize: '16px',
                fontFamily: 0,
                color: '#161b20',
              },
            },
            // states: {
            //   hover: {
            //     filter: {
            //       type: 'lighten',
            //       value: 0.01,
            //     },
            //   },
            //   active: {
            //     allowMultipleDataPointsSelection: false,
            //     filter: {
            //       type: 'none',
            //     },
            //   },
            // },
          });
        } else if (week == true || (all == true && grafTemp == true)) {
          console.log('week||all');
          chart.updateOptions({
            labels: converted_labels,
            series: [
              {
                data: converted_data,
                type: 'bar',
                color: '#F47550',
              },
            ],
            chart: {
              id: 'myChart',
              type: 'bar',
              height: '550px',
              toolbar: {
                show: false,
              },
              zoom: {
                enabled: false,
              },
            },
            title: {
              text: 'Gemiddelde temperatuur per dag',
              align: 'center',
              style: {
                fontSize: '16px',
                color: '#161B20',
              },
            },
            dataLabels: {
              enabled: true,
            },
          });
        }
      }
    }
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
      if (bericht.gebruiker_gebruikerid != 1) {
        html += `<div class="container">
          <span class="time-left">${bericht.naam}</span>
            <p class="c-bericht js-berichten">${bericht.berichtinhoud}</p>
            <span class="time-right js-tijd">${bericht.datum}</span>
            </div>`;
      } else {
        html += `<div class="container darker">
              <span class="time-left__dark">${bericht.naam}</span>
              <p class="c-bericht__darker js-berichten">${bericht.berichtinhoud}</p>
              <span class="time-right__dark js-tijd">${bericht.datum}</span>
            </div>`;
      }
    }
    htmlBerichtDisplay.innerHTML = html;
  } catch (error) {
    console.error(error);
  }
};

const showQuickReplies = function (jsonObject) {
  try {
    console.log(jsonObject.quickreplies);
    let teller = 0;
    for (let optie of jsonObject.quickreplies) {
      teller = teller + 1;
      waarde = optie.berichtinhoud;
      document.querySelector(`.js-optie${teller}`).placeholder = waarde;
    }
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
      text: 'Aantal berichten laatste week',
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
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: false,
      },
    },
    stroke: {
      curve: 'straight',
    },
    grid: {
      borderColor: '#f1f1f1',
    },
    dataLabels: {
      enabled: true,
    },
    // xaxis: {
    //   type: 'datetime',
    //   labels: {
    //     datetimeFormatter: {
    //       year: 'yyyy',
    //       month: "MMM 'yy",
    //       day: 'dd MMM',
    //       hour: 'HH:mm',
    //     },
    //   },
    // },
    series: [
      {
        name: 'Aantal berichten',
        data: data,
        type: 'bar',
        color: '#F4A950',
      },
    ],
    labels: labels,
    noData: {
      text: 'Loading...',
    },
    tooltip: {
      enabled: true,
      // formatter: 'HH:mm:ss',
      offsetY: 0,
      x: {
        show: true,
        format: 'dd MMM',
      },
      style: {
        fontSize: '16px',
        fontFamily: 0,
        color: '#161b20',
      },
    },
    states: {
      hover: {
        filter: {
          type: 'lighten',
          value: 0.01,
        },
      },
      active: {
        allowMultipleDataPointsSelection: false,
        filter: {
          type: 'none',
        },
      },
    },
  };
  chart = new ApexCharts(document.querySelector('.js-chart'), options);
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

const getQuickReplies = function () {
  const url = `http://${lanIP}/api/v1/quickReplies/`;
  handleData(url, showQuickReplies, showError);
};

const getDataBerichtenWeek = function () {
  const url = `http://${lanIP}/api/v1/historiek/berichten/week/`;
  handleData(url, showData, showError);
};

const getDataBerichtenAll = function () {
  const url = `http://${lanIP}/api/v1/historiek/berichten/all/`;
  handleData(url, showData, showError);
};

const getDataDag = function () {
  const url = `http://${lanIP}/api/v1/historiek/temp/dag/`;
  handleData(url, showData, showError);
};

const getDataWeek = function () {
  const url = `http://${lanIP}/api/v1/historiek/temp/week/`;
  handleData(url, showData, showError);
};

const getDataAll = function () {
  const url = `http://${lanIP}/api/v1/historiek/temp/all/`;
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
      nieuweHome = `<a href="home.html?id=${idGebruiker}" class="c-nav__link js-nav">Bericht</a>`;
      nieweMessage = `<a href="kamer.html?id=${idGebruiker}" class="c-nav__link js-nav">Kamer</a>`;
      nieuweHistoriek = `<a href="historiek.html?id=${idGebruiker}" class="c-nav__link js-nav">Historiek</a>`;
      htmlNavHome.innerHTML = nieuweHome;
      htmlNavMessage.innerHTML = nieweMessage;
      htmlNavHistoriek.innerHTML = nieuweHistoriek;
      htmlNavHomeMobile.innerHTML = nieuweHome;
      htmlNavMessageMobile.innerHTML = nieweMessage;
      htmlNavHistoriekMobile.innerHTML = nieuweHistoriek;
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
    if (dag == true) {
      getDataDag();
    } else if (week == true) {
      getDataWeek();
    } else if (all == true) {
      getDataAll();
    }
  });
  socketio.on('B2F_refreshBerichtenChart', function () {
    if (weekBer == true) {
      getDataBerichtenWeek();
    } else if (allBer == true) {
      getDataBerichtenAll();
    } else {
    }
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
    if (event.key == 'Enter') {
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
    if (event.key == 'Enter') {
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
          actie: 'aan',
          knopid: id,
        });
      } else if (id == 11) {
        socketio.emit('F2B_verander_ventilator', {
          actie: 'uitt',
          knopid: id,
        });
      } else if (id == 12) {
        socketio.emit('F2B_verander_led', {
          knopid: id,
          actie: 'auto',
        });
      } else if (id == 13) {
        document.querySelector('.js-shutdownTab').style.display = 'none';
      } else if (id == 14) {
        socketio.emit('F2B_shutdown');
        document.querySelector('.js-shutdownTab').style.display = 'none';
      }
    });
  }
  const gewensteTemp = document.querySelector('.js-gewensteTemp');
  const gewensteTempKnop = document.querySelector('.js-sendTemp');
  let htmlTemp = '';
  const errorMelding = document.querySelector('.js-meldingVent');
  gewensteTempKnop.addEventListener('click', function () {
    let gewensteTempWaarde = gewensteTemp.value;
    if (gewensteTempWaarde > 100 || gewensteTempWaarde < 0) {
      htmlTemp = 'Error, geef waarde tussen 0 & 100';
      console.log(htmlTemp);
    } else {
      console.log(gewensteTempWaarde);
      socketio.emit('F2B_verander_ventilatorAuto', {
        actie: 'auto',
        temp: gewensteTempWaarde,
      });
      htmlTemp = `Huidige setpoint: <b>${gewensteTempWaarde} °C</b>`;
    }
    // errorMelding.innerHTML = htmlTemp;
  });
  gewensteTemp.addEventListener('keypress', function (event) {
    htmlTemp = 'Huidige setpoint: <b> °C';
    let gewensteTempWaarde = gewensteTemp.value;
    if (event.key == 'Enter') {
      if (gewensteTempWaarde > 100 || gewensteTempWaarde < 0) {
        socketio.emit('F2B_verander_ventilatorAuto', {
          actie: 'auto',
          temp: gewensteTempWaarde,
        });
      } else {
        console.log(gewensteTempWaarde);
        socketio.emit('F2B_verander_ventilatorAuto', {
          actie: 'auto',
          temp: gewensteTempWaarde,
        });
        htmlTemp = `Huidige setpoint: <b>${gewensteTempWaarde} °C</b>`;
      }
    }
    // errorMelding.innerHTML = htmlTemp;
  });
  const vent = document.querySelector('.js-showVentilator');
  vent.addEventListener('click', function () {
    document.querySelector('.js-ventTab').style.display = 'flex';
  });
  const ventCross = document.querySelector('.js-crossVent');
  ventCross.addEventListener('click', function () {
    document.querySelector('.js-ventTab').style.display = 'none';
  });

  const leds = document.querySelector('.js-showLeds');
  leds.addEventListener('click', function () {
    document.querySelector('.js-ledTab').style.display = 'flex';
  });
  const ledCross = document.querySelector('.js-crossLed');
  ledCross.addEventListener('click', function () {
    document.querySelector('.js-ledTab').style.display = 'none';
  });

  const shutdownPopup = document.querySelector('.js-showShutdown');
  shutdownPopup.addEventListener('click', function () {
    document.querySelector('.js-shutdownTab').style.display = 'flex';
  });
  const crossShutdown = document.querySelector('.js-crossShutdown');
  crossShutdown.addEventListener('click', function () {
    document.querySelector('.js-shutdownTab').style.display = 'none';
  });
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

  socketio.on('B2F_verander_status_vent', function (jsonObject) {
    console.log(jsonObject);
    if (jsonObject.status == 1) {
      const element = document.querySelector('.js-statusVent');
      console.log(element);
      element.classList.add('c-statusGroen');
    } else {
      const element = document.querySelector('.js-statusVent');
      element.classList.remove('c-statusGroen');
    }
  });
  socketio.on('B2F_verander_tempHtml', function (jsonObject) {
    console.log(jsonObject);
    let htmlTemp = '';
    const errorMelding = document.querySelector('.js-meldingVent');
    const gewensteTempWaarde = jsonObject.gewTemp;
    if (gewensteTempWaarde == -1) {
      errorMelding.innerHTML = 'Huidige setpoint: <b> °C</b>';
    } else {
      if (gewensteTempWaarde > 100 || gewensteTempWaarde < 0) {
        htmlTemp = 'Error, geef waarde tussen 0 & 100';
        console.log(htmlTemp);
      } else {
        console.log(gewensteTempWaarde);
        htmlTemp = `Huidige setpoint: <b>${gewensteTempWaarde} °C</b>`;
      }
      errorMelding.innerHTML = htmlTemp;
    }
  });
  socketio.on('B2F_verander_status_leds', function (jsonObject) {
    if (jsonObject.status == 1) {
      const element = document.querySelector('.js-statusLeds');
      console.log(element);
      element.classList.add('c-statusLedsGroen');
    } else {
      const element = document.querySelector('.js-statusLeds');
      element.classList.remove('c-statusLedsGroen');
    }
  });
};

const listenToSocketBericht = function () {
  const verstuurKnop = document.querySelector('.js-send');
  verstuurKnop.addEventListener('click', function () {
    const bericht = document.querySelector('.js-bericht');
    let urlParams = new URLSearchParams(window.location.search);
    let idGebruiker = urlParams.get('id');
    if (bericht.value != '' && bericht.value.length < 129) {
      if (bericht.value != vorigeBer) {
        socketio.emit('F2B_verstuur_bericht', {
          berichtinhoud: bericht.value,
          id: idGebruiker,
        });
        console.log('test');
        getBerichten();
        vorigeBer = bericht.value;
        bericht.value = '';
        window.location.reload();
      }
    }
  });
  let ber = document.querySelector('.js-bericht');
  ber.addEventListener('keypress', function (event) {
    if (event.key == 'Enter') {
      const bericht = document.querySelector('.js-bericht');
      let urlParams = new URLSearchParams(window.location.search);
      let idGebruiker = urlParams.get('id');
      if (bericht.value != '' && bericht.value.length < 129) {
        if (bericht.value != vorigeBer) {
          socketio.emit('F2B_verstuur_bericht', {
            berichtinhoud: bericht.value,
            id: idGebruiker,
          });
          console.log('test');
          getBerichten();
          vorigeBer = bericht.value;
          bericht.value = '';
          window.location.reload();
        }
      }
    }
  });
  socketio.on('B2F_nieuw_bericht', function (jsonObject) {
    getBerichten();
    window.location.reload();
  });
};

const listenToPeriode = function () {
  const periodeSelect = document.querySelector('.js-periodeSelect');
  periodeSelect.addEventListener('change', function () {
    console.log('test');
    console.log(this.value);
    if (this.value == 'dag') {
      console.log('dag');
      getDataDag();
      week = false;
      all = false;
      dag = true;
    } else if (this.value == 'week') {
      console.log('week');
      getDataWeek();
      dag = false;
      all = false;
      week = true;
      // listenToSocketHistoriek();
    } else if (this.value == 'all') {
      console.log('all');
      getDataAll();
      week = false;
      dag = false;
      all = true;
    }
  });
};

const listenToKnoppen = function () {
  let grafiekBerichten = document.querySelector('.js-grafiekBerichten');
  let grafiekTemperatuur = document.querySelector('.js-grafiekTemperatuur');
  let grafiekTempDisplay = document.querySelector('.js-tempDisplay');
  // let grafiekTempDisplayGraph = document.querySelector('.js-tempDisplayGraph');
  let grafiekBerichtenDisplay = document.querySelector('.js-berDisplay');
  // let grafiekBerichtenDisplayGraph = document.querySelector(
  //   '.js-berDisplayGraph'
  // );
  console.log(grafiekTempDisplay);
  grafiekBerichten.addEventListener('click', function () {
    if (grafBer == false) {
      console.log('Berichten');
      grafiekBerichtenDisplay.classList.add('c-berichtenTonen');
      grafiekBerichtenDisplay.classList.remove('c-berichtenVerwijderen');
      // grafiekBerichtenDisplayGraph.classList.add('c-berichtenTonen');
      // grafiekBerichtenDisplayGraph.classList.remove('c-berichtenVerwijderen');
      grafiekTempDisplay.classList.add('c-temperatuurVerwijderen');
      grafiekTempDisplay.classList.remove('c-temperatuurTonen');
      // grafiekTempDisplayGraph.classList.add('c-temperatuurVerwijderen');
      // grafiekTempDisplayGraph.classList.remove('c-temperatuurTonen');
      const periodeSelect = document.querySelector('.js-periodeSelect');
      periodeSelect.innerHTML =
        '<option value="dag" selected>Dag</option> <option value="week">Week</option> <option value="all">All</option>';
      grafTemp = false;
      grafBer = true;
      dag = false;
      weekBer = true;
      getDataBerichtenWeek();
    }
  });
  grafiekTemperatuur.addEventListener('click', function () {
    if (grafTemp == false) {
      console.log('Temperatuur');
      grafiekTempDisplay.classList.add('c-temperatuurTonen');
      grafiekTempDisplay.classList.remove('c-temperatuurVerwijderen');
      // grafiekTempDisplayGraph.classList.add('c-temperatuurTonen');
      // grafiekTempDisplayGraph.classList.remove('c-temperatuurVerwijderen');
      grafiekBerichtenDisplay.classList.add('c-berichtenVerwijderen');
      grafiekBerichtenDisplay.classList.remove('c-berichtenTonen');
      // grafiekBerichtenDisplayGraph.classList.add('c-berichtenVerwijderen');
      // grafiekBerichtenDisplayGraph.classList.remove('c-berichtenTonen');
      const periodeSelect = document.querySelector('.js-periodeSelectBer');
      periodeSelect.innerHTML =
        '<option value="week" selected>Week</option> <option value="all">All</option>';
      grafBer = false;
      grafTemp = true;
      dag = true;
      getDataDag();
    }
  });
};

const listenToPeriode1 = function () {
  const periodeSelect = document.querySelector('.js-periodeSelectBer');
  periodeSelect.addEventListener('change', function () {
    console.log('test');
    console.log(this.value);
    if (this.value == 'week') {
      console.log('week');
      getDataBerichtenWeek();
      allBer = false;
      weekBer = true;
    } else if (this.value == 'all') {
      console.log('week');
      getDataBerichtenAll();
      weekBer = false;
      allBer = true;
    }
  });
};
const listenToWijzigen = function () {
  const quickReplies = document.querySelector('.js-quickReplies');
  quickReplies.addEventListener('click', function () {
    document.querySelector('.js-replyTab').style.display = 'flex';
  });
  const replyCross = document.querySelector('.js-crossReplies');
  replyCross.addEventListener('click', function () {
    document.querySelector('.js-replyTab').style.display = 'none';
    const optie1 = (document.querySelector('.js-optie1').value = '');
    const optie2 = (document.querySelector('.js-optie2').value = '');
    const optie3 = (document.querySelector('.js-optie3').value = '');
    const optie4 = (document.querySelector('.js-optie4').value = '');
    errorquick = document.querySelector('.js-errorQuick');
    errorquick.innerHTML = '';
    getQuickReplies();
  });
  const veranderQuick = document.querySelector('.js-change');
  veranderQuick.addEventListener('click', function () {
    const optie1 = document.querySelector('.js-optie1').value;
    const optie2 = document.querySelector('.js-optie2').value;
    const optie3 = document.querySelector('.js-optie3').value;
    const optie4 = document.querySelector('.js-optie4').value;
    if (
      optie1.length < 11 &&
      optie2.length < 5 &&
      optie3.length < 11 &&
      optie4.length < 5
    ) {
      socketio.emit(
        'F2B_verander_quickReplies',
        [
          {
            id: 1,
            inhoud: optie1,
          },
        ],
        [
          {
            id: 2,
            inhoud: optie2,
          },
        ],
        [
          {
            id: 3,
            inhoud: optie3,
          },
        ],
        [
          {
            id: 4,
            inhoud: optie4,
          },
        ]
      );
    } else {
      errorquick = document.querySelector('.js-errorQuick');
      errorquick.innerHTML = 'Error';
    }
    socketio.on('B2F_gewijzigd', function (jsonObject) {
      errorquick = document.querySelector('.js-errorQuick');
      errorquick.innerHTML = 'Gewijzigd';
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
  htmlNavHomeMobile = document.querySelector('.js-navHomeMobile');
  htmlNavMessageMobile = document.querySelector('.js-navMessageMobile');
  htmlNavHistoriekMobile = document.querySelector('.js-navHistoriekMobile');
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
        console.log('Dashboard');
        listenToUI();
        listenToSocket();
        gebruiker();
        toggleNav();
      } else if (htmlHistoriek) {
        console.log('Historiek');
        gebruiker();
        listenToKnoppen();
        getDataBerichtenWeek();
        listenToPeriode();
        listenToPeriode1();
        listenToSocketHistoriek();
        toggleNav();
      } else if (htmlBericht) {
        console.log('Bericht');
        listenToSocketBericht();
        listenToWijzigen();
        getBerichten();
        getQuickReplies();
        gebruiker();
        toggleNav();
      }
    } else {
      window.location.href = 'index.html';
    }
  }
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
