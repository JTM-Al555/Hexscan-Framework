from ai.cve_lookup import (
    CVELookup
)


class CVEMapper:

    def __init__(self, technologies):

        self.technologies = (
            technologies
        )

        self.lookup = CVELookup()

    def map_cves(self):

        results = {}

        for tech in self.technologies:

            cves = (
                self.lookup.search(
                    tech
                )
            )

            results[tech] = cves

        return results