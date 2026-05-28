"""Tests for the User entity."""

from __future__ import annotations

import pytest

from entity.models.user import User


def test_user_creation_stores_core_fields() -> None:
    """Create a user and verify core fields are stored."""
    # Arrange
    user_id = "user-001"
    email = "user@example.com"
    display_name = "Magic User"

    # Act
    user = User(user_id=user_id, email=email, display_name=display_name)

    # Assert
    assert user.user_id == user_id
    assert user.email == email
    assert user.display_name == display_name
    assert user.is_active is True


def test_user_rejects_blank_display_name() -> None:
    """Raise ValueError when display name is blank."""
    # Arrange
    user_id = "user-002"
    email = "blank@example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="display_name must not be blank"):
        User(user_id=user_id, email=email, display_name="   ")


def test_user_deactivate_sets_is_active_false() -> None:
    """Deactivate user and ensure active flag is false."""
    # Arrange
    user = User(
        user_id="user-003",
        email="active@example.com",
        display_name="Active User",
    )

    # Act
    user.deactivate()

    # Assert
    assert user.is_active is False
