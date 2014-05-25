from cx_Freeze import setup, Executable
import requests.certs

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], include_msvcr=True,
                    include_files=[(requests.certs.where(),'cacert.pem')])
import sys
# base = 'Win32GUI' if sys.platform=='win32' else None
base=None

executables = [
    Executable('scripts\\hecs.py', base=base, targetName = 'hecs.exe')
]

setup(name='hecs',
      version = '1.0',
      description = 'Hecs',
      options = dict(build_exe = buildOptions),
      executables = executables)
