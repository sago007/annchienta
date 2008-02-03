#makefile for annchienta

C_FLAGS = $(shell python-config --includes) $(shell sdl-config --cflags) -I/usr/include/freetype2
LD_FLAGS = -Lbin -lirrXML $(shell python-config --libs) $(shell sdl-config --libs) -lGL -lpng -lfreetype -lSDL_mixer

SWIG_CPP_FILE = src/annchienta_wrap.cpp
SWIG_INTERFACE_FILE = src/annchienta_interface.i

XML_LIBRARY = bin/libirrXML.a

EXECUTABLE = bin/annchienta


all: $(EXECUTABLE)


$(EXECUTABLE): $(SWIG_CPP_FILE) $(XML_LIBRARY)
	@echo "Compiling the executable..."
	@$(CXX) $(C_FLAGS) -o $(EXECUTABLE) src/*.cpp $(LD_FLAGS)


$(SWIG_CPP_FILE):
	@echo "Generating Python wrappers..."
	@swig -python -c++ -o $(SWIG_CPP_FILE) -outdir bin $(SWIG_INTERFACE_FILE)

$(XML_LIBRARY):
	@echo "Compiling xml library..."
	@$(CXX) -c src/xml/*.cpp
	@$(AR) rcs $(XML_LIBRARY) *.o
	@$(RM) *.o

clean:
	@echo "Removing binaries..."
	@$(RM) $(EXECUTABLE)

cleanall:
	@echo "Removing binaries and python wrappers..."
	@$(RM) bin/* $(SWIG_CPP_FILE)
