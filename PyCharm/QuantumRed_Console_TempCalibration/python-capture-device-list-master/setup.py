from distutils.core import setup, Extension

module_device = Extension('device',
                        sources = ['device.cpp'], 
                        #library_dirs=['G:\Program Files\Microsoft SDKs\Windows\v6.1\Lib']
                        library_dirs=[r'C:\Program Files (x86)\Windows Kits\10\Lib']
                      )

setup (name = 'WindowsDevices',
        version = '1.0',
        description = 'Get device list with DirectShow',
        ext_modules = [module_device])
