const { genHead } = require('./head.js')


async function getStatus(host, port) {
    try {
        let response = await fetch(`http://${host}:${port}/api/status`);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
          }
        return await response.text();
    } catch (error) {
        console.error(error.message);
    }
}

async function pasteImage(host, port) {
    const statussvg = document.getElementById('statussvg');
    let status = await getStatus(host, port);
    statussvg.innerHTML = status;
}


function init() {
    const host = window.location.hostname;
    const port = window.location.port;
    genHead(host, port);
    pasteImage(host, port);
}

init()
