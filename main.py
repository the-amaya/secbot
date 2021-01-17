import discord
from urllib.request import urlopen
from PIL import Image
import io

cameras = {
	'driveway': '10.0.50.101',
	'porch': '10.0.50.102',
	'backdeck': '10.0.50.100',
	'mudroom': '10.0.50.104',
	'racoon': '10.0.50.106',
}

class MyClient(discord.Client):

	async def on_ready(self):
		print('Logged on as', self.user)

	async def on_message(self, message):
		word_list = ['driveway', 'porch', 'backdeck', 'mudroom', 'racoon']

		# don't respond to ourselves
		if message.author == self.user:
			return

		messageContent = message.content
		if len(messageContent) > 0:
			for word in word_list:
				if word == messageContent:
					img_file = urlopen('http://' + cameras.get(messageContent) + '/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=wuuPhkmUCeI9WG7C&user=admin&password=camera')
					img = Image.open(img_file)
					img.save('img.png')
					await message.channel.send(file=discord.File('img.png'))
			if messageContent == 'list':
				await message.reply(cameras.keys(), mention_author=True)


client = MyClient()
client.run('bot_token')