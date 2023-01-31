#!/usr/bin/env python3

import sys
import curses, curses.panel

from Modes_Calcultator import *

class Guit_Screen(object):
    def __init__(self, screen):
        self.MC = Modes_Calculator()#"D#", "Mixolydian")
        self.screen = screen
        curses.noecho()
        curses.mousemask(-1)#curses.NO_MOUSE_EVENTS)

        self._init_colors()
        #self._set_cursor_positions()
        self.Statusbar = "Press 'q' to exit | ©2021 CC-BY-NC by S4mdf0o1"

        curses.curs_set(0)
        self.Actual_Note = self.MC.Note
        self.Actual_Mode = self.MC.Mode
        self.Actual_Degree = self.MC.Intervals[0]
        #sys.exit(self.MC.Neck)
        self.display()

    def _init_colors( self ):
        curses.start_color()
        curses.use_default_colors()
        #if curses.can_change_color():
        #    curses.init_color(0, 0, 0, 0)
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        #curses.init_pair(1, curses.COLOR_GREEN,     -1 )
        #curses.init_pair(2, curses.COLOR_YELLOW,    -1 )
        #curses.init_pair(3, curses.COLOR_CYAN,      -1 )
        #curses.init_pair(4, curses.COLOR_MAGENTA,   -1 )
        #curses.init_pair(5, curses.COLOR_RED,       -1 )
        self.note_cur_pos = 0
        self.note_colors = []

    def add_note_color( self, cur_pos, size, code ):
        self.note_colors.append((cur_pos, size, code))

    
    def set_cursor_position( self, offs_y = 0, offs_x = 0 ):
        nc = self.note_colors
        y, x = nc[ self.note_cur_pos ][0]
        self.screen.move( y, x )
        self.screen.chgat(y, x, nc[ self.note_cur_pos ][1], 
                            nc[ self.note_cur_pos ][2] | curses.A_NORMAL )
        self.note_cur_pos += offs_y
        if self.note_cur_pos > len( nc ) - 1:
            self.note_cur_pos = 0
        elif self.note_cur_pos < 0:
            self.note_cur_pos = len( nc ) - 1
        y, x = nc[ self.note_cur_pos ][0]
        self.screen.move( y, x )
        self.screen.chgat(y, x, nc[ self.note_cur_pos ][1], 
                            nc[ self.note_cur_pos ][2] | curses.A_REVERSE )
        self.Actual_Note = self.MC.Notes_List[y-2][0]
        self.Actual_Mode = self.MC.Notes_List[y-2][1]
        self.Actual_Degree = self.MC.Intervals[y-2]
        self.update_head()
        #self.set_statusbar( "{}, {}, {} ".format( self.Actual_Note, self.Actual_Mode, self.Actual_Degree, self.note_cur_pos ))

    def change_note( self, offset = 0 ):
        self.MC.set_next_note( offset )
        self.display( )

    def change_mode( self, offset = 0 ):
        self.MC.set_next_mode( offset )
        self.display( )

    def change_to( self, note, mode ):
        self.MC = Modes_Calculator( note, mode )
        self.Actual_Note = self.MC.Note
        self.Actual_Mode = self.MC.Mode
        self.Actual_Degree = self.MC.Intervals[0]
        self.display()

