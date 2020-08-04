import asyncio
import discord
from discord.ext import commands
import sqlite3
import random
import requests
from colorama import init

TOKEN = 'NzMxNDk2ODU5OTQzODI5NTc0.Xwm54g.HLLcR9NpotFjKT8JKCDIpNuEncw'

client = commands.Bot(command_prefix='!')
client.remove_command('help')
client.remove_command('take')
random.seed(version=2)
# ---------------------------------------------------------------------------------------------
#                                         Constants
# ---------------------------------------------------------------------------------------------

IdZombieRole = 717072591466266697
MainChanel = 717049939385122860
AuditChatel = 734018873476775977
IdServer = 717049938927812719

api_key = 'cd34d7bf-2d6f-45f8-90be-73ff7f2f1c94'
guild = 'EpicRush'
# ---------------------------------------------------------------------------------------------
#                                         sqlite3
# ---------------------------------------------------------------------------------------------
conection = sqlite3.connect('DataBase.db')
cursor = conection.cursor()


# ---------------------------------------------------------------------------------------------
#                                         Commands
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
#                                         Hypixel
# ---------------------------------------------------------------------------------------------
@client.command(pass_context=True)
async def gxp(ctx, nick):
    author = ctx.message.author
    res = cursor.execute(f"SELECT exp FROM GXP WHERE name = '{nick}'")
    # WHERE name = '{nick}'
    await ctx.send(f'Weakly GEXP {nick} - {res.fetchone()[0]}')
    # for i in res.fetchall():
    #    for j in i:
    #        print(j, end=' ')
    #    print()


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def update(ctx):
    await ctx.channel.send('Updating....')
    g = requests.get("https://api.hypixel.net/guild?key=" + api_key + "&name=" + guild)
    g = g.json()
    counter = 0
    players = []

    for i in range(len(g['guild']['members'])):
        counter += 1
        uuid = g['guild']['members'][i]['uuid']
        x = requests.get("https://playerdb.co/api/player/minecraft/" + uuid)
        x = x.json()
        name = x['data']['player']['username']

        for names in name:
            print("name=", name)
        #          name = (f"{name: <16}")
        expHistory = g['guild']['members'][i]['expHistory']
        expHistory = sum(expHistory.values())
        init()

        expHistory = "{:,}".format(sum(g['guild']['members'][i]['expHistory'].values()))
        players.append([name, expHistory])
    counter = 0
    print("DELETE FROM GXP")
    cursor.execute("DELETE FROM GXP")
    for i in players:
        counter += 1
        cursor.execute("INSERT INTO GXP('name','exp','pos') VALUES (?, ?, ?)",
                       (i[0], int(i[1].replace(',', '')), counter))
    conection.commit()
    await ctx.channel.send('Updating comlited')


@client.command(pass_context=True)
async def top(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='TOP-25', colour=discord.Color.green())
    TopMembers = []
    for i in range(1, 126):
        try:
            name = cursor.execute(f"SELECT name FROM GXP WHERE pos = {i}").fetchone()[0]
            exp = cursor.execute(f"SELECT exp FROM GXP WHERE pos = {i}").fetchone()[0]
            print(name)
            print(exp)
            exp = str(exp)
            exp = exp.replace(',', '')
            exp = int(exp)
            TopMembers.append([name, exp])
        except TypeError:
            pass
    print(TopMembers)
    TopMembers.sort(key=lambda i: i[1], reverse=True)
    counter = 0
    for i in TopMembers:
        counter += 1
        emb.add_field(name=f'{counter}. {i[0]}', value=f'{i[1]} GEXP', inline=False)
    conection.commit()
    await ctx.channel.send(embed=emb)


@client.command(pass_context=True)
async def notop(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='TOP-25(NO)', colour=discord.Color.green())
    TopMembers = []
    for i in range(1, 126):
        try:
            name = cursor.execute(f"SELECT name FROM GXP WHERE pos = {i}").fetchone()[0]
            exp = cursor.execute(f"SELECT exp FROM GXP WHERE pos = {i}").fetchone()[0]
            print(name)
            print(exp)
            exp = str(exp)
            exp = exp.replace(',', '')
            exp = int(exp)
            TopMembers.append([name, exp])
        except TypeError:
            pass
    print(TopMembers)
    TopMembers.sort(key=lambda i: i[1], reverse=False)
    counter = 0
    for i in TopMembers:
        counter += 1
        emb.add_field(name=f'{counter}. {i[0]}', value=f'{i[1]} GEXP', inline=False)
    conection.commit()
    await ctx.channel.send(embed=emb)


