"""The sprites doomfetch pulls out of a WAD.

Sprite lumps are named NAMEFR: a four-character identifier, a frame letter,
and a rotation (1 = facing the viewer, 0 = rotation-less, typical for items).
The status bar faces (STF*) live outside S_START/S_END and are addressed by
their lump name directly.

"since" records which IWAD a sprite first appears in:
  shareware  also present in DOOM1.WAD (episode 1)
  doom       full DOOM.WAD only (episodes 2-4)
  doom2      DOOM2.WAD / TNT / Plutonia only
Freedoom reuses the same lump names, so this table works there unchanged.

Lumps missing from the given WAD are skipped silently at build time.
"""

# name: (lump, title, category, since)
SPRITES = {
    # --- Monsters --------------------------------------------------------
    "zombieman":       ("POSSA1", "Zombieman",            "monster", "shareware"),
    "shotgunguy":      ("SPOSA1", "Shotgun Guy",          "monster", "shareware"),
    "imp":             ("TROOA1", "Imp",                  "monster", "shareware"),
    "pinky":           ("SARGA1", "Demon (Pinky)",        "monster", "shareware"),
    "baron":           ("BOSSA1", "Baron of Hell",        "monster", "shareware"),
    "cacodemon":       ("HEADA1", "Cacodemon",            "monster", "doom"),
    "lostsoul":        ("SKULA1", "Lost Soul",            "monster", "doom"),
    "cyberdemon":      ("CYBRA1", "Cyberdemon",           "monster", "doom"),
    "spidermastermind": ("SPIDA1", "Spider Mastermind",   "monster", "doom"),
    "chaingunner":     ("CPOSA1", "Heavy Weapon Dude",    "monster", "doom2"),
    "hellknight":      ("BOS2A1", "Hell Knight",          "monster", "doom2"),
    "revenant":        ("SKELA1", "Revenant",             "monster", "doom2"),
    "mancubus":        ("FATTA1", "Mancubus",             "monster", "doom2"),
    "arachnotron":     ("BSPIA1", "Arachnotron",          "monster", "doom2"),
    "painelemental":   ("PAINA1", "Pain Elemental",       "monster", "doom2"),
    "archvile":        ("VILEA1", "Arch-Vile",            "monster", "doom2"),
    "wolfss":          ("SSWVA1", "Wolfenstein SS",       "monster", "doom2"),
    "commanderkeen":   ("KEENA0", "Commander Keen",       "monster", "doom2"),
    "marine":          ("PLAYA1", "Doom Marine",          "monster", "shareware"),

    # --- Status bar faces ------------------------------------------------
    "doomguy":         ("STFST01", "Doomguy",              "face", "shareware"),
    "doomguy-grin":    ("STFEVL0", "Doomguy (Evil Grin)",  "face", "shareware"),
    "doomguy-ouch":    ("STFOUCH0", "Doomguy (Ouch)",      "face", "shareware"),
    "doomguy-rampage": ("STFKILL0", "Doomguy (Rampage)",   "face", "shareware"),
    "doomguy-god":     ("STFGOD0", "Doomguy (God Mode)",   "face", "shareware"),
    "doomguy-dead":    ("STFDEAD0", "Doomguy (Dead)",      "face", "shareware"),

    # --- Weapons ---------------------------------------------------------
    "chainsaw":        ("CSAWA0", "Chainsaw",             "weapon", "shareware"),
    "shotgun":         ("SHOTA0", "Shotgun",              "weapon", "shareware"),
    "supershotgun":    ("SGN2A0", "Super Shotgun",        "weapon", "doom2"),
    "chaingun":        ("MGUNA0", "Chaingun",             "weapon", "shareware"),
    "rocketlauncher":  ("LAUNA0", "Rocket Launcher",      "weapon", "shareware"),
    "plasmagun":       ("PLASA0", "Plasma Rifle",         "weapon", "doom"),
    "bfg9000":         ("BFUGA0", "BFG9000",              "weapon", "doom"),

    # --- Ammo ------------------------------------------------------------
    "clip":            ("CLIPA0", "Clip",                 "ammo", "shareware"),
    "ammobox":         ("AMMOA0", "Box of Bullets",       "ammo", "shareware"),
    "shells":          ("SHELA0", "Shotgun Shells",       "ammo", "shareware"),
    "shellbox":        ("SBOXA0", "Box of Shells",        "ammo", "shareware"),
    "rocket":          ("ROCKA0", "Rocket",               "ammo", "shareware"),
    "rocketbox":       ("BROKA0", "Box of Rockets",       "ammo", "shareware"),
    "cell":            ("CELLA0", "Energy Cell",          "ammo", "doom"),
    "cellpack":        ("CELPA0", "Energy Cell Pack",     "ammo", "doom"),

    # --- Items -----------------------------------------------------------
    "medikit":         ("MEDIA0", "Medikit",              "item", "shareware"),
    "stimpack":        ("STIMA0", "Stimpack",             "item", "shareware"),
    "healthbonus":     ("BON1A0", "Health Bonus",         "item", "shareware"),
    "armorbonus":      ("BON2A0", "Armor Bonus",          "item", "shareware"),
    "armor-green":     ("ARM1A0", "Armor",                "item", "shareware"),
    "armor-blue":      ("ARM2A0", "Mega Armor",           "item", "shareware"),
    "soulsphere":      ("SOULA0", "Soulsphere",           "item", "shareware"),
    "megasphere":      ("MEGAA0", "Megasphere",           "item", "doom2"),
    "invulnerability": ("PINVA0", "Invulnerability",      "item", "doom"),
    "invisibility":    ("PINSA0", "Partial Invisibility", "item", "shareware"),
    "berserk":         ("PSTRA0", "Berserk",              "item", "doom"),
    "radsuit":         ("SUITA0", "Radiation Suit",       "item", "shareware"),
    "computermap":     ("PMAPA0", "Computer Area Map",    "item", "shareware"),
    "lightamp":        ("PVISA0", "Light Amplification",  "item", "shareware"),
    "backpack":        ("BPAKA0", "Backpack",             "item", "shareware"),

    # --- Keys ------------------------------------------------------------
    "bluekey":         ("BKEYA0", "Blue Keycard",         "key", "shareware"),
    "redkey":          ("RKEYA0", "Red Keycard",          "key", "shareware"),
    "yellowkey":       ("YKEYA0", "Yellow Keycard",       "key", "shareware"),
    "blueskull":       ("BSKUA0", "Blue Skull Key",       "key", "doom"),
    "redskull":        ("RSKUA0", "Red Skull Key",        "key", "doom"),
    "yellowskull":     ("YSKUA0", "Yellow Skull Key",     "key", "doom"),

    # --- Props -----------------------------------------------------------
    "barrel":          ("BAR1A0", "Exploding Barrel",     "prop", "shareware"),
    "candle":          ("CANDA0", "Candle",               "prop", "shareware"),
    "candelabra":      ("CBRAA0", "Candelabra",           "prop", "shareware"),
    "techpillar":      ("ELECA0", "Tech Pillar",          "prop", "shareware"),
    "column":          ("COLUA0", "Column",               "prop", "shareware"),
}

CATEGORIES = ["monster", "face", "weapon", "ammo", "item", "key", "prop"]

# A curated pool for fetch tools, so you don't end up staring at an ammo
# clip every time you open a terminal.
ICONIC = [
    "imp", "pinky", "cacodemon", "baron", "hellknight", "revenant",
    "mancubus", "archvile", "cyberdemon", "lostsoul", "zombieman",
    "shotgunguy", "marine", "doomguy", "doomguy-grin", "doomguy-god",
    "chainsaw", "shotgun", "supershotgun", "chaingun", "rocketlauncher",
    "plasmagun", "bfg9000", "soulsphere", "megasphere", "medikit",
    "armor-blue", "barrel",
]
