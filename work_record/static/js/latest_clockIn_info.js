let latestClockInDiv = document.getElementById("latestClockInDiv").textContent;

console.log(latestClockInDiv);

if (!(latestClockInDiv === "None")) {
  ltstClockInDivTrim = latestClockInDiv.replace(/\s+/g, "");
  let tempClockInDivNum = ltstClockInDivTrim.slice(1);
  let clockInDivNum = tempClockInDivNum.slice(0, -1);

  let clockInDilety = clockInDivNum.split(",");

  let clockInDivInfoAry = new Array(clockInDilety.length);

  for (let i = 0; i < clockInDilety.length; i++) {
    tempClockInDivInfo = clockInDilety[i].slice(1);
    clockInDivInfoAry[i] = tempClockInDivInfo.slice(0, -1);
  }

  const SERNO = 2;
  const CLOCKINTIME = 4;
  const clockInDivName = { 1: "開始", 2: "終了", 3: "中断", 4: "再開" };
  let sermoClockIn = Number(clockInDivInfoAry[SERNO]);
  document.getElementById("latestClockIn").innerHTML =
    "あなたは" +
    clockInDivInfoAry[CLOCKINTIME] +
    "に" +
    clockInDivName[sermoClockIn] +
    "を押しました";
} else {
  document.getElementById("latestClockIn").innerHTML = "";
}
