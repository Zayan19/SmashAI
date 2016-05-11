An AI bot developed for Super Smash Bros Melee. The AI plays as Fox. Credits goes to Ahmed Khan and Zayan Imtiaz.

As of now it's still in the very early stages. Basic Smash commands have been
programmed in. It also can recover when off stage. But there is still a lot of work to be done.

If you wish to test it you will need:

-A new version of Dolphin
-Super Smash Bros Melee
-Linux or OSX

To setup and run:

1. Start it once with make and the memory watcher will be made for you
2. You will need to put the GCPad.ini file inside your Dolphin Profiles folder. It should be at ~/.config/dolphin-emu/Profiles/GCPad (create the folder if it doesn't exist)
3. Navigate to ~/.local/share/dolphin-emu/Pipes (create it if it doesn't exist)
4. Create new pipe called SmashBot with the command mkfifo SmashBot
5. Navigate to Dolphin controls and select Player 2 with Standard Controller. Load the created pipe SmashBot and load the GCPadNew.ini file. You should see the analogs highlight in red 
6. Finally start up Super Smash Bros Melee and choose Fox inside a game with the settings from step 5 loaded. When you type make, the AI will start executing!
