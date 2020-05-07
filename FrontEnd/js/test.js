var record = 10;
var maxpage = null;
var currentPage = 1;
var urlPref = "http://localhost:8000/app/"

function init() {
    getMaxPage(10);
    setTimeout(()=>{turnPageByNumber(1);}, 100);
}

/**
 * Turn player pages
 * @param {HTMLElement} obj 
 */
function turnPage(obj) {
    clearTableContainer();
    
    var page = null;
    Number.parseInt(obj.innerText);
    getPage(page, record);
    console.log("Page"+page);
    console.log("MaxPage"+maxpage);
    var tmp = null;
    var i;

    if (page <= 2) {
        console.log(1);
        for(i=1; i<=5; i++) {
            tmp = document.getElementById("p-"+i);
            tmp.firstChild.innerText = i;
            tmp.classList.remove("active");
        }
        obj.parentElement.classList.add("active");
    } else if (page <= maxpage - 2) {
        console.log(2);
        for(i=1; i<=5; i++) {
            tmp = document.getElementById("p-"+i);
            tmp.firstChild.innerText = page + (i-3);
            tmp.classList.remove("active");
        }
        document.getElementById("p-3").classList.add("active");
    } else {
        console.log(3);
        for(i=1; i<=5; i++) {
            tmp = document.getElementById("p-"+i);
            tmp.firstChild.innerText = maxpage-(5-i);
            tmp.classList.remove("active");
        }
        obj.parentElement.classList.add("active");
    }
}

function turnPageByNumber(page) {
    console.log("Turn");
    clearTableContainer();
    getPage(page, record);
    var pag = document.getElementById("pagination");
    pag.innerHTML = '';
    // First page btn
    pag.innerHTML += ('<li class="page-item"><a class="page-link" href="#" onclick="turnPageByNumber('+ 1 +')">'+ 'First' +'</a></li>');
    // Prev page btn
    if (page != 1) {
        pag.innerHTML += ('<li class="page-item"><a class="page-link" href="#" onclick="turnPageByNumber('+ (page-1) +')">'+ '<<' +'</a></li>');
    } else {
        pag.innerHTML += ('<li class="page-item disabled"><a class="page-link" href="#" onclick="turnPageByNumber('+ (page-1) +')">'+ '<<' +'</a></li>');
    }
    // Middle
    if (page <= 2) {
        for(i=1; i<=5; i++) {
            if(i==page){
                pag.innerHTML += ('<li class="page-item active"><a class="page-link" href="#" onclick="turnPageByNumber('+ i +')">'+ i +'</a></li>');
            } else {
                pag.innerHTML += ('<li class="page-item"><a class="page-link" href="#" onclick="turnPageByNumber('+ i +')">'+ i +'</a></li>');
            }
        }
    } else if (page <= maxpage - 2) {
        for(i=1; i<=5; i++) {
            if(i == 3){
                pag.innerHTML += ('<li class="page-item active"><a class="page-link" href="#" onclick="turnPageByNumber('+ (page + (i-3)) +')">'+ (page + (i-3)) +'</a></li>');
            } else {
                pag.innerHTML += ('<li class="page-item"><a class="page-link" href="#" onclick="turnPageByNumber('+ (page + (i-3)) +')">'+ (page + (i-3)) +'</a></li>');
            }
        }
    } else {
        for(i=1; i<=5; i++) {
            if(page == maxpage-(5-i)) {
                pag.innerHTML += ('<li class="page-item active"><a class="page-link" href="#" onclick="turnPageByNumber('+ (maxpage-(5-i)) +')">'+ (maxpage-(5-i)) +'</a></li>');
            } else {
                pag.innerHTML += ('<li class="page-item"><a class="page-link" href="#" onclick="turnPageByNumber('+ (maxpage-(5-i)) +')">'+ (maxpage-(5-i)) +'</a></li>');
            }
        }
    }
    // Next page btn
    if (page != maxpage) {
        pag.innerHTML += ('<li class="page-item"><a class="page-link" href="#" onclick="turnPageByNumber('+ (page+1) +')">'+ '>>' +'</a></li>');
    } else {
        pag.innerHTML += ('<li class="page-item disabled"><a class="page-link" href="#" onclick="turnPageByNumber('+ (page+1) +')">'+ '>>' +'</a></li>');
    }
    // Last page btn
    pag.innerHTML += ('<li class="page-item"><a class="page-link" href="#" onclick="turnPageByNumber('+ (maxpage) +')">'+ 'Last' +'</a></li>');

    currentPage = page;
}