#    def update_neck( self ):
#        nk = self.MC.Neck
#        #for t in range(len( nk )-1, -1, -1):
#        for t in range(len( nk )):
#            for f in range(len( nk[ t ])):
#                #intrv = self
#
#                if f == 1:
#                    self.head.addstr( 19-t, 20+(f*3)-1, "║")#, color )
#                    self.head.addstr( 10-t, 20+(f*3)-1, "║")#, color )
#                elif f > 1:
#                    #x = 20+(f*3) if len(nk[t][f])
#                    self.head.addstr( 19-t, 20+(f*3)-1, "┆")#nk[t][f] + " ")#, color )
#                    self.head.addstr( 10-t, 20+(f*3)-1, "┆")#nk[t][f] + " ")#, color )
#                self.head.addstr( 19-t, 20+(f*3), nk[t][f] + " "*(len(nk[t][f])-1))#nk[t][f] + " ")#, color )
#                self.head.addstr( 10-t, 20+(f*3), nk[t][f] + " "*(len(nk[t][f])-1))#nk[t][f] + " ")#, color )
                    #sys.exit("{}, {}, {}".format(t, f, nk[t][f]))
    def get_color( self, intrv ):
        n = intrv#intrvs[i]
        if n in ("❶",):
            color = curses.color_pair(47)
        elif n in ("♭➁","➁♭"):
            color = curses.color_pair(232)
        elif n in ("➁","❷",):
            color = curses.color_pair(220)#208)
        elif n in ("➂m",):
            color = curses.color_pair(40)
        elif n in ("❸","➂"):
            color = curses.color_pair(209)
        elif n in ("❹","➃",):
            color = curses.color_pair(208)#20)
        elif n in ("➃♯","♯➃",):
            color = curses.color_pair(0)
        elif n in ("♭➄","➄♭"):#, "➆m", "➆", "❼"):
            color = curses.color_pair(232)
        elif n in ("➄","❺",):
            if self.Actual_Mode in ("Ionian", "Lydian", "Mixolydian"):
                color = curses.color_pair(12)
            else:
                color = curses.color_pair(79)
        elif n in ("➅♭","♭➅",):
            color = curses.color_pair(232)
        elif n in ("❻","➅",):
            color = curses.color_pair(230)
        elif n in ("❼","➆",):
            color = curses.color_pair(210)
        elif n in ("➆m",):
            color = curses.color_pair(118)
        elif n in ("_",):
            color = curses.color_pair(0)
        if n in ( "➃♯", "♯➃") and self.Actual_Mode == "Lydian" \
                or  n in ("➆m",) and self.Actual_Mode == "Mixolydian" \
                or  n in ("❻","➅",) and self.Actual_Mode == "Dorian" \
                or  n in ("♭➁","➁♭",) and self.Actual_Mode == "Phrygian" \
                or  n in ("♭➄","➄♭",) and self.Actual_Mode == "Locrian":
            color = curses.color_pair(197)
        return color

    def get_mode_color(self, mode ):
        pass

    def update_head( self ):
        scale = self.MC.get_scale(self.Actual_Note, self.Actual_Mode)
        intrv = self.MC.get_intervals(scale, self.Actual_Mode)
        for i in range( len( scale )):
            color = self.get_color( intrv[ i ] )
            self.head.addstr( 2, 20+(i*2), scale[ i ] + " ", color )
            self.head.addstr( 1, 20+(i*2), intrv[ i ] + " ", color )
            self.head.attron(curses.color_pair(0))
        #self.update_neck()
        nk = self.MC.Neck
        #for t in range(len( nk )-1, -1, -1):
        for t in range(len( nk )):
            for f in range(len( nk[ t ])):
                if nk[t][f] != " ":
                    i = intrv[ scale.index( nk[t][f] ) ]
                    color = self.get_color(i)
                else:
                    i = " "

                if f > 0:
                    self.head.addstr( 19-t, 20+(f*3)-1, "┆")#nk[t][f] + " ")#, color )
                    self.head.addstr( 10-t, 20+(f*3)-1, "┆")#nk[t][f] + " ")#, color )
                    if f == 1:
                        self.head.addstr( 19-t, 20+(f*3)-1, "║")#, color )
                        self.head.addstr( 10-t, 20+(f*3)-1, "║")#, color )
                    elif f == 13:
                        self.head.addstr( 19-t, 20+(f*3)-1, "│")#, color )
                        self.head.addstr( 10-t, 20+(f*3)-1, "│")#, color )
                    elif f == 6 and t == 0:
                        self.head.addstr( 14-t, 20+(f*3)-1, "◉")#, color )
                        
                    #x = 20+(f*3) if len(nk[t][f])
                self.head.addstr( 19-t, 20+(f*3), nk[t][f] + " ", color )
                self.head.addstr( 10-t, 20+(f*3), i + " ", color )
        self.head.refresh()

    def display( self ):
        self.screen.clear()
        self.height, self.width = self.screen.getmaxyx()
        self.window = curses.initscr()

        head_h = 25
        head_w = self.width - 1
        neck_w = 14
        neck_intrv_w = 20

        self.head = self.window.subwin( head_h, self.width, 0, 0)
        self.head.box()
        #sys.exit(self.MC.Neck)
        #self.head_panel = curses.panel.new_panel(self.head)

        nb_frets = (self.width - 3) // 2
        if nb_frets > 18:
            nb_frets = 16
        self.MC.set_frets( nb_frets )#(self.height - head_h -5) )
        

        self.neck_intrv = self.window.subwin( self.height - head_h -1, neck_intrv_w, head_h, 0)
        
        self.neck = self.window.subwin( self.height - head_h -1, neck_w, head_h, neck_intrv_w +1)
        #self.neck_panel = curses.panel.new_panel(self.neck)

        #head_panel.bottom()
        #self.screen.refresh()

        addh  = self.head.addstr
        #if self.cursor_position == 0:
        #self.head.attron(curses.color_pair(1))
        nl = self.MC.Notes_List
        self.note_cur_pos = 0
        self.note_colors = []
        for i in range( len( nl )):
            if len( nl[i] ) > 0:
                if nl[i][1] == "Ionian":
                    color = curses.color_pair(84)
                elif nl[i][1] == "Dorian":
                    color = curses.color_pair(118)#208)#124)
                elif nl[i][1] == "Phrygian":
                    color = curses.color_pair(232)#118)
                elif nl[i][1] == "Lydian":
                    color = curses.color_pair(229)
                elif nl[i][1] == "Mixolydian":
                    color = curses.color_pair(215)
                elif nl[i][1] == "Eolian":
                    color = curses.color_pair(40)#15)
                elif nl[i][1] == "Locrian":
                    color = curses.color_pair(208)#118)#106)
                addh( 2 + i, 2, nl[i][0] + " "*4, color )
                addh( 2 + i, 5, nl[i][1], color )
                self.add_note_color( ( 2+i, 2 ), len(nl[i][1]) +3, color )
        #    if i == 0:
        #        addh( 1, 20, self.MC.get_intervals_as_str())
        #        addh( 2, 20, self.MC.get_scale_as_str())
        
        
        self.head.refresh()

