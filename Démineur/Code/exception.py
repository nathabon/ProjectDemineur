class InvalidPlatformSystem(Exception):
    def __init__(self, userPlatform):
        self.message = f"Your system platform is {userPlatform}, not Windows or MAC."
        super().__init__(self.message)