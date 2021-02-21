const fs = require('fs');
const discord = require('discord.js');
const http = require('http');

const server = http.createServer((req, res) => {
// Set the response HTTP header with HTTP status and Content type
res.writeHead(200, {'Content-Type': 'text/plain'});
// Send the response body "Hello World"
res.end('The bot is online\n');
});
const port = 8080
server.listen(port, () => {
console.log('Hello world listening on port', port);
});




const client = new discord.Client({ disableMentions: 'everyone' });

const { Player } = require('discord-player');
const help = require('./commands/core/help');

client.player = new Player(client);
client.config = require('./config/bot');
client.emotes = client.config.emojis;
client.filters = client.config.filters;
client.commands = new discord.Collection();


fs.readdirSync('./commands').forEach(dirs => {
    const commands = fs.readdirSync(`./commands/${dirs}`).filter(files => files.endsWith('.js'));

    for (const file of commands) {
        const command = require(`./commands/${dirs}/${file}`);
        console.log(`Loading command ${file}`);
        client.commands.set(command.name.toLowerCase(), command);
    };
});


client.ws.on('INTERACTION_CREATE', async interaction => {
    const infos = client.commands.filter(x => x.category == 'Infos').map((x) => '`' + x.name + '`').join(', ');
    const music = client.commands.filter(x => x.category == 'Music').map((x) => '`' + x.name + '`').join(', ');
    const others = client.commands.filter(x => x.category == 'Others').map((x) => '`' + x.name + '`').join(', ');
    const mod = client.commands.filter(x => x.category == 'Modération').map((x) => '`' + x.name + '`').join(', ');
    const meme = client.commands.filter(x => x.category == 'meme').map((x) => '`' + x.name + '`').join(', ');
    const amus = client.commands.filter(x => x.category == 'Among Us').map((x) => '`' + x.name + '`').join(', ');
    client.api.interactions(interaction.id, interaction.token).callback.post({data: {
      type: 4,
      data: {
        embeds: [
            {
                color: 'ORANGE',
                author: { name: 'Help pannel' },
                footer: { text: '' },
                fields: [
                    { name: 'Bot', value: infos },
                    { name: 'Autre', value: others },
                    { name: 'Modération', value: mod },
                    { name: 'meme', value: meme },
                    { name: 'Among Us', value: amus },
                    { name: 'Musique', value: music },
                    { name: 'Filtres', value: client.filters.map((x) => '`' + x + '`').join(', ') },
                ],
                timestamp: new Date(),
                description: `To use filters, ${client.config.discord.prefix}filter (the filter). Example : ${client.config.discord.prefix}filter 8D.`,
            }
        ]
        }
      }
    })
})


const events = fs.readdirSync('./events').filter(file => file.endsWith('.js'));
const player = fs.readdirSync('./player').filter(file => file.endsWith('.js'));

for (const file of events) {
    console.log(`Loading discord.js event ${file}`);
    const event = require(`./events/${file}`);
    client.on(file.split(".")[0], event.bind(null, client));
};

for (const file of player) {
    console.log(`Loading discord-player event ${file}`);
    const event = require(`./player/${file}`);
    client.player.on(file.split(".")[0], event.bind(null, client));
};

client.login(client.config.discord.token);