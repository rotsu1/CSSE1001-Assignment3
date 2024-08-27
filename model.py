from typing import Optional
from constants import *
from a3_support import *

class Plant:
    """ Abstract plant class, which implements default behaviour and specifies
        required functions for all plant subclasses.
    """
    _NAME = 'abstract plant'

    def __init__(self):
        """ Constructor for this type of plant. """
        self._stage = 1
    
    def get_name(self) -> str:
        """ Returns the name of the plant. """
        return self._NAME
    
    def get_stage(self) -> int:
        """ Returns the current stage of the plant. """
        return self._stage
    
    def can_harvest(self) -> bool:
        """ Returns True iff the plant is ready to be harvested. """
        return self._stage >= 3
    
    def remove_on_harvest(self) -> bool:
        """ Returns True iff the plant should be removed from the grid after
            being harvested. """
        return True

    def age(self) -> None:
        """ Ages the plant by one day, and makes any necessary changes to the
            plants stage.
        """
        raise NotImplementedError('Plant subclasses must implement age()')
    
    def harvest(self) -> Optional[tuple[str, int]]:
        """ Harvests the plant iff it is ready to be harvested. Otherwise, does
            nothing.
        
            Returns:
                The name and quantity of the harvested item, or None if the
                harvest is unsuccessful.
        """
        raise NotImplementedError('Plant subclasses must implement harvest()')


class PotatoPlant(Plant):
    """ Potato plant has 5 stages, with stages 0-4 lasting one day each. At \
        stage 5 it is ready for harvest.
    """
    _NAME = 'potato'

    def age(self) -> None:
        self._stage = min(self._stage + 1, 5)
    
    def can_harvest(self) -> bool:
        return self._stage == 5
    
    def harvest(self) -> Optional[tuple[str, int]]:
        if self.can_harvest():
            return ('Potato', 1)


class KalePlant(Plant):
    """ Kale plant has 5 stages, with stage 5 being harvest. """
    _NAME = 'kale'
    def __init__(self) -> None:
        super().__init__()
        self._days = 0

    def age(self) -> None:
        self._days += 1
        self._stage = 5 if self._days >= 6 else (self._days + 1) // 2 + 1

    def can_harvest(self) -> bool:
        return self._stage == 5
    
    def harvest(self) -> Optional[tuple[str, int]]:
        if self.can_harvest():
            return ('Kale', 1)


class BerryPlant(Plant):
    """ Berry plant has 6 stages, with stage 6 being harvest. After harvest,
        the berry tree returns to stage 5 and regrows to stage 6 every 4
        days.
    """
    _NAME = 'berry'
    _DAYS_TO_STAGE = [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 6]

    def __init__(self) -> None:
        super().__init__()
        self._days = 0
        self._days_since_harvest = 0

    def age(self) -> None:
        self._days += 1

        # Before first harvest, use the _DAYS_TO_STAGE mapping
        if self._days <= 13:
            self._stage = self._DAYS_TO_STAGE[self._days]
            return

        # After plant has matured, it can be harvested after 4 days have elapsed
        # since the last harvest
        self._days_since_harvest += 1
        if self._days_since_harvest >= 4 or self._stage == 6:
            self._stage = 6
        else:
            self._stage = 5
        
    def remove_on_harvest(self) -> bool:
        return False
    
    def can_harvest(self) -> bool:
        return self._stage == 6
    
    def harvest(self) -> Optional[tuple[str, int]]:
        if self.can_harvest():
            self._stage = 5
            self._days_since_harvest = 0
            return ('Berry', 3)


