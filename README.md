# Valheim-Mod-Manager

Simple CLI-based Valheim mod manager made in response to the `Network Error Bug` that many Linux users seem to experience -- making it __impossible__ to download certain mods on Linux machines. This script is designed to be used as a standalone mod manager, and is currently compatible with **all** mods available on [thunderstore.io](https://thunderstore.io/c/valheim/).

## Who Should Use This?

Any Linux user who is encountering problems with being able to download mods may find this useful, specifically the `Network Error Bug` that I have experienced on multiple Arch-based machines.

*Note:* If you not are using Linux, or are not experiencing this specific bug, I'd recommend you use [Thunderstore Mod Manager](https://www.overwolf.com/app/thunderstore-thunderstore_mod_manager) instead - as setup and maintenance of mods will be much smoother.

## Requirements

1. Python version > 3.0.0 must be installed
2. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) package manager
3. Resolve dependencies by executing the following in the project directory
   ```
   conda env create -f environment.yml
   ```

## Setup + Configuration
1. Navigate to [BepInEx](https://thunderstore.io/c/valheim/p/denikson/BepInExPack_Valheim/) and select _manual download_
2. Extract BepInEx from the zip folder
3. Inside the extracted folder denikson-BepInExPack_Valheim-X.X.XXXX there should be another folder named **BepInExPack_Valheim**, place the contents of this folder into /home/YOUR_NAME_HERE/.local/share/Steam/steamapps/common/Valheim (or wherever your Valheim games folder is installed to)
4. Make _start_game_bepinex.sh_ into an executable by running `chmod +x start_game_bepinex.sh`
5. Open `config.ini` in the project directory and change `mods_dir` to be your copied directory from above, so that your config.ini file looks like
   ```
   [PARAMETERS]
   mods_dir = /home/YOUR_NAME_HERE/.local/share/Steam/steamapps/common/Valheim/BepInEx/plugins
   mods_csv = mods.csv
   dependencies_csv = dependencies.csv
   ```

## Usage

### Adding Mods

Adding mods is as easy as copying the URL for the modpage on the Thunderstore website and pasting it into the `mods.csv` file in the project directory, for example to add [Jotunn](https://thunderstore.io/c/valheim/p/ValheimModding/Jotunn/), [CreatureLevelAndLootControl](https://thunderstore.io/c/valheim/p/Smoothbrain/CreatureLevelAndLootControl/), and [PlantEverything](https://thunderstore.io/c/valheim/p/Smoothbrain/CreatureLevelAndLootControl/) your mods.csv will look like
   ```
   https://thunderstore.io/c/valheim/p/ValheimModding/Jotunn/
   https://thunderstore.io/c/valheim/p/Smoothbrain/CreatureLevelAndLootControl/
   https://thunderstore.io/c/valheim/p/Advize/PlantEverything/
   ```
_Note: Mod Dependencies will be automatically identified and installed, you do not need to add all the dependencies in mods.csv_

### Removing Mods

To remove mods just delete the corresponding webpage URL in `mods.csv`, in the above example we can remove [CreatureLevelAndLootControl](https://thunderstore.io/c/valheim/p/Smoothbrain/CreatureLevelAndLootControl/) by simply removing it's URL
   ```
   https://thunderstore.io/c/valheim/p/ValheimModding/Jotunn/
   https://thunderstore.io/c/valheim/p/Advize/PlantEverything/
   ```

### Downloading Mods

Once you've modified your `mods.csv` file to your liking, you can run the script to actually install them. First ensure that you are in the conda environment
 ```
conda activate vmm
 ```
Then in the project directory run
```
python vmm.py
```
_Note: This may take a while depending on how many mods you've installed and your internet download speed!_


### Updating Mods

To update mods to their latest version, all you need to do is run the script again
```
python vmm.py
```
_Note: Remember to execute this command in the conda env_ `vmm`

## Launching the Game

After you've run the script to install the mods you're ready to play! In steam you should be able to set launch paramters to make the game initialize using BepInEx according to the [Arch Linux Wiki](https://wiki.archlinux.org/title/Valheim) and just push play and launch as normal. **BUT** this isn't personally working for me, nor is any other variation of launch parameter, so if this is not working then a workaround is to open the game file directory containing _start_game_bepinex.sh_ and execute the command manually with `./start_game_bepinex.sh`.

_Note: It may take a while to launch, typically a few minutes depending on your number of mods_
