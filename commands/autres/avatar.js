module.exports = {
	name: 'avatar',
	description: 'Get the avatar URL of the tagged user(s), or your own avatar.',
	aliases: ['icon', 'pfp'],
	category: 'Others',
	execute(client, message, args) {
		if (!message.mentions.users.size) {
			return message.channel.send(message.author.displayAvatarURL({ dynamic: true }));
		}

		const avatarList = message.mentions.users.map(user => {
			return user.displayAvatarURL({ dynamic: true });
		});
		

		message.channel.send(avatarList);
	},
};