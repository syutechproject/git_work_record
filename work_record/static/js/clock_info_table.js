window.onload = function () {
  let clockInHistory = document.getElementById("clockInHistory").textContent;

  clockInHistoryTrim = clockInHistory.replace(/\s+/g, "");

  if (clockInHistoryTrim.indexOf("[") != -1) {
    clockInHistoryTrim = clockInHistoryTrim.slice(1);
    clockInHistoryTrim = clockInHistoryTrim.slice(0, -1);
  }

  let tempClockInHistory = clockInHistoryTrim.slice(1);
  let modClockInHistory = tempClockInHistory.replace(/\)/g, "");

  let clockInHistoryAry = modClockInHistory.split(",(");

  let table = document.createElement("table");
  let tr = document.createElement("tr");
  let th1 = document.createElement("th");
  let th2 = document.createElement("th");
  let th3 = document.createElement("th");

  th1.textContent = "日付";
  tr.appendChild(th1);
  table.appendChild(tr);
  th2.textContent = "時刻";
  tr.appendChild(th2);
  table.appendChild(tr);
  th3.textContent = "区分";
  tr.appendChild(th3);
  table.appendChild(tr);

  for (let i = 0; i < clockInHistoryAry.length; i++) {
    let strClockInHistory = clockInHistoryAry[i].split(",");
    let strClockInAry = new Array(strClockInHistory.length);

    for (let j = 0; j < strClockInHistory.length; j++) {
      tempStrClockInHistory = strClockInHistory[j].slice(1);
      strClockInAry[j] = tempStrClockInHistory.slice(0, -1);
    }
    const CLOCK_IN_DIV_NUM = 2;
    const clockin_div = Number(strClockInAry[CLOCK_IN_DIV_NUM]);
    const clockInDivName = { 1: "開始", 2: "終了", 3: "中断", 4: "再開" };
    strClockInAry[CLOCK_IN_DIV_NUM] = clockInDivName[clockin_div];

    let tr = document.createElement("tr");
    let td1 = document.createElement("td");
    let td2 = document.createElement("td");
    let td3 = document.createElement("td");

    const TIME = 1;
    const DTAE = 4;
    const CLOCK_IN_DIV = 2;

    td1.textContent = strClockInAry[TIME];
    tr.appendChild(td1);
    table.appendChild(tr);
    td2.textContent = strClockInAry[DTAE];
    tr.appendChild(td2);
    table.appendChild(tr);
    td3.textContent = strClockInAry[CLOCK_IN_DIV];
    tr.appendChild(td3);
    table.appendChild(tr);
  }

  document.getElementById("maintable").appendChild(table);
};
