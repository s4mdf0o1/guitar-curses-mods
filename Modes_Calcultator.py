#!/usr/bin/env python3
# -*- codepage: utf-8 -*-

import sys

#Tunes = ( 'E', 'A', 'D', 'G', 'B', 'E' )
#Frets = 18
#steps = ['1', 'b2', '2', 'b3',  '3',  '4',  'b5',  '5',  'b6',  '6',  'b7',  '7',
#    '1', 'b9', '9', 'b10', '10', '11', 'b12', '12', 'b13', '13', 'b14', '14', 'b15', '15']
#nums = ("➀","➁","➂","➃","➄","➅","➆","➈","⑪","⑬")
#nums_neg = ("❶","❷","❸","❹","❺","❻","❼","❾","⓫"")
#symbols = ("✕", "♯", "♭", "△", "⚬", "∅","♮", "⬤")
#All_ints = (("❶",),("♭❷",),("❷",),("❸m",),("❸",),("❹",),("♯❹","♭❺"),("❺",),("♯❺","♭❻"),("❻",),("❼m",),("❼",))

#All_ints = ("❶","♭❷","❷","❸m","❸","❹","♯❹","❺","♭❻","❻","❼m","❼")
#All_notes = (("B♯","C"),("C♯","D♭"),("D",),("D♯","E♭"),("E","F♭"),("E♯","F"),("F♯","G♭"),("G",),("G♯","A♭"),("A",),("A♯","B♭"),("B","C♭"))
#print(All_notes)
#Weights = ( T, T, H, T, T, T, H )
#Modes = ( "Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Eolian", "Locrian" )
#Notes = ( "C", "D", "E", "F", "G", "A", "B" )

