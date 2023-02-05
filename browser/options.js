// Saves options to chrome.storage
function save_options() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    chrome.storage.sync.set({
        username: username, password: password
    }, function () {
        // Update status to let user know options were saved.
        const status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(function () {
            status.textContent = '';
        }, 750);
    });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
    // Use default value color = 'red' and likesColor = true.
    chrome.storage.sync.get({
        username: 'Ryan', password: 'abc'
    }, function (items) {
        document.getElementById('username').value = items.username;
        document.getElementById('password').value = items.password;
    });
}

document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click', save_options);