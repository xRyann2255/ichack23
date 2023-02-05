let buffer = {};
let ips = {};

chrome.webRequest.onCompleted.addListener((event) => {
    try {
        let host = new URL(event.url).host;
        let parent = event.initiator ? new URL(event.initiator).host : host;

        if (!(parent in ips)) ips[parent] = {};
        if (!(host in ips[parent])) ips[parent][host] = {};

        ips[parent][host] = event.ip;
    } catch (e) {
        console.log("ERR: Invalid URL either " + event.initiator + " or " + event.url);
        console.log(event);
    }
}, {urls: ['<all_urls>']});

chrome.runtime.onConnect.addListener(function (port) {
    console.assert(port.name === "carbonara");
    port.onMessage.addListener(function (msg) {
        if (!(msg.host in ips)) console.log("ERR: Do not have IP for this connection: " + msg);

        if (!(msg.parent in buffer)) buffer[msg.parent] = {};
        if (!(msg.host in buffer[msg.parent])) buffer[msg.parent][msg.host] = {};

        buffer[msg.parent][msg.host]["transfer_size"] = (buffer[msg.parent][msg.host]["transfer_size"] || 0) + msg.transfer_size;
        buffer[msg.parent][msg.host]["duration"] = (buffer[msg.parent][msg.host]["duration"] || 0.0) + msg.duration;
        buffer[msg.parent][msg.host]["ip"] = ips[msg.parent][msg.host];
    });
});

let auth = {
    "username": "Ryan",
    "password": "abc"
};

function flushBuffer() {
    buffer["auth"] = auth;
    fetch("http://localhost:3001/example", {
        method: "post", body: JSON.stringify(buffer, function (key, val) {
            if (val == null) return "N/A";
            return val.toFixed ? Number(val.toFixed(3)) : val;
        }), headers: {
            "Content-Type": "application/json", "Accept": "application/json"
        }, mode: "no-cors"
    }).then(request => {
        // console.log(request);
        if (request.ok) buffer = {};
    });
}

function getUsernamePassword() {
    chrome.storage.sync.get({
        username: 'Ryan', password: 'abc'
    }, function (items) {
        auth = {"username": items.username, "password": items.password};
    });
}

const interval = setInterval(() => {
    console.log(buffer);
    flushBuffer();
}, 5 * 1000)