H = 1
T = 2
class Modes_Calculator(object):
    Tunes = ( 'E', 'A', 'D', 'G', 'B', 'E' )
    Frets = 18
    All_notes = (("B♯","C"),("C♯","D♭"),("D",),("D♯","E♭"),("E","F♭"),("E♯","F"),("F♯","G♭"),("G",),("G♯","A♭"),("A",),("A♯","B♭"),("B","C♭"))
    Weights = ( T, T, H, T, T, T, H )
    Modes = ( "Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Eolian", "Locrian" )
    Notes = ( "C", "D", "E", "F", "G", "A", "B" )
    All_ints = ("❶","♭❷","❷","❸m","❸","❹","♯❹","❺","♭❻","❻","❼m","❼")
    All_ints = ("❶","♭➁","➁","➂m","➂","➃","♯➃","➄","♭➅","➅","➆m","➆")
    All_ints = ("❶","➁♭","❷","➂m","❸","❹","➃♯","❺","➅♭","❻","➆m","❼")

    def __init__(self, Note="C", Mode="Ionian"):
        self.Note = Note.replace('b', '♭').replace('#', '♯')
        self.Mode = Mode.replace('ien', 'ian')
        self.calculate( self.Note, self.Mode )

    def calculate( self, Note, Mode ):
        self.Scale = self.get_scale( Note, Mode )
        #self.Modes.index( Mode ) - len( self.Modes ), self.Notes.index( Note[0] ) - len( self.Notes ))
        #self.Notes_List = [ n for n in self.Scale if n != "_" ]
        self.Intervals = self.get_intervals( self.Scale, Mode )
        self.Neck = self.get_neck_notes( self.Tunes, self.Frets, self.Scale )
        self.Notes_List = self.get_notes_list( Note, Mode )

    def get_notes_list( self, note, mode ):
        notes_list = []
        mode_idx = self.Modes.index( mode ) - len( self.Modes )
        note_idx = self.Notes.index( note[0] ) - len( self.Notes )

        offset = self.select_note_weight( note )
        self.Notes_List = []
        for i in range( len( self.Notes )): 
            Mode_pos = mode_idx + i 
            Note_pos = note_idx + i 
            if i == 0:    
                notes_list.append( (note, self.Mode ))
            else:
                real_note = self.get_real_note( self.Notes[ Note_pos ], offset )
                notes_list.append( ( real_note, self.Modes[ Mode_pos ] ))

            if self.Weights[ Mode_pos ] > 1:
                notes_list.append( () )
            offset += self.Weights[ Mode_pos ]
        return notes_list
        
    def set_note( self, note ):
        self.Note = note.replace('b', '♭').replace('#', '♯')
        self.calculate( note, self.Mode )
    def set_next_note( self, offset ):
        for i in range( len( self.All_notes )):
            if self.Note in self.All_notes[i]:
                idx = i
                break
        idx += offset
        if idx > len( self.All_notes ) - 1:
            idx = 0
        elif idx < 0:
            idx = len( self.All_notes ) - 1
        if idx in (0, 5):
            note = self.All_notes[idx][1]
        elif idx in (4, 11):
            note = self.All_notes[idx][0]
        else:
            note = self.All_notes[idx][0]
        self.set_note( note )

    def set_mode( self, mode ):
        self.Mode = mode.replace('ien', 'ian')
        self.calculate( self.Note, mode )
    def set_next_mode( self, offset ):
        idx = self.Modes.index( self.Mode ) + offset 
        if idx > len( self.Modes ) - 1:
            idx = 0
        elif idx < 0:
            idx = len( self.Modes ) - 1
        self.set_mode( self.Modes[ idx ] )

    def set_frets( self, frets ):
        self.Frets = frets
    def set_tunes( self, tunes ):
        if tunes is tuple:
            self.Tunes = tunes
        else:
            print("Error : {} is not a valid tune".format(tunes))

    def select_note_weight( self, note ):
        for i in range( len( self.All_notes )):
            if note in self.All_notes[i]:
                return i - len( self.All_notes )

    def get_real_note( self, note, offset):
        if note == self.All_notes[ offset ][0][0]:
            return self.All_notes[ offset ][0]
        else:
            return self.All_notes[ offset ][-1]

    def get_scale( self, note, mode):#_idx, note_idx ):
        scale = []
        mode_idx = self.Modes.index( mode ) - len( self.Modes )
        note_idx = self.Notes.index( note[0] ) - len( self.Notes )

        offset = self.select_note_weight( note )
        #self.Notes_List = []
        for i in range( len( self.Notes )):
            Mode_pos = mode_idx + i
            Note_pos = note_idx + i
            if i == 0:        
                scale.append( note )
                #self.Notes_List.append( (note, self.Mode ))
            else:
                real_note = self.get_real_note( self.Notes[ Note_pos ], offset )
                scale.append( real_note )
                #self.Notes_List.append( ( real_note, self.Modes[ Mode_pos ] ))

            if self.Weights[ Mode_pos ] > 1:
                scale.append( "_" )
                #self.Notes_List.append( () )
            offset += self.Weights[ Mode_pos ]
        return scale

    def get_intervals( self, scale, mode ):
        intrv = []
        for i in range(len(scale)):
            if scale[ i ] != "_":
                if mode == "Locrian" and self.All_ints[i] == "➃♯":
                    intrv.append( "➄♭" )
                else:
                    intrv.append( self.All_ints[i] )
            else:
                intrv.append("_")
        return tuple(intrv)
    def get_neck_notes( self, tunes, frets, scale ):
        neck = []
        #neck_intrv = []
        for t_idx in range(len( tunes )):
            neck.append([])
            #neck_intrv.append([])
            offset_t = self.select_note_weight( tunes[ t_idx ] )
            for fr in range( frets ):
                f = fr
                if fr > 12:
                    f -= 12
                note = self.All_notes[ offset_t+f ]
                if note[0] in scale:
                    neck[ t_idx ].append( note[0] )
                elif note[-1] in scale:
                    neck[ t_idx ].append( note[-1] )
                else:
                    neck[ t_idx ].append( " " )
                #if note[0] in scale or note[-1] in scale:
                #    neck_intrv[ t_idx ].append( scale.index( note ))
                #else:
                #    neck_intrv[ t_idx ].append( "|" )
        return neck

    def get_neck_notes_as_str( self ):
        neck = self.Neck
        str_neck = ""
        matrix = list( zip( *neck[::1] ))
        for st in range( self.Frets ):#len( matrix )):
            str_neck += " "
            for fr in range( len( matrix[ st ] )):
                if st == 0 and matrix[st][fr] == "|":
                    str_neck += "_"
                else:
                    str_neck += matrix[st][fr]
                if len( matrix[st][fr] ) < 2:
                    if st in (5,7,9,12,17) and fr == 2:
                        str_neck += "◉"
                    else:
                        str_neck += " "
            if st == 0:
                str_neck += "\n" + "―" *13 + "\n"
            elif st == 11:
                str_neck += "\n " + "―" *11 + "\n"
            else:
                str_neck += "\n " + "-" *11 + "\n"
        return str_neck
    def get_neck_intervals_as_str( self ):
        neck = self.Neck
        #print(" |  |  |  |  |  |\n ➀ ♭➁  ➂m♯➃  ➄  ➅\n ----------------\n")

        str_neck_intrv = ""
        idx = -1
        matrix = list( zip( *neck[::1] ))
        for st in range( self.Frets ):#len( matrix )):
            #str_neck_intrv += " "
            #print(matrix[ st ])
            for fr in range( len( matrix[ st ] )):
                str_fr = " "# if st > 0 else ""
                    #str_fr = " "
                #str_fr = ""
                if matrix[st][fr] in self.Scale:
                    idx = self.Scale.index( matrix[st][fr] )
                else:
                    idx = -1
                if st == 0 and idx < 0: #matrix[st][fr] == "|":
                    #if st == 0:
                    str_fr += "✕ "
                    #else:
                    #    str_neck_intrv +=  matrix[st][fr]
                else:
                    if matrix[st][fr] == "|":
                        str_fr += matrix[st][fr] + " "
                    else:
                        if len(self.Intervals[idx]) < 2:
                            str_fr += self.Intervals[idx] + " "
                        else:
                            if self.Intervals[idx][1] == "m":
                                str_fr += self.Intervals[idx]
                            else:
                                str_fr = str_fr[:-1] + self.Intervals[idx] + " "
                    #print( idx, matrix[st][fr], self.Intervals[idx],)
                        #str_neck_intrv += self.Intervals[idx] #matrix[st][fr]
                    #else:
                        #str_neck_intrv +=  matrix[st][fr]
                #print( matrix[st][fr], len( matrix[st][fr] ))
                if idx and len( self.Intervals[idx]) <2 :#len(matrix[st][fr] ) < 2
                    if st in (5,7,9,12,17) and fr >4 : #== 2:
                        str_fr += "◉"
                    #else:
                        #if idx in (1,4) or self.Intervals[idx] == "➃":
                            #print( "\'{}\' / \'{}\'".format( matrix[st][fr], self.Intervals[idx]))
                    #    if len(self.Intervals[idx] != "➃":
                    #        str_fr += " "
                str_neck_intrv += str_fr
            if st == 0:
                str_neck_intrv += "\n" + "―" *18 + "\n"
            elif st == 11:
                str_neck_intrv += "\n " + "―" *16 + "\n"
            else:
                str_neck_intrv += "\n " + "-"*16 +"\n"
        return str_neck_intrv
        
    def get_scale_as_str( self ):
        s = ""
        for n in self.Scale:
            s += n + " " if len( n ) < 2 else n
        return s + "|" 
    def get_intervals_as_str( self ):
        s = ""
        for i in self.Intervals:
            s += i + " " if len( i ) < 2 else i
        return s + "|"
    def get_note_mode_as_str( self ):
        return "{} {}".format( self.Note, self.Mode )
    def get_note_mode_list_as_str( self ):
        idx_m = self.Modes.index( self.Mode ) - len( self.Modes )
        s = ""
        for i in range( len( self.Notes_List )):
            e = " " * (3 - len( self.Notes_List[ i ] ))
            s += e.join(( self.Notes_List[ i ], self.Modes[ idx_m + i ], "\n" ))
        return s

