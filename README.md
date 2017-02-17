# OSRBox
Small python script to interact with the OSRBox Virtual COM Port

OSRBox homepage : http://www.ipsp.ucl.ac.be/recherche/projets/OSRBox/

## Usage
1. Download the FTDI Virtual COM Port Drivers located [here](http://www.ftdichip.com/Drivers/VCP.htm).
2. Do the usual `git clone <x>` || `git init && git remote add origin <x>`.
3. Resolve dependencies with `pip install -r requirements.txt`.
4. Configure the key emulations within OSRBox.yml.
5. Start OSRBoxDriver.py !

If you don't know what is the used COM port, you can still list those with :
```cmd
python -m serial.tools.list_ports
```
By default the driver will stand in idle mode until a COM port is connected.

## Artefact
To create a windows executable just type :
```cmd
python setup.py py2exe
```
The OSRBoxDriver and its dependencies should now stand in the `dist/` folder.
