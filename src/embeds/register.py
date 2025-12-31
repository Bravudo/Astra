import discord
import os

RobloxIcon = "<:roblox:1430379231552209038>"
DiscordIcon = "<:discord:1423392381910253638>"


async def send_register_embed(channel, user_id, join_number, roblox_id, roblox_username, roblox_displayname):
    user = await channel.guild.fetch_member(user_id)
    username = user.name

    embed = discord.Embed(
        title=f'Registro Astryn',
        description=f'{user.mention}',
        color=discord.Color.from_rgb(255, 255, 255) 
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name=f"{DiscordIcon} Username", value=username, inline=True)
    embed.add_field(name=f"{DiscordIcon} Entrada", value=join_number, inline=True)
    embed.add_field(name=f"{DiscordIcon} ID", value=user_id, inline=True)

    if roblox_id == None:
        embed.add_field(name=f"{RobloxIcon} Sem dados Roblox 🚫", value="\u200b", inline=True)
    else:
        embed.add_field(name=f"{RobloxIcon} Username", value=roblox_username, inline=True)
        embed.add_field(name=f"{RobloxIcon} Displayname", value=roblox_displayname, inline=True)
        embed.add_field(name=f"{RobloxIcon} ID", value=roblox_id, inline=True)
        
    await channel.send(embed=embed)

async def send_register_button_embed(ctx, view):
    embed = discord.Embed(
        title="Veficação Astryn",
        description=":comet: O último passo para se tornar um cidadão de Astryn é nossa verificação."
        "\n\n☀️ **Clique** no botão abaixo e descubra se você é digno de se juntar a nós.",
        color=discord.Color.from_rgb(0, 102, 255)
    )
    embed.set_footer(text="ASR x Your Name")
    embed.set_image(url="https://i.pinimg.com/originals/3f/15/ad/3f15ad3ab9ab529a639e455a6141a961.gif")
    await ctx.send(embed=embed, view=view)