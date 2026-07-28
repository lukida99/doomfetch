.PHONY: install freedoom shareware uninstall check clean

# Default: search for an installed IWAD. WAD=/path/to/DOOM2.WAD overrides it.
install:
	@./install.sh $(if $(WAD),--wad "$(WAD)")

freedoom:
	@./install.sh --freedoom

shareware:
	@./install.sh --shareware

uninstall:
	@./install.sh --uninstall

# Syntax check, no WAD required
check:
	@python3 -m py_compile bin/doomfetch build/*.py && echo "python ok"
	@bash -n install.sh && echo "install.sh ok"

clean:
	@rm -rf build/__pycache__ bin/__pycache__
