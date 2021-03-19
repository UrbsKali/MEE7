const { writeFile } = require('fs');

module.exports = {
	name: 'say',
	description: 'Hello, it\'s me',
    aliases: ['s'],
	category: 'Music',
	async execute(client,message, args) {

		if (!message.member.voice.channel) return message.channel.send(`${client.emotes.error} - You're not in a voice channel !`);

        if (message.guild.me.voice.channel && message.member.voice.channel.id !== message.guild.me.voice.channel.id) return message.channel.send(`${client.emotes.error} - You are not in the same voice channel !`);

        if (!args[0]) return message.channel.send(`${client.emotes.error} - Please indicate somethings to say !`);

		const { exec } = require('child_process');

		exec(`pico2wave --wave=text2say.wav --lang=fr-FR "${args.join(" ")}"  `, (err, stdout, stderr) => {
			if (err) {
				//some err occurred
				return message.channel.send(`${client.emotes.error} Some nefarious things are inside me : \n ${err}`)
			}
		});
			
		 
		
		const connection = await message.member.voice.channel.join();
		connection.play('text2say.wav');
		exec(`rm text2say.wav`, (err, stdout, stderr) => {
			if (err) {
				//some err occurred
				return message.channel.send(`${client.emotes.error} Some nefarious things are inside me : \n ${err}`)
			}
		});
		return true
        
	},
};