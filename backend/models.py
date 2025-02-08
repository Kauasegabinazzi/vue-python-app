 
from dataclasses import dataclass
from typing import List

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    user: str
    password: str
    is_user_admin: bool = False
    is_user_manager: bool = False
    is_user_tester: bool = False
    user_timezone: str = "UTC"
    is_user_active: bool = True
    created_at: str = None 