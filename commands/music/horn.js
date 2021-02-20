module.exports = {
	name: 'horn',
	description: 'Pwieeeeeeeeeee',
    aliases: ['h'],
	category: 'Music',
	async execute(client,message, args) {

		if (!message.member.voice.channel) return message.channel.send(`${client.emotes.error} - You're not in a voice channel !`);

        if (message.guild.me.voice.channel && message.member.voice.channel.id !== message.guild.me.voice.channel.id) return message.channel.send(`${client.emotes.error} - You are not in the same voice channel !`);			
		 
		const connection = await message.member.voice.channel.join();
		connection.play('data/mlg-air-horn.mp3');

        
	},
};