import asyncio
import discord
from discord.ext import commands
from src.services.bloxlink import findroblox
from src.services.bd.config import Database
from src.slash_commands.default import isAuthenticated
from src.embeds.register import send_register_button_embed



#----Cargos-----#
#Retirar
noverify_role = 1420818499437330524

#Colocar
verify_role = 1420859819950215278
member_role = 1420643710961455175

add_member_roles = [verify_role, member_role]
remove_member_roles = [noverify_role]
#---------------#
JoinChannel = 1420650846353494066
RoleChannel = 1420646241305624687
clanTag = "ASR"
locked_button = False
class Register(discord.ui.View):
    try:
        def __init__(self):
            super().__init__(timeout=None)
            self.db = Database()
            
        @discord.ui.button(label="☀️", style=discord.ButtonStyle.primary, custom_id="register")
        async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                global locked_button
                guild = interaction.guild
                user = interaction.user
                user_id = int(user.id)
                new_name = ""
                
                if locked_button == True:
                    await interaction.response.send_message("⏳ **Aguarde!** Outro usuário está se sendo inspecionado. **(1m)**", ephemeral=True)
                    return
                try:
                    checkAuthenticated = await isAuthenticated(user.display_name)
                    if checkAuthenticated:
                            await interaction.response.send_message("😵‍💫 Você já foi verificado, não se preocupe.", ephemeral=True)
                            return
                    else:
                        try:
                                locked_button = True
                                  
                                await interaction.response.defer(ephemeral=True)
                                await interaction.followup.send(
                                    f":star2: Enquanto te inspecionamos, aproveite para entender como funciona o servidor na <#{JoinChannel}> e as nossas <#{RoleChannel}>!"
                               , ephemeral=True )

                                username = user.display_name
                                join_number = 99
                                ExistUser = (await self.db.select.same_user_data(int(user_id)))

                                #Se o usuário não existir, cria um novo
                                if ExistUser == None:
                                    join_number = int(await self.db.select.last_join_number()) 
                                #Se o usuario já existir, utiliza as informações da primeira pesquisa
                                else:
                                    join_number = ExistUser

                                if len(str(join_number)) == 1:
                                        join_number_name = "0" + str(join_number)
                                        new_name = f"‹ {join_number_name} › {clanTag} {username}"
                                else:
                                    new_name = f"‹ {join_number} › {clanTag} {username}"
                                
                                if len(new_name) > 32:
                                    new_name = new_name[:32]

                                
                                await findroblox(interaction, user, int(join_number))
                                await asyncio.sleep(50)
                                await add_remove_rules(guild, user, add_member_roles, remove_member_roles)
                                await user.edit(nick=new_name)

                                #Mensagem final
                                await interaction.followup.send(
                                    f":dizzy: <@{user_id}>, você foi aceito como cidadão e lhe foi concedida permissão de acessar toda a **Astryn**!"
                                ,ephemeral=True)
                                locked_button = False
                        except Exception as e:
                                print(f'Erro ao se registrar: {e}')
                except Exception as e:
                                print(f'Erro ao tentar registrar usuário por botão: {e}')  
            finally:
                await asyncio.sleep(60)
                locked_button = False

    except Exception as e:
        print(f'Erro ao tentar spawnar o botão de registro: {e}')
            
@commands.command()
@commands.has_permissions(administrator=True)
async def register(ctx):
    view = Register()
    await send_register_button_embed(ctx, view)


async def reduction_name(name):
    name = name[:32]
    return name

async def add_remove_rules(guild, user, add, remove): 
    add_role = [guild.get_role(role_id) for role_id in add]
    remove_role = [guild.get_role(role_id) for role_id in remove]
    if add_role:
        await user.add_roles(*add_role) 
    if remove_role:
        await user.remove_roles(*remove_role)
        return   

async def newpeople_setup(bot):
    bot.add_command(register)
    bot.add_view(Register())