class Player:
    """ Represents the player in the game. """

    START_ENERGY = 100

    def __init__(self) -> None:
        """ Constructor for the player. """
        self._energy = self.START_ENERGY
        self._money = 0
        self._inventory = {
            'Potato Seed': 5,
            'Kale Seed': 5,
        }
        self._position = (0, 0)
        self._direction = DOWN
        self._selected_item = None
    
    def get_energy(self) -> int:
        """ Returns the player's current energy. """
        return self._energy
    
    def get_money(self) -> int:
        """ Returns the player's current money. """
        return self._money
    
    def get_inventory(self) -> dict[str, int]:
        """ Returns the player's current inventory, mapping item names to
            amounts.
        """
        return self._inventory
    
    def select_item(self, item_name: str) -> None:
        """ Selects the item with the given name, if it's in the inventory. """
        if item_name in self._inventory.keys():
            self._selected_item = item_name
    
    def get_selected_item(self) -> Optional[str]:
        """ Returns the name of the currently selected item, or None if no item
            is selected.
        """
        return self._selected_item
    
    def get_position(self) -> tuple[int, int]:
        """ Returns the player's current (row, col) position. """
        return self._position
    
    def reset_energy(self) -> None:
        """ Resets the player's energy to the starting amount. """
        self._energy = self.START_ENERGY

    def reduce_energy(self, amount: int) -> None:
        """ Reduces the player's energy by the given amount. Note that this
            method will not ensure the player's energy remains non-negative.
        
        Parameters:
            amount: The amount to reduce the player's energy by.
        """
        self._energy -= amount

    def sell(self, item_name: str, price: int) -> None:
        """ Sells one instance of the given item for the given price, if the
            player has some of the item available.
        
        Parameters:
            item_name: The name of the item to sell.
            price: The price to sell the item for.
        """
        amount = self._inventory.get(item_name, 0)
        if amount > 0:
            self._money += price
            self.remove_item((item_name, 1))

    def buy(self, item_name: str, price: int) -> None:
        """ Buys one instance of the given item for the given price, if the
            player has enough money.

        Parameters:
            item_name: The name of the item to buy.
            price: The price to buy the item for.
        """
        if self._money >= price:
            self._money -= price
            self.add_item((item_name, 1))

    def add_item(self, to_add: tuple[str, int]) -> None:
        """ Adds the given amount of the given item to the player's inventory.
        
        Parameters:
            to_add: A tuple of the item name and amount to add.
        """
        item_name, amount = to_add
        self._inventory[item_name] = self._inventory.get(item_name, 0) + amount

    def remove_item(self, to_remove: tuple[str, int]) -> None:
        """ Removes the given amount of the given item from the player's
            inventory.

        Parameters:
            to_remove: A tuple of the item name and amount to remove.
        """
        item_name, amount = to_remove
        new_amount = self._inventory.get(item_name, 0) - amount
        if new_amount <= 0:
            self._inventory.pop(item_name)
        else:
            self._inventory[item_name] = new_amount

    def set_position(self, position: tuple[int, int]) -> None:
        """ Sets the player's position to the given position.
        
        Parameters:
            position: The new position to set.
        """
        self._position = position
    
    def set_direction(self, new_direction: str) -> None:
        """ Sets the player's direction to the given direction.

        Parameters:
            new_direction: The new direction to set.
        
        Pre-condition:
            new_direction in {UP, DOWN, LEFT, RIGHT}
        """
        self._direction = new_direction
    
    def get_direction(self) -> str:
        """ Returns the player's current direction. """
        return self._direction


