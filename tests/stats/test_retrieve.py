from __future__ import absolute_import, print_function, unicode_literals

import pytest
import responses

from pysyncgateway import Stats
from pysyncgateway.exceptions import GatewayDown


@pytest.fixture
def expected_stats(syncgateway_version_str):
    """
    Returns:
        list (str): List of stats returned by the current version of SG.
    """
    stats = [
        'cb',
        'cmdline',
        'goroutine_stats',
        'mc',
        'memstats',
        'syncGateway_changeCache',
        'syncGateway_db',
        'syncGateway_dcp',
        'syncGateway_gocb',
        'syncGateway_httpListener',
        'syncGateway_index',
        'syncGateway_index_clocks',
        'syncGateway_rest',
        'syncGateway_stats',
    ]
    if syncgateway_version_str.startswith('1.5.'):
        return stats
    return sorted(stats + [
        'goblip',
        'syncGateway_import',
        'syncGateway_query',
    ])


# --- TESTS ---


def test(admin_client, expected_stats):
    stats = Stats(admin_client)

    result = stats.retrieve()

    assert result is True
    assert sorted(list(stats.data)) == expected_stats


# --- FAILURES ---


@responses.activate
def test_bad_json(admin_client):
    """
    expvars endpoint returns something non-JSON nasty, raises ValueError
    """
    stats = Stats(admin_client)
    responses.add(responses.GET, stats.url, body=':D')

    with pytest.raises(ValueError):
        stats.retrieve()


@responses.activate
def test_missing_endpoint(admin_client):
    """
    expvars endpoint goes AWOL
    """
    stats = Stats(admin_client)

    with pytest.raises(GatewayDown):
        stats.retrieve()
