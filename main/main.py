from ota_update.main.ota_updater import OTAUpdater

 def download_and_install_update_if_available():
     o = OTAUpdater('https://github.com/Kilswifter/ColorSkate')
     o.download_and_install_update_if_available('Avenue Belle Vue', 'Westfield19')


 def start():
     # your custom code goes here. Something like this: ...
     # from main.x import YourProject
     # project = YourProject()
     # ...
     print('test123456789')
     import colorskate.py


 def boot():
     print('device booted')
     download_and_install_update_if_available()
     import startup.py
     start()


 boot()
