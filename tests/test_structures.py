from src.structures import Stack


def test_stack_push_pop_peek_and_min() -> None:
    s = Stack()
    assert s.is_empty() is True
    assert len(s) == 0

    s.push(3)
    assert s.peek() == 3
    assert s.min() == 3
    assert len(s) == 1

    s.push(5)
    assert s.min() == 3

    s.push(2)
    assert s.min() == 2

    s.push(2)
    assert s.min() == 2

    assert s.pop() == 2
    assert s.min() == 2

    assert s.pop() == 2
    assert s.min() == 3

    assert s.pop() == 5
    assert s.min() == 3

    assert s.pop() == 3
    assert s.is_empty() is True
    assert len(s) == 0
