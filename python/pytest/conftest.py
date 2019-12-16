from selenium import webdriver
import pytest
import time

# creds
API_KEY = ''
API_SECRET = ''
base = 'a.blazemeter.com'
API_KEY = '63fbd156fce37fe333752284'
API_SECRET = 'cde938e138374324fb9cdd6c95aa547af6247ec43654fbf1058a1cf211c3d269266931f6'
base = 'bza-199-artem-artem.blazemeter.net'

BUILD_ID = int(time.time())

### BlazeGrid capabilites

@pytest.fixture(scope="module")
def driver(request):
    blazegrid_url = 'https://{}:{}@{}/api/v4/grid/wd/hub'.format(API_KEY, API_SECRET, base)
    desired_capabilities = {
        # 'browserName': 'chrome',
        'blazemeter.locationId': 'harbor-5ca1d0f356e140733411a936',
        'browserName': 'chrome',
        'blazemeter.projectId': '1',
        'blazemeter.testName': request.fspath.purebasename,
    }
    driver = webdriver.Remote(command_executor=blazegrid_url, desired_capabilities=desired_capabilities)
    yield driver
    driver.quit()


@pytest.fixture(scope="function", autouse=True)
def name_reporter(request, driver):
    args = {
        'testCaseName': request.node.name,
        'testSuiteName': request.fspath.purebasename
    }
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    yield
    tests_failed = request.node.rep_call.failed or request.node.rep_setup.failed
    status = 'failed' if tests_failed else 'success'
    args = {
        'status': status,
        'message': 'test \{0}'.format(status)
    }
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    rep = __multicall__.execute()
    setattr(item, "rep_" + rep.when, rep)
    return rep
