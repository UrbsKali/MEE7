module.exports = {
	name: 'unmute-all',
	description: 'unmute all people inside your VC',
	aliases: ['uma'],
	category: 'Among Us',
	execute(client, message, args) {
        const channel = message.channel
        const members = channel.members
        members.forEach(member => {
            member.voice.setMute(false)
        });
        return message.reply("Done.")
	},
};