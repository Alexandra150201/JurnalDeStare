var cal = {
  // (A) PROPERTIES
  // (A1) FLAGS & DATA
  mon : true, // monday first
  events : null, // events data for current month/year
  sMth : 0, // selected month
  sYear : 0, // selected year
  sDIM : 0, // number of days in selected month
  sF : 0, // first date of the selected month (yyyymmddhhmm)
  sL : 0, // last date of the selected month (yyyymmddhhmm)
  sFD : 0, // first day of the selected month (mon-sun)
  sLD : 0, // last day of the selected month (mon-sun)
  ready : 0, // to track loading

  // (A2) HTML ELEMENTS
  hMth : null, hYear : null, // month & year
  hCD : null, hCB : null, // calendar days & body


  // (B) SUPPORT FUNCTION - AJAX FETCH
  ajax : (req, data, onload) => {
    // (B1) FORM DATA
    let form = new FormData();
    for (let [k,v] of Object.entries(data)) { form.append(k,v); }

    // (B2) FETCH
    fetch(req + "/", { method:"POST", body:form })
    .then(res => res.text())
    .then(txt => onload(txt))
    .catch(err => console.error(err));
  },

  // (C) INIT CALENDAR
  init : () => {
    // (C1) GET HTML ELEMENTS
    cal.hMth = document.getElementById("calMonth");
    cal.hYear = document.getElementById("calYear");
    cal.hCD = document.getElementById("calDays");
    cal.hCB = document.getElementById("calBody");

    let now = new Date(), nowMth = now.getMonth() + 1;
    for (let [i,n] of Object.entries({
      1 : "Ianuarie", 2 : "Februarie", 3 : "Martie", 4 : "Aprilie",
      5 : "Mai", 6 : "Iunie", 7 : "Iulie", 8 : "August",
      9 : "Septembrie", 10 : "Octombrie", 11 : "Noiembrie", 12 : "Decembrie"
    })) {
      let opt = document.createElement("option");
      opt.value = i;
      opt.innerHTML = n;
      if (i==nowMth) { opt.selected = true; }
      cal.hMth.appendChild(opt);
    }
    cal.hYear.value = parseInt(now.getFullYear());
    cal.hMth.onchange = cal.load;
    cal.hYear.onchange = cal.load;
    document.getElementById("calBack").onclick = () => cal.pshift();
    document.getElementById("calNext").onclick = () => cal.pshift(1);

    let days = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă","Duminică"];
    for (let d of days) {
      let cell = document.createElement("div");
      cell.className = "calCell";
      cell.innerHTML = d;
      cal.hCD.appendChild(cell);
    }

    cal.load();
  },

  // (D) SHIFT CURRENT PERIOD BY 1 MONTH
  pshift : forward => {
    cal.sMth = parseInt(cal.hMth.value);
    cal.sYear = parseInt(cal.hYear.value);
    if (forward) { cal.sMth++; } else { cal.sMth--; }
    if (cal.sMth > 12) { cal.sMth = 1; cal.sYear++; }
    if (cal.sMth < 1) { cal.sMth = 12; cal.sYear--; }
    cal.hMth.value = cal.sMth;
    cal.hYear.value = cal.sYear;
    cal.load();
  },

  // (E) LOAD EVENTS
  load : () => {
    // (E1) SET SELECTED PERIOD
    cal.sMth = parseInt(cal.hMth.value);
    cal.sYear = parseInt(cal.hYear.value);
    cal.sDIM = new Date(cal.sYear, cal.sMth, 0).getDate();
    cal.sFD = new Date(cal.sYear, cal.sMth-1, 1).getDay();
    cal.sLD = new Date(cal.sYear, cal.sMth-1, cal.sDIM).getDay();
    let m = cal.sMth;
    if (m < 10) { m = "0" + m; }
    cal.sF = parseInt(String(cal.sYear) + String(m) + "010000");
    cal.sL = parseInt(String(cal.sYear) + String(m) + String(cal.sDIM) + "2359");

    // (E2) AJAX GET EVENTS
    const pacientSelect = document.getElementById('pacient-select');
    pacientSelect.addEventListener('change', () => {
      cal.ajax("/home/terapeut/get", { month : cal.sMth, year : cal.sYear, pacient: pacientSelect.value }, evt => {
      cal.events = JSON.parse(evt);
      cal.draw();
    });

    });
   cal.ajax("/home/terapeut/get", { month : cal.sMth, year : cal.sYear, pacient: pacientSelect.value }, evt => {
   cal.events = JSON.parse(evt);
   cal.draw();});

  },

  // (F) DRAW CALENDAR
  draw : () => {
    // (F1) CALCULATE DAY MONTH YEAR
    // note - jan is 0 & dec is 11 in js
    // note - sun is 0 & sat is 6 in js
    let now = new Date(), // current date
        nowMth = now.getMonth()+1, // current month
        nowYear = parseInt(now.getFullYear()), // current year
        nowDay = cal.sMth==nowMth && cal.sYear==nowYear ? now.getDate() : null ;

    // (F2) DRAW CALENDAR ROWS & CELLS
    // (F2-1) INIT + HELPER FUNCTIONS
    let rowA, rowB, rowC, rowMap = {}, rowNum = 1,
        cell, cellNum = 1,
    rower = () => {
      rowA = document.createElement("div");
      rowB = document.createElement("div");
      rowC = document.createElement("div");
      rowA.className = "calRow";
      rowA.id = "calRow" + rowNum;
      rowB.className = "calRowHead";
      rowC.className = "calRowBack";
      cal.hCB.appendChild(rowA);
      rowA.appendChild(rowB);
      rowA.appendChild(rowC);
    },
    celler = day => {
      cell = document.createElement("div");
      cell.className = "calCell";
      if (day) { cell.innerHTML = day; }
      rowB.appendChild(cell);
      cell = document.createElement("div");
      cell.className = "calCell";
      if (day===undefined) { cell.classList.add("calBlank"); }
      if (day!==undefined && day==nowDay) { cell.classList.add("calToday"); }
      rowC.appendChild(cell);
    };
    cal.hCB.innerHTML = ""; rower();

    // (F2-2) BLANK CELLS BEFORE START OF MONTH
    if (cal.mon && cal.sFD != 1) {
      let blanks = cal.sFD==0 ? 7 : cal.sFD ;
      for (let i=1; i<blanks; i++) { celler(); cellNum++; }
    }
    if (!cal.mon && cal.sFD != 0) {
      for (let i=0; i<cal.sFD; i++) { celler(); cellNum++; }
    }

    // (F2-3) DAYS OF THE MONTH
    for (let i=1; i<=cal.sDIM; i++) {
      rowMap[i] = { r : rowNum, c : cellNum };
      celler(i);
      if (cellNum%7==0 && i!=cal.sDIM) { rowNum++; rower(); }
      cellNum++;
    }
    
    // (F2-4) BLANK CELLS AFTER END OF MONTH
    if (cal.mon && cal.sLD != 0) {
      let blanks = cal.sLD==6 ? 1 : 7-cal.sLD;
      for (let i=0; i<blanks; i++) { celler(); cellNum++; }
    }
    if (!cal.mon && cal.sLD != 6) {
      let blanks = cal.sLD==0 ? 6 : 6-cal.sLD;
      for (let i=0; i<blanks; i++) { celler(); cellNum++; }
    }

    // (F3) DRAW EVENTS
    if (Object.keys(cal.events).length > 0) { for (let [id,evt] of Object.entries(cal.events)) {
      // (F3-1) EVENT START & END DAY
      let sd = new Date(evt.date), ed = new Date(evt.date);
      if (sd.getFullYear() < cal.sYear) { sd = 1; }
      else { sd = sd.getMonth()+1 < cal.sMth ? 1 : sd.getDate(); }
      if (ed.getFullYear() > cal.sYear) { ed = cal.sDIM; }
      else { ed = ed.getMonth()+1 > cal.sMth ? cal.sDIM : ed.getDate(); }

      // (F3-2) "MAP" ONTO HTML CALENDAR
      cell = {}; rowNum = 0;
      for (let i=sd; i<=ed; i++) {
        if (rowNum!=rowMap[i]["r"]) {
          cell[rowMap[i]["r"]] = { s:rowMap[i]["c"], e:0 };
          rowNum = rowMap[i]["r"];
        }
        if (cell[rowNum]) { cell[rowNum]["e"] = rowMap[i]["c"]; }
      }

      // (F3-3) DRAW HTML EVENT ROW
      for (let [r,c] of Object.entries(cell)) {
        let o = c.s - 1 - ((r-1) * 7), // event cell offset
            w = c.e - c.s + 1; // event cell width
        rowA = document.getElementById("calRow"+r);
        rowB = document.createElement("div");
        rowB.className = "calRowEvt";
        rowB.innerHTML = cal.events[id]["result"];
        rowB.style.color = "white";
        rowB.style.backgroundColor  = cal.events[id]["color"];;
        rowB.classList.add("w"+w);
        if (o!=0) { rowB.classList.add("o"+o); }
        rowB.onclick = () => cal.show(id);
        rowA.appendChild(rowB);
      }
    }}
  },


};

window.onload = cal.init;