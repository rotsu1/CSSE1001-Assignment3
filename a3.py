__author__ = "Ryu Otsu"
__email__ = "s4800316@uqconnenct.edu.au"
__date__ = "24/05/2023"

import tkinter as tk
from tkinter import filedialog # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *

class InfoBar(AbstractGrid):
    """
    The view class that displays the number of days elapsed, player's energy and
    player's health.
    """
    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """
        Parameters:
            master: Window/Frame in which the InfoBar is going to be displayed.         
        """
        super().__init__(master, (2, 3), (715, INFO_BAR_HEIGHT))

    def redraw(self, day: int, money: int, energy: int) -> None:
        """
        Refreshes the InfoBar by redrawing everything on it.

        Parameters:
            day: Number of days elapsed.
            money: Amount of money the player has.
            energy: Amount of energy the player has.
        """
        self.clear()
        self._info_top = ["Day:", "Money:", "Energy:"]
        self._info_bottom = [day, f"${money}", energy]
        
        for row in range(2):
            for column in range(3):
                if not row:
                    self.annotate_position(
                        (row, column), self._info_top[column], HEADING_FONT
                        )
                else:
                    self.annotate_position(
                        (row, column), self._info_bottom[column]
                        )
        
class FarmView(AbstractGrid):
    """
    The view class that displays the farm map, player and plants.
    """
    def __init__(
        self,
        master: tk.Tk | tk.Frame,
        dimensions: tuple[int, int],
        size: tuple[int, int], **kwargs
        ) -> None:
        """
        Parameters:
            master: Window/Frame in which the FarmView is going to be displayed.
            dimensions: Number of rows and columns (rows, columns).
            size: Size of the FarmView (width in pixels, height in pixels).
        """
        super().__init__(master, dimensions, size)
        self._cache = {}

    def redraw(
        self,
        ground: list[str],
        plants: dict[tuple[int, int], "Plant"],
        player_position: tuple[int, int],
        player_direction: str
        ) -> None:
        """
        Refreshes the FarmView by redrawing everything on it.

        Parameters:
            ground: Current map.
            plants: Plants that are currently on the farm.
            player_position: Current player's position.
            player_direction: Currenct player's direction.
        """
        self.clear()
        for row, letters in enumerate(ground):
            for column, ground_type in enumerate(letters):
                image_name = f"images/{IMAGES[ground_type]}"
                size = self.get_cell_size()
                ground = get_image(image_name, size, self._cache)
                midpoint = self.get_midpoint((row, column))
                self.create_image(midpoint, image = ground)
                
                if (row, column) in plants:
                    image_name = (
                        f"images/{get_plant_image_name(plants[(row, column)])}"
                        )
                    plant = get_image(image_name, size, self._cache)
                    self.create_image(midpoint, image = plant)
                    
                if (player_position[0], player_position[1]) == (row, column):
                    image_name = f"images/{IMAGES[player_direction]}"
                    player = get_image(image_name, size, self._cache)
                    self.create_image(midpoint, image = player)
                    
