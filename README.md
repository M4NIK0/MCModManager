MC Mod Manager is a free and open-source project, it permits (and will permit for some features)
profiles gestion (options, mods, configs...) without any install, with it's portable capability.

Then, i didn't reached v1.0 for now, and it means that every update is important, to get the most stable and useful version, since only a few features are up for now.
To finish the warnings (most of it):
This program is ONLY supported for Python 3.8 and 3.9 ONLY, i didn't test it on others...
I use PyQt5, os, random, shutil, sys and time, for now so you should install these (if not alredy done) before running my software, even if i alredy made a small code to install these from the run.bat.

It should be easy to use:
- Create a pack (from an alreddy installed one in your .minecraft) by clicking File > Save
  You can name it as you want (as long as it follows naming rules for windows folders)
  In the version textbox, type the Minecraft (and loader for now) version, like Forge 1.19.1
  In the mods textbox, type all the mods you want (i will implement a detection later, it's manual for now) separated by ","
  The last textbox is for others options, if you have not only options, optionsshaders and optionsof, just type their name and separate by ","
- Load a pack from it's box (by cliking Load)
  Warning ! for now, i didn't implemented the backup feature, it will discard all your options and configs when you do it, so be careful !
- Import a pack from a .mcmp file (which is basically a .zip with a different name, to ensure it's a pack and not a random zip)
- Delete a pack from it's box (There is a small message box to confirm, it's not an action that you can undo, be careful)

The export feature will come in the next update !
It will make the final feature (for now) to get used and should pass MCMM in v1.0 if i don't find any bug.
Don't forget to read the changelog to see every features i can add from an update to another !

Thanks for reading, see you soon for the next update !

v0.9.6 - Maniko
