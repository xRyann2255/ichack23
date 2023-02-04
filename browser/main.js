console.log("Welcome to this extension!");

// Using Netmask
// const netmask = new Netmask('10.0.0.0/12');
// console.log(netmask.contains('10.0.8.10'));
// console.log(netmask.contains('192.168.1.20'));

this.setTimeout(() => {
    console.log(getTotalTransferredSize())
}, 5000)

window.addEventListener("beforeunload", function () {
    console.log(getTotalTransferredSize())
}, false)

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
    return entries.reduce((acc, e) => {
        return e && e.transferSize ? acc + e.transferSize : acc;
    }, 0)
}
