pyinstaller -F -w -i="icon.ico" --add-data="icon.ico;." main.py
copy ".\dist\main.exe" ".\dist\MoviDect.exe"