from aiogram.fsm.state import State, StatesGroup

class GameStates(StatesGroup):
    captain_name = State()
    team_name = State()
    city = State()
    first_solution = State()
    constrained_solution = State()
