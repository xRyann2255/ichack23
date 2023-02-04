console.log("Welcome to this extension!");

const startTime = Date.now();
const resolver = new doh.DohResolver('https://1.1.1.1/dns-query');

// setInterval(getTotalTransferredSize,1000);

setTimeout(() => {
    getTotalTransferredSize();
}, 15000)

window.onbeforeunload = function () {
    const differenceTime = Date.now() - startTime
    console.log("Time diff, ", differenceTime)
    const size = getTotalTransferredSize()
    console.log(size)

    fetch("http://localhost:3001/example", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"page_view_time": differenceTime, "hosts": aggregated}),
        keepalive: true,
        mode: "no-cors"
    })
}

let aggregated = {};

function getAndSaveIpForHost(host) {
    resolver.query(host, 'A')
        .then(response => {
            // no IP what ?
            if (!response || !response.answers || response.answers.length < 1) return;

            // filter out non-IP values
            let filtered = response.answers.filter(function (answer, index, array) {
                return answer.type === 'A';
            });

            // if none of the values are actual IPs, make another DoH request
            if (filtered.length < 1) {
                getAndSaveIpForHost(response.answers[0]);
                return;
            }

            // it returns multiple IP addresses, but I just take the first one
            aggregated[host]["ip"] = filtered[0].data;

            // debugging
            // console.log("host: " + host + ", IP: " + ip);
        })
        .catch(err => console.error(err));
}

/* https://developer.mozilla.org/en-US/docs/Web/API/Resource_Timing_API/Using_the_Resource_Timing_API */
function getTotalTransferredSize() {
    // Check for support of the PerformanceResourceTiming.*size properties and print their values
    // if supported.
    if (performance === undefined) {
        console.log("= Display Size Data: performance NOT supported");
        return;
    }

    const entries = performance.getEntries();
    if (entries === undefined) {
        console.log("= Display Size Data: performance.getEntriesByType() is NOT supported");
        return;
    }

    entries.forEach(function (entry, index, array) {
        if (!(entry && entry.transferSize && entry.duration)) return;

        try {
            // get just the host from the full resource URL
            let host = new URL(entry.name).host;

            // initialise an entry for this host if it is new
            if (!aggregated[host]) aggregated[host] = {};

            // add to the total transferred data sum, assuming zero if not in structure
            aggregated[host]["transferred"] = (aggregated[host]["transferred"] || 0) + entry.transferSize;
            aggregated[host]["request_time"] = (aggregated[host]["request_time"] || 0) + entry.duration;

            // if we don't have an IP for this host get it from Cloudflare DoH
            if (!aggregated[host]["ip"]) getAndSaveIpForHost(host);
        } catch (err) {
            console.error(err);
        }
    })

    console.log(aggregated);

    return entries.reduce((acc, e) => {

        // console.log(e);
        return e && e.transferSize ? acc + e.transferSize : acc;
    }, 0)
}