class ItemView(tk.Frame):
    """
    The view class that displays the relevant information of the plants and
    buttons for a single item.
    """
    def __init__(
        self,
        master: tk.Frame,
        item_name: str,
        amount: int,
        select_command: Optional[Callable[[str], None]] = None,
        sell_command: Optional[Callable[[str], None]] = None,
        buy_command: Optional[Callable[[str], None]] = None
        ) -> None:
        """
        Parameters:
            master: Frame in which the ItemView is going to be stored.
            item_name: Name of the item.
            amoumt: Amount of the item.
            select_command: The command that is called when the item is selected
                (left click on the label or frame).
            sell_command: The command that is called when the item is sold
                (click on the sell button).
            buy_command: The command that is called whent the item is bought
                (click on the buy button).
        """
        super().__init__(master)
        self._item = item_name
        self._amount = amount
        # This will determine whether the item is selected or not.
        self._selected = False
        
        self._label = tk.Label(self)
        self._label.pack(side = tk.LEFT)
        
        if item_name in BUY_PRICES:
            # buy_command will be handled in the FarmGame class
            self._buy_button = tk.Button(
                self,
                text = "Buy",
                command = lambda: buy_command(item_name)
                )
            self._buy_button.pack(side = tk.LEFT)
        
        # sell_command will be handled in the FarmGame class.
        self._sell_button = tk.Button(
            self,
            text = "Sell",
            command = lambda: sell_command(item_name)
            )
        self._sell_button.pack(side = tk.LEFT)

        # select_command will be handled in the FarmGame class.
        self._label.bind("<Button-1>", lambda event: select_command(item_name))
        self.bind("<Button-1>", lambda event: select_command(item_name))
        

    def update(self, amount: int, selected: bool = False) -> None:
        """
        Updates the text on the label, and the colour of the ItemView.

        Parameters:
            amount: Amount of the item
            selected: Whether the item is selected or not
        """
        if not amount:
            amount = 0
        self._amount = amount
        
        self._label.config(
            text = f"{self._item}: {self._amount}\n" + \
            f"Sell price: ${SELL_PRICES[self._item]}\n" + \
            f"Buy price: ${BUY_PRICES.get(self._item, 'N/A')}"
            )

        # Checks which colour the inventory should be.
        if amount <= 0:
            colour = INVENTORY_EMPTY_COLOUR
            self.unselect()
        elif selected:
            colour = INVENTORY_SELECTED_COLOUR
            self.select()
        elif amount > 0:
            colour = INVENTORY_COLOUR

        self.config(bg = colour)
        self._label.config(bg = colour)
        self._sell_button.config(highlightbackground = colour)
        if self._item in BUY_PRICES:
            self._buy_button.config(highlightbackground = colour)

    def get_amount(self) -> int:
        """
        Returns the amount of the item.
        """
        return self._amount

    def get_item(self) -> str:
        """
        Returns the item name.
        """
        return self._item

    def get_selected(self) -> bool:
        """
        Returns whether the item is selected or not.
        """
        return self._selected

    def unselect(self) -> None:
        """
        It makes the item not selected.
        """
        self._selected = False

    def select(self) -> None:
        """
        It makes the item selected.
        """
        self._selected = True
    
