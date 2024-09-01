// node.exe .\js\list-files.js
const fs = require('fs');

const listConfigs = () => {
    const dir = 'output'
    const files = fs.readdirSync(dir);
    var configsList = [];

    for (const file of files) {
        const stats = fs.statSync(`${dir}/${file}`);
        console.log(stats);
        configsList.push(
            {
                name: file,
                mtime: stats.mtime.toLocaleString("ru-RU", {timeZone: "Europe/Moscow"}),
                size: stats.size,
                uri: `/${file}`,
            }
        )
    }
    console.log(configsList)
    return configsList;
}

module.exports = {
    listConfigs,
}
