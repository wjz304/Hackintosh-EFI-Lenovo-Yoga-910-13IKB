

import os, sys, json, shutil, datetime, zipfile
import urllib3
import wget

PM = urllib3.PoolManager()


date_curr = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
date_last = ''

date_last_file = 'VERTIME'
try:
    with open(date_last_file,'r') as f:
        date_last = f.readline(1)
except:
    pass



class UpdateKexts():
    def __init__(self, alpha = True) -> None:
        self.alpha = True
        self.kexts = [
            ['Lilu', 'EFI/OC/Kexts/Lilu.kext', 'Lilu.kext'],
            ['WhateverGreen', 'EFI/OC/Kexts/WhateverGreen.kext', 'WhateverGreen.kext'],
            # ['ECEnabler', 'EFI/OC/Kexts/ECEnabler.kext', 'ECEnabler.kext'],
            ['VirtualSMC', 'EFI/OC/Kexts/VirtualSMC.kext', 'Kexts/VirtualSMC.kext'],
            ['VirtualSMC', 'EFI/OC/Kexts/SMCSuperIO.kext', 'Kexts/SMCSuperIO.kext'],
            ['VirtualSMC', 'EFI/OC/Kexts/SMCProcessor.kext', 'Kexts/SMCProcessor.kext'],
            ['VirtualSMC', 'EFI/OC/Kexts/SMCBatteryManager.kext', 'Kexts/SMCBatteryManager.kext'],
            ['AppleALC', 'EFI/OC/Kexts/AppleALC.kext', 'AppleALC.kext'],
            ['CPUFriend', 'EFI/OC/Kexts/CPUFriend.kext', 'CPUFriend.kext'],
            # ['CPUFriendDataProvider', 'EFI/OC/Kexts/CPUFriendDataProvider.kext', 'CPUFriendDataProvider.kext'],
            ['NVMeFix', 'EFI/OC/Kexts/NVMeFix.kext', 'NVMeFix.kext'],
            ['HibernationFixup', 'EFI/OC/Kexts/HibernationFixup.kext', 'HibernationFixup.kext'],
            # ['ThunderboltReset', 'EFI/OC/Kexts/ThunderboltReset.kext', 'ThunderboltReset.kext'],
            # ['VoodooI2C', 'EFI/OC/Kexts/VoodooI2C.kext', 'VoodooI2C.kext'],
            # ['VoodooI2CHID', 'EFI/OC/Kexts/VoodooI2CHID.kext', 'VoodooI2CHID.kext'],
            # ['VoodooTSCSync', 'EFI/OC/Kexts/VoodooTSCSync.kext', 'VoodooTSCSync.kext'],
            ['VoodooInput', 'EFI/OC/Kexts/VoodooInput.kext', 'VoodooInput.kext'],
            ['VoodooPS2Controller', 'EFI/OC/Kexts/VoodooPS2Controller.kext', 'VoodooPS2Controller.kext'],
            ['BrightnessKeys', 'EFI/OC/Kexts/BrightnessKeys.kext', 'BrightnessKeys.kext'],
            ['NoTouchID', 'EFI/OC/Kexts/NoTouchID.kext', 'NoTouchID.kext'],
            ['AirportBrcmFixup', 'EFI/OC/Kexts/AirportBrcmFixup.kext', 'AirportBrcmFixup.kext'],
            ['BrcmPatchRAM', 'EFI/OC/Kexts/BlueToolFixup.kext', 'BlueToolFixup.kext'],
            ['BrcmPatchRAM', 'EFI/OC/Kexts/BrcmBluetoothInjector.kext', 'BrcmBluetoothInjector.kext'],
            ['BrcmPatchRAM', 'EFI/OC/Kexts/BrcmFirmwareData.kext', 'BrcmFirmwareData.kext'],
            ['BrcmPatchRAM', 'EFI/OC/Kexts/BrcmPatchRAM3.kext', 'BrcmPatchRAM3.kext'],
        ]
        self.dortaniaKextsJson = None

    def __initDortaniaJson(self):
        dortaniaUrl = 'https://raw.githubusercontent.com/dortania/build-repo/builds/config.json'
        #res = PM.request('GET', dortaniaUrl)
        #self.dortaniaKextsJson = json.loads(res.data.decode('utf-8'))
        wget.download(dortaniaUrl, out='dortaniaConfig.json')
        with open('dortaniaConfig.json', mode="rb") as f:
            self.dortaniaKextsJson = json.loads(f.read())
        os.remove('dortaniaConfig.json')


    def upgradeDortaniaKexts(self, kextName, dstPath, srcPath):
        print('upgrade {}'.format(kextName))
        if self.dortaniaKextsJson is None:
            self.__initDortaniaJson()

        if self.dortaniaKextsJson[kextName]['versions'][len(self.dortaniaKextsJson[kextName]['versions'])-1]['date_built'] > date_last:
            url = self.dortaniaKextsJson[kextName]['versions'][len(self.dortaniaKextsJson[kextName]['versions'])-1]['links']['release']
            data = PM.request('GET', url)

            with open('./tmp.zip','wb') as f:   # with open( './'+url.split('/')[-1], 'wb') as f:
                f.write(data.data)

            with zipfile.ZipFile('./tmp.zip') as zf:
                zf.extractall('./tmp')
            os.remove('./tmp.zip')

            shutil.rmtree(dstPath)
            shutil.copytree('./tmp/' + srcPath, dstPath)
            shutil.rmtree('./tmp')
    
    def upgradeI2C(self):
        print('upgrade {}'.format('VoodooI2C and VoodooI2CHID'))
        res = PM.request('GET', 'https://api.github.com/reposVoodooI2C/VoodooI2C/releases')
        self.i2c = json.loads(res.data.decode('utf-8'))
        for i2cVer in self.i2c:
            if self.alpha is False and 'alpha' in i2cVer['name'].lower():
                continue
            if i2cVer['published_at'] > date_last:
                for item in i2cVer['assets']:
                    if not 'debug' in item['name'].lower() and '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        data = PM.request('GET', url)
                        with open('./tmp.zip','wb') as f:   # with open( './'+url.split('/')[-1], 'wb') as f:
                            f.write(data.data)

                        with zipfile.ZipFile('./tmp.zip') as zf:
                            zf.extractall('./tmp')
                        os.remove('./tmp.zip')

                        shutil.rmtree('EFI/OC/Kexts/VoodooI2C.kext')
                        shutil.copytree('./tmp/VoodooI2C.kext', 'EFI/OC/Kexts/VoodooI2C.kext')
                        shutil.rmtree('EFI/OC/Kexts/VoodooI2CHID.kext')
                        shutil.copytree('./tmp/VoodooI2CHID.kext', 'EFI/OC/Kexts/VoodooI2CHID.kext')
                        shutil.rmtree('./tmp')
                        break
            break
        
    def upgradeEC(self):
        print('upgrade {}'.format('ECEnabler'))
        res = PM.request('GET', 'https://api.github.com/1Revenger1/ECEnabler/releases')
        self.i2c = json.loads(res.data.decode('utf-8'))
        for i2cVer in self.i2c:
            if self.alpha is False and 'alpha' in i2cVer['name'].lower():
                continue
            if i2cVer['published_at'] > date_last:
                for item in i2cVer['assets']:
                    if not 'debug' in item['name'].lower() and '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        data = PM.request('GET', url)
                        with open('./tmp.zip','wb') as f:   # with open( './'+url.split('/')[-1], 'wb') as f:
                            f.write(data.data)

                        with zipfile.ZipFile('./tmp.zip') as zf:
                            zf.extractall('./tmp')
                        os.remove('./tmp.zip')

                        shutil.rmtree('EFI/OC/Kexts/ECEnabler.kext')
                        shutil.copytree('./tmp/ECEnabler.kext', 'EFI/OC/Kexts/ECEnabler.kext')
                        shutil.rmtree('./tmp')
                        break
            break

    def upgradeIntel(self):
        print('upgrade {}'.format('AirportItlwm'))
        res = PM.request('GET', 'https://api.github.com/repos/OpenIntelWireless/itlwm/releases')
        self.itlwm = json.loads(res.data.decode('utf-8'))
        for itlwmVer in self.itlwm:
            if self.alpha is False and 'alpha' in itlwmVer['name'].lower():
                continue
            if itlwmVer['published_at'] > date_last:
                for item in itlwmVer['assets']:
                    if 'ventura' in item['name'].lower():
                        url = item['browser_download_url']
                        data = PM.request('GET', url)
                        with open('./tmp.zip','wb') as f:   # with open( './'+url.split('/')[-1], 'wb') as f:
                            f.write(data.data)

                        with zipfile.ZipFile('./tmp.zip') as zf:
                            zf.extractall('./tmp')
                        os.remove('./tmp.zip')

                        shutil.rmtree('EFI/OC/Kexts/AirportItlwm.kext')
                        shutil.copytree('./tmp/Ventura/AirportItlwm.kext', 'EFI/OC/Kexts/AirportItlwm.kext')
                        shutil.rmtree('./tmp')
                        break
            break

        print('upgrade {}'.format('IntelBluetoothFirmware and IntelBluetoothInjector'))
        res = PM.request('GET', 'https://api.github.com/repos/OpenIntelWireless/IntelBluetoothFirmware/releases')
        self.ibt = json.loads(res.data.decode('utf-8'))
        for ibtVer in self.ibt:
            if self.alpha is False and 'alpha' in ibtVer['name'].lower():
                continue
            if ibtVer['published_at'] > date_last:
                for item in ibtVer['assets']:
                    if '.zip' in item['name'].lower():
                        url = item['browser_download_url']
                        data = PM.request('GET', url)
                        with open('./tmp.zip','wb') as f:   # with open( './'+url.split('/')[-1], 'wb') as f:
                            f.write(data.data)

                        with zipfile.ZipFile('./tmp.zip') as zf:
                            zf.extractall('./tmp')
                        os.remove('./tmp.zip')

                        shutil.rmtree('EFI/OC/Kexts/IntelBluetoothFirmware.kext')
                        shutil.copytree('./tmp/IntelBluetoothFirmware.kext', 'EFI/OC/Kexts/IntelBluetoothFirmware.kext')
                        shutil.rmtree('EFI/OC/Kexts/IntelBluetoothInjector.kext')
                        shutil.copytree('./tmp/IntelBluetoothInjector.kext', 'EFI/OC/Kexts/IntelBluetoothInjector.kext')
                        shutil.rmtree('./tmp')
                        break
            break

    def upgradeOC(self):
        print('upgrade {}'.format('OpenCore_Mod'))
        url = ''
        if self.alpha is False:
            url = 'https://api.github.com/repos/OlarilaHackintosh/OpenCore_NO_ACPI/releases'
        else:
            url = 'https://api.github.com/repos/wjz304/OpenCore_NO_ACPI_Build/releases'
        res = PM.request('GET', url)
        self.ocmod = json.loads(res.data.decode('utf-8'))
        for ocVer in self.ocmod:
            if ocVer['published_at'] > date_last:

                for item in ocVer['assets']:
                    if 'release' in item['name'].lower():
                        url = item['browser_download_url']
                        data = PM.request('GET', url)
                        with open('./tmp.zip','wb') as f:   # with open( './'+url.split('/')[-1], 'wb') as f:
                            f.write(data.data)

                        with zipfile.ZipFile('./tmp.zip') as zf:
                            zf.extractall('./tmp')
                        os.remove('./tmp.zip')

                        os.remove('EFI/BOOT/BOOTx64.efi')
                        shutil.copy('./tmp/X64/EFI/BOOT/BOOTx64.efi', 'EFI/BOOT/BOOTx64.efi')

                        os.listdir('EFI/OC/Drivers')
                        for efi in os.listdir('EFI/OC/Drivers'):
                            os.remove('EFI/OC/{}'.format(efi))
                            shutil.copy('./tmp/X64/EFI/OC/Drivers/{}'.format(efi), 'EFI/OC/Drivers/{}'.format(efi))

                        with open('EFI/OC/Resources/Image/Acidanthera/GoldenGate/Background.icns', mode="rb") as f:
                            background = f.read()
                        shutil.rmtree('EFI/OC/Resources')
                        shutil.copytree('./tmp/X64/EFI/OC/Resources', 'EFI/OC/Resources', ignore= shutil.ignore_patterns('.*'))
                        os.remove('EFI/OC/Resources/Image/Acidanthera/GoldenGate/Background.icns')
                        with open('EFI/OC/Resources/Image/Acidanthera/GoldenGate/Background.icns', mode="wb") as f:
                            f.write(background)
                        break
            break


        pass

    def update(self):

        if self.alpha is True:
            for kext in self.kexts:
                try:
                    self.upgradeDortaniaKexts(kext[0], kext[1], kext[2])
                except:
                    print('Dortania Kexts update error!')
                    return 1
        else:
            # no idea
            pass

        try:
            self.upgradeI2C()
            self.upgradeEC()
        except:
            print('I2C Kexts update error!')
            return 2
            
        try:
            self.upgradeOC()
        except:
            print('OC update error!')
            return 3

if __name__ == '__main__':
    u1 = UpdateKexts(alpha = True)
    ret = u1.update()

    if ret is True:
        with open(date_last_file, mode="wb") as f:
            f.write(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
    else:
        print('error!')
    
    sys.exit(ret)