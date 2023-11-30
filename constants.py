# User vehicle
DEFAULT_USER_VEHICLE_IMG = 'assets/user_vehicle.png'
# NPC vehicle
DEFAULT_NPC_VEHICLE_IMG = 'assets/npc_vehicle.png'

DEFAULT_CROSS_ROAD_IMG = 'assets/Cross_road.png'

DEFAULT_BANANA_IMG = 'assets/banana.png'

DEFAULT_ROADBLOCK_IMG = 'assets/stop.png'

DEFAULT_CAR_IMG = 'assets/car.jpeg'

DEFAULT_CAR_SPEED = 25

DEFAULT_NPC_SPEED = 20

DEFAULT_NPC_POSITION_X = {
    'OPPOSITE': 1600,
    'CROSS': 845
}

DEFAULT_NPC_POSITION_Y = {
    'OPPOSITE': 475,
    'CROSS': 0
}

 # Log
LOG_CODES = {
    '1001': "Avoidable obstacle detected, reduce speed",
    '1002': "Unavoidable obstacle detected, emergency stop",
    '1003': "Potential collision detected, emergency stop"
}

DEFAULT_ROWS_FOR_CONFIGURATION_DIALOG = [
    ("Scenario 1", "☐", "☐", "☐", "☐", "☐"),
    ("Scenario 2", "☐", "☐", "🗹", "☐", "☐"),
    ("Scenario 3", "☐", "☐", "🗹", "🗹", "☐"),
    ("Scenario 4", "☐", "☐", "🗹", "☐", "🗹"),
    ("Scenario 5", "☐", "🗹", "☐", "☐", "☐"),
    ("Scenario 6", "☐", "🗹", "☐", "🗹", "☐"),
    ("Scenario 7", "🗹", "☐", "☐", "☐", "☐"),
    ("Scenario 8", "🗹", "☐", "☐", "🗹", "☐"),
    ("Scenario 9", "🗹", "☐", "🗹", "☐", "☐"),
]

DEFAULT_COLUMNS_FOR_CONFIGURATION_DIALOG = [
    "Scenarios",
    "Obstacle: Unavoidable",
    "Obstacle: Avoidable",
    "Make a Turn",
    "Other Car: Opposite Direction",
    "Other Car: Cross Direction"
]

SCENARIO_TO_CONFIGURATION_MAP = {
    "Scenario 1": {
        "UnavoidableObstacle": False,
        "AvoidableObstacle": False,
        "MakeATurn": False,
        "OtherCarOpposite": False,
        "OtherCarCross": False,
    },
    "Scenario 2": {
        "UnavoidableObstacle": False,
        "AvoidableObstacle": False,
        "MakeATurn": True,
        "OtherCarOpposite": False,
        "OtherCarCross": False,
    },
    "Scenario 3": {
        "UnavoidableObstacle": False,
        "AvoidableObstacle": False,
        "MakeATurn": True,
        "OtherCarOpposite": True,
        "OtherCarCross": False,
    },
    "Scenario 4": {
        "UnavoidableObstacle": False,
        "AvoidableObstacle": False,
        "MakeATurn": False,
        "OtherCarOpposite": False,
        "OtherCarCross": False,
    },
    "Scenario 5": {
        "UnavoidableObstacle": False,
        "AvoidableObstacle": True,
        "MakeATurn": False,
        "OtherCarOpposite": False,
        "OtherCarCross": False,
    },
    "Scenario 6": {
        "UnavoidableObstacle": False,
        "AvoidableObstacle": True,
        "MakeATurn": False,
        "OtherCarOpposite": True,
        "OtherCarCross": False,
    },
    "Scenario 7": {
        "UnavoidableObstacle": True,
        "AvoidableObstacle": False,
        "MakeATurn": False,
        "OtherCarOpposite": False,
        "OtherCarCross": False,
    },
    "Scenario 8": {
        "UnavoidableObstacle": True,
        "AvoidableObstacle": False,
        "MakeATurn": False,
        "OtherCarOpposite": True,
        "OtherCarCross": False,
    },
    "Scenario 9": {
        "UnavoidableObstacle": True,
        "AvoidableObstacle": False,
        "MakeATurn": True,
        "OtherCarOpposite": False,
        "OtherCarCross": False,
    },
}