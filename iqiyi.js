function getCookie(a) {
    var b = document.cookie.split("; ");
    for (var i = 0; i < b.length; i++) {
        var c = b[i].split("=");
        if (a == c[0]) return unescape(c[1])
    }
    return null
}
var req1 = new XMLHttpRequest();
req1.open("GET", "https://static.iqiyi.com/js/common/f6a3054843de4645b34d205a9f377d25.js", false);
req1.onload = function() {
    var a = document.createElement("script");
    a.text = req1.responseText;
    document.getElementsByTagName("head")[0].appendChild(a)
};
req1.send(null);
var src = window.location.href.indexOf("tw.iqiyi.com") != -1 ? "03020031010010000000" : "03020031010000000000";
var movieinfo = playerObject._player.package.engine.adproxy.engine.movieinfo;
var params = "/jp/dash?tvid=" + movieinfo.tvid + "&bid=620&vid=" + movieinfo.vid + "&src=" + src + "&vt=0&rs=1&uid=" + getCookie("P00003") + "&ori=pcw&ps=0&k_uid=" + getCookie("QC005") + "&pt=0&d=0&s=&lid=&cf=&ct=&k_tag=1&ost=0&ppt=0&dfp=" + getCookie("__dfp") + "&locale=zh_cn&k_err_retries=0&qd_v=2&tm=" + (new Date()).getTime() + "&qdy=a&qds=0&k_ft2=8191&callback=NILAODA&ut=1";
window.dashUrl = "https://cache.video.iqiyi.com" + params + "&vf=" + cmd5x(params);