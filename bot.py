
import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# GAME DATA
# =========================

characters = [
    {
        "name": "Eminem",
        "clues": [
            "I am an American rapper.",
            "I am also known as Slim Shady.",
            "I made the song Lose Yourself."
        ]
    },
    {
        "name": "Shah Rukh Khan",
        "clues": [
            "I am an Indian actor.",
            "I am known as the King of Bollywood.",
            "I starred in Pathaan."
        ]
    },
    {
        "name": "Spider-Man",
        "clues": [
            "I am a superhero.",
            "I can shoot webs.",
            "Peter Parker is one version of me."
        ]
    }
]

songs = [
    ("🌃 💡 🚗", "Blinding Lights"),
    ("👸 💎", "Princess Diana"),
    ("☀️ 🌻", "Sunflower"),
    ("🚀 🌙", "Starboy"),
    ("🔥 🎉", "Party Rock Anthem")
]

wyr_questions = [
    ("Never listen to music again", "Never watch movies again"),
    ("Be invisible", "Read minds"),
    ("Have unlimited money", "Have unlimited free time"),
    ("Never use YouTube again", "Never use Discord again"),
    ("Travel anywhere for free", "Eat anything for free")
]

roasts = [
    "Bro's WiFi has more personality than him 💀",
    "Even Google doesn't know what you're doing 💀",
    "Bro's loading screen has been stuck since birth 😂",
    "Your aim is so bad, even NPCs dodge you 💀",
    "Bro entered the server and lowered the IQ 💀",
    "You're not useless, you can still be a bad example 😂"
]

scores = {}


def add_score(user_id, points):
    scores[user_id] = scores.get(user_id, 0) + points


# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


# =========================
# GUESS THE CHARACTER
# =========================

@bot.tree.command(name="character", description="Guess the character!")
async def character(interaction: discord.Interaction):

    character_data = random.choice(characters)

    embed = discord.Embed(
        title="🧠 GUESS THE CHARACTER",
        description=f"**Clue 1:** {character_data['clues'][0]}\n\n"
                    "Type your answer in chat!\n"
                    "💰 **100 XP**",
    )

    await interaction.response.send_message(embed=embed)

    def check(message):
        return (
            message.channel == interaction.channel
            and not message.author.bot
        )

    try:
        message = await bot.wait_for(
            "message",
            timeout=30,
            check=check
        )

        if message.content.lower().strip() == character_data["name"].lower():
            add_score(message.author.id, 100)

            await interaction.channel.send(
                f"🎉 **Correct!** {message.author.mention} "
                f"guessed **{character_data['name']}**!\n"
                f"🏆 **+100 XP**"
            )
        else:
            await interaction.channel.send(
                f"❌ Wrong answer!\n"
                f"The answer was **{character_data['name']}**."
            )

    except Exception:
        await interaction.channel.send(
            f"⏰ Time's up!\n"
            f"The answer was **{character_data['name']}**."
        )


# =========================
# GUESS SONG FROM EMOJI
# =========================

@bot.tree.command(
    name="songemoji",
    description="Guess the song from emojis!"
)
async def songemoji(interaction: discord.Interaction):

    emoji, answer = random.choice(songs)

    embed = discord.Embed(
        title="🎵 GUESS THE SONG",
        description=f"# {emoji}\n\n"
                    "Type the song name!\n"
                    "💰 **100 XP**"
    )

    await interaction.response.send_message(embed=embed)

    def check(message):
        return (
            message.channel == interaction.channel
            and not message.author.bot
        )

    try:
        message = await bot.wait_for(
            "message",
            timeout=30,
            check=check
        )

        if message.content.lower().strip() == answer.lower():
            add_score(message.author.id, 100)

            await interaction.channel.send(
                f"🎉 **Correct!** {message.author.mention}\n"
                f"🎵 Song: **{answer}**\n"
                f"🏆 **+100 XP**"
            )
        else:
            await interaction.channel.send(
                f"❌ Wrong!\n🎵 The answer was **{answer}**."
            )

    except Exception:
        await interaction.channel.send(
            f"⏰ Time's up!\n🎵 The answer was **{answer}**."
        )


# =========================
# WOULD YOU RATHER
# =========================

@bot.tree.command(
    name="wyr",
    description="Play Would You Rather!"
)
async def wyr(interaction: discord.Interaction):

    option_a, option_b = random.choice(wyr_questions)

    embed = discord.Embed(
        title="🤔 WOULD YOU RATHER?",
        description=f"🅰️ **{option_a}**\n\n"
                    f"🅱️ **{option_b}**\n\n"
                    "React with 🅰️ or 🅱️!"
    )

    message = await interaction.response.send_message(
        embed=embed,
        wait=True
    )

    await message.add_reaction("🅰️")
    await message.add_reaction("🅱️")


# =========================
# ROAST
# =========================

@bot.tree.command(
    name="roast",
    description="Roast someone!"
)
async def roast(
    interaction: discord.Interaction,
    user: discord.Member
):

    roast_text = random.choice(roasts)

    await interaction.response.send_message(
        f"🔥 **Roast incoming...**\n\n"
        f"{user.mention}\n"
        f"💀 {roast_text}"
    )


# =========================
# ROAST YOURSELF
# =========================

@bot.tree.command(
    name="roastme",
    description="Get yourself roasted!"
)
async def roastme(interaction: discord.Interaction):

    roast_text = random.choice(roasts)

    await interaction.response.send_message(
        f"🔥 {interaction.user.mention}\n\n"
        f"💀 {roast_text}"
    )


# =========================
# PROFILE
# =========================

@bot.tree.command(
    name="profile",
    description="Check your XP!"
)
async def profile(interaction: discord.Interaction):

    xp = scores.get(interaction.user.id, 0)

    await interaction.response.send_message(
        f"👤 **{interaction.user.display_name}**\n"
        f"🏆 XP: **{xp}**"
    )


# =========================
# LEADERBOARD
# =========================

@bot.tree.command(
    name="leaderboard",
    description="View the XP leaderboard!"
)
async def leaderboard(interaction: discord.Interaction):

    if not scores:
        await interaction.response.send_message(
            "🏆 Leaderboard is empty!"
        )
        return

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    text = "🏆 **BAXODI GAMES LEADERBOARD**\n\n"

    for position, (user_id, xp) in enumerate(
        sorted_scores[:10],
        start=1
    ):
        user = bot.get_user(user_id)

        if user:
            text += f"**{position}.** {user.mention} — `{xp} XP`\n"

    await interaction.response.send_message(text)


# =========================
# START BOT
# =========================

if not TOKEN:
    print("ERROR: DISCORD_TOKEN is missing!")

else:
    bot.run(TOKEN)
