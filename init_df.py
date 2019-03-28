import pandas as pd

df = pd.DataFrame()
characters = ["Mario", "Donkey Kong", "Link", "Samus", "Dark Samus", "Yoshi", "Kirby", "Fox", "Pikachu", "Luigi", "Ness", "Captain Falcon", "Jigglypuff",
"Peach", "Daisy", "Bowser", "Ice Climbers", "Sheik", "Zelda", "Dr. Mario", "Pichu", "Falco", "Marth", "Lucina", "Young Link", "Ganondorf", 
"Mewtwo", "Roy", "Chrom", "Mr. Game & Watch", "Meta Knight", "Pit", "Dark Pit", "Zero Suit Samus", "Wario", "Snake", "Ike", "Pokémon Trainer", "Diddy Kong", 
"Lucas", "Sonic", "King DeDeDe", "Olimar", "Lucario", "R.O.B.", "Toon Link", "Wolf", "Villager", "Mega Man", "Wii-Fit Trainer", "Rosalina & Luma", "Little Mac", 
"Greninja", "Palutena", "Pac-Man", "Robin", "Shulk", "Bowser JR.", "Duck Hunt Duo", "Ryu", "Ken", "Cloud", "Corrin", "Bayonetta", "Inkling", 
"Ridley", "Simon", "Richter", "King K. Rool", "Isabelle", "Incineroar", "Piranha Plant", "Mii Brawler", "Mii Swordfighter", "Mii Gunner"]
df["opponent"] = characters
df["win"] = 0
df["lose"] = 0
df.to_csv("./csv/pichu_lv9.csv", index=False)