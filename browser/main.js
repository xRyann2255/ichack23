console.log("WELCOME TO THIS EXTENSIONS")
// const LABEL = "ichack23-ext: timelog"
console.log(window.performance)

window.addEventListener("DOMContentLoaded", function () {
    display_size_data()
})

window.addEventListener("beforeunload", function () {
    // console.timeEnd(LABEL)
})

/* https://developer.mozilla.org/en-US/docs/Web/API/Resource_Timing_API/Using_the_Resource_Timing_API */
function calculate_load_times() {
    // Check performance support
    if (performance === undefined) {
        console.log("= Calculate Load Times: performance NOT supported");
        return;
    }

    // Get a list of "resource" performance entries
    const resources = performance.getEntriesByType("resource");
    if (resources === undefined || resources.length <= 0) {
        console.log("= Calculate Load Times: there are NO `resource` performance records");
        return;
    }

    console.log("= Calculate Load Times");
    resources.forEach((resource, i) => {
        console.log(`== Resource[${i}] - ${resource.name}`);
        // Redirect time
        let t = resource.redirectEnd - resource.redirectStart;
        console.log(`… Redirect time = ${t}`);

        // DNS time
        t = resource.domainLookupEnd - resource.domainLookupStart;
        console.log(`… DNS lookup time = ${t}`);

        // TCP handshake time
        t = resource.connectEnd - resource.connectStart;
        console.log(`… TCP time = ${t}`);

        // Secure connection time
        t = (resource.secureConnectionStart > 0) ? (resource.connectEnd - resource.secureConnectionStart) : "0";
        console.log(`… Secure connection time = ${t}`);

        // Response time
        t = resource.responseEnd - resource.responseStart;
        console.log(`… Response time = ${t}`);

        // Fetch until response end
        t = (resource.fetchStart > 0) ? (resource.responseEnd - resource.fetchStart) : "0";
        console.log(`… Fetch until response end time = ${t}`);

        // Request start until response end
        t = (resource.requestStart > 0) ? (resource.responseEnd - resource.requestStart) : "0";
        console.log(`… Request start until response end time = ${t}`);

        // Start until response end
        t = (resource.startTime > 0) ? (resource.responseEnd - resource.startTime) : "0";
        console.log(`… Start until response end time = ${t}`);
    });
}

function display_size_data() {
    // Check for support of the PerformanceResourceTiming.*size properties and print their values
    // if supported.
    if (performance === undefined) {
        console.log("= Display Size Data: performance NOT supported");
        return;
    }

    const supportedEntries = PerformanceObserver.supportedEntryTypes
    for (supportedEntry of supportedEntries) {
        console.log(supportedEntry)
        const entries = performance.getEntriesByType(supportedEntry);
        if (entries === undefined) {
            console.log("= Display Size Data: performance.getEntriesByType() is NOT supported");
            return;
        }

        // For each "resource", display its *Size property values
        console.log("= Display Size Data");
        entries.forEach((entry, i) => {
            console.log(`== Resource[${i}] - ${entry.name}`);
            if ("decodedBodySize" in entry) {
                console.log(`… decodedBodySize[${i}] = ${entry.decodedBodySize}`);
            } else {
                console.log(`… decodedBodySize[${i}] = NOT supported`);
            }

            if ("encodedBodySize" in entry) {
                console.log(`… encodedBodySize[${i}] = ${entry.encodedBodySize}`);
            } else {
                console.log(`… encodedBodySize[${i}] = NOT supported`);
            }

            if ("transferSize" in entry) {
                console.log(`… transferSize[${i}] = ${entry.transferSize}`);
            } else {
                console.log(`… transferSize[${i}] = NOT supported`);
            }
        });

    }

    //   const entries = performance.getEntriesByType("resource");
    //   if (entries === undefined) {
    //     console.log("= Display Size Data: performance.getEntriesByType() is NOT supported");
    //     return;
    //   }

    //   // For each "resource", display its *Size property values
    //   console.log("= Display Size Data");
    //   entries.forEach((entry, i) => {
    //     console.log(`== Resource[${i}] - ${entry.name}`);
    //     if ("decodedBodySize" in entry) {
    //       console.log(`… decodedBodySize[${i}] = ${entry.decodedBodySize}`);
    //     } else {
    //       console.log(`… decodedBodySize[${i}] = NOT supported`);
    //     }

    //     if ("encodedBodySize" in entry) {
    //       console.log(`… encodedBodySize[${i}] = ${entry.encodedBodySize}`);
    //     } else {
    //       console.log(`… encodedBodySize[${i}] = NOT supported`);
    //     }

    //     if ("transferSize" in entry) {
    //       console.log(`… transferSize[${i}] = ${entry.transferSize}`);
    //     } else {
    //       console.log(`… transferSize[${i}] = NOT supported`);
    //     }
    //   });
}