// Copyright 2024 RnD Center "ELVEES", JSC

const { genHead } = require('./head.js')


function init() {
    const host = window.location.hostname;
    const port = window.location.port;
    genHead(host, port);
}

init();
