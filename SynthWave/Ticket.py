import discord
from discord import app_commands
import asyncio
from asyncio import events

from discord.ext import commands, tasks
from  itertools import cycle

id_cargo_atendente = 1#1k
canalmsgticekt = 2#
idmsgticekt = 3#

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [          
            discord.SelectOption(value="atendimento",label="Atendimento", emoji="📨",description="Iremos te ajudar !"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "atendimento":

            embed2 = discord.Embed(
                colour=discord.Color.red(),
                title="Novo Ticket",
               description="Clique abaixo para criar um ticket"
            )

            await interaction.response.send_message(embed=embed2,ephemeral=True,view=CreateTicket())
   

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Dropdown())


class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value=None

    @discord.ui.button(label="Abrir Ticket",style=discord.ButtonStyle.blurple,emoji="➕")

    # Submit Ticket #
    async def confirm(self,interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()
        
        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True,content=f"Você já tem um atendimento em andamento!")
                    return
        
        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.edit_original_response(content=f"Você já tem um atendimento em andamento!",view=None)
                    return


        if ticket != None:
            await ticket.edit(archived=False)
            await ticket.edit(name=f"{interaction.user.name} ({interaction.user.id})",auto_archive_duration=10080,invitable=False)
        else:
            ticket = await interaction.channel.create_thread(name=f"{interaction.user.name} ({interaction.user.id})",auto_archive_duration=10080)#,type=discord.ChannelType.public_thread)
            await ticket.edit(invitable=False)

        embed3 = discord.Embed(
                colour=discord.Color.red(),
                title="Criei um ticket para você!",
               description=f"{ticket.mention}"
            )

        await interaction.response.send_message(ephemeral=True,embed=embed3)


        embed4 = discord.Embed(
                colour=discord.Color.red(),
                title=f"",
               description=f"Por Favor deixe todas as informações possiveis para poder nos ajudar a te atender melhor !\n\n Depois de Atendido caso queira fechar o ticket por favor use `/fecharticket` para encerrar o atendimento! \n\n<@&{id_cargo_atendente}>"
            )

        await ticket.send(f"📩  **|** {interaction.user.mention} ticket criado! <@&{id_cargo_atendente}>",embed=embed4)



class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False 

    async def setup_hook(self) -> None:
        self.add_view(DropdownView())
    

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  
            await tree.sync() 
            self.synced = True
            print(f"Entramos como {self.user}.") 
            
        server = 1
           
        statuses = [f'En {server} Servidores', f'Desarrollado por SynthWaveCo','Buen dia?', 'si es necesario usame !','en yt'] 


        displaying = cycle(statuses)

        running = True

        while running:
            
            current_status = next(displaying)
            await self.change_presence(status=discord.Status.online, activity=discord.Game(name=current_status ,type=3))
            await asyncio.sleep(20)

         
            message = await self.get_channel(canalmsgticekt).fetch_message(idmsgticekt)
            embed = discord.Embed(
                colour=discord.Color.from_rgb(255,0,0),
                title="Central De Ajuda",
                description=f"**╰ Selecione qual atendimento mais te ajuda !**",
                
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1057713749110292610/1092092448232189992/ticket.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1057713749110292610/1063994034919571576/fotor_2023-1-14_22_31_49.png")
            embed.set_footer(text="V.3 - 14/11/2023 | Beta by SynthWaveCo")
            embed.add_field(name=f"\u200b", value="\u200b", inline=False)
            embed.add_field(name=f"> Selecione", value="```📨 Atendimento para criar seu Ticket ```", inline=False)
            
            
            await message.edit(embed=embed,view=DropdownView())


    
intents = discord.Intents.default()
aclient = client()

tree = app_commands.CommandTree(aclient)



########################### Setup ##################
@tree.command( name = 'setup', description='Setup')

@app_commands.checks.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    await asyncio.sleep(2)
    
    embed = discord.Embed(
        colour=discord.Color.from_rgb(255,0,0),
        title="Central De Ajuda",
        description=f"**╰ Selecione qual atendimento mais te ajuda !**",        
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1057713749110292610/1092092448232189992/ticket.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1057713749110292610/1063994034919571576/fotor_2023-1-14_22_31_49.png")
    embed.set_footer(text="V.3 - 14/11/2023 | Beta by SynthWaveCo")
    embed.add_field(name=f"\u200b", value="\u200b", inline=False)
    embed.add_field(name=f"> Selecione", value="```📨 Atendimento para criar seu Ticket ```", inline=False)
      
     
    await interaction.followup.send(embed=embed,view=DropdownView())

@setup.error
async def setup_error(ctx: discord.Interaction, error, ):
    if isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message(f"{ctx.user.mention} Ifelizmente ou felizmente né :man_tipping_hand: , Você não tem permissão pra isso !",ephemeral=True)


@tree.command( name="fecharticket",description='Feche um atendimento atual.')
async def _fecharticket(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    await asyncio.sleep(2)
    mod = interaction.guild.get_role(id_cargo_atendente)
    if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.roles:
        await interaction.followup.send(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
        await interaction.channel.edit(archived=True)
    else:
        await interaction.followup.send("Isso não pode ser feito aqui...")


import config
from config import token
aclient.run(token)

