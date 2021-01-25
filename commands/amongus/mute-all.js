module.exports = {
	name: 'mute-all',
	description: 'mute all people inside your VC',
	aliases: ['ma'],
	category: 'Among Us',
	execute(client, message, args) {

        const channel = message.channel
        const members = channel.members
        members.forEach(member => {
            member.voice.setMute(true)
        });
        return message.reply("Done.")
	},
};