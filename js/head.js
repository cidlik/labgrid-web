// Copyright 2024 RnD Center "ELVEES", JSC

function genHead (host, port) {
    const links = [
        { href: 'status', text: 'Статус' },
        { href: 'configs', text: 'Конфигурационные файлы' },
        { href: 'help', text: 'Помощь' },
    ];

    const navbar = document.getElementById('navbar');

    links.forEach(link => {
        const a = document.createElement('a');
        a.href = `http://${host}:${port}/${link.href}`;
        a.textContent = link.text;
        navbar.appendChild(a);
    });
}

module.exports = {
    genHead,
}
