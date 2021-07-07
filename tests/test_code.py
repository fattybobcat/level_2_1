import pytest

from io import StringIO
import sys
from codes import (load_obscene_words, fetch_detailed_pull_requests)


@pytest.mark.parametrize(
    'db_path, expected',
    [
        ([[1, 2, 3], [4]], {1, 2, 3, 4}),
        ([[1, 2], ['x', 'y']], {1, 2, 'x', 'y'}),
        ([], set()),
    ]
)
def test_load_obscene_words(db_path, expected, mocker):
    mock_sqlite = mocker.patch('codes.sqlite3')
    mock_sqlite.connect().cursor().execute().fetchall.return_value = db_path
    assert load_obscene_words('path') == expected


@pytest.mark.parametrize(
    'open_pull_requests, pull_request, expected',
    [
        ([{'number': 0}, {'number': 1}], {'number': 1}, {1: {'number': 1}}),
        ([{'number': 2}], None, {}),
        ([{'number': 3}], {'number': 4}, {4: {'number': 4}}),
     ]
 )
def test_fetch_detailed_pull_requests(mocker, open_pull_requests, pull_request, expected):
    mock_api = mocker.Mock()
    mock_api.fetch_pull_request.return_value = pull_request
    assert fetch_detailed_pull_requests(mock_api, open_pull_requests) == expected
