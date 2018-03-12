# VibHub-WoW

A [VibHub](https://github.com/JasXSL/VibHub-Client) connector app for World of Warcraft! Supports Windows 10 and probably 7. Only supports 64bit WoW.

# Install

1. [Download a pre-built zip file from releases](https://github.com/JasXSL/VibHub-WoW/releases). Unzip it somewhere on your drive.
2. Run VibHubWow.exe

# Connect VibHub to WoW via Weakauras 2

1. Set DeviceID to your VibHub device's ID.
2. Hit Save.
3. Load up World of Warcraft (you'll probably want to run it windowed or windowed fullscreen).
4. [Install the weakauras 2 addon](https://www.curseforge.com/wow/addons/weakauras-2?page=2).
5. Open weakauras settings by typing /wa in chat and hitting enter.
6. Click New > Import
7. In the VibHub app window, click Get Weakaura, the code will be copied to your clipboard.
8. Hit ctrl+v in the paste area of your new weakaura, then click Import.
9. If the new weakaura showed up off screen, you can select your weakaura and click the Display tab, then find X offset and Y offset and change these to 0. Then simply drag the small red box to wherever you want it on your screen, such as one of the edges.
10. In your VibHub app window, click Pick Target and then OK. Then click the red box in WoW to start reading from it.
11. Congrats! Your VibHub device should now trigger whenever you are damaged.

# Configuration and sliders

| Input | Default | Description |
|---|---|---|
| Max Intensity | 255 | Sets the maximum power that can be sent to the vibrator(s) |
| Min Intensity | 30 | Sets the minimum power that can be sent to the vibrator(s), regardless of how little damage you took from a hit. A too low value might prevent the vibrator from receiving enough power to turn on at all. Try to set this to a value where your vibration just turns on from a weak hit. |
| Intens:HP Ratio | 5 | How many percent of vibrational power should be added per percent damage you take. You can divide 100 by this value and it will tell you how many percent damage you need to take to reach max vibration. A ratio of 5 means you'll have to lose 20% HP to reach full power. This value ramps fairly exponentially, and a too high value means your vibrator will be maxed out from just a few weak hits. |
| DeviceID | TestDevice | This is the device ID for your VibHub device, keep it secret! |
| Server | vibhub.io | VibHub relay server to use. For most intents and purposes you can just use the official vibhub.io one, but if network security is a must you can look into [hosting your own VibHub server](https://github.com/JasXSL/VibHub-Server). |
| Pick Target | 0,0 | Draws a black transparent box across your screen, allowing you to click your weakaura to start reading it. You'll have to use this the first install, and whenever you move your WoW window or weakaura. |
