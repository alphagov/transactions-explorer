from hamcrest import assert_that, is_
from lib.filters import digest


class TestDigest:
    def setUp(self):
        digest.set_digests(None)

    def test_load_digests_in_yaml_format(self):
        digests = """
            asset.type: asset-4678abfe2.type
        """

        digest.load_digests(digests)

        assert_that(
            digest.digest('asset.type'),
            is_('asset-4678abfe2.type')
        )

    def test_return_plain_asset_if_digest_is_unknown(self):
        assert_that(
            digest.digest('unregistered_asset.js'),
            is_('unregistered_asset.js')
        )
