CC    = g++
FLAGS        = # -std=gnu99 -Iinclude
CFLAGS       = -fPIC #-g #-pedantic -Wall -Wextra -ggdb3
LDFLAGS      = -shared

DEBUGFLAGS   = -O0 -D _DEBUG
RELEASEFLAGS = -O2 -D NDEBUG -fwhole-program

TARGET  = eval.so
SOURCES = $(wildcard *.cpp)
HEADERS = $(wildcard *.h)
OBJECTS = $(SOURCES:.cpp=.o)


all: $(TARGET)

$(TARGET): clean
	$(CC) $(LDFLAGS) -Wl,-soname,eval -O2 -o $(TARGET) $(CFLAGS) $(SOURCES)

clean:
	rm -f $(OBJECTS) $(TARGET)
