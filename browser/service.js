chrome.runtime.onInstalled.addListener(() => {
    const sentUrls = []
    chrome.tabs.onUpdated.addListener((tabId, tab) => {
        if (!tab.url) {
            return;
        }
        console.log(chrome)

        // chrome.tabs.sendMessage(tabId, {
        //     type: "NEW",
        //     url: tab.url
        // })

        chrome.runtime.onMessage.addListener((data) => {
            const index = data.url + data["page_view_time"]
            if(sentUrls.indexOf(index) === -1) {
                fetch("http://localhost:3001/example", {
                    method: "post",
                    body: JSON.stringify(data),
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    mode: "no-cors"
                })
                sentUrls.push(index)
            }
            return true;
        })
    })
})