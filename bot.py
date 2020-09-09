import discord
from youtube_dl import YoutubeDL
from discord.ext import commands
from time import sleep
import random
import os
import platform
import sys
import soundfile as sf
#from pretty_help import PrettyHelp
import asyncio
from async_timeout import timeout
from functools import partial
import re
import urllib.request
import urllib.error
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


tmp_json = '''{
  "type": "service_account",
  "project_id": "mylittleyggdrasil",
  "private_key_id": "a0ec162566ba315634fc4fa827391263953505e1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDKdL/vsv7QssrQ\nrDDFzhUcUH/8JRjNM7OeERLFhsBlPhKTDVO51v7TEsOoxE+DKmIITeleCToiJLPa\nsIhTPNRwPHAwL7PoEk++hS5CiHsOKSInkQND5R5FF3w6Fp3aMnM8J03HXVWVH7Ft\nGGF9zqQQhOspbnGmaVD/Ycixp38g2NpjEyKle733zs0iZIOVSRIB39IJjRmG+qGN\nstauxSiZpAFKigHEuw4N4yET7UaIGLrUVxJztRaf8euJ9HTrLd6pU8NMzN37yVAp\nzFN1DkTQRhSfuoQI5qg9xmYslqFealigTJ/E1WaOAM7ssn1rvSAR0h3hu22Jv7dq\n/VciC1jTAgMBAAECggEAECVIa0rIlIc1sneQ+i1ptJTc6BRjSnYdlHUDHLqW3Fwb\nahvNegwhzV55ORvSxYCbSdNA0a2Fs9RefYnHjW/T91Fylv0u6UqQjn6bhlXRDnuM\nTEB91KvQgq0RTKaiFxUf6IOv6b7RRO++nBcuKzTQE7st7+Ntb9qFSaCYO0bC1jEg\nlDVs5T06K1bOV3Ff3WcuwpPJ4SIAN7kEUrR4MzjdjQN4Y3CwnCBGP0EgXq/QwRMB\njEMYz2M/FCeiTmJM2LE9HtwUkz2Clg9fHhUPB1SSzr3Qc5ig/JxFfgJRwGZR2HYd\n1Aspp3+9VBI+znZg6zHqQ+vnHQbNn2AmnNg9599u4QKBgQD8Y1DCmBMjloCJ1nZQ\nkG/kuR6ZZEFwQTfL21kxUh+n7f9Jm55nm2CMqxvO1vU0ikuL4MO+TOehbBILoPdH\nIGyxnyy/KQhOp2p3suEJHtVWFIkz5M+qxJEOsgEKqrBi/6zJuV42i6miTfMayFuL\nMHyVsDbTjxOX81az2JjezYWPswKBgQDNWn8kumdulnOT4gXLCvf6YUq87FL3fAVM\nyJLDOyPilvjrwS+7htb5BVpuF9UNOJ14Q1vUXEmHWuCpBp4L0u4mWVIS5E79NyF8\n68eNniuzbR35OaCv6kUWjn+k/i+B5r0N4LxRb1+x8MYfq3561hb1HoTIImnK2ha5\n54dhny2CYQKBgFUsmyOguMzIzMY3pyQXKnvQ8X+osuDUUaUteFNJuL8udXn81591\nc0bls/PA3W2GwmoJR2XghEcYtppQD0NksOncovg8O753h1mv93vhePOc6JSnwmGK\nBr4j2nAkHHS8fi5xrVbRGUVZ8xH1zdcSXOkTV91bqqwcBgWZsjV2vH07AoGBAJo1\nARFVoWJcPMKqkmsc+4bcFMG2Pb93NIuqevt8p7/6W0a+tdd+tGQf7v6JiwX4o9ex\nzX21J8orJlYHkBuU9B18KbPiGqbwBYfHjvz78Bk3MbD743z20ZbUv2npL0e/O+z1\n/LSyjAwVoNIbeElKB8deeZvIq+UWzMYh5XobjJNBAoGBAJVgi4uUqW/iPBOciXmB\nUx18r71d7VBWvkkdjDKYmLpa4Qg4WEaQEfX8v9aLdgkIBU4r4VpGkS5OSUHFt79E\nbCds6WV2Ibt4vm5S/h+L6XoaPvG7WETO4Udzbhr0q7PVlVyMFizGYe8fyW9LRhbB\nT3hsQFvesJ8QH9jXxvg+Snca\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-9tvmd@mylittleyggdrasil.iam.gserviceaccount.com",
  "client_id": "103125697931273272235",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9tvmd%40mylittleyggdrasil.iam.gserviceaccount.com"
}'''
tmp_json = json.loads(tmp_json, strict=False)
cred = credentials.Certificate(tmp_json)
firebase_admin.initialize_app(cred)