if __name__ == "__main__":
    try:
        Note = sys.argv[1].replace("b","♭").replace("#","♯")
    except:
        Note = "C" 
    try:
        Mode = sys.argv[2].replace("ien", "ian")
    except:
        Mode = "Ionian"

    MC = Modes_Calculator( Note, Mode )
    print( MC.get_note_mode_as_str() )
    #print( MC.get_scale_as_str() )
    #print( MC.get_intervals_as_str() )
    #print( MC.get_neck_notes_as_str() )
    #print( MC.get_neck_intervals_as_str() )
    #print( MC.get_note_mode_list_as_str() )
    #print( MC.Scale )
    #print( MC.Intervals )
    #print( MC.Notes_List )
    for st in range(len(MC.Neck)):
        for fr in range(len(MC.Neck[st])):
            print( MC.Neck[st][fr] + " ", end='')
        print()
    #print( "\n".join(MC.Neck))
    #print( dir(MC))
#sys.exit(0)




#A2="_x_A_____B_E_ / A2\n | | | | | |\n -----------\n | | E A | |\n -----------\n | | | | | |\n\n"
#X2="_x_❶_____❷_❺_ / X2\n | | | | | |\n -----------\n | | ❺ ❶ | |\n -----------\n | | | | | |\n\n"
#print( A2 )
#print( X2 )
# 'm' = '-'
# '△' = 'M7'
# '∅' = 'm7b5'
# '⚬7' = 'dim7'
 
#Ionien:     ❶ _ ❷ _ ❸ ❹ _ ❺ _ ❻ _ ❼ |
#                    /             /
#Dorien      ❶ _ ❷ ➂m_ ❹ _ ❺ _ ❻ ➆m_ |
#               /             /
#Phrygien    ❶ ♭➁_ ➂m_ ❹ _ ❺ ♭➅_ ➆m_ |
#Lydien      ❶ _ ❷ _ ❸ _ ♯➃❺ _ ❻ _ ❼ |
#                       /         /
#Mixolydien  ❶ _ ❷ _ ❸ ❹ _ ❺ _ ❻ ➆m_ |
#                   /         /
#Eolien      ❶ _ ❷ ➂m_ ❹ _ ❺ ♭➅_ ➆m_ |
#               /         /
#Locrien     ❶ ♭➁_ ➂m_ ❹ ♭➄_ ♭➅_ ➆m_ |

# ♭➁   ♭❷

#  _x_A_____B_E_ A2
#   | | | | | |
#   -----------
#   | | E A | |
#   -----------
#   | | | | | |
#
