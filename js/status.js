// Copyright 2024 RnD Center "ELVEES", JSC

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

async function pastePlaces(host, port) {
    const status = document.getElementById('status');
    const raw = await getStatus(host, port);
    const data = JSON.parse(raw);
    for (const [place_name, place_value] of Object.entries(data)) {
        console.log(place_name, place_value);
        const table = document.createElement("table");
        // place name
        let row = table.insertRow();
        let cell = row.insertCell();
        cell.textContent = place_name;
        // acquired status
        row = table.insertRow()
        cell = row.insertCell();
        cell.textContent = `Acquired: ${place_value["acquired"]}`;
        // resources
        row = table.insertRow()
        cell = row.insertCell();
        const spoiler = document.createElement("details");
        const spoiler_table = document.createElement("table");
        let spoiler_row, spoiler_cell;
        for (const [resource_name, resource_value] of Object.entries(place_value["resources"])) {
            console.log(`${resource_name}:${resource_value}`);
            spoiler_row = spoiler_table.insertRow();
            spoiler_cell = spoiler_row.insertCell();
            spoiler_cell.textContent = resource_name;
            spoiler_cell = spoiler_row.insertCell();
            let r_arg_table, r_arg_row, r_arg_cell;
            r_arg_table = document.createElement("table");
            for (const [r_arg_name, r_arg_value] of Object.entries(resource_value)) {
                console.log(`${r_arg_name}:${r_arg_value}`);
                r_arg_row = r_arg_table.insertRow();
                r_arg_cell = r_arg_row.insertCell();
                r_arg_cell.textContent = r_arg_name;
                r_arg_cell = r_arg_row.insertCell();
                r_arg_cell.textContent = r_arg_value;
            }
            spoiler_cell.appendChild(r_arg_table);
        }
        spoiler.appendChild(spoiler_table);
        cell.appendChild(spoiler);
        status.appendChild(table);
    }
}


function init() {
    const host = window.location.hostname;
    const port = window.location.port;
    genHead(host, port);
    pastePlaces(host, port);
}

init();
