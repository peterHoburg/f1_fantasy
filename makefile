
build:
	pyinstaller ./src/f1_fantasy/__main__.py -F --add-binary ./src/f1_fantasy/data:./f1_fantasy/data -n f1-fantasy