# ---------------------------------------------------------------------------------------------
#                                    Ban/Kick
# ---------------------------------------------------------------------------------------------

# Chat clear
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=1000):
    await ctx.channel.purge(limit=amount + 1)


# Kick
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)

    await member.kick(reason=reason)
    await ctx.send(F'{member.mention} was kiked')


# Ban
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)

    await member.ban(reason=reason)
    await ctx.send(F'{member.mention} was baned')


# Unban
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)
    banned_users = await ctx.guild.bans()

    for ban_ in banned_users:
        user = ban_.user

        await ctx.guild.unban(user)
        await ctx.send(f'{user.mention} was unbaned')

        return


# ---------------------------------------------------------------------------------------------
#                                    Help list
# ---------------------------------------------------------------------------------------------


# Help for users
@client.command(pass_context=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Help', colour=discord.Color.green())
    emb.add_field(name=f'!help', value='Show this list', inline=False)
    emb.add_field(name=f'!rules', value='Show list with server rules', inline=False)
    emb.add_field(name=f'!money', value='Show your balance', inline=False)
    emb.add_field(name=f'!top', value='Shows TOP-25 GXP the best players', inline=False)
    emb.add_field(name=f'!notop', value='Shows TOP-25 GXP the worst players', inline=False)
    emb.add_field(name=f'!buy [role]', value='Buy role', inline=False)
    emb.add_field(name=f'!sbbuy [item]', value='Buy item in SkyBlock', inline=False)
    emb.add_field(name=f'!lvlinfo', value='Show your LVL', inline=False)
    emb.add_field(name=f'!luck [bet]', value='Jewish casino (Chance to win 40%.)', inline=False)
    await ctx.author.send(embed=emb)
    await ctx.send(f"Help list sent to {ctx.author.mention} in private messages")


# Help for admins
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def helpA(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Help', colour=discord.Color.green())
    emb.add_field(name=f'!clear [How many messages]', value='Clearning chat', inline=False)
    emb.add_field(name=f'!ban [player] [reason]', value='Ban player', inline=False)
    emb.add_field(name=f'!unban [player]', value='Unban player', inline=False)
    emb.add_field(name=f'!kick [player]', value='Kick player', inline=False)
    emb.add_field(name=f'!mute [player] [time(min)]', value='Mute player', inline=False)
    emb.add_field(name=f'!setrank [player] [rank]', value='Set player rank', inline=False)
    emb.add_field(name=f'!rankup [player]', value='Rank up player', inline=False)
    emb.add_field(name=f'!rankdown [player]', value='Rank down player', inline=False)
    emb.add_field(name=f'!take [player] [count]', value='Take money from the player', inline=False)
    emb.add_field(name=f'!award [player] [count]', value='Give money to the player', inline=False)
    emb.add_field(name=f'!update', value='Update TOP list', inline=False)
    emb.add_field(name=f'!addshop [role] [count]', value='Add new role in Roleshop', inline=False)
    emb.add_field(name=f'!removeshop [role]', value='Remove role from Roleshop', inline=False)
    emb.add_field(name=f'!shop', value='Show role shoplist', inline=False)
    emb.add_field(name=f'!addshopsb [item] [count]', value='Add new role in SkyBlock Shop ', inline=False)
    emb.add_field(name=f'!removeshopsb [item]', value='Remove role from SkyBlock Shop', inline=False)
    emb.add_field(name=f'!sbshop', value='Show SkyBlock shoplist', inline=False)
    emb.add_field(name=f'!xpinfo', value='Show your XP', inline=False)
    await ctx.author.send(embed=emb)
    await ctx.send(f"Help list sent to {ctx.author.mention} in private messages")


@client.command(pass_context=True)
async def rules(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Rules', colour=discord.Color.red())
    emb.add_field(name=f':page_facing_up: :page_facing_up:  :page_facing_up: ', value=':pushpin: 1. Be respectful, civil, and welcoming. \n :pushpin: 2. No insults, racism, sexism, homophobia, transphobia, and other \
    kinds of discriminatory speech. \n :pushpin: 3. No NSFW content \n :pushpin: 4. Do not join the server to promote your content. \n :pushpin: 5. The primary language of this server is English.')
    await ctx.author.send(embed=emb)
    await ctx.send(f"Rules sent to {ctx.author.mention} in private messages")


# ---------------------------------------------------------------------------------------------
#                                    Ranks
# ---------------------------------------------------------------------------------------------


# Mute
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time=60):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    await member.add_roles(mute_role)
    await ctx.send(f"{member.mention}, was muted for {time} min")
    await asyncio.sleep(int(time) * 60)
    await member.remove_roles(mute_role)
    await ctx.send(f"{member.mention}, was unmuted")


# set rank
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def setrank(ctx, member: discord.Member, rank):
    await ctx.channel.purge(limit=1)
    zombie_role = discord.utils.get(ctx.message.guild.roles, name='zombie')
    Skeleton_role = discord.utils.get(ctx.message.guild.roles, name='Skeleton')
    Creeper_role = discord.utils.get(ctx.message.guild.roles, name='Creeper')
    if rank.lower() == 'zombie':
        await member.remove_roles(Skeleton_role)
        await member.remove_roles(Creeper_role)
        await member.add_roles(zombie_role)
        await ctx.send(f'Set Rank {member.mention} Zombie')
    elif rank.lower() == 'skeleton':
        await member.add_roles(Skeleton_role)
        await member.remove_roles(Creeper_role)
        await member.add_roles(zombie_role)
        await ctx.send(f'Set Rank {member.mention} Skeleton')
    elif rank.lower() == 'creeper':
        await member.add_roles(Skeleton_role)
        await member.add_roles(Creeper_role)
        await member.add_roles(zombie_role)
        await ctx.send(f'Set Rank {member.mention} Creeper')


# Rank down
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def rankdown(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    Skeleton_role = discord.utils.get(ctx.message.guild.roles, name='Skeleton')
    Creeper_role = discord.utils.get(ctx.message.guild.roles, name='Creeper')
    member_roles = member.roles
    promote_this_time = False
    for i in member_roles:
        if 'Creeper' in str(i) and not promote_this_time:
            await ctx.send(f'Lowered {member.mention} from Creeper to Skeleton')
            await member.remove_roles(Creeper_role)
            promote_this_time = True
    for i in member_roles:
        if 'Skeleton' in str(i) and not promote_this_time:
            await ctx.send(f'Lowered {member.mention} from Skeleton to Zombie')
            await member.remove_roles(Skeleton_role)
            promote_this_time = True
    for i in member_roles:
        if 'Zombie' in str(i) and not promote_this_time:
            await ctx.send(f'Below is just the floor')
            promote_this_time = True


# Rank up
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def rankup(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    Skeleton_role = discord.utils.get(ctx.message.guild.roles, name='Skeleton')
    Creeper_role = discord.utils.get(ctx.message.guild.roles, name='Creeper')
    member_roles = member.roles
    promote_this_time = False
    for i in member_roles:
        if 'Creeper' in str(i) and not promote_this_time:
            await ctx.send(f'Please promote {member.mention} manually')
            promote_this_time = True
    for i in member_roles:
        if 'Skeleton' in str(i) and not promote_this_time:
            await member.add_roles(Creeper_role)
            await ctx.send(f'Promoted {member.mention} from Skeleton to Creeper')
            promote_this_time = True
    for i in member_roles:
        if 'Zombie' in str(i) and not promote_this_time:
            await member.add_roles(Skeleton_role)
            await ctx.send(f'Promoted {member.mention} from Zombie to Skeleton')
            promote_this_time = True


# ---------------------------------------------------------------------------------------------
#                                    Cash
# ---------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def luck(ctx, cash):
    cash = int(cash)
    if cash > 10000:
        await ctx.send("It's too much.Try no more than 10000")
    elif cash < 0:
        await ctx.send("Stupid?")
    elif cash >= cursor.execute(f"Select cash from users where id = {ctx.author.id}").fetchone()[0]:
        await ctx.send("You don't have enough money")
    else:
        if random.randint(1, 100) in range(41):
            cursor.execute(f"Update users SET cash = cash + {cash} Where id = {ctx.author.id}")
            await ctx.send(F"{ctx.author} won {cash}!")
        else:
            cursor.execute(f"Update users SET cash = cash - {cash} Where id = {ctx.author.id}")
            await ctx.send(F"{ctx.author} lost {cash}!")


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def paycheck(ctx):
    for i in client.get_guild(IdServer).members:
        member_roles = i.roles
        for j in member_roles:
            if str(j) == 'Zombie':
                cursor.execute(f"UPDATE users SET cash = cash + {1000} WHERE id = {i.id}")
            if str(j) == 'Skeleton':
                cursor.execute(f"UPDATE users SET cash = cash + {2000} WHERE id = {i.id}")
            if str(j) == 'Creeper':
                cursor.execute(f"UPDATE users SET cash = cash + {2000} WHERE id = {i.id}")
            if str(j) == 'Wither':
                cursor.execute(f"UPDATE users SET cash = cash + {5000} WHERE id = {i.id}")
    emb = discord.Embed(title='Paycheck', colour=discord.Color.green())
    emb.add_field(name='Use this command to see your cash:', value='!cash', inline=False)
    emb.add_field(name='Everyone who has roles will receive:',
                  value='Zombie - 1000 :dollar: \n Skeleton - 3000 :dollar: \n Creeper - 5000 :dollar: \n Wither - 10000 :dollar: ',
                  inline=False)
    await ctx.channel.send(embed=emb)
    conection.commit()


@client.command(aliases=['money'])
async def cash(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    if member is None:
        await ctx.send(embed=discord.Embed(
            description=f"""Balance {ctx.author} is {cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}:moneybag:"""
        ))
    else:
        await ctx.send(embed=discord.Embed(
            description=f"""Balance {member} is {cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}:moneybag:"""
        ))


@client.command(aliases=['award'])
@commands.has_permissions(administrator=True)
async def give(ctx, member: discord.Member = None, amount: int = None):
    await ctx.channel.purge(limit=1)
    if member is None:
        await ctx.send(f"{ctx.author}, Please enter username.")
    elif amount is None:
        await ctx.send(f"{ctx.author}, Indicate the amount you wish to charge.")
    elif amount < 1:
        await ctx.send(f"{ctx.author}, This is too little.")
    else:
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
        conection.commit()


@client.command(aliases=['without'])
@commands.has_permissions(administrator=True)
async def take(ctx, member: discord.Member = None, amount: int = None):
    await ctx.channel.purge(limit=1)
    if member is None:
        await ctx.send(f"{ctx.author}, Please enter username.")
    elif amount is None:
        await ctx.send(f"{ctx.author}, Indicate the amount you wish to charge.")
    elif amount < 1:
        await ctx.send(f"{ctx.author}, This is too little.")
    else:
        cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, member.id))
        conection.commit()


# ---------------------------------------------------------------------------------------------
#                                    XP and LVL info
# ---------------------------------------------------------------------------------------------


@client.command(aliases=['xpinfo'])
@commands.has_permissions(administrator=True)
async def __xpinfo(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    if member is None:
        await ctx.send(embed=discord.Embed(
            description=f"""Balance EXP {ctx.author} is {cursor.execute("SELECT EXP FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}:green_apple:"""
        ))

    else:
        await ctx.send(embed=discord.Embed(
            description=f"""Balance EXP {member} is {cursor.execute("SELECT EXP FROM users WHERE id = {}".format(member.id)).fetchone()[0]}:green_apple:"""
        ))


@client.command(aliases=['lvlinfo'])
async def __lvlinfo(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    if member is None:
        await ctx.send(embed=discord.Embed(
            description=f"""lvl {ctx.author} is {cursor.execute("SELECT LVL FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}"""
        ))

    else:
        await ctx.send(embed=discord.Embed(
            description=f"""lvl {member} is {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}"""
        ))


# ---------------------------------------------------------------------------------------------
#                                    Role Shop
# ---------------------------------------------------------------------------------------------

@client.command(aliases=['rich'])
async def __rich(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="TOP-10 (Money)")
    counter = 0
    for row in cursor.execute(f"SELECT name, cash FROM users Order BY cash Desc Limit 10"):
        counter += 1
        embed.add_field(name=f'{counter} place |{row[0]}', value=f'Cash: {row[1]}:dollar:', inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['addshop'])
@commands.has_permissions(administrator=True)
async def __addshop(ctx, role: discord.Role = None, cost: int = None):
    await ctx.channel.purge(limit=1)
    if role is None:
        await ctx.send('Select role')
    elif cost is None:
        await ctx.send('Select cost')
    elif cost < 0:
        await ctx.send('Stupid?')
    else:
        cursor.execute(f"INSERT INTO shop VALUES ({role.id},{ctx.guild.id},{cost})")
        conection.commit()
        await ctx.send('Success!')


@client.command(aliases=['removeshop'])
@commands.has_permissions(administrator=True)
async def __removeshop(ctx, role: discord.Role = None):
    await ctx.channel.purge(limit=1)
    if role is None:
        await ctx.send('Select role')
    else:
        cursor.execute(f"DELETE FROM shop WHERE role_id = {role.id}")
        await ctx.send('Success!')
        conection.commit()


@client.command(aliases=['roleshop'])
@commands.has_permissions(administrator=True)
async def shop(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="Role shop")
    for row in cursor.execute(f"SELECT role_id, cost FROM shop WHERE id = {ctx.guild.id}"):
        if ctx.guild.get_role(row[0]) != None:
            embed.add_field(name=f'It cost {row[1]}',value=f'You buy the role{ctx.guild.get_role(row[0]).mention}',inline=False)
#            embed.add_field(name=f'{ctx.guild.get_role(row[0]).mention} - {row[1]}', value=f'To buy it use !buy {ctx.guild.get_role(row[0]).mention}', inline=False)
        else:
            pass
    await ctx.send(embed=embed)


@client.command(aliases=['buy'])
async def __buy(ctx, role: discord.Role = None):
    await ctx.channel.purge(limit=1)
    if role is None:
        await ctx.send('Select role')
    else:
        if role in ctx.author.roles:
            await ctx.send('You already have this role')
        elif cursor.execute(f"Select cost from shop where role_id = {role.id}").fetchone()[0] > \
                cursor.execute(f"Select cash from users where id = {ctx.author.id}").fetchone()[0]:
            await ctx.send("You don't have enough money")
        else:
            await ctx.author.add_roles(role)
            cursor.execute(
                f"Update users SET cash = cash - {cursor.execute(f'Select cost from shop where role_id = {role.id}').fetchone()[0]} Where id = {ctx.author.id}")
            channel = client.get_channel(AuditChatel)
            await channel.send(f'{ctx.author.mention} bought {role} role')
            await ctx.send('Success!')


# ---------------------------------------------------------------------------------------------
#                                    SkyBlock Shop
# ---------------------------------------------------------------------------------------------

@client.command(aliases=['addshopsb'])
@commands.has_permissions(administrator=True)
async def __addshopsb(ctx, item=None, cost: int = None):
    await ctx.channel.purge(limit=1)
    if item is None:
        await ctx.send('Select item')
    elif cost is None:
        await ctx.send('Select cost')
    elif cost < 0:
        await ctx.send('Stupid?')
    else:
        cursor.execute(f"INSERT INTO sbshop VALUES ('{item}',{cost})")
        conection.commit()
        await ctx.send('Success!')


@client.command(aliases=['removeshopsb'])
@commands.has_permissions(administrator=True)
async def __removeshopsb(ctx, item=None):
    await ctx.channel.purge(limit=1)
    if item is None:
        await ctx.send('Select item')
    else:
        cursor.execute(f"DELETE FROM sbshop WHERE item = '{item}'")
        await ctx.send('Success!')
        conection.commit()


@client.command(aliases=['sbshop'])
@commands.has_permissions(administrator=True)
async def shopsb(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="SkyBlock shop")
    for row in cursor.execute(f"SELECT item, cost FROM sbshop"):
        embed.add_field(name=f'{row[0]} - {row[1]}:dollar:', value=f'To buy it use !sbbuy {row[0]}', inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['sbbuy'])
async def __buysb(ctx, item=None, ):
    await ctx.channel.purge(limit=1)
    if item is None:
        await ctx.send('Select item')
    else:
        if cursor.execute(f"Select cost from sbshop where item = '{item}'").fetchone()[0] > \
                cursor.execute(f"Select cash from users where id = {ctx.author.id}").fetchone()[0]:
            await ctx.send("You don't have enough money")
        else:
            A = {cursor.execute(f"Select cost from sbshop where item = '{item}'").fetchone()[0]}
            A = int(str(A)[1:-1])
            cursor.execute(f"Update users SET cash = cash - {A} Where id = {ctx.author.id}")
            channel = client.get_channel(AuditChatel)
            await channel.send(f'{ctx.author.mention} waiting order ({item})')
            await ctx.send('Success!')


# ---------------------------------------------------------------------------------------------
#                                    Events
# ---------------------------------------------------------------------------------------------

@client.event
async def on_message(message):
    await client.process_commands(message)
    if not str(message.content).startswith('!'):
        xp = len(message.content) // 10
        if xp > 10:
            xp = 10
        cursor.execute(f"UPDATE users SET EXP = EXP + {xp} Where id = {message.author.id}")
    EXP = cursor.execute("SELECT EXP FROM users WHERE id = {}".format(message.author.id)).fetchone()[0]
    LVL = cursor.execute("SELECT LVL FROM users WHERE id = {}".format(message.author.id)).fetchone()[0]
    if EXP >= 50 + LVL * 35:
        cursor.execute(f"UPDATE users SET EXP = EXP - (50 + {LVL} * 10) Where id = {message.author.id}")
        cursor.execute(f"UPDATE users SET LVL = LVL + 1 Where id = {message.author.id}")
        if message.author != 'EpicRushBot#8883':
            await message.channel.send(f'{message.author}, achived {LVL + 1} LVL!')
        cursor.execute(f"UPDATE users SET cash = cash + {1000 + LVL * 500} WHERE id = {message.author.id}")
    conection.commit()


# Bot conected
@client.event
async def on_ready():
    print('Bot conected ')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('EpicRush TOP'))
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    id INT,
    cash BUGINT,
    EXP INT,
    lvl INT,
    server_id INT
    )""")
    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1, {IdServer})")
    cursor.execute("""CREATE TABLE IF NOT EXISTS GXP(name STR,exp INT,pos INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS shop(role_id INT,id INT,cost INT)""")
    #    cursor.execute('''DROP table if exists sbshop''')
    cursor.execute("""CREATE TABLE IF NOT EXISTS sbshop(item STR, cost INT)""")
    conection.commit()


# Member role
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=IdZombieRole)
    await member.add_roles(role)
    if cursor.execute(f'Select id FROM users WHERE id = {member.id}').fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}, {member.id}, 0, 0, 1')")
        conection.commit()
    else:
        pass


# don't touch it!!
"""
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(description=f'{ctx.author.name}, Command not found!',
                                           colour=discord.Color.red()))

"""
# ---------------------------------------------------------------------------------------------
#                                     Errors
# ---------------------------------------------------------------------------------------------

# Set rank error
@setrank.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


# Rank down error
@rankdown.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


# Rank up error
@rankup.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


# Clear error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


# Kick error
@kick.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


# Ban error
@ban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


# Un ban error
@unban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


@give.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


@take.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


@paycheck.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


# Mute error
@mute.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, This command is needed only for the Administration.')


# HelpA error
@helpA.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


@__addshop.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


@__removeshop.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


@__addshopsb.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


@__removeshopsb.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name},  missing argument')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name}, You don't have enough permissions")


# ---------------------------------------------------------------------------------------------
#                                     Run
# ---------------------------------------------------------------------------------------------

client.run(TOKEN)
