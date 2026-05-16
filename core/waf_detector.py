class WAFDetector:

    def __init__(self, headers):

        self.headers = headers

    def detect(self):

        server = (
            self.headers.get(
                "server",
                ""
            ).lower()
        )

        powered = (
            self.headers.get(
                "x-powered-by",
                ""
            ).lower()
        )

        cookies = str(
            self.headers
        ).lower()

        wafs = []

        # CLOUDFLARE
        if (
            "cloudflare" in server
            or "__cf_bm" in cookies
            or "cf-ray" in cookies
        ):

            wafs.append(
                "Cloudflare"
            )

        # AKAMAI
        if (
            "akamai" in server
            or "akamaighost" in server
        ):

            wafs.append(
                "Akamai"
            )

        # SUCURI
        if (
            "sucuri" in server
            or "x-sucuri" in cookies
        ):

            wafs.append(
                "Sucuri"
            )

        # IMPERVA
        if (
            "imperva" in server
            or "incap_ses" in cookies
        ):

            wafs.append(
                "Imperva"
            )

        # FASTLY
        if "fastly" in server:

            wafs.append(
                "Fastly"
            )

        # AWS WAF
        if (
            "awselb" in cookies
            or "aws" in server
        ):

            wafs.append(
                "AWS WAF"
            )

        # F5 BIG-IP
        if (
            "bigip" in cookies
            or "f5" in server
        ):

            wafs.append(
                "F5 BIG-IP"
            )

        return {

            "detected": (
                len(wafs) > 0
            ),

            "wafs": wafs
        }