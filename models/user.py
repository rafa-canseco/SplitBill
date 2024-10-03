class User:
    def __init__(
        self,
        privy_id: str,
        name: str,
        email: str,
        walletAddress: str,
        is_profile_complete: bool = False,
        is_invited: bool = False,
    ):
        self.id = None
        self.privy_id = privy_id
        self.name = name
        self.email = email
        self.walletAddress = walletAddress
        self.is_profile_complete = is_profile_complete
        self.is_invited = is_invited