db = firestore.client()

# need ffmepg and python 3.6
def get_fb(collection):
    users_ref = db.collection(u'{0}'.format(collection))
    docs = users_ref.stream()
    to_return = {}
    for doc in docs:
        to_return[doc.id] = doc.to_dict()

    return to_return

def create_doc(collection, document, data):
    db.collection(u'{0}'.format(collection)).document(u'{0}'.format(document)).set(data)

    city_ref = db.collection(u'{0}'.format(collection)).document(u'{0}'.format(document))

    # Set the capital field
    city_ref.update({u'{0}'.format(collection): True})

def update_doc(collection, document, data : dict):
    db.collection(u'{0}'.format(collection)).document(u'{0}'.format(document)).update(firestore.ArrayUnion(data))

    city_ref = db.collection(u'{0}'.format(collection)).document(u'{0}'.format(document))


def delete_doc(collection, document):
    db.collection(u'{0}'.format(collection)).document(u'{0}'.format(document)).delete()


def get_prefix(bot, message):

    prefixes = get_fb('prefix')
    prefixes = prefixes[str(message.guild.id)]["pre"]
    return prefixes

client = discord.Client()
bot = commands.Bot(command_prefix = get_prefix, description='MEE7, a Bot to control them all !') #help_command=PrettyHelp()
bot.remove_command('help')


@commands.command(pass_context=True)
async def help(ctx):

    """Gives a link to my Github, **With all my projects  MORTY !!**"""

    embed = discord.Embed(title="WIP", description="Help command is work in progress, try again soon !",
                           color=0xffff00)
    await ctx.channel.send(embed=embed)


async def check_bad_word(message):
    bad_words = get_fb('bad_word')
    for auth_channel in bad_words[str(message.guild.id)]["excluded"]:
        if str(message.channel.id) != auth_channel :
            for bad_word in bad_words[str(message.guild.id)]['bad']:
                if message.content == bad_word :
                    await message.delete()



async def check_custom(message):

    customs = get_fb('custom_command')

    server_custom = customs[str(message.guild.id)]
    for keys in server_custom :
        if message.content == "$"+keys:
            await message.channel.send(server_custom[keys])


if platform.system() == "Windows":
    import Sapi as sapi
    voice = sapi.Sapi()


def save_off_data(data, name_of_the_file_to_save):
    file_off = open(name_of_the_file_to_save, "w+")
    file_off.write(str(data))
    file_off.close()


def read_token():
    file_tmp = open('token.txt', 'r')
    return file_tmp.read()


def create_audio(text, lang="fr-FR"):
    if platform.system() == "Windows":
        voice.create_recording('msg.wav', text)
    elif platform.system() == "Linux":
        os.system('pico2wave -l '+ lang +' -w msg.wav ' + '"' + text + '"')
    else:
        print('OS incopatible with the system of TTS, if your are on Mac, Stay Tuned, the MaJ is comming soon !')


def clear():
    # use to clear on different os
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def quitting(nb=0):
    if nb == 0:
        clear()
        print(' _____________________')
        print('/                     \ ')
        print('|     Quitting..      |')
        print('\_____________________/\n')
        sys.exit()
    else:
        clear()
        print(' _____________________')
        print('/                     \ ')
        print('| Error !, Quitting.. |')
        print('\_____________________/\n')
        sys.exit(nb)


