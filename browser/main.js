<<<<<<< HEAD
console.log("WELCOME TO THIS EXTENSIONS")
=======
console.log("Welcome to this extension!");

// Using Netmask
// const netmask = new Netmask('10.0.0.0/12');
// console.log(netmask.contains('10.0.8.10'));
// console.log(netmask.contains('192.168.1.20'));
>>>>>>> origin/browser-ext

const startTime = Date.now()

window.onbeforeunload = function () {
    const differenceTime = Date.now() - startTime
    console.log("Time diff, ", differenceTime)
    const size = getTotalTransferredSize()
    console.log(size)

    fetch("http://localhost:3001/example", {
        method: "POST",
        body: JSON.stringify({ differenceTime, size }),
        keepalive: true,
        mode: "no-cors"
    })
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
<<<<<<< HEAD
    return entries.reduce((acc, e) => (!e || !e.transferSize) ? acc : acc + e.transferSize, 0)
=======
    return entries.reduce((acc, e) => {
        return e && e.transferSize ? acc + e.transferSize : acc;
    }, 0)
>>>>>>> origin/browser-ext
}
