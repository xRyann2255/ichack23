console.log("Welcome to this extension!");

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
    
    return entries.reduce((acc, e) => e && e.transferSize ? acc + e.transferSize : acc, 0)
}