#        addn = self.neck.addstr
#        addn( 1, 0, self.MC.get_neck_notes_as_str())
#        #self.screen.addstr( 2, 2, self.MC.get_neck_notes_as_str())
#        addni = self.neck_intrv.addstr
#        addni( 1, 0, self.MC.get_neck_intervals_as_str())
#        
#        self.neck.box()
#        self.neck.refresh()
#        self.neck_intrv.box()
#        self.neck_intrv.refresh()
        #curses.panel.update_panels()
        self.screen.refresh()

        self.set_cursor_position()
        #if not self.cursor_position:
        #    self.set_statusbar()

        self.interact( )

    def navigate( self, key ):
        if key == curses.KEY_DOWN:
            self.set_cursor_position( +1, 0 )
        elif key == curses.KEY_UP:
            self.set_cursor_position( -1, 0 )
        elif key == curses.KEY_LEFT:
            self.set_cursor_position( 0, -1 )
        elif key == curses.KEY_RIGHT:
            self.set_cursor_position( 0, +1 )
        elif key in (curses.KEY_ENTER, ord('\n')):
            self.change_to( self.Actual_Note, self.Actual_Mode )
            #self.set_statusbar(" ".join([self.MC.Note, self.MC.Mode, self.Actual_Note, self.Actual_Mode]))
        elif key == ord('+'):
            self.change_note( +1 )
        elif key == ord('-'):
            self.change_note( -1 )
        elif key == ord('*'):
            self.change_mode( +1 )
        elif key == ord('/'):
            self.change_mode( -1 )

    def set_statusbar( self, sb = "" ):
        y, x = self.screen.getyx()
        if sb != "":
            self.Statusbar = "Press 'q' to exit | " + sb
        else:
            sb = self.Statusbar
        #else:
            #y, x = self.screen.getyx()
            #sb = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(x, y)
        self.screen.addstr(self.height-1, 0, sb + " " * (self.width - len(sb) - 1))
        self.screen.move( y, x )
        self.screen.refresh()
        #self.set_cursor_position()

    def interact( self ):
        #functs = [ ("exit", exit) ]
        #cur_pos = self.cursor_names.index[ cur_name ]
        #y, x = self.cursor_positions[ cur_pos ]
        #self.screen.move( y, x )
        #self.cursor_pos = cur_pos

        while True:
            k = self.screen.getch()
            if k == ord('q'):
                exit()
            elif k in ( curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT, 
                        curses.KEY_ENTER, ord('\n'), ord('+'), ord('-'), ord('*'), ord('/') ):
                self.navigate( k )
            elif k in ( curses.KEY_RESIZE, ):
                try:
                    self.display()
                except curses.error:
                    sys.exit("Terminal size is too small\nMinimal size : height: 22, width:44")
        self.Statusbar = "'q': exit || +,-,*,/: change Note/Mode || 'Enter': set Note" 
        self.set_status_bar( self.Statusbar )
        #self.screen.addstr(4, 10, self.MC.get_scale_as_str())
        #self.screen.addstr(5, 10, self.MC.get_intervals_as_str())
        #i = 0
        #for l in self.MC.get_neck_intervals_as_str().split('\n'):
        #    if 10 + i < self.height:
        #        self.screen.addstr( 10 + i, 20, l )
        #    else:
        #        break
        #    i +=1

        #self.window = self.screen.newwin( 0, 0 )
        #key = self.screen.getch()
        #exit()


if __name__ == "__main__":
    curses.wrapper(Guit_Screen)

