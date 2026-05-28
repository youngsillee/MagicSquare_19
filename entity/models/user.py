"""User entity for MagicSquare domain."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class User:
    """Represent a user in the MagicSquare domain.

    Attributes:
        user_id: Unique identifier of the user.
        email: Email address used for communication and login.
        display_name: Public name shown in user-facing areas.
        is_active: Whether the user account is active.
    """

    user_id: str
    email: str
    display_name: str
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate core invariants after initialization.

        Raises:
            ValueError: If any required field is blank.
        """
        if not self.user_id.strip():
            raise ValueError("user_id must not be blank")
        if not self.email.strip():
            raise ValueError("email must not be blank")
        if not self.display_name.strip():
            raise ValueError("display_name must not be blank")

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
