# Makefile for annchienta

# Global makefile variables.
SWIG = swig
MAKE = make
MKDIR = mkdir
CP = cp
ECHO = echo
INSTALL = install
OWNER = bin
GROUP = bin

# Some compiler and linker flags.
C_FLAGS = $(shell python-config --includes) $(shell sdl-config --cflags) -I/usr/include/freetype2
LD_FLAGS = -Lbin -lirrXML $(shell python-config --libs) $(shell sdl-config --libs) -lGL -lpng -lfreetype -lSDL_mixer

# Swig files.
SWIG_CPP_FILE = src/annchienta_wrap.cpp
SWIG_INTERFACE_FILE = src/annchienta_interface.i

# Some local build directories.
BIN_DIR = bin
MODULE_DIR = modules
GAME_DIR = games

# The install directories.
EXECUTABLE_INSTALL_DIR = /usr/games
DATA_INSTALL_DIR = /usr/share/annchienta

# Names for build targets.
XML_LIBRARY = libirrXML.a
EXECUTABLE = annchienta.bin
SCRIPT = annchienta

# Directory where the game will store save files and logs.
WRITE_DIR = $(HOME)/.annchienta

# Default: just build the main executable and a trigger script.
all: $(BIN_DIR)/$(EXECUTABLE) $(BIN_DIR)/$(SCRIPT)

$(BIN_DIR)/$(EXECUTABLE): $(SWIG_CPP_FILE) $(BIN_DIR)/$(XML_LIBRARY)
        # Compile all cpp files in src to the executable.
	$(CXX) $(C_FLAGS) -o $(BIN_DIR)/$(EXECUTABLE) src/*.cpp $(LD_FLAGS)

$(SWIG_CPP_FILE):
        # Call swig to scan the swig interface file.
	$(SWIG) -python -c++ -o $(SWIG_CPP_FILE) -outdir $(MODULE_DIR) $(SWIG_INTERFACE_FILE)

$(BIN_DIR)/$(XML_LIBRARY):
        # Compile all cpp files in src/xml, then ar them
        # together to a static library.
	$(CXX) -c src/xml/*.cpp
	$(AR) rcs $(BIN_DIR)/$(XML_LIBRARY) *.o
	$(RM) *.o

$(BIN_DIR)/$(SCRIPT):
        # Throw together a script that will trigger the game.
	$(ECHO) "mkdir -p" $(WRITE_DIR) > $(BIN_DIR)/$(SCRIPT)
	$(ECHO) $(EXECUTABLE) "\$$1" $(DATA_INSTALL_DIR)/$(MODULE_DIR) $(WRITE_DIR) >> $(BIN_DIR)/$(SCRIPT)

clean:
        # Remove all build files.
	$(RM) $(BIN_DIR)/$(EXECUTABLE) $(BIN_DIR)/$(XML_LIBRARY) $(BIN_DIR)/$(SCRIPT) $(MODULE_DIR)/annchienta.py $(SWIG_CPP_FILE)

update:
        # Quickly recompile the executable
	$(RM) $(BIN_DIR)/$(EXECUTABLE)
	$(MAKE) $(BIN_DIR)/$(EXECUTABLE)

install: all
        # Make sure the necessary directories are there.
	$(MKDIR) -p $(EXECUTABLE_INSTALL_DIR) $(DATA_INSTALL_DIR)
        # Install executable to executable install dir.
	$(INSTALL) -c -o $(OWNER) -g $(GROUP) -m 755 $(BIN_DIR)/$(EXECUTABLE) $(EXECUTABLE_INSTALL_DIR)
	$(INSTALL) -c -o $(OWNER) -g $(GROUP) -m 755 $(BIN_DIR)/$(SCRIPT) $(EXECUTABLE_INSTALL_DIR)
        # Copy games and modules to data install dir
	$(CP) -r $(MODULE_DIR) $(GAME_DIR) $(DATA_INSTALL_DIR)

uninstall:
        # Remove executable.
	$(RM) $(EXECUTABLE_INSTALL_DIR)/$(EXECUTABLE) $(EXECUTABLE_INSTALL_DIR)/$(SCRIPT)
        # Remove entire data install dir.
	$(RM) -r $(DATA_INSTALL_DIR)