def nb_serv():
    nb = 0
    for i in bot.guilds:
        nb = nb + 1
    return nb

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = YoutubeDL(ytdlopts)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.url = data.get('webpage_url')
        self.alt_title = data.get('alt_title')
        if not data.get('alt_title'):
            self.alt_title = self.title
        self.creator = data.get('creator')
        if not data.get('creator'):
            self.creator = data.get('uploader')
        self.thumbnail = data.get('thumbnail')

    def __getitem__(self, item: str):
        """
        Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {
                "title": data["title"], "url": data["url"], "alt_title":
                    data["alt_title"],
                "uploader": data["uploader"], "creator": data["creator"],
                "duration": data["duration"],
                "view_count": data["view_count"], "like_count": data["like_count"],
                "dislike_count": data["dislike_count"],
                "thumbnail": data["thumbnail"], "webpage_url": data["webpage_url"],
                "requester": ctx.author.name
            }

        return cls(discord.FFmpegPCMAudio(source, before_options='-nostdin', options='-vn'),
                   data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """
        Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire.
        """
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url'], before_options='-nostdin', options='-vn'),
                   data=data, requester=requester)

class MusicPlayer:
    """
    A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different
    guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current',
                 'np', 'volume', 'repeat', 'repeating')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None
        self.repeat = False
        self.repeating = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            vc = self._guild.voice_client
            if len(vc.channel.members) == 1:
                embed = discord.Embed(
                    description="There are no users in the voice channel! Disconnecting...",
                    color=0x00ff00
                )
                await self._channel.send(embed=embed)
                self.destroy(self._guild)
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    if self.repeat and self.current is not None:
                        source = self.repeating
                    else:
                        source = await self.queue.get()
                        self.repeating = source
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source,
                                          after=lambda _: self.bot.loop.call_soon_threadsafe(
                                              self.next.set))
            embed = discord.Embed(title="Now Playing", description=source.alt_title,
                                  color=0x00ff00)
            embed.add_field(name="Requested By", value=source.requester)
            embed.set_thumbnail(url=vc.source.thumbnail)
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Provides Music Playback Functionality. User must be in a voice channel."""

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.name = "Music"

    async def cog_check(self, ctx):
        if not ctx.author.voice:
            embed = discord.Embed(
                description="You must join a voice channel to be able to use this command!",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
            return False
        elif not ctx.guild:
            embed = discord.Embed(
                description="You must be in a guild in order to use these commands!",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
            return False
        return True

    async def cleanup(self, guild):
        await guild.voice_client.disconnect()

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    def gather_playlist(self, url):
        sTUBE = ''
        cPL = ''
        amp = 0
        final_url = []

        if 'list=' in url:
            eq = url.rfind('=') + 1
            cPL = url[eq:]

        else:
            return [url]

        try:
            yTUBE = urllib.request.urlopen(url).read()
            sTUBE = str(yTUBE)
        except urllib.error.URLError as e:
            print(e.reason)

        tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
        mat = re.findall(tmp_mat, sTUBE)

        if mat:

            for PL in mat:
                yPL = str(PL)
                if '&' in yPL:
                    yPL_amp = yPL.index('&')
                final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])

            all_url = list(set(final_url))
            return all_url

        else:
            return [url]

    @commands.command(aliases=["join"])
    async def summon(self, ctx):
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            raise NotInVoiceChannel('You are not currently in a voice channel!')

        vc = ctx.voice_client
        out = f"Connected to: {channel}"
        if vc:
            if vc.channel.id == channel.id:
                out = "I'm already in that channel!"
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                out = f'Moving to channel: <{channel}> timed out.'
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                out = f'Connecting to channel: <{channel}> timed out.'

        embed = discord.Embed(description=out, color=0x00ff00)
        await ctx.send(embed=embed, delete_after=20)

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, search):

        if not len(ctx.message.embeds) == 1 and "https://" in search:
            return

        embed = discord.Embed(title='Searching ...',
                              description='The search  `' + search + '`  is being processed',
                              color=0xffff00)
        await ctx.channel.send(embed=embed)

        if not ctx.voice_client:
            await ctx.invoke(self.summon)

        if ctx.author in ctx.voice_client.channel.members:
            vc = ctx.voice_client
            async with ctx.typing():
                player = self.get_player(ctx)
                playlist = self.gather_playlist(search)
                if len(playlist) > 1:
                    embed = discord.Embed(
                        description=f"Added {len(playlist)} songs to the Queue!",
                        color=0x00ff00
                    )
                    await ctx.send(embed=embed)
                    for track in playlist:
                        try:
                            source = await YTDLSource.create_source(ctx, track, loop=self.bot.loop,
                                                                    download=True)
                            await player.queue.put(source)
                        except:
                            pass
                else:
                    source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop,
                                                            download=True)
                    await player.queue.put(source)
                    embed = discord.Embed(
                        title=f"Added to the queue!",
                        description=f"[{source['alt_title']} - {source['creator']}]({source['url']})",
                        color=0x00ff00
                    )
                    embed.set_thumbnail(url=source["thumbnail"])
                    await ctx.send(embed=embed)

    @commands.command(brief="Pauses the current song.")
    async def pause(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client
        if vc is not None and ctx.author in vc.channel.members:
            out = f'{ctx.author}: Paused the song!'
            if not vc or not vc.is_playing():
                out = "I'm not currently playing anything!"
            elif vc.is_paused():
                out = "The player is already paused!"
            vc.pause()
            await ctx.send(embed=discord.Embed(description=out, color=0x00ff00))

    @commands.command(brief="Resumes the current song.", aliases=["r"])
    async def resume(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client
        out = f'{ctx.author}: Resumed the song!'
        if vc is not None and ctx.author in vc.channel.members:
            if not vc or not vc.is_connected():
                out = 'I am not currently playing anything!'
            elif not vc.is_paused():
                out = "The player is not currently paused!"

        vc.resume()
        await ctx.send(embed=discord.Embed(description=out, color=0x00ff00))

    @commands.command(aliases=["fs"], brief="Forceskips the song!")
    @commands.has_permissions(manage_guild=True)
    async def forceskip(self, ctx):
        """
        Force skips the song!
        Requires "manage_guild" perms!
        """
        vc = ctx.voice_client
        if vc is not None and ctx.author in vc.channel.members:
            if not vc or not vc.is_connected():
                embed = discord.Embed(
                    description="I am not currently playing anything!",
                    color=0x00ff00
                )
                return await ctx.send(embed=embed, delete_after=20)
            if vc.is_paused():
                pass
            elif not vc.is_playing():
                return
        if vc:
            vc.stop()

    @commands.command(brief="Skips the song.", aliases=["sk"])
    async def skip(self, ctx):
        """Skip the currently playing song."""
        vc = ctx.voice_client
        if vc is not None and ctx.author in vc.channel.members:
            if not vc or not vc.is_connected():
                embed = discord.Embed(
                    title="Music Player",
                    description="I am not currently playing anything!",
                    color=0x00ff00
                )
                return await ctx.send(embed=embed, delete_after=20)
            if vc.is_paused():
                pass
            elif not vc.is_playing():
                return

            def stop():
                vc.stop()

            if len(vc.channel.members) > 2:
                embed = discord.Embed(
                    title="Music Player",
                    description=f"""
        {ctx.author.mention} has requested the current song be skipped!
        If a majority vote is reached, I will skip this track!""",
                    color=0x00ff00
                )
                msg = await ctx.send(embed=embed)
                await msg.add_reaction("✅")
                await asyncio.sleep(1)
                await msg.add_reaction("❎")
                await asyncio.sleep(1)
                pro = 0
                against = 0
                total = len(vc.channel.members) - 1

                def check(r, u):
                    return u in vc.channel.members

                try:
                    for i in range(120):
                        reaction, user = await self.bot.wait_for("reaction_add", check=check)
                        if pro >= total * .75:
                            stop()
                            break
                        elif against >= total * .75:
                            raise Exception
                        elif str(reaction.emoji) == "✅":
                            pro = pro + 1
                        elif str(reaction.emoji) == "❎":
                            against = against + 1
                        await asyncio.sleep(1)
                    emebd = discord.Embed(
                        title="Music Player",
                        description="A majority was reached! Skipping...",
                        color=0x00ff00
                    )
                except Exception as e:
                    embed = discord.Embed(
                        description="A majority vote was not reached!",
                        color=0x00ff00
                    )
                await msg.edit(embed=embed, delete_after=20)
            else:
                embed = discord.Embed(
                    description="The song has been skipped!",
                    color=0x00ff00
                )
                await ctx.send(embed=embed, delete_after=20)
                stop()

    @commands.command(aliases=['q'], brief="Provides queued songs")
    async def queue(self, ctx):
        """Provides a list of upcoming songs!"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(
                embed=discord.Embed(description='I am not currently connected to voice!',
                                    color=0x00ff00), delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send(
                embed=discord.Embed(description='There are currently no more queued songs.',
                                    color=0x00ff00))

        text = "\n\n".join(i["alt_title"] for i in player.queue._queue)

        embed = discord.Embed(title=f'In Queue - {len(player.queue._queue)}', description=text)
        await ctx.send(embed=embed)

    @commands.command(aliases=['np', "play?"], brief="Displays the current song")
    async def playing(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(
                embed=discord.Embed(description='I am not currently connected to voice!',
                                    color=0x00ff00), delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send(
                embed=discord.Embed(description='I am not currently playing anything!',
                                    color=0x00ff00))

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        embed = discord.Embed(title="Now Playing", description=vc.source.alt_title,
                              color=0x00ff00)
        embed.add_field(name="Requested By", value=vc.source.requester)
        embed.set_thumbnail(url=vc.source.thumbnail)
        player.np = await ctx.send(embed=embed)

    @commands.command(aliases=['vol', "v"], brief="Changes the player volume!")
    async def volume(self, ctx, *, vol: float):
        """Change the player volume. Please specify a value between 1 and 100!"""
        vc = ctx.voice_client
        if vc is not None and ctx.author in vc.channel.members:
            if not vc or not vc.is_connected():
                return await ctx.send(
                    embed=discord.Embed(description='I am not currently connected to voice!',
                                        color=0x00ff00),
                    delete_after=20)

            if not 0 < vol < 101:
                return await ctx.send(
                    embed=discord.Embed(description='Please enter a value between 1 and 100.',
                                        color=0x00ff00),
                    delete_after=20)

            player = self.get_player(ctx)

            if vc.source:
                vc.source.volume = vol / 100

            player.volume = vol / 100
            await ctx.send(
                embed=discord.Embed(description=f'{ctx.author}: Set the volume to {vol}%',
                                    color=0x00ff00))

    @commands.command(brief="Changes the player volume!", aliases=["loop", "l"])
    async def repeat(self, ctx):
        """Repeats the currently playing song"""
        vc = ctx.voice_client
        if vc is not None and ctx.author in vc.channel.members:
            if not vc or not vc.is_connected():
                return await ctx.send(
                    embed=discord.Embed(description='I am not currently connected to voice!',
                                        color=0x00ff00),
                    delete_after=20)
            try:
                player = self.get_player(ctx)

                if player.repeat:
                    player.repeat = False
                    out = f"The song {vc.source.title} is no longer on repeat!"
                else:
                    player.repeat = True
                    out = f"The song {vc.source.title} is now on repeat!"

            except AttributeError:
                out = "There is not currently a song playing!"
            embed = discord.Embed(description=out, color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command(aliases=["destroy", "kill"], brief="Stops and kills the player!")
    async def stop(self, ctx):
        """Stop the currently playing song and destroy the player."""
        vc = ctx.voice_client
        if vc is not None and ctx.author in vc.channel.members:
            if not vc or not vc.is_connected():
                embed = discord.Embed(
                    description='I am not currently playing anything!',
                    color=0x00ff00
                )
                return await ctx.send(embed=embed)
            await self.cleanup(ctx.guild)
            embed = discord.Embed(
                description="The player has been stopped!",
                color=0x00ff00
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["s"])
    async def say(self, ctx, *, txt):
        """Have your poetry told by MEE7"""

        channels = ctx.author.voice.channel
        vc = ctx.voice_client
        vc.pause()

        create_audio(txt)
        f = sf.SoundFile('msg.wav')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("msg.wav"), 1)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else vc.resume())

    @say.before_invoke
    async def ensure_voice(self, ctx):
        embed1 = discord.Embed(title='Attention',
                               description='Vous devez être connecté à un chat vocal pour faire cette commande !',
                               color=0xff0000)
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(embed=embed1)
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

class TextBot(commands.Cog):

    @commands.command()
    async def who(self, ctx):

        """Do you want to know who I am? """

        await ctx.channel.send('I am a bot dev by <@423567995609022464> because he had the laziness to make the code of the game')
        sleep(2)
        await ctx.channel.send('But I can be nice')

    @commands.command()
    async def my_secret(self, ctx):

        """It's Mine !"""

        await ctx.channel.send("I'm sexy and You Know it")


    @commands.command()
    async def rules(self, ctx):

        """Displays the rules of the internet !"""

        embed = discord.Embed(title="The Official Rules of Internet", description='1) Do not talk about rules 2-33 \n '
                                                                                  '34) There is porn of it. No '
                                                                                  'exceptions. \n 35) '
                                                                                  'The exception to rule #34 is the '
                                                                                  'citation of rule #34.\n 36) '
                                                                                  'Anonymous does not '
                                                                                  'forgive.\n 37) There are no girls '
                                                                                  'on the internet.\n38) A cat is '
                                                                                  'fine too \n 39) '
                                                                                  'One cat leads to another. \n 40) '
                                                                                  'Another cat leads to zippocat.\n '
                                                                                  '41) Everything '
                                                                                  'is someone\'s sexual fetish. \n42) '
                                                                                  'It is delicious cake. You must eat '
                                                                                  'it.\n 43) '
                                                                                  'It is a delicious trap. You must '
                                                                                  'hit it.\n 44) /b/ sucks today. \n '
                                                                                  '45) Cock goes '
                                                                                  'in here.\n  46) They will not '
                                                                                  'bring back Snacks.\n 47) You will '
                                                                                  'never have sex.\n '
                                                                                  '48) ???\n49) Profit.\n50. You can '
                                                                                  'not divide by zero. ',
                              color=0x00ff00)
        await ctx.channel.send(embed=embed)


    """@commands.command()
    async def alfred(self, ctx):
        \"""Lui pas argent\"""
        embed = discord.Embed(title="Lui pas Argent", description="soyez généreux ! \n https://www.paypal.me/alfreddv",
                              color=0x00ff00)
        embed2 = discord.Embed(title="Vraiment !", description="soyez généreux ! \n https://www.paypal.me/alfreddv",
                               color=0x00ff00)
        await ctx.channel.send(embed=embed)
        sleep(5)
        await discord.DMChannel.send(ctx.author, embed=embed2)"""


class Image(commands.Cog):
    @commands.command()
    async def rule39(self, ctx):

        """Rule 39 of the internet : One cat lead to another !"""

        cat = [
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.5nwmIr_3MijZRB8foelYEQHaEA%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.4rO3V6NT5pOprlvO2kVPlwHaHa%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.yRLu6PUtmlw3_zjopUMA7QHaEK%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.gUCtpmRygWrQla_QCow9ywHaEK%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.KZhF_ZflSx4mDW0rTu0_tQHaEK%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.dueVPqO9-3v9YDPVN8NsOwHaEK%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.kMMQaZAN0r8XG2nPhNQTAQHaGK%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.GQ_d9vxjKCagvMyDJJChkQHaDI%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.z4yjVQPQRziGGFOZN0w2_gHaFj%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.38PecBnWvJ3PILEWx6qlhwHaGg%26pid%3DApi&f=1',
            'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.oQNQj1dOlVSLbX5DEO6xRwHaEQ%26pid%3DApi&f=1', ]
        msg = "Rule 39 : One cat lead to another !  \n " + str(cat[random.randint(0, 10)])
        await ctx.channel.send(msg)


    @commands.command()
    async def panik(self, ctx):

        """PAAANIK"""

        panik = ['https://static-cdn.jtvnw.net/emoticons/v1/300334467/2.0',
                 'https://tenor.com/view/panic-kermit-gif-10311610']
        await ctx.channel.send(panik[random.randint(0, 1)])


class Project(commands.Cog):
    @commands.command()
    async def github(self, ctx):

        """Gives a link to my Github, **With all my projects  MORTY !!**"""

        embed = discord.Embed(title="My Github", description="↑↑↑ Link to my github, with my project !",
                              url="https://github.com/UrbsKali", color=0x00ff00)
        await ctx.channel.send(embed=embed)


    @commands.command()
    async def jeu(self, ctx):

        """You want to know the progress of the game project I'm doing!"""

        emebed = discord.Embed(title="In Progress ! ",
                               description='The game is under heavy development,, \n'
                                           'you can download it by clicking on "In Progress". \n '
                                           'For online play : https://coursbeast.000webhostapp.com/',
                               color=0xffff00,
                               url="https://urbskali.github.io/game/download")

        emebed.set_footer(text="Version : None")
        await ctx.channel.send(embed=emebed)

    @commands.command()
    async def nitrofree(self, ctx):

        """This Command describes very well what it will do"""

        embed = discord.Embed(title='Nitro Next Gen',
                              description='The NitroNextGen is coming soon, you will get your free nitro! \n '
                                          '\nLink to the github project : \n https://github.com/UrbsKali/NitroNextGen',
                              color=0x00ff00)
        await ctx.channel.send(embed=embed)


class Moderation(commands.Cog):

    """You know what it is"""

    @commands.command(aliases=["c"])
    async def clear(self, ctx, amount=10):

        """Clear x message on a channel"""

        try:
            await ctx.channel.purge(limit=amount)
            embed = discord.Embed(title='Done.',
                                  description=f'{amout} messages have been delete ',
                                  color=0x00ff00,
                                  )
        except Exception as e:
            embed = discord.Embed(title='Done.',
                                  description='The messages aren\'t delete,\n Try again later \nError : {0}'.format(e),
                                  color=0xff0000)
        await ctx.channel.send(embed=embed, delete_after=5)

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason="a MEE6 fanatic"):

        """Ban somebody from your server"""

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title='Done.',
                                  description='{0} has been banned \n '.format(member),
                                  color=0x00ff00)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason="a MEE6 fanatic"):

        """Kick somebody from the server"""

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title='Done.',
                                  description='{0} was well kicked \n '.format(member),
                                  color=0x00ff00)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def unban(self, ctx, *, member):
        try:
            banned_user = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")
            for ban_entry in banned_user:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    embed = discord.Embed(title="Sucefull",
                                          description="{0} has been unban sucefully !".format(member),
                                          color=0x00ff00)
                    await ctx.guild.unban(user)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Error",
                                          description="{0} is not banned !".format(member),
                                          color=0xff0000)
                    await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)





    @commands.command(aliases=["cp", 'prefix'])
    async def changeprefix(self, ctx, prefix):
        try:

            list = get_fb('prefix')
            old = list[str(ctx.guild.id)]["pre"]
            list[str(ctx.guild.id)]["pre"] = prefix
            delete_doc('prefix', str(ctx.guild.id))
            create_doc('prefix', str(ctx.guild.id), list[str(ctx.guild.id)])

            embed = discord.Embed(title="Done.",
                                  description="change prefix from {0} to {1}".format(old, prefix),
                                  color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=["aw", 'word'])
    async def addword(self, ctx, cmd_name):
        try:

            list = get_fb('bad_word')

            list[str(ctx.guild.id)]["bad"].append(cmd_name)
            delete_doc('bad_word', str(ctx.guild.id))
            create_doc('bad_word', str(ctx.guild.id), list[str(ctx.guild.id)])

            embed = discord.Embed(title="Done.",
                                  description="add word {0}".format(cmd_name),
                                  color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=["rw", 'rword'])
    async def addword(self, ctx, cmd_name):
        try:

            list = get_fb('bad_word')

            list[str(ctx.guild.id)]["bad"].pop(cmd_name)
            delete_doc('bad_word', str(ctx.guild.id))
            create_doc('bad_word', str(ctx.guild.id), list[str(ctx.guild.id)])

            embed = discord.Embed(title="Done.",
                                  description="remove word {0}".format(cmd_name),
                                  color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=["ach", 'add_exclused'])
    async def addchannel(self, ctx, cmd_name : discord.TextChannel):
        try:

            list = get_fb('bad_word')
            list[str(ctx.guild.id)]["excluded"].append(str(cmd_name.id))
            delete_doc('bad_word', str(ctx.guild.id))
            create_doc('bad_word', str(ctx.guild.id), list[str(ctx.guild.id)])

            embed = discord.Embed(title="Done.",
                                  description="add excluded channel {0}".format(cmd_name),
                                  color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=["rch", 'rem_exclused'])
    async def removechannel(self, ctx, cmd_name: discord.TextChannel):
        try:

            list = get_fb('bad_word')
            list[str(ctx.guild.id)]["excluded"].pop(str(cmd_name.id))
            delete_doc('bad_word', str(ctx.guild.id))
            create_doc('bad_word', str(ctx.guild.id), list[str(ctx.guild.id)])

            embed = discord.Embed(title="Done.",
                                  description="add excluded channel {0}".format(cmd_name),
                                  color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)


    @commands.command(aliases=["ac", 'command'])
    async def addcommand(self, ctx, cmd_name, *, cmd):
        try:

            list = get_fb('custom_command')[str(ctx.guild.id)]
            list[cmd_name] = cmd
            delete_doc('custom_command', str(ctx.guild.id))
            create_doc('custom_command', str(ctx.guild.id), list)

            embed = discord.Embed(title="Done.",
                                  description="add command {0}".format(cmd_name),
                                  color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=["rc", 'rcommand'])
    async def removecommand(self, ctx, cmd_name):
        try:
            list = get_fb('custom_command')[str(ctx.guild.id)]
            list.pop(cmd_name)
            delete_doc('custom_command', str(ctx.guild.id))
            create_doc('custom_command', str(ctx.guild.id), list)
            embed = discord.Embed(title="Done.",
                                  description="remove command {0}".format(cmd_name),
                                  color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=["lc", 'ls'])
    async def listcommand(self, ctx):
        try:

            prefixes = get_fb("custom_command")
            cmds = prefixes[str(ctx.guild.id)]
            if cmds['custom_command']:
                cmds.pop('custom_command')

            embed = discord.Embed(title="Here it is :",
                                  description="command list {0}".format(cmds),
                                  color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=["sd"])
    async def shutdown(self, ctx):

        """Shutdown the bot, uniquely for my creator"""
        try:
            if ctx.author.id == 423567995609022464:
                embed = discord.Embed(title='Okay.',
                                      description='Shutdown in progress',
                                      color=0x00ff00)
                await ctx.channel.send(embed=embed)
                quitting()
            else:
                embed = discord.Embed(title='Wait a minute.',
                                      description='You can\'t do that',
                                      color=0xff0000)
                await ctx.channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description="{0}".format(e),
                                  color=0xff0000)
            await ctx.send(embed=embed)





