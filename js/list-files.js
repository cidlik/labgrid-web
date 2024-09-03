const host = window.location.hostname;
const port = window.location.port;


async function getConfigs() {
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


async function buildConfigTable() {
    const configslist = document.getElementById('configslist');
    let configs = await getConfigs();
    for (const config of configs) {
        const p = document.createElement('p');
        const a = document.createElement('a');
        a.textContent = config['name'];
        a.href = `http://${host}:${port}/api/configs/${config["name"]}`
        p.appendChild(a);
        configslist.appendChild(p);
    }
}


module.exports = {
    buildConfigTable,
}
