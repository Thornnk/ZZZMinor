import cx_Freeze

exe = [cx_Freeze.Executable('rACE.py', base = 'Win32GUI')]

cx_Freeze.setup(
    name='rACE',
    version = '1.0',
    options={'build_exe': {'packages': ['pygame'],
                           'include_files': ['files', 'wheel.ico']}},
    executables = exe

    )