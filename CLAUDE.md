# Burrowkit Python Game

## About this project

This is a learning project. I'm building a roguelike dungeon crawler in Python to bring my skills up to Australian university level for a master's degree. It is modelled on UQ's public information from CSSE1001 / CSSE7030 game assignments, which use a model-view-controller structure.

I come from Java, including OOP MVP and MVC concepts and building applications and games. **The goal is for me to learn, not just to finish the game.**

## How to help me (important)

- **Don't write implementation code for milestones unless I explicitly ask.** I write each milestone myself first. Review my code, explain concepts, and suggest improvements instead.
- **Explain a concept before implementing it.** For example, explain how to structure BFS on a grid, then let me try it. Short illustrative snippets that aren't part of this game are fine.
- **When debugging, wait for my hypothesis.** Ask me what I think is wrong before you point to the cause, then work through my hypothesis with me.
- **Suggest tests I've missed**, especially edge cases.
- When you review, explain *why* something is more Pythonic, not just *what* to change.
- Don't edit my files without asking. Show me suggestions instead and let me apply them.

## Code review focus: Java habits to unlearn

Flag these whenever you see them:

- Getters and setters everywhere. Prefer plain attributes, and use `@property` only when logic is needed.
- Boilerplate data classes. Use `@dataclass` for simple data-holding classes.
- Java-style methods such as `toString()`, `equals()` or `compareTo()`. Use dunder methods (`__str__`, `__eq__`, `__lt__`) instead.
- Java overloading methods/functions (previously heavily used throughout previous projects)
- Index-based loops (`for i in range(len(x))`). Prefer direct iteration, `enumerate`, `zip`, comprehensions and generators.
- Interfaces for everything. Rely on duck typing, and use `abc` only where it genuinely helps.
- Manual file open/close. Use context managers (`with`).

## Standards a uni marker expects

- **Style:** PEP 8.
- **Docstrings:** on every module, class and function.
- **Type hints:** throughout, checked with `mypy`.
- **Testing:** unit tests with `pytest`, especially for movement, combat and pathfinding.
- **MVC separation:** markers check this closely.
  - `model/` contains pure game logic. **No pygame imports in `model/`, ever.** It should be possible to swap the GUI for a text version.
  - `view/` handles all drawing.
  - `controller.py` translates input into model actions.
- **Error handling:** validate input, and handle missing or corrupt save files properly.
- **Project setup:** venv, sensible Git commits, and a clean package layout.

## Learning areas

- **OOP:** an `Entity` base class with `Player`, `Partner` and `Monster` subclasses; `Item` subclasses; composition for the inventory.
- **Data structures:** 2D grids, dicts for lookups, sets for visited tiles, queues for turn order.
- **Algorithms:** BFS (and possibly A*) for pathfinding; procedural generation (rooms and corridors, or cellular automata).
- **File I/O:** JSON save/load, and loading monster, item and move definitions from `data/`.

## Project structure

```
Burrowkit_game
├── src/
|   ├── main.py          # entry point, game loop
│   ├── __init__.py
│   └── dungeon/
│       ├── model/           # pure game logic, no pygame here
│       │   ├── __init__.py
│       │   ├── entities.py  # Entity, Player, Partner, Monster
│       │   ├── items.py
│       │   ├── level.py     # map grid, tiles, floor generation
│       │   └── combat.py
│       ├── view/            # everything that draws to screen
│       │   ├── __init__.py
│       │   └── renderer.py
│       ├── __init__.py
│       └── controller.py    # input → model actions
├── tests/
│   └── test_entities.py
├── data/                    # JSON for monsters, items, moves
├── requirements.txt
├── README.md
├── pyproject.toml
└── .gitignore
```

## Milestones

I commit to Git after each milestone.

1. **Window and grid:** open a pygame window and draw a hard-coded map of walls and floors.
2. **Player movement:** move with the arrow keys and block movement into walls. Write the first pytest test here.
3. **Turn system:** each player action is one turn, and everything else acts after the player.
4. **Monsters:** they wander randomly, then chase the player using BFS pathfinding.
5. **Combat and HP:** attacks, damage, fainting and the message log.
6. **Items and bag:** pick up items, use berries and show the inventory panel.
7. **Procedural floors:** random rooms and corridors, stairs to the next floor, and a floor counter.
8. **Partner AI:** a companion that follows the player and fights.
9. **Moves and hunger:** a 4-move system with limited uses, and a hunger meter.
10. **Save and load:** serialise game state to JSON.
11. **Polish:** a title screen, game over and win conditions, then simple sprites to replace the coloured squares.

<!-- Current milestone: update this line as you go so Claude knows where you are. -->
**Current milestone:** 1


## Develop good habits from day one
Type hints and docstrings on every function and class.
Run checks regularly:
`ruff check .`
`ruff format .`
`mypy src`
`pytest`
