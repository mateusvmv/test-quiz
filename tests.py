import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_no_empty_choice_name():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)

def test_no_long_choice_name():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a' * 101, False)

def test_no_unmarked_correct_choice_is_returned_on_correct():
    question = Question(title='q1', max_selections=3)
    a = question.add_choice('a', True)
    b = question.add_choice('b', True)
    c = question.add_choice('c', True)
    assert question.correct_selected_choices([a.id, b.id]) == [a.id, b.id]

def test_no_marked_incorrect_choice_is_returned_on_correct():
    question = Question(title='q1', max_selections=3)
    a = question.add_choice('a', True)
    b = question.add_choice('b', False)
    c = question.add_choice('c', True)
    assert question.correct_selected_choices([a.id, b.id]) == [a.id]

def test_no_unmarked_incorrect_choice_is_returned_on_correct():
    question = Question(title='q1', max_selections=3)
    a = question.add_choice('a', True)
    b = question.add_choice('b', False)
    c = question.add_choice('c', False)
    assert question.correct_selected_choices([a.id]) == [a.id]

def test_no_selecting_more_than_max():
    question = Question(title='q1')
    question.add_choice('a', True)
    question.add_choice('b', True)
    question.add_choice('c', True)
    with pytest.raises(Exception):
        question.correct_selected_choices(['a', 'b'])
    with pytest.raises(Exception):
        question.correct_selected_choices(['a', 'c'])
    with pytest.raises(Exception):
        question.correct_selected_choices(['b', 'c'])

def test_choice_id_invalid_after_remove():
    question = Question(title='q1')
    a = question.add_choice('a', True)

    question.remove_choice_by_id(a.id)
    with pytest.raises(Exception):
        question.remove_choice_by_id(a.id)

def test_choice_id_invalid_after_remove_all():
    question = Question(title='q1')
    a = question.add_choice('a', True)

    question.remove_all_choices()
    with pytest.raises(Exception):
        question.remove_choice_by_id(a.id)

def test_change_correct_choices():
    question = Question(title='q1', max_selections=3)
    a = question.add_choice('a', True)
    b = question.add_choice('b', True)
    c = question.add_choice('c', True)

    abc = [a.id, b.id, c.id]
    ab = [a.id, b.id]
    ac = [a.id, c.id]

    assert question.correct_selected_choices(abc) == abc

    question.set_correct_choices(ab)
    assert question.correct_selected_choices(abc) == ab
    assert question.correct_selected_choices(ab) == ab
    assert question.correct_selected_choices([ c.id ]) == []

    question.set_correct_choices(ac)
    assert question.correct_selected_choices(abc) == ac
    assert question.correct_selected_choices(ab) == [a.id]

def test_no_invalid_id_when_setting_correct_choices():
    question = Question(title='q1', max_selections=3)
    with pytest.raises(Exception):
        question.set_correct_choices([ 1 ])