@bot.event
async def on_ready():
    clear()
    print('\n ____________________________________________________ ')
    print('/ We have logged in as {0.user}                     \ '.format(bot))  # this line work uniquely with a username like
    print('| Ready to bot !                                      \ ')            # MEE7#0035
    print('| Here we go again ...                                /')
    print('\____________________________________________________/\n')
    print('Guilds : ', nb_serv(), '\n')
    print('Logs :\n')
    await bot.change_presence(activity=discord.Game(name="Improving in progress ...")) #discord.Activity(name='Fall Guys', application_id=705398418125881346, state="In Game", details="details", timestamps={'start': 9999999999})


@bot.event
async def on_guild_join(guild) :

    create_doc('prefix', str(guild.id), {'prefix':"$"})

    create_doc('bad_word', str(guild.id), {"bad": [], "excluded" : []})

    create_doc('custom_command', str(guild.id), {})


@bot.event
async def on_guild_remove(guild) :
    delete_doc('prefix', str(guild.id))

    delete_doc('bad_word', str(guild.id))

    delete_doc('custom_command', str(guild.id))


@bot.event
async def on_member_join(member) :

    channel_id = get_fb("hello_msg")
    channel_id = channel_id[str(member.guild.id)]["do_verif"]
    channel = client.get_channel(channel_id)
    embed = discord.Embed(title='Hey',
                          description=f"Hello {member}, please check the :white_check_mark: to continue !",
                          color=0xff0000)
    msg = await discord.DMChannel.send(member, embed=embed)
    await msg.add_reaction("✅")

    for i in range(120):
        reaction, user = await bot.wait_for("reaction_add")
        if str(reaction.emoji) == "✅":
            print("chech confirmed")
            role = discord.utils.get(member.guild.roles, id=751466420847771839)
            await member.add_roles(role)

        await asyncio.sleep(1)