class FarmGame:
    """
    The controller class for the farm game.
    """
    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """
        Parameters:
            master: Window in which all of the view classes are going to be
                displayed.
            map_file: The map file that is going to be loaded.
        """
        self._master = master
        master.title("Farm Game")
        master.geometry("715x755")

        self._plants = {
            "Potato Seed": PotatoPlant,
            "Kale Seed": KalePlant,
            "Berry Seed": BerryPlant
            }
        
        self.cache = {}
        banner_image = get_image("images/header.png", (700, 130), self.cache)
        banner = tk.Label(master, image = banner_image)
        banner.pack(side = tk.TOP)
        
        self._farm_model = FarmModel(map_file)
        self._player = self._farm_model.get_player()

        self._infobar = InfoBar(self._master)
        next_day = tk.Button(
            text = "Next day",
            command = self.new_day
            )
        next_day.pack(side = tk.BOTTOM)           
        self._infobar.pack(side = tk.BOTTOM)


        self._farmview = FarmView(
            self._master,
            (self._farm_model.get_dimensions()[0],
             self._farm_model.get_dimensions()[1]),
            (FARM_WIDTH, 500)
            )
        self._farmview.pack(side = tk.LEFT)
        
        self._frames = []
        for item in ITEMS:
            amount = self._player.get_inventory().get(item)    
            if amount == None:
                amount = 0
                
            self._itemview = ItemView(
                master, item, amount,
                select_command = (
                    lambda event, _item = item: self.select_item(_item)
                    ),
                buy_command = (
                    lambda event, _item = item: self.buy_item(_item)
                    ),
                sell_command = (
                    lambda event, _item = item: self.sell_item(_item)
                    )
                )
            self._itemview.pack(side = tk.TOP, expand = True, fill = "both")
            self._itemview.config(
                bg = INVENTORY_EMPTY_COLOUR,
                highlightbackground = INVENTORY_OUTLINE_COLOUR,
                highlightthickness = 1
                )
            self._frames.append(self._itemview)
            
        self._master.bind("<KeyPress>", self.handle_keypress)
        self.new_day()

    def new_day(self) -> None:
        """
        Increments the day by 1 and resets the energy to 100.
        """
        self._farm_model.new_day()
        self.redraw()

    def redraw(self) -> None:
        """
        Refreshes the all of the view classes by redrawing everything on it.
        """
        self._farmview.redraw(
            self._farm_model.get_map(),
            self._farm_model.get_plants(),
            self._farm_model.get_player_position(),
            self._farm_model.get_player_direction()
            )
        
        self._infobar.redraw(
            (self._farm_model.get_days_elapsed() - 1),
            self._player.get_money(),
            self._player.get_energy()
            )
        
        for item_frame in self._frames:
            item = item_frame.get_item()
            amount = self._player.get_inventory().get(item)
            if not item_frame.get_selected():
                item = False
            item_frame.update(amount, item)

    def handle_keypress(self, event: tk.Event) -> None:
        """
        Event handler for key press.
        
        Parameters:
            event: Keypress.
        """
        position = self._farm_model.get_player_position()
        
        if event.keysym in ["w", "a", "s", "d"]:
            if event.keysym == "w":
                direction = UP
                
            if event.keysym == "a":
                direction = LEFT
                
            if event.keysym == "s":
                direction = DOWN
                
            if event.keysym == "d":
                direction = RIGHT
                
            self._farm_model.move_player(direction)
            
        elif event.keysym == "t":
            self._farm_model.till_soil(position)
            
        elif event.keysym == "u":
            self._farm_model.untill_soil(position)
            
        elif event.keysym == "p":
            item = self._player.get_selected_item()
            row, col = position
            
            if not item or \
                self._farm_model.get_map()[row][col] != SOIL or \
                item not in self._player.get_inventory():
                return
            
            if item.endswith("Seed"):
                
                # Checks if the item is selected in the itemview.
                for item_frame in self._frames:
                    if item_frame.get_item() == item:
                        selected = item_frame.get_selected()
                        
                # This prevents from planting when the item is selceted within
                # the player's object but not selected in the itemview.
                if selected:
                    plant = self._plants[item]()
                    self._farm_model.add_plant(position, plant)
                    self._player.remove_item((item, 1))
                    
        elif event.keysym == "h":
            harvest = self._farm_model.harvest_plant(position)
            
            if harvest:
                self._player.add_item(harvest)
                
        elif event.keysym == "r":
            self._farm_model.remove_plant(position)
            
        self.redraw()       

    def select_item(self, item_name: str) -> None:
        """
        Event handler for the left mouse click on the label or frame in
        ItemView.

        Parameters:
            item_name: Name of item.
        """
        for item_frame in self._frames:
            amount = item_frame.get_amount()
            item = item_frame.get_item()
            
            if item_frame.get_selected():
                item_frame.unselect()
                
            elif item == item_name and amount > 0:
                self._player.select_item(item_name)
                item_frame.select()
                
        self.redraw()

    def buy_item(self, item_name: str) -> None:
        """
        Event handler for the buy button in ItemView.

        Parameters:
            item_name: Name of item.
        """
        self._player.buy(item_name, BUY_PRICES[item_name])  
        self.redraw()

    def sell_item(self, item_name: str) -> None:
        """
        Event handler for the sell button in ItemView.

        Parameters:
            item_name: Name of item.
        """
        self._player.sell(item_name, SELL_PRICES[item_name])
        self.redraw()

def play_game(root: tk.Tk, map_file: str) -> None:
    """
    Loads the game.

    Parameters:
        root: Master window
        map_file: Map file to play.
    """
    controller = FarmGame(root, map_file)
    root.mainloop()

def main() -> None:
    root = tk.Tk()
    play_game(root, "maps/map1.txt")

if __name__ == '__main__':
    main()
