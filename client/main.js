let USERNAME;
let PASSWORD;

function adjustSiteColor(amount, maxAmount) {
    let p = 1 - (amount / maxAmount)
    if (p > 0.5) {
        let r = Math.round(208 + (1 - p) * 2 * 47);
        let rHex = r.toString(16)
        if (rHex.length == 1) {
            rHex = "0" + rHex;
        }
        return "#" + rHex + "ffd0";
    } else {
        let g = Math.round(208 + p * 2 * 47);
        let gHex = g.toString(16)
        if (gHex.length == 1) {
            gHex = "0" + gHex;
        }
        return "#FF" + gHex + "d0";
    }
}

function adjustCategoryColor(amount, maxAmount) {
    let p = 1 - (amount / maxAmount)
    if (p > 0.5) {
        let r = Math.round(160 + (1 - p) * 2 * 95);
        let rHex = r.toString(16)
        if (rHex.length == 1) {
            rHex = "0" + rHex;
        }
        return "#" + rHex + "ffa0";
    } else {
        let g = Math.round(160 + p * 2 * 95);
        let gHex = g.toString(16)
        if (gHex.length == 1) {
            gHex = "0" + gHex;
        }
        return "#FF" + gHex + "a0";
    }
}

// call after update to `categories` variable, will update the statistics table
function updateCategories(categories) {
    let categoriesElement = document.getElementById("categories");
    categoriesElement.replaceChildren();
    // getting totals
    let total = 0;
    let maxCategoryAmount = 0;
    let maxSiteAmount = 0;
    for (const key in categories) {
        let category = categories[key]
        let categoryTotal = 0;
        for (const site of category.sites) {
            categoryTotal += site.amount;
            maxSiteAmount = Math.max(maxSiteAmount, site.amount);
        }
        category.amount = categoryTotal;
        maxCategoryAmount = Math.max(maxCategoryAmount, category.amount);
        total += categoryTotal;
    }

    let categoryTemplate = document.getElementById("templates").getElementsByClassName("category")[0]
    let siteTemplate = document.getElementById("templates").getElementsByClassName("site")[0]

    for (const key in categories) {
        let category = categories[key]
        let categoryElement = categoryTemplate.cloneNode(true)
        for (const site of category.sites) {
            site.percentage = Math.round(site.amount / total * 100);
        }
        category.percentage = Math.round(category.amount / total * 100);

        for (const site of category.sites) {
            let siteElement = siteTemplate.cloneNode(true)
            categoryElement.appendChild(siteElement);

            siteElement.getElementsByClassName("siteIcon")[0].src = site.icon;
            siteElement.getElementsByClassName("siteName")[0].innerHTML = site.name;
            siteElement.getElementsByClassName("siteAmount")[0].innerHTML = Math.round(site.amount * 100) / 100 + " kg";
            siteElement.getElementsByClassName("sitePercent")[0].innerHTML = "(" + Math.round(site.percentage * 100) / 100 + "%)";

            siteElement.style.backgroundColor = adjustSiteColor(site.amount, maxSiteAmount);
        }

        categoryElement.classList.add("categoryCollapse")

        let categoryHeader = categoryElement.getElementsByClassName("categoryHeader")[0];

        categoryHeader.getElementsByClassName("categoryName")[0].innerHTML = key;
        categoryHeader.getElementsByClassName("categoryAmount")[0].innerHTML = Math.round(category.amount * 100) / 100 + " kg";
        categoryHeader.getElementsByClassName("categoryPercent")[0].innerHTML = "(" + Math.round(category.percentage * 100) / 100 + "%)";
        categoryHeader.style.backgroundColor = adjustCategoryColor(category.amount, maxCategoryAmount);

        categoriesElement.appendChild(categoryElement);
    }

    document.getElementById("statsKg").innerHTML = Math.round(total * 100) / 100 + " kg"
}


function toggleCollapse(element) {
    element.classList.toggle("categoryCollapse")
}

function onLoad() {
}

async function loadCategories() {
    const categories = {
        "Streaming": {percentage: 0, amount: 0, sites: [
                {name: "Netflix", icon: "https://raw.githubusercontent.com/karlhadwen/netflix/master/public/favicon.ico", percentage: 0, amount: 42.4325},
                {name: "Amazon Prime", icon: "https://upload.wikimedia.org/wikipedia/commons/d/de/Amazon_icon.png", percentage: 0, amount: 24.231742},
                {name: "Disney+", percentage: 0, amount: 5.241}
            ]
        }, "Shopping": {percentage: 0, amount: 0, sites: [
                {name: "Amazon", icon: "https://upload.wikimedia.org/wikipedia/commons/d/de/Amazon_icon.png", percentage: 0, amount: 18.5235},
                {name: "Ebay", percentage: 0, amount: 16.1245}
            ]
        }
    };
    const data = await fetch(
            "http://localhost:5000/api/"+USERNAME+"?password="+PASSWORD
        ).then(response => response.json());
    console.log(data);
    updateCategories(JSON.parse(data));
}

