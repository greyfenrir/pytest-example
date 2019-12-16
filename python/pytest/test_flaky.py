import time
import pytest

@pytest.mark.Flaky
class TestDemoGrid(object):
    def test_flaky(self, driver):
        time_now = int(time.time())
        driver.get("http://blazedemo.com/echo.php?echo=" + str(time_now))
        assert 0 == time_now % 2, "Failed to receive write value"