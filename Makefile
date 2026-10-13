# geany-playdate — Geany plugin for Panic Playdate
#
#   make          build playdate.so
#   make install  install into ~/.local/lib/geany (user) or PREFIX
#   make clean    remove build artifacts

CC       ?= gcc
PKG       = geany gtk+-3.0 glib-2.0 gobject-2.0 gmodule-2.0
CFLAGS   ?= -O2 -Wall -Wextra -Wno-unused-parameter
CFLAGS   += $(shell pkg-config --cflags $(PKG)) -fPIC -std=c11
LDFLAGS  += $(shell pkg-config --libs $(PKG)) -shared

# Geany loads plugins from ~/.config/geany/plugins/ and $prefix/lib/geany
GEANY_LIBDIR ?= $(HOME)/.config/geany/plugins
# where to drop the bundled tags file (plugin also installs to configdir/tags)
GEANY_TAGSDIR ?= $(HOME)/.config/geany/tags

SRCS = src/playdate.c src/config.c src/build.c src/errors.c src/tags.c
OBJS = $(SRCS:.c=.o)

TARGET = playdate.so

.PHONY: all clean install uninstall tags

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $@ $(LDFLAGS)

src/%.o: src/%.c src/playdate.h
	$(CC) $(CFLAGS) -c $< -o $@

install: $(TARGET)
	install -d $(GEANY_LIBDIR)
	install -m 755 $(TARGET) $(GEANY_LIBDIR)/$(TARGET)
	@echo "Installed $(GEANY_LIBDIR)/$(TARGET)"
	@echo "Enable the plugin in Geany: Tools → Plugin Manager → Playdate"
	@echo "Optional API tags: Geany → Tools → Playdate → Install API Tags"

tags:
	install -d $(GEANY_TAGSDIR)
	install -m 644 tags/playdate.lua.tags $(GEANY_TAGSDIR)/playdate.lua.tags
	@echo "Installed $(GEANY_TAGSDIR)/playdate.lua.tags"

uninstall:
	rm -f $(GEANY_LIBDIR)/$(TARGET)
	rm -f $(GEANY_TAGSDIR)/playdate.lua.tags

clean:
	rm -f $(OBJS) $(TARGET)
