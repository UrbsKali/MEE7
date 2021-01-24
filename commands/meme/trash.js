const discord = require('discord.js');
const DIG = require("discord-image-generation");

module.exports = {
	name: 'trash',
	description: 'if your are a trash then go with them',
	category: 'meme',
	async execute(client, message, args) {
        if (!message.mentions.users.size) {
            let img = await new DIG.Trash().getImage(message.author.displayAvatarURL({ dynamic: true, format: 'png' }))
            // Add the image as an attachement
            let attach = new discord.MessageAttachment(img, "Trash.png");
            return message.channel.send(attach)
		}

        // Make the image
        let img = await new DIG.Trash().getImage(message.mentions.users.first().displayAvatarURL({dynamic: true, format: 'png'}))
        // Add the image as an attachement
        let attach = new discord.MessageAttachment(img, "Trash.png");
        message.channel.send(attach)
	},
};