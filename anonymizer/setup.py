try:
    from subprocess import call
    import sys
    if sys.version_info[0] >= 3:
        call(['pip', 'install', 'pytest'])
        call(['pip', 'install', 'pytest-cov'])
    else:
        print("Please use Python 3.")
except Exception as e:
    print(e)