function clearTableContainer() {
    var obj = document.getElementById("mainInject");
    obj.innerHTML = "";
}

/**
 * Get data from backend and render it to the front end.
 * @param {Number} page 
 * @param {Number} records 
 */
function getPage(page, records) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", urlPref + "data?page=" + page + "&record=" + records);
    xhr.onreadystatechange = function () {
        if (xhr.status == 200 && xhr.readyState == 4) {
            renderData(JSON.parse(JSON.parse(xhr.responseText).data));
        }
    };
    xhr.send();
}

/**
 * Render data to the front end.
 * @param {JSON} data 
 */
function renderData(data) {
    var tbody = document.getElementById("mainInject");
    for(var i=0; i<data.length; i++) {
        var tr = document.createElement("tr");
        var td = document.createElement("td");
        var img = document.createElement("img");
        if(data[i]["Real Face"] == 'Yes') {
            img.src = photoUrlRefactory(data[i]["Photo"]);
        } else {
            img.src = "https://cdn.sofifa.com/players/notfound_0_60.png";
        }
        img.alt = "Photo";
        td.appendChild(img)
        tr.appendChild(td);
        var dataColumns = ["Name", "Age", "Nationality", "Position", "Overall"]
        for(var j=0; j<dataColumns.length; j++) {
            var td2 = document.createElement("td");
            td2.textContent = data[i][dataColumns[j]];
            tr.appendChild(td2);
        }
        tbody.appendChild(tr);
    }
    
}

/**
 * Turn useless photo url into one that actually works.
 * @param {String} string 
 */
function photoUrlRefactory(string) {
    var regex = /4\/19\/(\d*).png/;
    res = regex.exec(string)[1];
    result = "https://cdn.sofifa.com/players/";
    if (res.length == 6) {
        result = result + res.substring(0,3) + '/' + res.substring(3,6) + '/19_60.png';
    } else if (res.length == 5) {
        result = result + '0' + res.substring(0,2) + '/' + res.substring(2,5) + '/19_60.png';
    } else if (res.length == 4) {
        result = result + '00' + res.substring(0,1) + '/' + res.substring(1,4) + '/19_60.png';
    } else {
        result = result + '000/';
        for(var i=0; i<3-res.length; i++) {
            result += '0';
        }
        result += res;
        result += '/19_60.png';
    }
    return result;
}

/**
 * Retreive maxium pages from server.
 * @param {Number} record 
 */
function getMaxPage(record) {
    ajax("GET", urlPref + "maxpages?record="+record).then(function(data) {
        maxpage = Number.parseInt(data);
        console.log(maxpage);
    });
}

/**
 * Integrated ajax method. Returns a promise.
 * @param {String} method 
 * @param {String} url 
 */
function ajax(method, url) {
    return new Promise(function(resolve, reject){
        var xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onreadystatechange = function () {
            if (xhr.status == 200 && xhr.readyState == 4) {
                jason = JSON.parse(xhr.responseText).data;
                resolve(jason);
            }
        };
        
        xhr.send();
    })
}

/**
 * Query for best players.
 */
function submitBestPlayer() {
    var backform = document.querySelectorAll("form[name=back] input");
    var midform = document.querySelectorAll("form[name=mid] input");
    var frontform = document.querySelectorAll("form[name=front] input");
    
    var backContainer = [];
    var midContainer = [];
    var frontContainer = [];
    
    var i = null;
    var tmp;
    for(i=0; i<back.length; i++) {
        tmp = back[i];
        if (tmp.checked) {
            backContainer.push(tmp.value);
        }
    }

    for(i=0; i<mid.length; i++) {
        tmp = mid[i];
        if (tmp.checked) {
            midContainer.push(tmp.value);
        }
    }

    for(i=0; i<front.length; i++) {
        tmp = front[i];
        if (tmp.checked) {
            frontContainer.push(tmp.value);
        }
    }
    if(backContainer.length + midContainer.length + frontContainer.length != 10) {
        return;
    }

    // Submit
    var xhr = new XMLHttpRequest();
    xhr.open("POST", urlPref+"team");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4 && xhr.status == 200) {
            renderFootballField(JSON.parse(xhr.responseText).data);
        }
    }
    obj = {
        "back": backContainer, 
        "mid": midContainer,
        "front": frontContainer
    }
    jason = JSON.stringify(obj);
    xhr.send(jason);
}

