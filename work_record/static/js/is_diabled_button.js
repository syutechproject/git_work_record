let latstClockInDiv = document.getElementById("latestClockInDiv").textContent;
console.log("#####latstClockInDiv#####");
console.log(latstClockInDiv);

latstClockInDivTrim = latstClockInDiv.replace(/\s+/g, "");
let tempClockInDivInfo = latstClockInDivTrim.slice(1);
let ClockInDivInfo = tempClockInDivInfo.slice(0, -1);

let clockInDilety = ClockInDivInfo.split(",");

let clockInDivInfoAry = new Array(clockInDilety.length);

for (let i = 0; i < clockInDilety.length; i++) {
  tempClockInDivInfoAry = clockInDilety[i].slice(1);
  clockInDivInfoAry[i] = tempClockInDivInfoAry.slice(0, -1);
}

const SERNO = 2;
let clockInDivNum = clockInDivInfoAry[SERNO];
console.log(clockInDivNum);
const clockInDivDict = { 1: "start", 2: "finish", 3: "stop", 4: "resume" };
let clockInDiv = clockInDivDict[clockInDivNum];

console.log(clockInDiv);

const clockInDivArray = ["start", "finish", "stop", "resume"];

for (let i = 0; i < clockInDivArray.length; i++) {
  if (document.getElementById(clockInDivArray[i]).disabled === true) {
    document.getElementById(clockInDivArray[i]).removeAttribute("disabled");
  }
}

document.getElementById(clockInDiv).setAttribute("disabled", true);
