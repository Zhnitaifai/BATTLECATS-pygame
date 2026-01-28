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
* Lion Cat: \**Tokyo Drift stats playing*
* Bird Cat: I believe I can fly
* Fish Cat: Likes to eat things. Especially red things
* Lizard Cat: Longer Range (eww, spit)
* Titan Cat: Extreme Attack power and Defense
* ???: An mysterious ally, ready to assist your army at a price

Deploy cats with Money
* Money Generates passively
* Upgrade to increase money generation
* Defeating enemies grants extra money
* Every unit has a cooldown, so make sure to manage your cats effectively

In the game of Battle Cats, enemy deployment is dictated by:
- Time interval between deployment
- Time before the interval can trigger
- At what point in the stage can the interval trigger
- Whether if the units will deploy infinitely or to a finite amount

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

## Challenges faced
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
	