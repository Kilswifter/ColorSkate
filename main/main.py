from ota_updater import OTAUpdater

def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/Kilswifter/ColorSkate')
    o.using_network('Avenue Belle Vue', 'Westfield19')
    o.download_updates_if_available()

def start():
    # your custom code goes here. Something like this: ...
    # from main.x import YourProject
    # project = YourProject()
    # ...
    print('test123456789')


    o = OTAUpdater('https://github.com/Kilswifter/ColorSkate')
    o.check_for_update_to_install_during_next_reboot()



def boot():
    print('boot sequence started')
    download_and_install_update_if_available()
    start()


boot()
