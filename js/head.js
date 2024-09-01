function genHead () {
    const host = window.location.hostname;
    const port = window.location.port;
    const links = [
        { href: 'status', text: 'Статус' },
        { href: 'configs', text: 'Конфигурационные файлы' },
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