class FarmModel:
    """ Represents the model for the farm game. """

    def __init__(self, map_file: str) -> None:
        """ Constructor for the farm model.
        
        Parameters:
            map_file: The path to the file containing the map to use.
        """
        self._map = read_map(map_file)
        self._plants = {}
        self._player = Player()
        self._days_elapsed = 1
    
    def get_plants(self) -> dict[tuple[int, int], Plant]:
        """ Returns the plants currently on the farm, as a dictionary mapping
            positions to plants.
        """
        return self._plants
    
    def get_player(self) -> Player:
        """ Returns the player in this game. """
        return self._player
    
    def add_plant(self, position: tuple[int, int], plant: Plant) -> bool:
        """ Adds the given plant to the given position, if the player has enough
            energy and there is no plant already at that position. Also handles
            reducing the player's energy appropriately for planting.
        
        Parameters:
            position: The position at which to add the plant.
            plant: The plant to add.
        
        Returns:
            True if the plant was added, False otherwise.
        """
        # Return early if not enough energy
        if self._player.get_energy() < PLANT_COST:
            return False

        if self._plants.get(position) is None:
            self._player.reduce_energy(PLANT_COST)
            self._plants[position] = plant
            return True
    
        return False
    
    def harvest_plant(
            self,
            position: tuple[int, int]
        ) -> Optional[tuple[str, int]]:
        """ Harvests the plant at the given position, if there is one that is
            ready for harvest. Also handles reducing the player's energy
            appropriately for harvesting, and removing the plant from the farm
            if it should be removed on harvest.

        Parameters:
            position: The position at which to harvest the plant.

        Returns:
            The result of harvesting the plant, or None if there was no plant
            at the given position.
        """
        # Return early if not enough energy
        if self._player.get_energy() < HARVEST_COST:
            return

        if self._plants.get(position) is not None:
            plant = self._plants[position]
            harvest_result = plant.harvest()
            if harvest_result is not None:
                if plant.remove_on_harvest():
                    self.remove_plant(position)
                self._player.reduce_energy(HARVEST_COST)
                return harvest_result
    
    def get_map(self) -> list[str]:
        """ Returns the map for this game. """
        return self._map
    
    def get_dimensions(self) -> tuple[int, int]:
        """ Returns the dimensions of the map for this game, as
            (number of rows, number of columns).
        """
        return (len(self._map), len(self._map[0]))
    
    def new_day(self) -> None:
        """ Advances the game by one day. """
        for plant in self._plants.values():
            plant.age()
        self._days_elapsed += 1
        self._player.reset_energy()
    
    def get_days_elapsed(self) -> int:
        """ Returns the number of days elapsed in this game. """
        return self._days_elapsed
    
    def get_player_position(self) -> tuple[int, int]:
        """ Returns the player's current position. """
        return self.get_player().get_position()

    def get_player_direction(self) -> str:
        """ Returns the player's current direction, as one of UP, DOWN, LEFT,
            or RIGHT.
        """
        return self.get_player().get_direction()

    def move_player(self, direction: str) -> None:
        """ Moves the player in the given direction, if possible. Also handles
            reducing the player's energy appropriately for moving.

        Parameters:
            direction: The direction to move the player in.

        Pre-condition:
            direction in {UP, DOWN, LEFT, RIGHT}
        """
        # Return early if not enough energy
        if self._player.get_energy() < MOVE_COST:
            return

        # Calculate new position
        move_delta = MOVE_DELTAS[direction]
        d_row, d_col = move_delta
        old_row, old_col = self.get_player_position()
        new_row, new_col = old_row + d_row, old_col + d_col

        # Cap positions at boundaries of map
        new_row = max(0, min(new_row, self.get_dimensions()[0] - 1))
        new_col = max(0, min(new_col, self.get_dimensions()[1] - 1))

        # Move player
        self._player.set_position((new_row, new_col))
        self._player.set_direction(direction)

        # Reduce energy if the move succeeded
        if (new_row, new_col) != (old_row, old_col):
            self._player.reduce_energy(MOVE_COST)

    def till_soil(self, position: tuple[int, int]) -> None:
        """ Tills the soil at the given position, if it is untilled soil.
            Reduces the player's energy appropriately.
        
        Parameters:
            position: The position at which to till the soil.
        """
        # Return early if not enough energy
        if self._player.get_energy() < TILL_COST:
            return

        row, col = position
        if self._map[row][col] == UNTILLED:
            self._player.reduce_energy(TILL_COST)
            self._map[row] = self._map[row][:col] + SOIL + self._map[row][col + 1:]
    
    def untill_soil(self, position: tuple[int, int]) -> None:
        """ Untills the soil at the given position, if it is tilled soil.
            Reduces the player's energy appropriately.

        Parameters:
            position: The position at which to untill the soil.
        """
        # Return early if not enough energy
        if self._player.get_energy() < UNTILL_COST:
            return

        row, col = position
        if position not in self._plants and self._map[row][col] == SOIL:
            self._player.reduce_energy(UNTILL_COST)
            self._map[row] = self._map[row][:col] + UNTILLED + self._map[row][col + 1:]

    def remove_plant(self, position: tuple[int, int]) -> None:
        """ Removes the plant at the given position, if there is one.
            Reduces the player's energy appropriately.

        Parameters:
            position: The position at which to remove the plant.
        """
        # Return early if not enough energy
        if self._player.get_energy() < REMOVE_COST:
            return

        if position in self._plants:
            self._player.reduce_energy(REMOVE_COST)
            self._plants.pop(position)