@bot.event
async def on_message(message):
    if message.author.id == 705398418125881346:
        return

    Gentil_mot = [' :older_adult: Okay Boomer', 'Ta gueule <@159985870458322944>', ':red_square: Le Rouge c\'est la couleur des vrais :red_square:',
                  '!ban <@159985870458322944>, mdr t\'es même pas capable de le faire',
                  ' :newspaper: Breaking news : <@159985870458322944> trainé en justice pour sa RGPD douteuse',
                  ' :newspaper: Breaking news : <@159985870458322944> bani de mee6\'s land, remplacé par mee7',
                  ' :white_check_mark:  Vérifié : <@159985870458322944>, pire bot du serveur {0.guild}'.format(message),
                  ]
    if message.author.id == 159985870458322944:
        r = int(random.random() * len(Gentil_mot))
        await message.channel.send(Gentil_mot[r])
    if message.content == "Hello There":
        await message.channel.send("General Kenobi")

    if message.content == "mdr":
        await message.channel.send("mdr.")
    if message.content == "lmao":
        await message.channel.send("lmao.")
    if message.content.lower() == "mee7 ?":
        await message.channel.send("yes ?")

    await check_bad_word(message)

    await check_custom(message)

    await bot.process_commands(message)







bot.add_cog(Music(bot))
bot.add_cog(TextBot(bot))
bot.add_cog(Image(bot))
bot.add_cog(Project(bot))
bot.add_cog(Moderation(bot))

bot.run(read_token())
