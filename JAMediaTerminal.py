#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaTerminal.py por:
#       Flavio Danesse      <fdanesse@gmail.com>
#                           CeibalJAM! - Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

import JAMediaObjects
from JAMediaObjects.JAMediaTerminal import JAMediaTerminal

from JAMediaObjects.JAMediaGlobales import get_separador
from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_pixels

JAMediaObjectsPath = JAMediaObjects.__path__[0]

import JAMediaManTree
from JAMediaManTree.JAMediaManTree import JAMediaManTree

from sugar3.activity import activity

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(
    JAMediaObjectsPath, "JAMediaTerminal.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)

class Ventana(activity.Activity):
    
    __gtype_name__ = 'WindowJAMediaTerminal'
    
    def __init__(self, handle):
        
        activity.Activity.__init__(self, handle)
        
        self.set_title("JAMediaTerminal")
        '''
        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "bash.svg"))
            
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.CENTER)
        '''
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        toolbar = Toolbar()
        paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        
        box.pack_start(toolbar, False, False, 0)
        box.pack_start(paned, True, True, 0)
        
        self.jamediaterminal = JAMediaTerminal()
        self.jamediamantree = JAMediaManTree()
        
        paned.pack1(self.jamediamantree, resize = True, shrink = False)
        paned.pack2(self.jamediaterminal, resize = False, shrink = False)
        
        self.set_canvas(box)
        
        self.show_all()
        
        self.maximize()
        
        self.jamediamantree.hide()
        
        toolbar.connect("salir", self.__salir)
        toolbar.connect("help", self.__help)
        
        import sys
        self.connect("destroy", sys.exit)
        
    def __salir(self, widget):
        """
        Sale de la aplicación.
        """
        
        import sys
        sys.exit(0)
    
    def __help(self, widget):
        """
        Muestra u oculta el manual.
        """
        
        if self.jamediamantree.get_visible():
            self.jamediamantree.hide()
            
        else:
            self.jamediamantree.show()
            self.jamediaterminal.set_size_request(-1, 300)
    
class Toolbar(Gtk.Toolbar):
    """
    Toolbar principal.
    """
    
    __gtype_name__ = 'ToolbarJAMediaTerminal'
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'help':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(
            JAMediaObjectsPath,
            "Iconos",
            "JAMediaTerminal.svg")
            
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(1.0))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        ### Ayuda.
        archivo = os.path.join(
            JAMediaObjectsPath,
            "Iconos",
            "activity-help.svg")
            
        boton = get_boton(archivo,
            flip = False,
            pixels = get_pixels(1.0))
            
        boton.set_tooltip_text("Ayuda")
        boton.connect("clicked", self.__emit_help)
        self.insert(boton, -1)
        
        ### Salir.
        archivo = os.path.join(
            JAMediaObjectsPath,
            "Iconos",
            "button-cancel.svg")
            
        boton = get_boton(archivo,
            flip = False,
            pixels = get_pixels(1.0))
            
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__emit_salir)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        self.show_all()
        
    def __emit_salir(self, widget):
        """
        Cuando se hace click en el boton salir.
        """
        
        self.emit('salir')

    def __emit_help(self, widget):
        """
        Cuando se hace click en el boton salir.
        """
        
        self.emit('help')
