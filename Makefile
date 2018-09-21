main.exe: addon.py index.py main.py
	python index.py
	pyinstaller main.py -F
	mv dist/main.exe main.exe

.PHONY: clean cleanall

clean:
	rm -rf build dist
	rm main.spec

cleanall: clean
	rm main.exe
