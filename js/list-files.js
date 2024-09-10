// Copyright 2024 RnD Center "ELVEES", JSC

async function getConfigs(host, port) {
    try {
        let response = await fetch(`http://${host}:${port}/api/configs`);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
          }
        return await response.json();
    } catch (error) {
        console.error(error.message);
    }
}


async function buildConfigTable(host, port) {
    const configslist = document.getElementById('configslist');
    const configs = await getConfigs(host, port);

    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tr = document.createElement('tr')
    for (header of ["Имя файла", "Время изменения", "Размер, Б"]) {
        const th = document.createElement("th");
        th.textContent = header;
        tr.append(th);
    }
    thead.appendChild(tr);
    table.appendChild(thead);
    for (const config of configs) {
        const row = table.insertRow();
        // config name
        let cell = row.insertCell();
        const a = document.createElement('a');
        a.textContent = config['name'];
        a.href = `http://${host}:${port}/api/configs/${config["name"]}`
        cell.appendChild(a);
        // modify time
        cell = row.insertCell();
        cell.textContent = config["mtime"];
        // size
        cell = row.insertCell();
        cell.textContent = config["size"];

    }
    configslist.appendChild(table);
}


module.exports = {
    buildConfigTable,
}