/**
 * Render a football field with data(optional)
 * @param {CanvasRenderingContext2D} ctx 
 */
function renderFootballField(data = null) {
    var obj = document.createElement("canvas");
    var H = 500;
    var W = 1000;
    obj.width = W;
    obj.height = H;
    var ctx = obj.getContext('2d');
    //Fill background
    ctx.fillStyle="#B4FF00";
    ctx.lineWidth = 5;
    ctx.strokeStyle="#FFFFFF";
    ctx.fillRect(0,0,W,H);
    //GK Left
    ctx.moveTo(0, 0.2*H);
    ctx.lineTo(0.1*W, 0.2*H);
    ctx.lineTo(0.1*W, 0.8*H);
    ctx.lineTo(0, 0.8*H);
    ctx.stroke();
    //GK Right
    ctx.moveTo(W, H-0.2*H);
    ctx.lineTo(W-0.1*W, H-0.2*H);
    ctx.lineTo(W-0.1*W, H-0.8*H);
    ctx.lineTo(W, H-0.8*H);
    ctx.stroke();
    //Middle Line
    ctx.moveTo(0.5*W, 0);
    ctx.lineTo(0.5*W, H);
    ctx.stroke();
    //Circle
    ctx.beginPath();
    ctx.arc(0.5*W, 0.5*H, 0.1*W, 0, 360)
    ctx.stroke();
    //Define position table
    positionTable = {
        //Most Front Strikers
        'LS': [0.8*W, 0.2*H],
        'ST': [0.8*W, 0.5*H],
        'RS': [0.8*W, 0.8*H],
        //Front Strikers
        'LF': [0.7*W, 0.2*H],
        'CF': [0.7*W, 0.5*H],
        'RF': [0.7*W, 0.8*H],
        'LW': [0.7*W, 0.1*H],
        'RW': [0.7*W, 0.9*H],
        //Mid-Front Offensive
        'LAM': [0.6*W, 0.3*H],
        'CAM': [0.6*W, 0.5*H],
        'RAM': [0.6*W, 0.8*H],
        //Mid Fielders
        'LM': [0.5*W, 0.2*H],
        'LCM':[0.5*W, 0.3*H],
        'CM': [0.5*W, 0.5*H],
        'RCM': [0.5*W, 0.7*H],
        'RM': [0.5*W, 0.8*H],
        //Mid-Back Defensive
        'LDM': [0.4*W, 0.2*H],
        'CDM': [0.4*W, 0.5*H],
        'RDM': [0.4*W, 0.8*H],
        //Back Defensive
        'LWB': [0.3*W, 0.1*H],
        'RWB': [0.3*W, 0.9*H],
        'LB': [0.3*W, 0.3*H],
        'LCB': [0.3*W, 0.3*H],
        'CB': [0.3*W, 0.5*H],
        //Goal Keeper
        'GK': [0.05*W, 0.5*H],
    };
    
    if (data != null) {
        var positionTuple = null;
        
        for(var i in data){
            ctx.fillStyle = "#00A8F3";  //Aqua blue
            positionTuple = positionTable[i];
            console.log(positionTuple)
            ctx.beginPath();
            ctx.arc(positionTuple[0], positionTuple[1], 16, 0, 360);
            ctx.fill();
            ctx.fillStyle = "#000000";  //White
            ctx.fillText(data[i], positionTuple[0]+16, positionTuple[1]);   //Player's Name
            ctx.fillText(i, positionTuple[0]+16, positionTuple[1]+16);   //Player's Position
        }
    }
    var _ = document.getElementById("c-canvas-container")
    _.innerHTML = "";
    _.appendChild(obj);
}