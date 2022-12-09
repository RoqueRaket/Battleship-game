import tkinter
import random
import json
import copy
import sys
from itertools import islice

class Start_menu:
    """Creates the start menu."""
    
    def __init__(self):
        root=tkinter.Tk()
        self.dict=dict
        self.root=root
        player_name=[]
        self.player_name=player_name
        self.start_menu()
    
    def highscore_read(self):
        """Finds all the current high scores and sorts them"""
        with open("Highscores.json","r") as file_open:
            self.data=json.load(file_open)

        self.sorted_data={}
        sorted_values=sorted(self.data.values())
        for i in sorted_values:
            for j in self.data.keys():
                if self.data[j]==i:
                    self.sorted_data[j]=self.data[j]
        self.sorted_data=dict(islice(self.sorted_data.items(),10))


    def start_menu(self):
        self.highscore_read()
        self.root.title("Start Menu")
        self.label=tkinter.Label(self.root,text="Welcome to the game Battleship!")
        self.label.pack()
        self.entry = tkinter.Entry(self.root)
        self.entry.pack()
        self.button = tkinter.Button(self.root,text="Start Game!",activebackground="white",command=lambda: self.use_entry())
        self.button.pack()
        text_box=tkinter.Text(self.root, height=11, width=20)
        text_list=["HALL OF FAME\n"]
        for i in self.sorted_data:
            text_list.append(str(i+": "))
            text_list.append(str(self.sorted_data[i]))
            text_list.append("\n")
        text="".join(text_list)
        text_box.insert(tkinter.END, text)
        text_box.pack()
        text_box.config(state=tkinter.DISABLED)
        self.quit_button=tkinter.Button(self.root,text="Exit Game",activebackground="white",command=lambda: sys.exit())
        self.quit_button.pack()
        self.root.mainloop()

    def use_entry(self):
        """Destroys the start menu and saves the players name when the game starts"""
        name=self.entry.get()
        self.player_name.append(name)
        self.root.destroy()