async function loadGraph() {
    const carbonOverTime = [
        [new Date("'December 17, 2022 03:24:00"), 50],
        [new Date("'December 17, 2022 04:00:00"), 60],
        [new Date("'December 17, 2022 05:00:00"), 100],
    ];

    var data = await fetch("http://localhost:5000/graph/"+USERNAME+"?password="+PASSWORD).then(response => response.json());
    console.log("Pear "+data);

    const xValues = [];
    const yValues = [];
    for (const carbonTime of carbonOverTime) {
        xValues.push(carbonTime[0]);
        yValues.push(carbonTime[1]);
    }

    const config = {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "rgba(0,0,0,1.0)",
                borderColor: "rgba(0,0,0,0.1)",
                data: yValues
            }]
        },
        options: {
            plugins: {
                legend: {display: false}
            },
            scales: {
                x: {
                    type: 'time'
                },
                y: {
                    min: 0
                }
            }
        }
    }

    const myChart = new Chart("carbonPerTime", config);
}

async function loadLeaderboard() {
    // const players = [
    //     {name: "Jack", amount: 52.73532532},
    //     {name: "Jim", amount: 253.7142893},
    //     {name: "Timothy", amount: 521.7142893},
    //     {name: "Nishant", amount: 525.4322893},
    //     {name: "Alex", amount: 598.3245434},
    //     {name: "Ryan", amount: 1089.57418789325}
    // ];
    // add type switch, as additional arg "type" = local/friends
    let data = await fetch("http://localhost:5000/leaderboard/"+USERNAME+"?password="+PASSWORD).then(response => response.json());
    console.log("banana"+data);
    const players = JSON.parse(data);

    let leaderboardElement = document.getElementById("leaderboard");
    leaderboardElement.replaceChildren();

    let headerTemplate = document.getElementById("templates").getElementsByClassName("leaderboard-header")[0]
    leaderboardElement.appendChild(headerTemplate.cloneNode(true));

    let rowElement = document.getElementById("templates").getElementsByClassName("leaderboard-row")[0]

    let rank = 0;
    for (const player of players) {
        rank++;
        let e = rowElement.cloneNode(true);
        e.getElementsByClassName("leaderboardName")[0].innerHTML = player.name;
        e.getElementsByClassName("leaderboardRank")[0].innerHTML = rank;
        e.getElementsByClassName("leaderboardAmount")[0].innerHTML = Math.round(player.amount * 100) / 100 + " kg";
        leaderboardElement.appendChild(e);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function leaderboardSlide() {
    let slider = document.getElementById("slider");
    slider.classList.add("slide2")
}

function mainSlide() {
    let slider = document.getElementById("slider");
    slider.classList.remove("slide3")
    slider.classList.remove("slide2")
}

async function addFriend() {
    // TODO: Connect to API
    var other = document.getElementById("friendField").value;
    let data = await fetch("http://localhost:5000/friends/"+USERNAME+"?password="+PASSWORD+"&other="+other).then(response => response.json());
    // console.log("coconut"+data);
    hideAddFriend();
    loadLeaderboard();
}

function showAddFriend() {
    document.getElementById("friendpopup").style.top = "50%";
}

function hideAddFriend() {
    document.getElementById("friendpopup").style.top = "-50%";
}

async function login() {
    let name = document.getElementById("nameField").value;
    let passwd = document.getElementById("passField").value;

    USERNAME = name;
    PASSWORD = passwd;

    let data = await fetch("http://localhost:5000/login?username=" + name + "&password=" + passwd);
    console.log(data)

    // TODO: connect to API
    if (data.status === 200) {
        loadCategories();
        loadGraph();
        loadLeaderboard();
        mainSlide();
    }
}

async function register() {
    let name = document.getElementById("nameField").value;
    let passwd = document.getElementById("passField").value;
    await fetch("http://localhost:5000/login", {
        method: "POST",
        body: JSON.stringify({
            username: name,
            password: passwd
        })
    });
    login();
}

window.onload = onLoad;