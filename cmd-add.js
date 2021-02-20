



async function main () {
    url = "https://discord.com/api/v8/applications/705398418125881346/guilds/652172028702490652/commands"
    const fetch = require('node-fetch')

    const response = await fetch(url, {
        method: 'post',
        body: JSON.stringify({
            "name": "help",
            "description": "All yours",
        }),
        headers: {
        'Authorization': 'Bot NzA1Mzk4NDE4MTI1ODgxMzQ2.XqrHeA.ck_uCe1dManlb4KnmOX-3oVMZi0',
        'Content-Type': 'application/json'
        }
    })
    const json = await response.json()

    console.log(json)
}
main()