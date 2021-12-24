"""Test :class:`TimePeriod`."""

import datetime

import pytest
import pytz

from nowplaypadgen.timeperiod import TimePeriod, TimePeriodError


@pytest.fixture(name="period")
def fixture_period():
    """Return TimePeriod fixture."""
    return TimePeriod()


def test_date_assignment(period):
    """Test the time setter and getter decorators."""

    period.starttime = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)
    assert isinstance(period.starttime, datetime.datetime)

    period.endtime = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
    assert isinstance(period.endtime, datetime.datetime)


def test_date_must_be_datetime_obj(period):
    """Test if none datetime objects will be refused."""

    with pytest.raises(TimePeriodError) as time_period_error:
        period.starttime = "Not a datetime.datetime object"

    assert "starttime has to be a datetime object" in str(time_period_error)

    with pytest.raises(TimePeriodError) as time_period_error:
        period.endtime = "Not a datetime.datetime object"

    assert "endtime has to be a datetime object" in str(time_period_error)


def test_date_must_be_tz_aware(period):
    """Test if none TZ aware datetime objects will be refused."""

    with pytest.raises(TimePeriodError) as time_period_error:
        period.starttime = datetime.datetime(2017, 8, 30, 21, 0, 0, 0)

    assert "starttime has to be a TZ aware datetime object" in str(time_period_error)

    with pytest.raises(TimePeriodError) as time_period_error:
        period.endtime = datetime.datetime(2017, 8, 30, 22, 0, 0, 0)

    assert "endtime has to be a TZ aware datetime object" in str(time_period_error)


def test_start_date_utc_conversion(period):
    """Test if datetime objects will be converted to UTC."""

    # Create localized start and end times
    zone_name = "Europe/Zurich"
    zurich_tz = pytz.timezone(zone_name)
    start = zurich_tz.localize(datetime.datetime(2017, 8, 30, 21, 0, 0, 0))
    end = zurich_tz.localize(datetime.datetime(2017, 8, 30, 22, 0, 0, 0))
    assert zone_name == start.tzinfo.zone
    assert zone_name == end.tzinfo.zone

    period.starttime = start
    period.endtime = end

    # Start and end times must be converted to UTC internally
    assert period.starttime.tzinfo.zone == "UTC"
    assert period.endtime.tzinfo.zone == "UTC"


def test_end_not_before_start_date(period):
    """Test that an end date can't be before a start date."""

    start = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
    end = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)

    period.starttime = start

    with pytest.raises(TimePeriodError) as time_period_error:
        period.endtime = end

    expected_error = f"endtime {end} has to be > than starttime {start}"
    assert expected_error in str(time_period_error)


def test_start_after_end_date(period):
    """Test that a start date can't be after and end date."""

    start = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
    end = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)

    period.endtime = end

    with pytest.raises(TimePeriodError) as time_period_error:
        period.starttime = start

    expected_error = f"starttime {start} has to be < than endtime {end}"
    assert expected_error in str(time_period_error)


def test_period_has_started(period):
    """Test that a period has started."""

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    period.starttime = now
    period.endtime = now + datetime.timedelta(hours=1)  # plus one hour

    assert period.active()
    assert period.started()
    assert not period.ended()


def test_period_has_not_started(period):
    """Test that a period hasn't started yet."""

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    period.starttime = now + datetime.timedelta(hours=1)  # plus one hour
    period.endtime = now + datetime.timedelta(hours=2)  # plus two hours
    assert not period.active()
    assert not period.started()
    assert not period.ended()


def test_period_has_ended(period):
    """Test that a period has ended."""

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    period.starttime = now - datetime.timedelta(hours=2)  # minus two hours
    period.endtime = now - datetime.timedelta(hours=1)  # minus one hour
    assert not period.active()
    assert period.started()
    assert period.ended()


def test_period_has_not_ended(period):
    """Test that a period hasn't ended yet."""

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    period.starttime = now
    period.endtime = now + datetime.timedelta(hours=1)  # plus one hour
    assert period.active()
    assert period.started()
    assert not period.ended()


def test_get_period_duration(period):
    """Test get duration (time delta) of a period."""

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    # The period spans one hour
    period.starttime = now
    period.endtime = now + datetime.timedelta(hours=1)

    expected_delta = datetime.timedelta(0, 3600)

    assert period.duration == expected_delta


def test_set_period_duration(period):
    """Test set duration (time delta) of a period."""

    duration = datetime.timedelta(hours=1)
    period.duration = duration

    assert period.duration == duration


def test_duration_must_be_timedelta(period):
    """Test if none timedelta period objects will be refused."""

    with pytest.raises(TimePeriodError) as time_period_error:
        period.duration = "Not a datetime.timedelta object"

    assert "duration has to be a timedelta object" in str(time_period_error)


def test_duration_must_be_positive(period):
    """Test that only positive durations will be accepted."""

    with pytest.raises(TimePeriodError) as time_period_error:
        period.duration = datetime.timedelta(seconds=-1)

    assert "duration must be positive" in str(time_period_error)


def test_duration_already_defined(period):
    """Test that a duration can't be changed."""

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    # This should automatically set the duration, as a start and end time is
    # known by the period
    period.starttime = now
    period.endtime = now + datetime.timedelta(hours=1)

    with pytest.raises(TimePeriodError) as time_period_error:
        period.duration = datetime.timedelta(hours=2)

    assert "duration already defined" in str(time_period_error)


def test_duration_sets_endtime(period):
    """Test that a duration will set a currently unknown end time."""

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    duration = datetime.timedelta(hours=1)

    period.starttime = now
    period.duration = duration

    assert period.endtime == now + duration


def test_duration_sets_starttime(period):
    """Test that a duration will set a currently unknown start time."""

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    duration = datetime.timedelta(hours=1)

    period.endtime = now
    period.duration = duration

    assert period.starttime == now - duration


def test_set_length(period):
    """Test that the duration can be set using seconds."""

    duration = datetime.timedelta(hours=1)
    period.set_length(3600)

    assert period.duration == duration
