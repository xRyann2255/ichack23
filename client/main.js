

function adjustSiteColor(amount, maxAmount) {
    let p = 1 - (amount / maxAmount)
    if (p > 0.5) {
        let r = Math.round(208 + (1 - p) * 2 * 47);
        console.log(r);
        let rHex = r.toString(16)
        console.log(rHex);
        if (rHex.length == 1) {
            rHex = "0" + rHex;
        }
        return "#" + rHex + "ffd0";
    } else {
        let g = Math.round(208 + p * 2 * 47);
        console.log(g);
        let gHex = g.toString(16)
        console.log(gHex);
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
        console.log(r);
        let rHex =r.toString(16)
        console.log(rHex);
        if (rHex.length == 1) {
            rHex = "0" + rHex;
        }
        return "#" + rHex + "ffa0";
    } else {
        let g = Math.round(160 + p * 2 * 95);
        console.log(g);
        let gHex = g.toString(16)
        console.log(gHex);
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
    for (const category of categories) {
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

    for (const category of categories) {
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

        categoryHeader.getElementsByClassName("categoryName")[0].innerHTML = category.name;
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
    loadCategories();
    loadGraph();
}

async function loadCategories() {
    const categories = [
        {
            name: "Streaming", percentage: 0, amount: 0, sites: [
                {name: "Netflix", icon: "https://raw.githubusercontent.com/karlhadwen/netflix/master/public/favicon.ico", percentage: 0, amount: 42.4325},
                {name: "Amazon Prime", icon: "https://upload.wikimedia.org/wikipedia/commons/d/de/Amazon_icon.png", percentage: 0, amount: 24.231742},
                {name: "Disney+", percentage: 0, amount: 5.241}
            ]
        },
        {
            name: "Shopping", percentage: 0, amount: 0, sites: [
                {name: "Amazon", icon: "https://upload.wikimedia.org/wikipedia/commons/d/de/Amazon_icon.png", percentage: 0, amount: 18.5235},
                {name: "Ebay", percentage: 0, amount: 16.1245}
            ]
        }
    ]; await sleep(2000); // TODO: replace when API

    updateCategories(categories);
}

async function loadGraph() {
    const carbonOverTime = [
        {time: new Date("'December 17, 2022 03:24:00"), amount: 50},
        {time: new Date("'December 17, 2022 04:00:00"), amount: 60},
        {time: new Date("'December 17, 2022 05:00:00"), amount: 100},
    ]; await sleep(5000); // TODO: replace when API

    const xValues = [];
    const yValues = [];
    for (const carbonTime of carbonOverTime) {
        xValues.push(carbonTime.time);
        yValues.push(carbonTime.amount);
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

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

window.onload = onLoad;