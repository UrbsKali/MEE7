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

client.player = new Player(client);
client.config = require('./config/bot');
client.emotes = client.config.emojis;
client.filters = client.config.filters;
client.commands = new discord.Collection();



//  commands 
/*
client.api.applications(client.user.id).guilds('689766890356080651').commands.post({data: {
    name: 'help',
    description: 'get the whole help of this bot'
}})
client.api.applications(client.user.id).guilds('652172028702490652').commands.post({data: {
    name: 'help',
    description: 'get the whole help of this bot'
}})
*/

fs.readdirSync('./commands').forEach(dirs => {
    const commands = fs.readdirSync(`./commands/${dirs}`).filter(files => files.endsWith('.js'));

    for (const file of commands) {
        const command = require(`./commands/${dirs}/${file}`);
        console.log(`Loading command ${file}`);
        client.commands.set(command.name.toLowerCase(), command);
    };
});

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