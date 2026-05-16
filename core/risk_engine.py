class RiskEngine:

    def __init__(self, results):

        self.results = results

        self.score = 0

        self.findings = []

    def check_ports(self):

        ports = self.results.get(
            "ports",
            []
        )

        dangerous = [

            21,
            22,
            23,
            25,
            3306,
            6379,
            27017
        ]

        for port in ports:

            if port in dangerous:

                self.score += 15

                self.findings.append(
                    (
                        "High",
                        f"Dangerous port exposed: {port}"
                    )
                )

    def check_headers(self):

        headers = self.results.get(
            "security_headers",
            {}
        )

        missing = headers.get(
            "missing_headers",
            []
        )

        if missing:

            self.score += (
                len(missing) * 3
            )

            self.findings.append(
                (
                    "Medium",
                    (
                        "Missing security headers: "
                        + ", ".join(missing)
                    )
                )
            )

    def check_js_secrets(self):

        js = self.results.get(
            "javascript_analysis",
            {}
        )

        for file, data in js.items():

            secrets = data.get(
                "secrets",
                {}
            )

            if secrets:

                self.score += 25

                self.findings.append(
                    (
                        "Critical",
                        (
                            f"Secrets exposed "
                            f"in JS file: {file}"
                        )
                    )
                )

    def check_crawler(self):

        crawler = self.results.get(
            "web_crawler",
            {}
        )

        interesting = crawler.get(
            "interesting",
            {}
        )

        admins = interesting.get(
            "admin_panels",
            []
        )

        if admins:

            self.score += 10

            self.findings.append(
                (
                    "Medium",
                    (
                        f"Admin panels discovered: "
                        f"{len(admins)}"
                    )
                )
            )

    def calculate_grade(self):

        if self.score >= 70:
            return "Critical"

        if self.score >= 50:
            return "High"

        if self.score >= 30:
            return "Medium"

        return "Low"

    def analyze(self):

        self.check_ports()

        self.check_headers()

        self.check_js_secrets()

        self.check_crawler()

        return {

            "risk_score": self.score,

            "risk_level": (
                self.calculate_grade()
            ),

            "findings": self.findings
        }