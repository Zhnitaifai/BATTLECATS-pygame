# BATTLECATS in pygame
## by Brendan Yap and Nguyen Doan

### Conquer the World with your Cat Army! 
### Defeat Mighty Foes! 
### Become Trendy on the Internet! 
### wait what?

## Goal: Destroy the enemy base using your Cats:
* Cat: A basic cat
* Tank Cat: Can barely move a pebble
* Axe Cat: Anti-Red Maniac
* Gross Cat: Long Range (and Legs)
* Lion Cat: \**Tokyo Drift stats playing**
* Bird Cat: I believe I can fly
* Fish Cat: Likes to eat things. Especially red things
* Lizard Cat: Longer Range (eww, spit)
* Titan Cat: Extreme Attack power and Defense
* ???: An mysterious ally, ready to assist your army at a price

Deploy cats with Money
* Money Generates passively
* Upgrade to increase money generation
* Defeating enemies grants extra money

In the game of Battle Cats, enemy deployment is dictated by:
- Time interval between deployment
- Time before the interval can trigger
- At what point in the stage can the interval trigger
- Whether if the units will deploy infinitely or to a finite amount

* Costs:
	* Cat: $75
	* Tank Cat: $150
	* Axe Cat: $300
	* Gross Cat: $400
	* Lion Cat: $750
	* Bird Cat: $975
	* Fish Cat: $1200
	* Lizard Cat: $1500
	* Titan Cat: $1950
	* ???: $4500

## Controls:
* Enter: Select/Confirm
* Arrow Keys (L and R): Select different Stage
* Deployment Keys:
	* q: Cat
	* w: Tank Cat
	* e: Axe Cat
	* r: Gross Cat
	* t: Lion Cat
	* a: Bird Cat
	* s: Fish Cat
	* d: Lizard Cat
	* f: Titan Cat
	* g: ???
* Tab: Upgrade Money
* Esc: Pause/Unpause Game
* F4: Quit Game
## Challenges:
* Units:
	* Too many elements: Due to the nature of the game, we can't specifically make all of the units and manage them all. We choose to use a class because then we can uniformly create and manage all instances of units systematically.
	* Detecting other units: Since each unit is their own object and can't really communicate with each other, we had to figure out a way to allow them to exchange their positions on the battlefield to allow enemy detection. This was solved by simply compiling each unit's positions into a list and using that list as a basis to detect enemies.
	* Dealing damage: Since there are two types of damage-type (single and area) and damage usually happens a few frames after the enemies were detected, we created a different function to find a list of "targets" (units that are being damaged) and making the attacking process a multi-step one, with it dealing damage when the animation reaches a certain frame.
* Base Game:
	* Different "stages" in the game: Since our game needs three seperate mode: the menu/level select, the actual battle, and the end screen, we used a match case to help sort out and manage the code for each section of the game.
	* Cat Cooldowns: To manage the cooldowns of each seperate unit, we made two seperate list: one with each cat's deployment-related stats (cost, cooldown), and one with just a cooldown counter for each unit. As you deploy a cat successfully, the counter will be increased by the cat's specific amount of cooldown and the counter will be decreased every frame.
	* Bases: We couldn't really figure out how to make bases work, since they're not really units and they are involved with more things than normal units. After a while, we figured that making them units is much easier than to create a class for them. We modify their stats to make them immobile and unable to attack and making getter functions to get their health, which is very relevant for enemy units deployment. 
	* Ending the battle: Since battles end when either bases die, we needed a way to detect when a base die. We initially thought of having bases send a death message of sorts to tell the game to end, but we figured that searching the unit dictionaries for the bases is much simpler and error-free, since units are deleted from the dictionary when they die.
	* Boss not deploying: After the enemy deployment was fixed, the only hurdle was that the boss of each stage wasn't being properly deployed. This turned out to be a Occam's Razor situation though, since we can just directly deploy the boss since only one of them spawn in a stage
- Enemy Deployment:
	- Boss did not spawn into the stage. Instead of using the same procedure of going through `currentEnemies`, the boss is simply spawned directly to the stage
	- Progress to attack the enemy base was very difficult as a result of constant deployment of enemies. Added limit to number of enemies spawned, with a 1 second buffer to prevent constant enemies blocking the base, making the game beatable.
## Peer Review
1. **Reviewed by Erisha:**
	- *Suggestion:* Reduce the lag when playing by adding a limit to the number of units deployed
	- *Implementation:* This was implemented through the limiting the amount of units deployed to 50 in the `deploy()` function
	```
	if side == 'cat' and len(catDict) < 51: # catDict is contains all currently deployed cats
	```
2. **Reviewed by Aaryan**
	- *Suggestion:* Add progression or level up system
	- *Implementation:* Added auto unlocking or new units for each stage. This helps scale with the difficulty of the stages
	<br>
	1. Korea unlocks Cat, Tank Cat, and Axe Cat
	2. Dubai unlocks Gross Cat
	3. South Africa unlocks Lion Cat
	4. Turkey unlocks Bird Cat
	5. Monaco unlocks Fish Cat
	6. Denmark unlocks Lizard Cat
	7. Canada unlocks Titan Cat
	8. Moon unlocks Bahamut Cat
	