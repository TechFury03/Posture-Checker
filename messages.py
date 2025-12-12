import random

bad_posture_messages = [
    "Your back called—it's filing a formal complaint.",
    "Stop slouching, you human question mark.",
    "Do you practice being a melted popsicle or is this natural?",
    "Your spine called HR. They want to talk.",
    "Congrats! You just invented a new posture called 'sad noodle.'",
    "Your back looks like it lost a fight with gravity.",
    "If slouching were an Olympic sport, you'd win gold… and shame.",
    "Stop being a potato. Stand up, you tuber.",
    "You look like a slumped over question mark. Fix it.",
    "Straighten up or be mistaken for a deflated balloon.",
    "Your back is developing serious resentment toward you.",
    "Are you a human pancake? Because you're flat-out wrong.",
    "You're slouching so hard, gravity called for backup.",
    "Your future chiropractor is already charging you.",
    "Your spine is filing harassment charges.",
    "Your posture is tragic. Literally. Fix it.",
    "Congratulations, you're officially a slouch potato.",
    "Are you trying to look like a question mark or a melted candle?",
    "Your back hates you more than Monday mornings.",
    "Do you have a license to slouch this badly?",
    "You're giving serious 'why even try' energy.",
    "Your posture is like a failed science experiment.",
    "Straighten up, or I'll tell everyone you're a noodle impersonator.",
    "Your spine is doing interpretive dance without permission.",
    "You're a human shrug emoji. Stop it.",
    "Even your chair is judging you.",
    "You look like you've been dragged by a gremlin.",
    "Gravity is winning, and you're losing badly.",
    "Do you sit like that to confuse people? Because it's working.",
    "Your back is plotting revenge. Take it seriously."
]

good_posture_messages = [
    "Look at you! A fully upright human!",
    "Congratulations! Your spine thanks you.",
    "Straight as an arrow. Nailed it!",
    "Whoa, someone's not a noodle anymore!",
    "You look like a million bucks standing like that.",
    "Good posture detected: all systems nominal.",
    "Your chair is jealous of your uprightness.",
    "Well done! Gravity is not winning today.",
    "Standing tall like a human skyscraper!",
    "Your back called—finally some respect.",
    "Posture level: legendary.",
    "Look at you, sitting/standing like a responsible adult!",
    "Nice! You're no longer a question mark.",
    "Your spine would give you a high-five if it could.",
    "Alert: upright human in the wild spotted!",
    "Straight, proud, and fabulous. Keep it up!",
    "You've achieved peak noodle-resistance today!",
    "Bravo! You're officially not a melted popsicle.",
    "Your future chiropractor approves.",
    "Level up! Human posture unlocked."
]

def get_random_bad_posture_message():
    return bad_posture_messages[random.randint(0, len(bad_posture_messages)-1)]

def get_random_good_posture_message():
    return good_posture_messages[random.randint(0, len(good_posture_messages)-1)]