const port = chrome.runtime.connect({name: "carbonara"});

let processed = 0;

/* https://developer.mozilla.org/en-US/docs/Web/API/Resource_Timing_API/Using_the_Resource_Timing_API */
function processAllMadeRequests() {
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

    if (processed >= entries.length) return;

    for (let i = processed; i < entries.length; i++) {
        let entry = entries[i];

        if (!(entry && entry.transferSize && entry.duration)) return;

        try {
            // get just the host from the full resource URL
            let host = new URL(entry.name).host;

            // send the message
            port.postMessage({
                "parent": document.location.host,
                "host": host,
                "transfer_size": entry.transferSize,
                "duration": entry.duration
            });
        } catch (err) {
            console.error(err);
        }
    }

    processed = entries.length;
}

(() => {
    const interval = setInterval(() => processAllMadeRequests(), 5 * 1000)

    window.onbeforeunload = function () {
        clearInterval(interval)
    }
})()