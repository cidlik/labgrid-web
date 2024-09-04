const { genHead } = require('./head.js')
const { buildConfigTable } = require('./list-files.js')


function init() {
    const host = window.location.hostname;
    const port = window.location.port;
    genHead(host, port);
    buildConfigTable(host, port);
}

init()
