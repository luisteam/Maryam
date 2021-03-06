# -*- coding: utf-8 -*-
from re import search, I


class cms_identify:
    """docstring for cms_identify"""

    def __init__(self, framework, content, headers):
        self.framework = framework
        self.content = content
        self.headers = headers
        self._cms = None

    def run_crawl(self):
        for i in dir(self):
            con1 = not i.startswith("__")
            con2 = not i.endswith("__")
            con3 = i not in ("_cms", "content", "headers",
                             "framework", "get_cms", "run_crawl")
            if(con1 and con2 and con3):
                getattr(self, i)()

    def adobeaem(self):
        mode = False
        mode |= search(
            r"<link[^>]*stylesheet[^>]*etc\/designs\/[^>]*\>[^<]*", self.content, I) is not None
        mode |= search(
            r"<link[^>]*etc\/clientlibs\/[^>]*\>[^<]*", self.content, I) is not None
        mode |= search(
            r"<script[^>]*etc\/clientlibs\/[^>]*\>[^<]*", self.content, I) is not None
        mode |= search(
            r"<script[^>]*\/granite\/[^>]*(\.js\")+\>[^<]*", self.content, I) is not None
        if(mode):
            self._cms = "Adobe AEM: Stack is based on Apache Sling + Apache Felix OSGi container + JCR Repo + Java"

    def drupal(self):
        mode = False
        regexs = [r"\<script type\=\"text\/javascript\" src\=\"[^\"]*\/misc\/drupal.js[^\"]*\"\>\<\/script\>",
                  r"<[^>]+alt\=\"Powered by Drupal, an open source content management system\"",
                  r"@import \"[^\"]*\/misc\/drupal.css\"",
                  r"jQuery.extend\(drupal\.S*",
                  r"Drupal.extend\(\S*",
                  r"name=\"?generator\"? content=\"?Varbase",
                  r"jQuery.extend\(drupal\.S*",
                  r"data-drupal-selector=",
                  r"name=\"?generator\"? content=\"?Drupal ([0-9]+)",
                  ]
        if('set-cookie' in self.headers.keys()):
            if(search(r"SESS[a-z0-9]{32}=[a-z0-9]{32}", self.headers["set-cookie"], I)):
                mode = "Drupal"
        if('x-drupal-cache' in self.headers.keys()):
            mode = "Drupal"
        for i in regexs:
            tmp_mode = search(i, self.content)
            if(tmp_mode):
                try:
                    mode = "Drupal version " + tmp_mode.group(1)
                except IndexError:
                    mode = "Drupal"
                break
        if(mode):
            self._cms = mode

    def joomla(self):
        mode = False
        if('set-cookie' in self.headers.keys()):
            mode |= search(
                r"mosvisitor=", self.headers["set-cookie"], I) is not None
        mode |= search(
            r"\<meta name\=\"Generator\" content\=\"Joomla! - Copyright \(C\) 200[0-9] - 200[0-9] Open Source Matters. All rights reserved.\" \/\>", self.content, I) is not None
        mode |= search(
            r"\<meta name\=\"generator\" content\=\"Joomla! (\d\.\d) - Open Source Content Management\" \/\>", self.content, I) is not None
        mode |= search(
            r"Powered by \<a href\=\"http://www.joomla.org\"\>Joomla!\<\/a\>.", self.content, I) is not None
        if(mode):
            self._cms = "Joomla"

    def magento(self):
        mode = False
        if('set-cookie' in self.headers.keys()):
            mode |= search(r"magento=[0-9a-f]+|frontend=[0-9a-z]+",
                           self.headers["set-cookie"], I) is not None
        mode |= search(
            r"images/logo.gif\" alt\=\"Magento Commerce\" \/\>\<\/a\>\<\/h1\>", self.content, I) is not None
        mode |= search(
            r"\<a href\=\"http://www.magentocommerce.com/bug-tracking\" id\=\"bug_tracking_link\"\>\<strong\>Report All Bugs\<\/strong\>\<\/a\>", self.content, I) is not None
        mode |= search(
            r"\<link rel\=\"stylesheet\" type\=\"text/css\" href\=\"[^\"]+\/skin\/frontend\/[^\"]+\/css\/boxes.css\" media\=\"all\"", self.content, I) is not None
        mode |= search(
            r"\<div id\=\"noscript-notice\" class\=\"magento-notice\"\>", self.content, I) is not None
        mode |= search(
            r"Magento is a trademark of Magento Inc. Copyright &copy; ([0-9]{4}) Magento Inc", self.content, I) is not None
        if(mode):
            self._cms = "Magento"

    def plone(self):
        mode = False
        if('x-caching-rule-id' in self.headers.keys()):
            mode |= search(r"plone-content-types",
                           self.headers["x-caching-rule-id"], I) is not None
        if('x-cache-rule' in self.headers.keys()):
            mode |= search(r"plone-content-types",
                           self.headers["x-cache-rule"], I) is not None
        mode |= search(
            r"\<meta name\=\"generator\" content\=\"[^>]*http:\/\/plone.org\" \/>", self.content, I) is not None
        mode |= search(
            r"(@import url|text\/css)[^>]*portal_css\/.*plone.*css(\)|\")", self.content, I) is not None
        mode |= search(
            r"src\=\"[^\"]*ploneScripts[0-9]+.js\"", self.content, I) is not None
        mode |= search(
            r"\<div class\=\"visualIcon contenttype-plone-site\"\>", self.content, I) is not None
        if(mode):
            self._cms = "Plone"

    def silverstripe(self):
        mode = False
        if('set-cookie' in self.headers.keys()):
            mode |= search(
                r"PastVisitor=[0-9]+.*", self.headers["set-cookie"], I) is not None
        mode |= search(
            r"\<meta name\=\"generator\"[^>]*content\=\"SilverStripe", self.content, I) is not None
        mode |= search(
            r"\<link[^>]*stylesheet[^>]*layout.css[^>]*\>[^<]*\<link[^>]*stylesheet[^>]*typography.css[^>]*\>[^<]*\<link[^>]*stylesheet[^>]*form.css[^>]*\>", self.content, I) is not None
        mode |= search(
            r"\<img src\=\"\/assets\/[^\/]+\/_resampled\/[^\"]+.jpg\"", self.content, I) is not None
        if(mode):
            self._cms = "SilverStripe"

    def wordpress(self):
        mode = False
        mode |= search(
            r"\<meta name\=\"generator\" content\=\"WordPress.com\" \/\>", self.content, I) is not None
        mode |= search(
            r"\<a href\=\"http://www.wordpress.com\"\>Powered by WordPress\<\/a\>", self.content, I) is not None
        mode |= search(r"\<link rel\=\'https://api.w.org/\'",
                       self.content, I) is not None
        mode |= search(r"\/wp-content\/plugins\/", self.content, I) is not None
        if(mode):
            self._cms = "WordPress"

    def concrete5(self):
        mode = False
        mode = search(
            r'<meta name="generator" content="concrete5',
            self.content) is not None
        mode |= search(r'/packages/concrete5_theme/themes/',
                       self.content) is not None
        if(mode):
            self._cms = "Concrete5"

    def typo3(self):
        mode = False
        mode = search(
            r'This website is powered by TYPO3|/typo3conf',
            self.content) is not None
        mode |= search(
            r'"generator" content="TYPO3 CMS">|/typo3temp/assets/',
            self.content) is not None
        if(mode):
            self._cms = "TYPO3"

    def hubspot(self):
        mode = False
        mode = search(
            r"<meta name=\"generator\" content=\"HubSpot\">", self.content) is not None
        mode2 = search(
            r"<!-- Generated by the HubSpot Template Builder - template version ([0-9]{1,6}\.[0-9]{1,6}) -->", self.content)
        alert = "HubSpot"
        if(mode2):
            mode |= True
            alert = "HubSpot version " + mode2.group(1)
        if(mode):
            self._cms = alert

    def squarespace(self):
        mode = False
        mode = search(r"<!-- This is Squarespace. -->",
                      self.content) is not None
        if(mode):
            self._cms = "Squarespace"

    @property
    def get_cms(self):
        return self._cms
