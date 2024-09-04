const { genHead } = require('./head.js')


async function getStatus() {
    const host = window.location.hostname;
    const port = window.location.port;
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

async function pasteImage() {
    const statussvg = document.getElementById('statussvg');
    let status = await getStatus();
    statussvg.innerHTML = status;
}


function init() {
    genHead()
    pasteImage()
}

init()
