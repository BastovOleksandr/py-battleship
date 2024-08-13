class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple,
        end: tuple,
        is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        elif start[0] == end[0] and start[1] != end[1]:
            for num in range(end[1] - start[1] + 1):
                self.decks.append(Deck(start[0], start[1] + num))
        else:
            for num in range(end[0] - start[0] + 1):
                self.decks.append(Deck(start[0] + num, start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if not self.is_drowned and deck.is_alive:
            deck.is_alive = False
            for deck in self.decks:
                if deck.is_alive:
                    return self.is_drowned
            self.is_drowned = True

        return self.is_drowned


class Battleship:
    def __init__(self, ships: list[tuple[tuple, tuple]]) -> None:
        self.field = {}
        for ship in ships:
            current_ship = Ship(ship[0], ship[1])
            for deck in current_ship.decks:
                self.field[(deck.row, deck.column)] = current_ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            sunk = self.field[location].fire(*location)
            return "Sunk!" if sunk else "Hit!"

        return "Miss!"

    def _validate_field(self) -> None:
        ships = set(self.field.values())
        if not (
            len(ships) == 10
            or self._validate_ships_count
            or self._validate_ship_location
        ):
            raise InvalidBattleshipField(
                "Incorrect ship coordinates in the passed list"
            )

    def print_field(self) -> None:
        empty = [["~" for _ in range(10)] for _ in range(10)]
        for ship in set(self.field.values()):
            marker = "*"
            if ship.is_drowned:
                marker = "x"
            for deck in ship.decks:
                if deck.is_alive:
                    empty[deck.row][deck.column] = u"\u25A1"
                else:
                    empty[deck.row][deck.column] = marker
        filled_field = ""

        for row in empty:
            filled_field += "\t".join(row) + "\n"

        print(filled_field)

    def _validate_ships_count(self) -> bool:
        ships_count = [0, 0, 0, 0]
        for ship in set(self.field.values()):
            ships_count[len(ship.decks) - 1] += 1
        return ships_count == [4, 3, 2, 1]

    def _validate_ship_location(self) -> bool:
        directions = [
            (-1, -1), (1, 1), (-1, 0), (0, -1),
            (-1, 1), (1, -1), (1, 0), (0, 1),
        ]

        for (row, column), ship in self.field.items():
            for dr, dc in directions:
                adjacent = (row + dr, column + dc)
                if adjacent in self.field and self.field[adjacent] != ship:
                    return False

        return False


class InvalidBattleshipField(Exception):
    pass
