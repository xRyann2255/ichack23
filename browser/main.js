console.log("WELCOME TO THIS EXTENSIONS")
// const LABEL = "ichack23-ext: timelog"
console.log(window.performance)

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
        if (!e || !e.transferSize)
            return acc
        else 
            return acc + e.transferSize
    }, 0)
}
