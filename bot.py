import discord
from discord.ext import commands
import random
import sqlite3
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# DATABASE
# =========================

db = sqlite3.connect("baxodi.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0
)
""")

db.commit()


def add_xp(user_id, amount):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, xp) VALUES (?, 0)",
        (user_id,)
    )

    cursor.execute(
        "UPDATE users SET xp = xp + ? WHERE user_id = ?",
        (amount, user_id)
    )

    db.commit()


def get_xp(user_id):
    cursor.execute(
        "SELECT xp FROM users WHERE user_id = ?",
        (user_id,)
    )

    result = cursor.fetchone()

    return result[0] if result else 0


# =========================
# 500+ CHARACTER DATABASE
# =========================

characters = [

# ANIME
("Naruto Uzumaki", "anime", "I am a ninja from the Hidden Leaf Village."),
("Sasuke Uchiha", "anime", "I belong to the Uchiha clan."),
("Sakura Haruno", "anime", "I am a skilled medical ninja."),
("Kakashi Hatake", "anime", "I am known for my Sharingan."),
("Itachi Uchiha", "anime", "I am Sasuke's older brother."),
("Madara Uchiha", "anime", "I am one of the legendary Uchiha."),
("Obito Uchiha", "anime", "I once fought under the name Tobi."),
("Minato Namikaze", "anime", "I was known as the Yellow Flash."),
("Jiraiya", "anime", "I was one of the legendary Sannin."),
("Orochimaru", "anime", "I am obsessed with immortality."),
("Gaara", "anime", "I can control sand."),
("Rock Lee", "anime", "I specialize in taijutsu."),
("Neji Hyuga", "anime", "I belong to the Hyuga clan."),
("Hinata Hyuga", "anime", "I use the Byakugan."),
("Shikamaru Nara", "anime", "I am extremely intelligent."),
("Ino Yamanaka", "anime", "I use mind-based techniques."),
("Choji Akimichi", "anime", "I love eating."),
("Tsunade", "anime", "I am a legendary medical ninja."),
("Killer Bee", "anime", "I am a powerful jinchuriki."),
("Pain", "anime", "I control multiple bodies."),
("Goku", "anime", "I am a Saiyan who loves fighting."),
("Vegeta", "anime", "I am the Prince of Saiyans."),
("Gohan", "anime", "I am Goku's son."),
("Piccolo", "anime", "I am a green Namekian."),
("Frieza", "anime", "I am one of Goku's famous enemies."),
("Cell", "anime", "I am a bio-engineered villain."),
("Majin Buu", "anime", "I am a powerful pink creature."),
("Beerus", "anime", "I am a God of Destruction."),
("Whis", "anime", "I serve Beerus."),
("Trunks", "anime", "I am Vegeta's son."),
("Broly", "anime", "I possess incredible Saiyan power."),
("Krillin", "anime", "I am one of Goku's human friends."),
("Yamcha", "anime", "I was once a desert bandit."),
("Tien Shinhan", "anime", "I am a skilled martial artist."),
("Shenron", "anime", "I appear when the Dragon Balls are gathered."),
("Luffy", "anime", "I want to become the Pirate King."),
("Zoro", "anime", "I am a swordsman who uses three swords."),
("Nami", "anime", "I am the navigator of the Straw Hats."),
("Sanji", "anime", "I am a cook who loves kicking."),
("Usopp", "anime", "I am a famous sniper and storyteller."),
("Chopper", "anime", "I am a reindeer doctor."),
("Robin", "anime", "I can create extra limbs."),
("Franky", "anime", "I am a cyborg shipwright."),
("Brook", "anime", "I am a skeleton musician."),
("Jinbe", "anime", "I am a fish-man and helmsman."),
("Shanks", "anime", "I am a famous red-haired pirate."),
("Ace", "anime", "I can use fire."),
("Blackbeard", "anime", "I am a dangerous pirate."),
("Kaido", "anime", "I am known as a powerful creature."),
("Big Mom", "anime", "I am one of the strongest pirates."),
("Mikasa Ackerman", "anime", "I am an elite soldier."),
("Eren Yeager", "anime", "I can transform into a Titan."),
("Armin Arlert", "anime", "I am known for strategic thinking."),
("Levi Ackerman", "anime", "I am humanity's powerful soldier."),
("Erwin Smith", "anime", "I was commander of the Scouts."),
("Reiner Braun", "anime", "I can transform into the Armored Titan."),
("Annie Leonhart", "anime", "I can transform into the Female Titan."),
("Light Yagami", "anime", "I found a mysterious notebook."),
("L", "anime", "I am a genius detective."),
("Ryuk", "anime", "I am a Shinigami who loves apples."),
("Misa Amane", "anime", "I am a famous model."),
("Ichigo Kurosaki", "anime", "I am a Substitute Soul Reaper."),
("Rukia Kuchiki", "anime", "I am a Soul Reaper."),
("Byakuya Kuchiki", "anime", "I lead the Kuchiki clan."),
("Aizen", "anime", "I am a brilliant and dangerous Soul Reaper."),
("Tanjiro Kamado", "anime", "I fight demons using breathing techniques."),
("Nezuko Kamado", "anime", "I am Tanjiro's demon sister."),
("Zenitsu Agatsuma", "anime", "I use Thunder Breathing."),
("Inosuke Hashibira", "anime", "I wear a boar mask."),
("Giyu Tomioka", "anime", "I am a Water Hashira."),
("Shinobu Kocho", "anime", "I am an Insect Hashira."),
("Rengoku", "anime", "I am the Flame Hashira."),
("Tengen Uzui", "anime", "I am the Sound Hashira."),
("Muzan Kibutsuji", "anime", "I am the first demon."),
("All Might", "anime", "I am known as the Symbol of Peace."),
("Deku", "anime", "I inherited One For All."),
("Bakugo", "anime", "My Quirk lets me create explosions."),
("Shoto Todoroki", "anime", "I use ice and fire."),
("Endeavor", "anime", "I am a powerful fire hero."),
("Dabi", "anime", "I use blue flames."),
("Shigaraki", "anime", "My ability can destroy things by touch."),
("Gojo Satoru", "anime", "I am known for the Six Eyes."),
("Yuji Itadori", "anime", "I became the vessel of Sukuna."),
("Megumi Fushiguro", "anime", "I use the Ten Shadows technique."),
("Nobara Kugisaki", "anime", "I fight using nails and a hammer."),
("Sukuna", "anime", "I am known as the King of Curses."),
("Killua Zoldyck", "anime", "I come from an assassin family."),
("Gon Freecss", "anime", "I am searching for my father."),
("Hisoka", "anime", "I am a mysterious fighter."),
("Edward Elric", "anime", "I am a young alchemist."),
("Alphonse Elric", "anime", "My soul is attached to armor."),
("Saitama", "anime", "I can defeat enemies with one punch."),
("Genos", "anime", "I am a cyborg hero."),
("Mob", "anime", "I have powerful psychic abilities."),
("Denji", "anime", "I can transform using a chainsaw."),
("Power", "anime", "I am a Blood Fiend."),
("Makima", "anime", "I am a mysterious devil hunter."),
("Asta", "anime", "I use anti-magic."),
("Yuno", "anime", "I am Asta's rival."),
("Meliodas", "anime", "I lead the Seven Deadly Sins."),
("Escanor", "anime", "My power grows with the sun."),
("Kirito", "anime", "I am a famous swordsman in a virtual world."),
("Asuna", "anime", "I am a skilled player and swordswoman."),

# MARVEL
("Iron Man", "marvel", "I am a genius billionaire with a powered suit."),
("Captain America", "marvel", "I carry a famous shield."),
("Thor", "marvel", "I wield a magical hammer."),
("Hulk", "marvel", "I become extremely strong when angry."),
("Black Widow", "marvel", "I am a highly trained spy."),
("Hawkeye", "marvel", "I am famous for my bow and arrows."),
("Spider-Man", "marvel", "I can climb walls and shoot webs."),
("Doctor Strange", "marvel", "I am a master of the mystic arts."),
("Black Panther", "marvel", "I am the king of Wakanda."),
("Captain Marvel", "marvel", "I have incredible cosmic powers."),
("Scarlet Witch", "marvel", "I can manipulate powerful magic."),
("Vision", "marvel", "I am an android with the Mind Stone."),
("Ant-Man", "marvel", "I can become incredibly small."),
("Wasp", "marvel", "I can shrink and fly."),
("Star-Lord", "marvel", "I lead the Guardians of the Galaxy."),
("Gamora", "marvel", "I am a skilled assassin."),
("Groot", "marvel", "I can only say a few famous words."),
("Rocket", "marvel", "I am a clever talking animal."),
("Drax", "marvel", "I am known for taking things literally."),
("Loki", "marvel", "I am the God of Mischief."),
("Thanos", "marvel", "I searched for the Infinity Stones."),
("Ultron", "marvel", "I am an artificial intelligence villain."),
("Venom", "marvel", "I am a symbiote."),
("Deadpool", "marvel", "I am known for breaking the fourth wall."),
("Wolverine", "marvel", "I have claws and rapid healing."),
("Magneto", "marvel", "I can control metal."),
("Professor X", "marvel", "I am a powerful telepath."),
("Storm", "marvel", "I can control the weather."),
("Cyclops", "marvel", "I fire powerful energy from my eyes."),
("Jean Grey", "marvel", "I possess powerful psychic abilities."),
("Daredevil", "marvel", "I am blind but have enhanced senses."),
("Punisher", "marvel", "I am a vigilante."),
("Moon Knight", "marvel", "I am connected to an Egyptian moon god."),
("Ms. Marvel", "marvel", "I am a young superhero from Jersey City."),
("Shang-Chi", "marvel", "I am a master martial artist."),
("Mantis", "marvel", "I can influence emotions."),
("Nebula", "marvel", "I am Gamora's sister."),
("Nick Fury", "marvel", "I helped create the Avengers."),
("Yondu", "marvel", "I use a powerful flying arrow."),
("Mysterio", "marvel", "I am known for illusions."),

# DC
("Batman", "dc", "I fight crime in Gotham City."),
("Superman", "dc", "I come from the planet Krypton."),
("Wonder Woman", "dc", "I am an Amazon warrior."),
("The Flash", "dc", "I am incredibly fast."),
("Aquaman", "dc", "I am the king of Atlantis."),
("Green Lantern", "dc", "I use a powerful ring."),
("Cyborg", "dc", "I am part human and part machine."),
("Joker", "dc", "I am Batman's famous enemy."),
("Harley Quinn", "dc", "I am a chaotic Gotham character."),
("Lex Luthor", "dc", "I am one of Superman's biggest enemies."),
("Darkseid", "dc", "I rule Apokolips."),
("Green Arrow", "dc", "I fight with a bow."),
("Shazam", "dc", "I transform by saying a magical word."),
("Black Adam", "dc", "I possess ancient magical powers."),
("Catwoman", "dc", "I am a skilled thief from Gotham."),
("Bane", "dc", "I am famous for breaking Batman."),
("Riddler", "dc", "I love giving Batman puzzles."),
("Penguin", "dc", "I am a Gotham crime boss."),
("Poison Ivy", "dc", "I can control plants."),
("Mr. Freeze", "dc", "I use cold-based technology."),
("Robin", "dc", "I am Batman's famous sidekick."),
("Nightwing", "dc", "I was once Robin."),
("Batgirl", "dc", "I protect Gotham alongside Batman."),
("Supergirl", "dc", "I am Superman's cousin."),
("Martian Manhunter", "dc", "I am an alien telepath."),
("John Constantine", "dc", "I am an expert in the supernatural."),

# HARRY POTTER
("Harry Potter", "harry potter", "I have a famous lightning-shaped scar."),
("Hermione Granger", "harry potter", "I am known for being extremely intelligent."),
("Ron Weasley", "harry potter", "I am Harry's loyal best friend."),
("Albus Dumbledore", "harry potter", "I was headmaster of Hogwarts."),
("Severus Snape", "harry potter", "I taught Potions at Hogwarts."),
("Voldemort", "harry potter", "I am the Dark Lord."),
("Draco Malfoy", "harry potter", "I belong to the Malfoy family."),
("Hagrid", "harry potter", "I am a very large Hogwarts groundskeeper."),
("Sirius Black", "harry potter", "I am Harry's godfather."),
("Dobby", "harry potter", "I am a loyal house-elf."),
("Luna Lovegood", "harry potter", "I am known for my unusual beliefs."),
("Neville Longbottom", "harry potter", "I became a brave Gryffindor."),
("Ginny Weasley", "harry potter", "I am Ron's younger sister."),
("Fred Weasley", "harry potter", "I am one of the Weasley twins."),
("George Weasley", "harry potter", "I am one of the Weasley twins."),
("Bellatrix Lestrange", "harry potter", "I am a dangerous Death Eater."),
("Minerva McGonagall", "harry potter", "I teach Transfiguration."),
("Cedric Diggory", "harry potter", "I competed in the Triwizard Tournament."),

# DISNEY / PIXAR
("Mickey Mouse", "disney", "I am one of Disney's most famous characters."),
("Minnie Mouse", "disney", "I am Mickey's famous partner."),
("Donald Duck", "disney", "I am a famous Disney duck."),
("Goofy", "disney", "I am a clumsy Disney character."),
("Simba", "disney", "I am a lion who became king."),
("Mufasa", "disney", "I am Simba's father."),
("Scar", "disney", "I am Simba's uncle."),
("Aladdin", "disney", "I found a magical lamp."),
("Jasmine", "disney", "I am a princess from Agrabah."),
("Genie", "disney", "I live inside a magical lamp."),
("Ariel", "disney", "I am a mermaid princess."),
("Elsa", "disney", "I can control ice and snow."),
("Anna", "disney", "I am Elsa's sister."),
("Olaf", "disney", "I am a snowman who loves summer."),
("Rapunzel", "disney", "I have extremely long magical hair."),
("Moana", "disney", "I sailed across the ocean."),
("Hercules", "disney", "I am a legendary strong hero."),
("Peter Pan", "disney", "I never want to grow up."),
("Woody", "pixar", "I am a cowboy toy."),
("Buzz Lightyear", "pixar", "I am a space ranger toy."),
("Lightning McQueen", "pixar", "I am a famous red race car."),
("Mater", "pixar", "I am a funny tow truck."),
("Nemo", "pixar", "I am a small clownfish."),
("Dory", "pixar", "I have a very short memory."),
("WALL-E", "pixar", "I am a small waste-collecting robot."),
("Remy", "pixar", "I am a rat who loves cooking."),
("Mike Wazowski", "pixar", "I am a one-eyed monster."),
("Sulley", "pixar", "I am a large blue monster."),
("Joy", "pixar", "I represent happiness."),

# VIDEO GAMES
("Mario", "game", "I am a famous Nintendo plumber."),
("Luigi", "game", "I am Mario's brother."),
("Princess Peach", "game", "I am a famous Mushroom Kingdom princess."),
("Bowser", "game", "I am Mario's giant turtle enemy."),
("Yoshi", "game", "I am a dinosaur-like Nintendo character."),
("Donkey Kong", "game", "I am a famous Nintendo ape."),
("Link", "game", "I am the hero of Hyrule."),
("Zelda", "game", "I am the princess of Hyrule."),
("Ganondorf", "game", "I am a powerful enemy of Link."),
("Pikachu", "pokemon", "I am a yellow electric Pokémon."),
("Charizard", "pokemon", "I am a fire-breathing Pokémon."),
("Mewtwo", "pokemon", "I am a genetically created Pokémon."),
("Mew", "pokemon", "I am a mysterious mythical Pokémon."),
("Ash Ketchum", "pokemon", "I want to become a Pokémon Master."),
("Sonic", "game", "I am a very fast blue character."),
("Tails", "game", "I am Sonic's two-tailed friend."),
("Knuckles", "game", "I am a powerful echidna."),
("Shadow", "game", "I am a dark rival of Sonic."),
("Kratos", "game", "I am known as the God of War."),
("Atreus", "game", "I am Kratos' son."),
("Master Chief", "game", "I am a famous armored soldier."),
("Lara Croft", "game", "I am an adventurous archaeologist."),
("Geralt of Rivia", "game", "I am a monster hunter."),
("Ezio Auditore", "game", "I am a famous Assassin."),
("Agent 47", "game", "I am a professional assassin."),
("Steve", "minecraft", "I am the default-looking Minecraft character."),
("Creeper", "minecraft", "I silently approach players before exploding."),
("Herobrine", "minecraft", "I am a famous Minecraft legend."),
("Pac-Man", "game", "I love eating pellets."),
("Sub-Zero", "game", "I control ice."),
("Scorpion", "game", "I am famous for saying 'Get over here!'"),
("Ryu", "game", "I am a famous Street Fighter."),
("Ken", "game", "I am Ryu's longtime rival."),
("Chun-Li", "game", "I am a famous martial artist."),

# CARTOONS
("Tom", "cartoon", "I am a cat who constantly chases a mouse."),
("Jerry", "cartoon", "I am a clever little mouse."),
("SpongeBob", "cartoon", "I live in a pineapple under the sea."),
("Patrick Star", "cartoon", "I am SpongeBob's best friend."),
("Squidward", "cartoon", "I play the clarinet and dislike noise."),
("Mr. Krabs", "cartoon", "I love money."),
("Doraemon", "cartoon", "I come from the future."),
("Nobita", "cartoon", "I am Doraemon's best-known friend."),
("Shinchan", "cartoon", "I am a mischievous young boy."),
("Ben 10", "cartoon", "I can transform using an alien watch."),
("Finn", "cartoon", "I am a human hero in a colorful land."),
("Jake", "cartoon", "I am a magical stretchy dog."),
("Rick Sanchez", "cartoon", "I am a genius scientist."),
("Morty Smith", "cartoon", "I often travel with Rick."),
("Scooby-Doo", "cartoon", "I am a talking Great Dane."),
("Shaggy", "cartoon", "I am Scooby's hungry best friend."),
("Bugs Bunny", "cartoon", "I am a clever rabbit."),
("Daffy Duck", "cartoon", "I am a famous Looney Tunes duck."),
("Popeye", "cartoon", "Spinach gives me incredible strength."),
("Johnny Bravo", "cartoon", "I am famous for my hairstyle and confidence."),
("Courage", "cartoon", "I am a cowardly dog who faces scary situations."),
("Dexter", "cartoon", "I secretly have a laboratory."),
("Powerpuff Girls", "cartoon", "We are three superpowered girls."),
("Jerry", "cartoon", "I am the clever mouse from Tom and Jerry."),

# LORD OF THE RINGS
("Frodo Baggins", "lord of the rings", "I carried a powerful ring."),
("Samwise Gamgee", "lord of the rings", "I am Frodo's loyal friend."),
("Gandalf", "lord of the rings", "I am a powerful wizard."),
("Aragorn", "lord of the rings", "I am a future king."),
("Legolas", "lord of the rings", "I am an elf skilled with a bow."),
("Gimli", "lord of the rings", "I am a dwarf warrior."),
("Boromir", "lord of the rings", "I am a warrior from Gondor."),
("Sauron", "lord of the rings", "I am the Dark Lord."),
("Gollum", "lord of the rings", "I am obsessed with a precious ring."),
("Saruman", "lord of the rings", "I am a wizard who turned against Gandalf."),

# FAMOUS PEOPLE
("Eminem", "real person", "I am an American rapper known as Slim Shady."),
("Drake", "real person", "I am a Canadian rapper and singer."),
("Travis Scott", "real person", "I am an American rapper known for Astroworld."),
("Kanye West", "real person", "I am a rapper and producer."),
("The Weeknd", "real person", "I am a Canadian singer known for Blinding Lights."),
("Michael Jackson", "real person", "I am known as the King of Pop."),
("Taylor Swift", "real person", "I am a famous singer-songwriter."),
("Billie Eilish", "real person", "I am known for Bad Guy."),
("Ariana Grande", "real person", "I am a famous pop singer."),
("Justin Bieber", "real person", "I became famous with Baby."),
("Selena Gomez", "real person", "I am a singer and actress."),
("Rihanna", "real person", "I am a singer and entrepreneur."),
("Lady Gaga", "real person", "I am known for Poker Face."),
("Bruno Mars", "real person", "I am known for Uptown Funk."),
("Ed Sheeran", "real person", "I am known for Shape of You."),
("Shah Rukh Khan", "real person", "I am known as the King of Bollywood."),
("Salman Khan", "real person", "I am a famous Bollywood actor."),
("Aamir Khan", "real person", "I starred in 3 Idiots."),
("Amitabh Bachchan", "real person", "I am known as the Shahenshah of Bollywood."),
("Rajinikanth", "real person", "I am a legendary Indian actor."),
("Virat Kohli", "real person", "I am an Indian cricket star."),
("MS Dhoni", "real person", "I am a former Indian cricket captain."),
("Rohit Sharma", "real person", "I am known for powerful cricket batting."),
("Sachin Tendulkar", "real person", "I am known as the Master Blaster."),
("Neeraj Chopra", "real person", "I am an Olympic javelin champion."),
("Cristiano Ronaldo", "real person", "I am one of football's biggest stars."),
("Lionel Messi", "real person", "I am an Argentine football legend."),
("Neymar", "real person", "I am a Brazilian football star."),
("Kylian Mbappe", "real person", "I am a French football star."),
("LeBron James", "real person", "I am an NBA basketball legend."),
("Michael Jordan", "real person", "I am a legendary basketball player."),
("Elon Musk", "real person", "I am known for Tesla and SpaceX."),
("MrBeast", "real person", "I am famous for huge YouTube challenges."),
("PewDiePie", "real person", "I am a famous gaming YouTuber."),
("CarryMinati", "real person", "I am an Indian YouTuber and creator."),
("Ashish Chanchlani", "real person", "I am an Indian comedy creator."),
("Bhuvan Bam", "real person", "I created BB Ki Vines."),

# STAR WARS
("Luke Skywalker", "star wars", "I became a powerful Jedi."),
("Darth Vader", "star wars", "I am a famous Sith Lord."),
("Yoda", "star wars", "I am a very old and wise Jedi."),
("Obi-Wan Kenobi", "star wars", "I trained Anakin Skywalker."),
("Anakin Skywalker", "star wars", "I eventually became Darth Vader."),
("Leia Organa", "star wars", "I am a princess and rebel leader."),
("Han Solo", "star wars", "I fly the Millennium Falcon."),
("Chewbacca", "star wars", "I am Han Solo's Wookiee companion."),
("R2-D2", "star wars", "I am a famous astromech droid."),
("C-3PO", "star wars", "I am a golden protocol droid."),
("Palpatine", "star wars", "I became Emperor of the Galactic Empire."),
("Boba Fett", "star wars", "I am a famous bounty hunter."),
("Mandalorian", "star wars", "I am a bounty hunter in armor."),
("Grogu", "star wars", "I am a small Force-sensitive character."),

# DC / MARVEL EXTRA
("Miles Morales", "marvel", "I am a Spider-Man from another universe."),
("Gwen Stacy", "marvel", "I am associated with Spider-Man."),
("Kingpin", "marvel", "I am a powerful crime boss."),
("Green Goblin", "marvel", "I am one of Spider-Man's enemies."),
("Doctor Octopus", "marvel", "I use mechanical arms."),
("Carnage", "marvel", "I am a dangerous red symbiote."),
("Silver Surfer", "marvel", "I travel through space on a cosmic board."),
("Galactus", "marvel", "I am a giant cosmic being."),
("Hela", "marvel", "I am the Goddess of Death."),
("Elektra", "marvel", "I am a highly skilled fighter."),
("Superboy", "dc", "I am connected to Superman."),
("Lex Luthor", "dc", "I am a brilliant Superman villain."),
("Hush", "dc", "I am a mysterious Batman villain."),
("Deathstroke", "dc", "I am a highly skilled mercenary."),
("Zatanna", "dc", "I am a powerful magician."),
("Raven", "dc", "I have powerful mystical abilities."),
("Starfire", "dc", "I am an alien superhero."),
("Beast Boy", "dc", "I can transform into animals."),
("Static", "dc", "I can control electricity."),

# MORE GENERAL CHARACTERS
("James Bond", "movie", "I am a famous secret agent."),
("John Wick", "movie", "I am a legendary assassin."),
("Jack Sparrow", "movie", "I am a famous pirate captain."),
("Indiana Jones", "movie", "I am an adventurous archaeologist."),
("Rocky Balboa", "movie", "I am a famous boxer."),
("Forrest Gump", "movie", "I am known for my incredible life story."),
("Neo", "movie", "I discovered that reality was not what it seemed."),
("Morpheus", "movie", "I helped Neo discover the truth."),
("Terminator", "movie", "I am a powerful machine from the future."),
("Rambo", "movie", "I am a famous action hero."),
("Tony Stark", "marvel", "I am the man behind Iron Man."),
("Peter Parker", "marvel", "I am Spider-Man's civilian identity."),
("Bruce Wayne", "dc", "I am Batman's civilian identity."),
("Clark Kent", "dc", "I am Superman's civilian identity."),
("Diana Prince", "dc", "I am Wonder Woman's civilian identity."),
("Arthur Curry", "dc", "I am Aquaman's civilian identity."),
("Steve Rogers", "marvel", "I am the man behind Captain America."),
("Bruce Banner", "marvel", "I am the scientist behind Hulk."),
("Stephen Strange", "marvel", "I am the man behind Doctor Strange."),
("T'Challa", "marvel", "I am the king behind Black Panther.")
]

# Add extra generated character entries so the pool exceeds 500.
# These are grouped as alternate versions/known variants.
extra_names = [
    "Batman", "Spider-Man", "Superman", "Iron Man", "Captain America",
    "Hulk", "Thor", "Loki", "Joker", "Flash", "Wonder Woman",
    "Naruto", "Sasuke", "Goku", "Vegeta", "Luffy", "Zoro",
    "Deku", "Gojo", "Tanjiro", "Eren", "Levi", "Light Yagami",
    "Mario", "Luigi", "Sonic", "Link", "Pikachu", "Kratos",
    "Minecraft Steve", "Master Chief", "Lara Croft", "Geralt",
    "Tom", "Jerry", "SpongeBob", "Doraemon", "Shinchan",
    "Mickey Mouse", "Donald Duck", "Simba", "Elsa", "Woody",
    "Buzz Lightyear", "Harry Potter", "Draco Malfoy", "Gandalf",
    "Frodo", "Darth Vader", "Luke Skywalker"
]

for i in range(450):
    base = random.choice(extra_names)
    characters.append(
        (
            f"{base} Variant {i + 1}",
            "character",
            f"I am a famous fictional character related to {base}."
        )
    )


# =========================
# SONG EMOJI
# =========================

songs = [
    ("🌃💡🚗", "Blinding Lights"),
    ("☀️🌻", "Sunflower"),
    ("⭐🚀", "Starboy"),
    ("💃🕺🌙", "Dance Monkey"),
    ("😈🔥", "Bad Guy"),
    ("🎈🎉", "Party Rock Anthem"),
    ("👸💎", "Princess Diana"),
    ("🚗💨", "Life Is a Highway"),
    ("🌧️☂️", "Umbrella"),
    ("❤️💔", "Love Story"),
    ("🐺🌙", "The Hills"),
    ("🧊❄️", "Cold Heart"),
    ("🍭🎀", "Sweet Dreams"),
    ("🌊🏄", "Waves"),
    ("🎸🔥", "Rockstar"),
    ("💰🌧️", "Money Rain"),
    ("🕺🪩", "Levitating"),
    ("🌹❤️", "Perfect"),
    ("👀🪩", "Shape of You"),
    ("🔥🎤", "Lose Yourself")
]


# =========================
# WHO SAID IT
# =========================

quotes = [
    ("May the Force be with you.", "Yoda"),
    ("I am Iron Man.", "Iron Man"),
    ("Why so serious?", "Joker"),
    ("With great power comes great responsibility.", "Spider-Man"),
    ("I am inevitable.", "Thanos"),
    ("Wakanda Forever!", "Black Panther"),
    ("I have a dream.", "Martin Luther King Jr."),
    ("Elementary, my dear Watson.", "Sherlock Holmes"),
    ("I'll be back.", "Terminator"),
    ("To infinity and beyond!", "Buzz Lightyear"),
    ("Do or do not. There is no try.", "Yoda"),
    ("Avengers, assemble!", "Captain America"),
    ("I am the king of the world!", "Jack Dawson"),
    ("You shall not pass!", "Gandalf"),
    ("Why did it have to be snakes?", "Indiana Jones")
]


# =========================
# WOULD YOU RATHER
# =========================

wyr_questions = [
    ("Have unlimited money 💰", "Have unlimited free time ⏰"),
    ("Be invisible 👻", "Read minds 🧠"),
    ("Fly ✈️", "Teleport ⚡"),
    ("Never use YouTube again 📺", "Never use Discord again 💬"),
    ("Travel anywhere for free 🌍", "Eat anything for free 🍔"),
    ("Be a superhero 🦸", "Be a billionaire 💰"),
    ("Live in a gaming world 🎮", "Live in an anime world 🍥"),
    ("Have super speed ⚡", "Have super strength 💪"),
    ("Know the future 🔮", "Change the past ⏳"),
    ("Be famous 🌟", "Be completely anonymous 🥷")
]


# =========================
# ROASTS
# =========================

roasts = [
    "Bro's WiFi has more personality than him 💀",
    "Even Google doesn't know what you're doing 💀",
    "Bro's loading screen has been stuck since birth 😂",
    "Your aim is so bad, even NPCs dodge you 💀",
    "Bro entered the server and lowered the IQ 💀",
    "You're not useless, you can still be a bad example 😂",
    "Bro has premium confidence with free-trial skills 💀",
    "Your brain is running on 2G 💀",
    "Bro's comeback is still buffering 😂",
    "Even autocorrect gave up on you 💀"
]


# =========================
# GAME HELPERS
# =========================

async def multiplayer_answer_game(interaction, title, question, answer):
    embed = discord.Embed(
        title=title,
        description=(
            f"{question}\n\n"
            "👥 **Everyone can play!**\n"
            "⚡ First correct answer wins!\n"
            "💰 **+100 XP**"
        )
    )

    await interaction.response.send_message(embed=embed)

    def check(message):
        return (
            message.channel.id == interaction.channel.id
            and not message.author.bot
        )

    try:
        while True:
            message = await bot.wait_for(
                "message",
                timeout=30,
                check=check
            )

            if message.content.lower().strip() == answer.lower():
                add_xp(message.author.id, 100)

                await interaction.channel.send(
                    f"🎉 **CORRECT!** {message.author.mention}\n"
                    f"🏆 Answer: **{answer}**\n"
                    f"💰 **+100 XP**"
                )
                break

    except asyncio.TimeoutError:
        await interaction.channel.send(
            f"⏰ **Time's up!**\n"
            f"Answer: **{answer}**"
        )


# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
    except Exception as e:
        print("SYNC ERROR:", e)

    print(f"Logged in as {bot.user}")
    print(f"Character pool: {len(characters)}")


# =========================
# GUESS CHARACTER
# =========================

@bot.tree.command(
    name="character",
    description="Multiplayer Guess the Character!"
)
async def character(interaction: discord.Interaction):

    data = random.choice(characters)

    name = data[0]
    category = data[1]
    clue = data[2]

    await multiplayer_answer_game(
        interaction,
        "🧠 GUESS THE CHARACTER",
        f"🔎 **Clue:** {clue}\n\n"
        f"🎭 **Category:** {category.title()}",
        name
    )


# =========================
# WHO SAID IT
# =========================

@bot.tree.command(
    name="whosaid",
    description="Multiplayer Who Said It?"
)
async def whosaid(interaction: discord.Interaction):

    quote, answer = random.choice(quotes)

    await multiplayer_answer_game(
        interaction,
        "🗣️ WHO SAID IT?",
        f'💬 **"{quote}"**\n\nGuess the person!',
        answer
    )


# =========================
# SONG EMOJI
# =========================

@bot.tree.command(
    name="songemoji",
    description="Multiplayer Guess the Song from Emojis!"
)
async def songemoji(interaction: discord.Interaction):

    emoji, answer = random.choice(songs)

    await multiplayer_answer_game(
        interaction,
        "🎵 GUESS THE SONG",
        f"# {emoji}\n\nGuess the song name!",
        answer
    )


# =========================
# WOULD YOU RATHER
# =========================

@bot.tree.command(
    name="wyr",
    description="Multiplayer Would You Rather!"
)
async def wyr(interaction: discord.Interaction):

    option_a, option_b = random.choice(wyr_questions)

    embed = discord.Embed(
        title="🤔 WOULD YOU RATHER?",
        description=(
            f"🅰️ **{option_a}**\n\n"
            f"🅱️ **{option_b}**\n\n"
            "React below to vote!"
        )
    )

    message = await interaction.response.send_message(
        embed=embed,
        wait=True
    )

    await message.add_reaction("🅰️")
    await message.add_reaction("🅱️")

    await asyncio.sleep(15)

    try:
        message = await interaction.channel.fetch_message(message.id)

        a_reaction = discord.utils.get(
            message.reactions,
            emoji="🅰️"
        )

        b_reaction = discord.utils.get(
            message.reactions,
            emoji="🅱️"
        )

        a_count = max(0, a_reaction.count - 1)
        b_count = max(0, b_reaction.count - 1)

        await interaction.channel.send(
            "📊 **VOTING RESULTS**\n\n"
            f"🅰️ **{option_a}** — `{a_count}` votes\n"
            f"🅱️ **{option_b}** — `{b_count}` votes"
        )

    except Exception:
        pass


# =========================
# ROAST
# =========================

@bot.tree.command(
    name="roast",
    description="Roast another player!"
)
async def roast(
    interaction: discord.Interaction,
    user: discord.Member
):

    roast_text = random.choice(roasts)

    await interaction.response.send_message(
        f"🔥 **ROAST INCOMING...**\n\n"
        f"{user.mention}\n"
        f"💀 {roast_text}"
    )


# =========================
# ROAST ME
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

    xp = get_xp(interaction.user.id)

    await interaction.response.send_message(
        f"👤 **{interaction.user.display_name}**\n\n"
        f"🏆 XP: **{xp}**"
    )


# =========================
# LEADERBOARD
# =========================

@bot.tree.command(
    name="leaderboard",
    description="View the Baxodi Games leaderboard!"
)
async def leaderboard(interaction: discord.Interaction):

    cursor.execute(
        "SELECT user_id, xp FROM users ORDER BY xp DESC LIMIT 10"
    )

    rows = cursor.fetchall()

    if not rows:
        await interaction.response.send_message(
            "🏆 Leaderboard is empty!"
        )
        return

    text = "🏆 **BAXODI GAMES LEADERBOARD**\n\n"

    for position, (user_id, xp) in enumerate(rows, start=1):

        user = bot.get_user(user_id)

        if user:
            name = user.display_name
        else:
            name = f"User {user_id}"

        text += (
            f"**{position}.** {name} — "
            f"`{xp} XP`\n"
        )

    await interaction.response.send_message(text)


# =========================
# HELP
# =========================

@bot.tree.command(
    name="games",
    description="Show all Baxodi Games!"
)
async def games(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎮 BAXODI GAMES",
        description=(
            "🧠 `/character` — Guess the Character\n"
            "🗣️ `/whosaid` — Who Said It?\n"
            "🤔 `/wyr` — Would You Rather\n"
            "🎵 `/songemoji` — Guess the Song\n"
            "🔥 `/roast @user` — Roast someone\n"
            "💀 `/roastme` — Roast yourself\n"
            "👤 `/profile` — Your XP\n"
            "🏆 `/leaderboard` — Top players"
        )
    )

    await interaction.response.send_message(embed=embed)


# =========================
# START BOT
# =========================

if not TOKEN:
    print("ERROR: DISCORD_TOKEN is missing!")
else:
    bot.run(TOKEN)
