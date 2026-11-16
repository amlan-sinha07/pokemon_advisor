
import subprocess
from types import SimpleNamespace

import pytest

from engine.damage_calc import DamageCalculator
from models.pokemon import Pokemon
from models.move import Move


@pytest.fixture
def calculator(tmp_path):

    calc = DamageCalculator()

    # A temporary file makes the executable existence check pass.
    calc.cpp_calc = tmp_path / "damage_calc.exe"
    calc.cpp_calc.write_text("test executable")

    return calc


def test_cpp_returns_integer(calculator, monkeypatch):

    fake_result = SimpleNamespace(
        returncode=0,
        stdout="72\n",
        stderr=""
    )

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: fake_result
    )

    result = calculator.calculate_cpp(
        50, 100, 100, 2.0, 1.5
    )

    assert result == 72


def test_missing_cpp_executable(calculator, tmp_path):

    calculator.cpp_calc = tmp_path / "missing.exe"

    result = calculator.calculate_cpp(
        50, 100, 100, 1.0, 1.0
    )

    assert result is None


def test_invalid_cpp_output(calculator, monkeypatch):

    fake_result = SimpleNamespace(
        returncode=0,
        stdout="Invalid damage",
        stderr=""
    )

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: fake_result
    )

    result = calculator.calculate_cpp(
        50, 100, 100, 1.0, 1.0
    )

    assert result is None


def test_cpp_nonzero_returncode(calculator, monkeypatch):

    fake_result = SimpleNamespace(
        returncode=1,
        stdout="",
        stderr="Invalid input"
    )

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: fake_result
    )

    result = calculator.calculate_cpp(
        50, 100, 100, 1.0, 1.0
    )

    assert result is None


def test_cpp_timeout(calculator, monkeypatch):

    def fake_run(*args, **kwargs):

        raise subprocess.TimeoutExpired(
            cmd=args[0],
            timeout=5
        )

    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )

    result = calculator.calculate_cpp(
        50, 100, 100, 1.0, 1.0
    )

    assert result is None


def test_python_fallback(calculator, monkeypatch,tmp_path):

    attacker = Pokemon(
        name="Pikachu",
        types=["Electric"],
        moves=[],
        stats={
            "hp": 100,
            "atk": 100,
            "spa": 100
        }
    )

    defender = Pokemon(
        name="Charizard",
        types=["Fire"],
        moves=[],
        stats={
            "hp": 100,
            "def": 100,
            "spd": 100
        }
    )

    move = Move(
        "Tackle",
        "Normal",
        50,
        "Physical",
        100
    )

    calculator.cpp_calc =tmp_path / "missing.exe"

    monkeypatch.setattr(
        calculator.type_calc,
        "effectiveness",
        lambda *args: 1.0
    )

    result = calculator.calculate(
        attacker,
        defender,
        move
    )
    print("Damage:", result["damage"])
    print("Effectiveness:", result["effectiveness"])
    print("STAB:", result["stab"])
    print("Engine:", result["engine"])

    assert result["damage"] == 24
    assert result["engine"] == "Python"
