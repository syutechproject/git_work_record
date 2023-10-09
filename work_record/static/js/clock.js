function addZero(num) {
  if (num < 10) num = "0" + num;
  return num;
}
function showClock() {
  let nowTime = new Date();
  let nowHour = addZero(nowTime.getHours());
  let nowMin = addZero(nowTime.getMinutes());
  let nowSec = addZero(nowTime.getSeconds());
  if (nowSec % 2) {
    col = ":";
  } else {
    col = " ";
  }
  let realTime = nowHour + col + nowMin;
  document.getElementById("viewTime").innerHTML = realTime;
}
setInterval("showClock()", 10);

function addZero(num) {
  if (num < 10) num = "0" + num;
  return num;
}
function showDay() {
  let now = new Date();
  let nowYear = now.getFullYear();
  let nowMonth = addZero(now.getMonth() + 1);
  let nowDay = addZero(now.getDate());
  let nowWeek = now.getDay();

  let dayWeek = new Array("日", "月", "火", "水", "木", "金", "土");

  let nowYYMMDD =
    nowYear + "年" + nowMonth + "月" + nowDay + "日(" + dayWeek[nowWeek] + ")";
  document.getElementById("viewDay").innerHTML = nowYYMMDD;
}
setInterval("showDay()", 10);
