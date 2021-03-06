# -*- coding: utf-8 -*-


class dns_find:
    """docstring for dns_find"""

    def __init__(
            self,
            framework,
            company,
            limit,
            count,
            engines,
            cookie=None,
            agent=None,
            proxy=None,
            timeout=None):
        self.framework = framework
        self.cookie = cookie
        self.agent = agent
        self.proxy = proxy
        self.timeout = timeout
        self.company = company
        self.limit = limit
        self.count = count
        self.engines = engines
        self._engines = ["bing", "google", "yahoo", "yandex", "metacrawler", "ask"]
        self._get_dns = []

    def run_crawl(self):
        pages = ""
        alert_mode = self.framework._global_options["verbosity"] == 2
        company = self.company
        for i in self.engines:
            if(i.lower() in self._engines):
                if(i.lower() == "google"):
                    company = "\"%s\"" % company

                if(alert_mode):
                    self.framework.alert("Search in \"%s\"" % i)
                try:
                    attr = getattr(self.framework, "%s_engine" % i)(
                        word=company,
                        limit=self.limit,
                        count=self.count,
                        cookie=self.cookie,
                        agent=self.agent,
                        proxy=self.proxy,
                        timeout=self.timeout)
                    attr.run_crawl()
                except Exception as e:
                    self.framework.error("Connection Error: " + e.message)
                else:
                    pages = pages + attr.get_pages
            else:
                if(alert_mode):
                    self.framework.error(
                        "Search Engine \"%s\" Not Found !" % i)

        self._get_dns = self.framework.page_parse(pages).get_dns(self.company)

    @property
    def get_dns(self):
        return self._get_dns
