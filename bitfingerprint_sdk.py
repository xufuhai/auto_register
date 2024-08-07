class BitFingerprintBrowser:
    def __init__(self, proxy, fingerprint):
        self.proxy = proxy
        self.fingerprint = fingerprint

    def open(self, url):
        # Implement opening the URL with the specified proxy and fingerprint
        pass

    def get_page(self):
        # Return a mock page object
        return MockPage()

    def close(self):
        # Implement closing the browser
        pass

class MockPage:
    def wait_for_load(self):
        # Implement waiting for the page to load
        pass

    def click(self, selector):
        # Implement click action
        pass

    def fill(self, selector, value):
        # Implement fill action
        pass

    def click_at(self, position):
        # Implement click at a specific position
        pass

