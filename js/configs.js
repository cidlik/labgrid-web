const { genHead } = require('./head.js')
const { buildConfigTable } = require('./list-files.js')


function init() {
    genHead();
    buildConfigTable();
}

init()
