#makefile for annchienta

C_FLAGS = $(shell python-config --includes) $(shell sdl-config --cflags) -I/usr/include/freetype2
LD_FLAGS = $(shell python-config --libs) $(shell sdl-config --libs) -lGL -lpng -lfreetype

SWIG_CPP_FILE = src/annchienta_wrap.cpp
SWIG_INTERFACE_FILE = src/annchienta_interface.i

EXECUTABLE = bin/annchienta


all: $(EXECUTABLE)


$(EXECUTABLE): $(SWIG_CPP_FILE)
	@echo "Compiling the executable..."
	@$(CXX) $(C_FLAGS) $(LD_FLAGS) -o $(EXECUTABLE) src/*.cpp


$(SWIG_CPP_FILE):
	@echo "Generating Python wrappers..."
	@swig -python -c++ -o $(SWIG_CPP_FILE) -outdir bin $(SWIG_INTERFACE_FILE)


clean:
	@echo "Removing binaries..."
	@$(RM) $(EXECUTABLE)

cleanall:
	@echo "Removing binaries and python wrappers..."
	@$(RM) bin/* $(SWIG_CPP_FILE)