class Game:
    """Contains the game."""

    def __init__(self,root,attempts,won_game):
        """Creates the buttons where the game is played."""
        self.root=root
        self.root.title("Battleship")
        self.won_game=won_game
        self.x=8 #X is number of rows
        self.y=8 #Y is number of columns
        hidden_board=[]
        for a in range(self.x):
            column=[]
            for b in range(self.y):
                column.append(0)
            hidden_board.append(column)
        self.hidden_board=hidden_board
        self.attempts=attempts
        ships_as_classes=[]
        self.ships_as_classes=ships_as_classes

        #Places the ships on the hidden board
        self.hidden_board=self.ship_placer(1,2,2)
        #Creates the buttons and puts them the matrix, so that each button has its coordinates on the hidden board as its key
        button_hidden_board=copy.deepcopy(self.hidden_board)
        self.button_hidden_board=button_hidden_board
        
        for x in range(self.x):
            for y in range(self.y):
                self.button_hidden_board[x][y]=tkinter.Button(self.root, text="("+str(x)+","+str(y)+")", height=3, width=10, bg="white", command=lambda x=x, y=y: self.hit_check(x,y))
                self.button_hidden_board[x][y].grid(row=x,column=y)
        
        self.quit_button=tkinter.Button(self.root,text="Exit Game",activebackground="white",command=lambda: sys.exit())
        self.quit_button.grid(row=self.x,column=0)

        self.main_button=tkinter.Button(self.root,text="Main Menu",activebackground="white",command=lambda: [self.root.destroy(),self.exit_class()])
        self.main_button.grid(row=self.x,column=1)

        self.cheat_button=tkinter.Button(self.root,text="Cheat",activebackground="white",command=lambda: self.cheat())
        self.cheat_button.grid(row=self.x,column=2)


    def exit_class(self):
        """Exits the current function and returns to the main menu."""
        return

    def ship_placer(self,length1_amount,length2_amount,length3_amount):
        """Places the ships on the hidden board. length1, length2, and length3 all specify the amount of ships of each length."""
        
        #List to store all the coordinates that border ships so that ships don't appear next to each other
        border_and_ship_list=[]
        ship_list=[]
        border_list=[]

        def length1_ship():
            """Returns the coordinates of one length 1 ship"""
            x=random.randint(0,self.x-1)
            y=random.randint(0,self.y-1)
            coordinate=(x,y)
            return coordinate
        
        def one_ship(length):
            """Returns coordinates of one length 3 ship"""
            x=random.randint(0,8-length)
            y=random.randint(0,8-length)
            orientation=random.choice(["horizontal","vertical"])
            if orientation=="horizontal":
                ship=[(x,y),(x+1,y),(x+2,y),(x+3,y),(x+4,y)]
            if orientation=="vertical":
                ship=[(x,y),(x,y+1),(x,y+2),(x,y+3),(x,y+4)]
            for i in range(5-length):
                ship.pop()
            return ship

        def border_adder(coordinate):
            """Adds the coordinates of the border of the ship 
            to the list so that ships don't appear next to each other."""
            border_list=[]
            for a in range(-1,2):
                for b in range(-1,2):
                    if 0<=coordinate[0]+a<=self.x:
                        if 0<=coordinate[1]+b<=self.y:
                            border_list.append((coordinate[0]+a,coordinate[1]+b))

            return border_list

        def long_ships(length,amount):
            """Generates the coordinates for the amount of ships specified with the length specified."""
            for a in range(amount):
                ship_coordinates=one_ship(length)
                while bool(set(ship_coordinates) & set(border_and_ship_list)) == True: #While the coordinates for the ship overlap with another ship the ships coordinates are generated again 
                    ship_coordinates=one_ship(length)
                for b in ship_coordinates:
                    ship_list.append(b)
                    border_list=border_adder(b)
                    for c in border_list:
                        border_and_ship_list.append(c)

        #Places the coordinates for the amount of ships with length 2 and 3
        long_ships(3,length3_amount)
        long_ships(2,length2_amount)

        #Generates the coordinates for the amount of ships with length 1
        for g in range(length1_amount):
            ship1_coordinates=length1_ship()
            while ship1_coordinates in border_and_ship_list: #While the coordinates for the ship overlap with another ship the ships coordinates are generated again 
                ship1_coordinates=length1_ship()
            ship_list.append(ship1_coordinates)
            border_list=border_adder(ship1_coordinates)
            for h in border_list:
                border_and_ship_list.append(h)

        #Places a 1 on the tile that is specified by the coordinates to indicate part of a ship
        for i in ship_list:
            self.hidden_board[i[0]][i[1]]=1

        return self.hidden_board

    def end(self):
        """Checks if all the ships have been found."""
        all_states=[]
        for a in range(self.x):
            for b in self.hidden_board[a]:
                all_states.append(b)
        if 1 not in all_states:
            self.won_game.append(1)
            self.game_over()

    def hit_check(self,x,y):
        """If a tile is clicked the function will check the hidden board to check the state of the button.
        #0 = Tile has not been clicked, no part of ship here
        #1 = Tile has not been clicked, part of ship is here
        #2 = Tile has been clicked, missed shot (no ship here)
        #3 = Tile has been clicked, ship has been hit (ship here)"""
        #Gives a game over message if all ships have been hit
        
        
        #Checks what is on the button and 
        if self.hidden_board[x][y]==2 or self.hidden_board[x][y]==3:
            self.warning()

        if self.hidden_board[x][y]==0:
            self.button_hidden_board[x][y].configure(text="Miss!",bg="blue",fg="white")
            self.hidden_board[x][y]=2
            self.attempts.append(1)

        if self.hidden_board[x][y]==1:
            self.button_hidden_board[x][y].configure(text="Hit!",bg="red",fg="white")
            already_tried_values=[]
            self.hit_ships_coordinates=set(self.boat_sunk_check(x,y,already_tried_values))
            self.hidden_board[x][y]=3
            self.end()
            self.amount_of_coordinates_hit=[]
            for i in self.hit_ships_coordinates:
                if self.hidden_board[i[0]][i[1]]==1 or self.hidden_board[i[0]][i[1]]==3:
                    self.amount_of_coordinates_hit.append(self.hidden_board[i[0]][i[1]])
            if 1 not in self.amount_of_coordinates_hit:
                self.ship_found()
            self.attempts.append(1)

    def boat_sunk_check(self,coordinate_x,coordinate_y,already_tried_values):
        """Returns the coordinates of the ship that contained the coordinates x and y."""
        already_tried_values.append((coordinate_x,coordinate_y))
        list_of_borders_coordinates=[]
        list_of_borders_values=[]
        for a in range(max(0,coordinate_y-1),min(self.x,coordinate_y+2)):
            for b in range(max(0,coordinate_x-1),min(self.y,coordinate_x+2)):
                list_of_borders_coordinates.append((b,a))
                list_of_borders_values.append(self.hidden_board[b][a])
        
        #Makes sure the program does not run backwards
        for j in already_tried_values:
            if j in list_of_borders_coordinates:
                index1=list_of_borders_coordinates.index(j)
                list_of_borders_coordinates.pop(index1)
                list_of_borders_values.pop(index1)
        #If the ships end is reached
        if 3 not in list_of_borders_values:
            if 1 not in list_of_borders_values:
                return already_tried_values
        
        counter=0
        index_list_for_middle_of_ship=[]
        
        for i in list_of_borders_values:
            if i == 3 or i == 1:
                counter=counter+1
        if counter==1: #If the player clicked the end of a ship the function runs along the ship recursively
            for m in list_of_borders_values:
                if m == 3 or m == 1:
                    index2=list_of_borders_values.index(m)
                    return self.boat_sunk_check(list_of_borders_coordinates[index2][0],list_of_borders_coordinates[index2][1],already_tried_values)
        if counter>1: #If the player clicked somewhere in the middle of the ship the recursive function branches out towards the sides
            if 1 not in list_of_borders_values: #Only 3s
                round=0
                for n in list_of_borders_values:
                    if n == 3 or n==1:
                        index_list_for_middle_of_ship.append(list_of_borders_values.index(n)+round)
                        round=round+1
                return self.boat_sunk_check(list_of_borders_coordinates[index_list_for_middle_of_ship[0]][0],list_of_borders_coordinates[index_list_for_middle_of_ship[0]][1],already_tried_values) + self.boat_sunk_check(list_of_borders_coordinates[index_list_for_middle_of_ship[1]][0],list_of_borders_coordinates[index_list_for_middle_of_ship[1]][1],already_tried_values)

            if 3 not in list_of_borders_values: #Only 1s
                round=0
                for n in list_of_borders_values:
                    if n == 3 or n==1:
                        index_list_for_middle_of_ship.append(list_of_borders_values.index(n)+round)
                        round=round+1
                return self.boat_sunk_check(list_of_borders_coordinates[index_list_for_middle_of_ship[0]][0],list_of_borders_coordinates[index_list_for_middle_of_ship[0]][1],already_tried_values) + self.boat_sunk_check(list_of_borders_coordinates[index_list_for_middle_of_ship[1]][0],list_of_borders_coordinates[index_list_for_middle_of_ship[1]][1],already_tried_values)

            else:
                round=0
                for n in list_of_borders_values:
                    if n == 3 or n==1:
                        index_list_for_middle_of_ship.append(list_of_borders_values.index(n))
                        round=round+1
            return self.boat_sunk_check(list_of_borders_coordinates[index_list_for_middle_of_ship[0]][0],list_of_borders_coordinates[index_list_for_middle_of_ship[0]][1],already_tried_values) + self.boat_sunk_check(list_of_borders_coordinates[index_list_for_middle_of_ship[1]][0],list_of_borders_coordinates[index_list_for_middle_of_ship[1]][1],already_tried_values)

    def warning(self):
        """Creates a window with a warning screen if the player clicks the same button twice."""

        gui=tkinter.Tk()
        gui.title("Heads up!")
        gui.geometry("")

        text=tkinter.Label(gui,text="Tile already pressed. Please press another tile!")
        text.pack()

        start=tkinter.Button(gui,text="Confirm",activebackground="white",command=lambda: gui.destroy())
        start.pack()

        gui.mainloop()

    def game_over(self):
        """Creates a window when the player finds all the ships."""

        gui=tkinter.Tk()
        gui.title("Game over!")
        gui.geometry("")

        text=tkinter.Label(gui,text="Well played! You found all the ships!")
        text.pack()

        start=tkinter.Button(gui,text="Confirm",activebackground="white",command=lambda: [gui.destroy(),self.root.destroy()])
        start.pack()

        gui.mainloop()

    def ship_found(self):
        """If a ship is found the player is notified with a window."""
        gui=tkinter.Tk()
        gui.title("Well done!")
        gui.geometry("")

        text=tkinter.Label(gui,text="You destroyed a ship!")
        text.pack()

        start=tkinter.Button(gui,text="Confirm",activebackground="white",command=lambda: gui.destroy())
        start.pack()

        gui.mainloop()

    def cheat(self):
        """If the player wants to cheat the board is shown with the ships revealed."""
        gui=tkinter.Tk()
        gui.title("Revealed board")
        gui.geometry("")
        for x in range(self.x):
            for y in range(self.y):
                if self.hidden_board[x][y]==1 or self.hidden_board[x][y]==3:
                    button=tkinter.Button(gui, text="("+str(x)+","+str(y)+")", height=3, width=10, bg="red")
                    button.grid(row=x,column=y)
                if self.hidden_board[x][y]==0 or self.hidden_board[x][y]==2:
                    button=tkinter.Button(gui, text="("+str(x)+","+str(y)+")", height=3, width=10, bg="blue")
                    button.grid(row=x,column=y)
        
        cheat=tkinter.Button(gui,text="Done with the cheating",activebackground="white",command=lambda: gui.destroy())
        cheat.grid(row=self.x,column=0)

        gui.mainloop()

def main():
    """Runs the whole program and menu system."""
    
    while True:
        #Start menu
        start_menu=Start_menu() #Dict är en dictinary som innehåller highscores
        attempts=[]
        won_game=[]
        counter=0
        #The game itself
        board=tkinter.Tk()
        game=Game(board,attempts,won_game)
        board.mainloop()
        #Saves the current players stats to the high score file
        if len(won_game)==1:
            name=start_menu.player_name
            for i in attempts:
                counter=counter+1
            start_menu.data.update({str(name[0]):int(counter)})
            json_object=json.dumps(start_menu.data, indent=4)
            with open("Highscores.json","w") as file_write:
                file_write.write(json_object)

if __name__ == "__main__":  
    main()
