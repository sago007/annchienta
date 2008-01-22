#makefile for annchienta

C_FLAGS = $(shell python-config --includes) $(shell sdl-config --cflags)
LD_FLAGS = $(shell python-config --libs) $(shell sdl-config --libs) -lGL -lpng

SWIG_CPP_FILE = src/annchienta_wrap.cpp
SWIG_INTERFACE_FILE = src/annchienta_interface.i

EXECUTABLE = bin/annchienta


all: $(EXECUTABLE)


$(EXECUTABLE): $(SWIG_CPP_FILE)
	@echo "Compiling the executable..."
	@$(CXX) $(C_FLAGS) $(LD_FLAGS) -o bin/annchienta src/*.cpp


$(SWIG_CPP_FILE):
	@echo "Generating Python wrappers..."
	@swig -python -c++ -o $(SWIG_CPP_FILE) -outdir bin $(SWIG_INTERFACE_FILE)


clean:
	@echo "Removing all..."
	@$(RM) $(SWIG_CPP_FILE) bin/* scripts/annchienta.py


recompile:
	@$(RM) bin/*
	@make all


rewrap:
	@$(RM) $(SWIG_CPP_FILE)
	@make all
