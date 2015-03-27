# Resources #

## Package ##
Returns the information for a single package

### URL: ###
> /api/package/name/version/format/

**Description:** Returns the metada for the package that you set in the URL

**Method:** GET

**Values to replace in the URL:**

_name:_ Name of the package to request information. e.g: Firefox

_version:_ Version of the package request information. e.g: 3.0.11

_format:_ Format to display the data. Only xml available at the moment.

**Authentication needed:** False

**URL example:** /api/package/firefox/3.0.11/xml/

**Answer example:**
```
<packages>
<package>
<name>Firefox</name>
<version>3.0.11</version>
<architecture>x32</architecture>
<short-description>
Mozilla Firefox is a free and open source web browser descended from the Mozilla Application Suite and managed by Mozilla Corporation
</short-description>
<long-description>
Firefox had 22.51% of the recorded usage share of web browsers as of May 2009, making it the second most popular browser in terms of current use worldwide, after Internet Explorer.

To display web pages, Firefox uses the Gecko layout engine, which implements most current web standards in addition to a few features which are intended to anticipate likely additions to the standards.

Latest Firefox features include tabbed browsing, a spell checker, incremental find, live bookmarking, a download manager, private browsing, location-aware browsing (aka "geolocation") based exclusively on a Google service and an integrated search system that uses Google by default in most localizations. Functions can be added through add-ons, created by third-party developers, of which there is a wide selection, a feature that has attracted many of Firefox's users.

Firefox runs on various versions of Mac OS X, Microsoft Windows, Linux, and many other Unix-like operating systems. Its current stable release is version 3.5, released on June 30, 2009. Firefox's source code is free software, released under a tri-license GNU GPL/GNU LGPL/MPL. Official versions are distributed under the terms of a proprietary EULA.
</long-description>
<section>Browsers</section>
<installed-size>15026</installed-size>
<maintainer>Mozilla Foundation<firefox@mozilla.com></maintainer>
<creator>Mozilla Foundation<firefox@mozilla.com></creator>
<publisher>Mozilla Foundation <firefox@mozilla.com></publisher>
<rights-holder>Mozilla Foundation<firefox@mozilla.com></rights-holder>
<filename>
http://download.mozilla.org/?product=firefox-3.0.11&os=linux&lang=en-US
</filename>
<release-date>09/07/09</release-date>
<supported>
<version>NT</version>
<version>XP</version>
</supported>
<changes>
Firefox 3.0.11 fixes several issues found in Firefox 3.0.10:

    * Fixed several security issues.
    * Fixed several stability issues.
    * Several issues were reported with the internal database, SQLite, which have now been fixed by upgrading to a newer version.
    * Fixed an issue where, in some specific cases, the bookmarks database would become corrupt. (bug 464486)
    * See the Firefox 3.0.10 release notes for changes in previous releases.
</changes>
<size>9500</size>
<languages>
<language>en</language>
</languages>
<license>Mozilla</license>
<sha256>45asa4s6a4s54as</sha256>
<homepage>http://www.firefox.com/</homepage>
<replaces>
<replace>Example 1.0-1</replace>
</replaces>
<provides/>
<pre-depends/>
<depends/>
<recommends>
<recommend>Example 1.0-1</recommend>
</recommends>
<suggests/>
<conflicts/>
<urls/>
</package>
</packages>
```


### URL: ###
> /api/package/name/latest/format/

**Description:** Returns the metada for the latest version of the package that you set in the URL

**Method:** GET

**Values to replace in the URL:**

_name:_ Name of the package to request information. e.g: Firefox

_format:_ Format to display the data. Only xml available at the moment.

**Authentication needed:** False

**URL example:** /api/package/firefox/latest/xml/

**Answer example:**
```
<packages>
<package>
<name>Firefox</name>
<version>3.0.11</version>
<architecture>x32</architecture>
<short-description>
Mozilla Firefox is a free and open source web browser descended from the Mozilla Application Suite and managed by Mozilla Corporation
</short-description>
<long-description>
Firefox had 22.51% of the recorded usage share of web browsers as of May 2009, making it the second most popular browser in terms of current use worldwide, after Internet Explorer.

To display web pages, Firefox uses the Gecko layout engine, which implements most current web standards in addition to a few features which are intended to anticipate likely additions to the standards.

Latest Firefox features include tabbed browsing, a spell checker, incremental find, live bookmarking, a download manager, private browsing, location-aware browsing (aka "geolocation") based exclusively on a Google service and an integrated search system that uses Google by default in most localizations. Functions can be added through add-ons, created by third-party developers, of which there is a wide selection, a feature that has attracted many of Firefox's users.

Firefox runs on various versions of Mac OS X, Microsoft Windows, Linux, and many other Unix-like operating systems. Its current stable release is version 3.5, released on June 30, 2009. Firefox's source code is free software, released under a tri-license GNU GPL/GNU LGPL/MPL. Official versions are distributed under the terms of a proprietary EULA.
</long-description>
<section>Browsers</section>
<installed-size>15026</installed-size>
<maintainer>Mozilla Foundation<firefox@mozilla.com></maintainer>
<creator>Mozilla Foundation<firefox@mozilla.com></creator>
<publisher>Mozilla Foundation <firefox@mozilla.com></publisher>
<rights-holder>Mozilla Foundation<firefox@mozilla.com></rights-holder>
<filename>
http://download.mozilla.org/?product=firefox-3.0.11&os=linux&lang=en-US
</filename>
<release-date>09/07/09</release-date>
<supported>
<version>NT</version>
<version>XP</version>
</supported>
<changes>
Firefox 3.0.11 fixes several issues found in Firefox 3.0.10:

    * Fixed several security issues.
    * Fixed several stability issues.
    * Several issues were reported with the internal database, SQLite, which have now been fixed by upgrading to a newer version.
    * Fixed an issue where, in some specific cases, the bookmarks database would become corrupt. (bug 464486)
    * See the Firefox 3.0.10 release notes for changes in previous releases.
</changes>
<size>9500</size>
<languages>
<language>en</language>
</languages>
<license>Mozilla</license>
<sha256>45asa4s6a4s54as</sha256>
<homepage>http://www.firefox.com/</homepage>
<replaces>
<replace>Example 1.0-1</replace>
</replaces>
<provides/>
<pre-depends/>
<depends/>
<recommends>
<recommend>Example 1.0-1</recommend>
</recommends>
<suggests/>
<conflicts/>
<urls/>
</package>
</packages>
```


---


## Packages ##
Returns the information for a set of packages

### URL: ###
> /api/packages/all/format/

**Details:** Retuns the metadata for all the packages in the repository

**Method:** GET

**Values to replace in the URL:**

_format:_ Format to display the data. Only xml available at the moment.

**Authentication needed:** False

**URL example:** /api/packages/all/xml/

**Answer example:**
```
<packages>
<package>
  <name>Example</name>
  <version>1.0-1</version>
  <architecture>32bit</architecture>
  <short-description>This is an example package</short-description>
  <long-description>This is my longer description. It includes\n    newlines and other characters.</long-description>
  <section>devel</section>

  <installed-size>1024</installed-size>
  <maintainer>Example Person&lt;email@address.com&gt;</maintainer>
  <creator>Example Person&lt;email@address.com&gt;</creator>
  <publisher>Example Person &lt;email@address.com&gt;</publisher>
  <rights-holder>Example Person&lt;email@address.com&gt;</rights-holder>

  <filename>\pool\e\example_1.0-1_32bit.zip</filename>
  <release-date>06/11/09</release-date>
  <supported xmlns="">
    <version>XP</version>
  </supported>
  <changes>Added feature A and Feature B. Fixed bugs #0001 and #0002.</changes>
  <size>100</size>

  <languages xmlns="">
    <language>en</language>
    <language>es</language>
  </languages>
  <license>GPL</license>
  <sha256>1a79a4d60de6718e8e5b326e338ae533</sha256>
  <homepage>http://example.com/</homepage>

  <replaces xmlns="" />
  <provides xmlns="" />
  <pre-depends xmlns="" />
  <depends xmlns="" />
  <recommends xmlns="" />
  <suggests xmlns="" />
  <conflicts xmlns="" />
  <urls xmlns="" />
</package><package>

  <name>Firefox</name>
  <version>3.0.11</version>
  <architecture>x32</architecture>
  <short-description>Mozilla Firefox is a free and open source web browser descended from the Mozilla Application Suite and managed by Mozilla Corporation</short-description>
  <long-description>Firefox had 22.51% of the recorded usage share of web browsers as of May 2009, making it the second most popular browser in terms of current use worldwide, after Internet Explorer.

To display web pages, Firefox uses the Gecko layout engine, which implements most current web standards in addition to a few features which are intended to anticipate likely additions to the standards.

Latest Firefox features include tabbed browsing, a spell checker, incremental find, live bookmarking, a download manager, private browsing, location-aware browsing (aka "geolocation") based exclusively on a Google service and an integrated search system that uses Google by default in most localizations. Functions can be added through add-ons, created by third-party developers, of which there is a wide selection, a feature that has attracted many of Firefox's users.

Firefox runs on various versions of Mac OS X, Microsoft Windows, Linux, and many other Unix-like operating systems. Its current stable release is version 3.5, released on June 30, 2009. Firefox's source code is free software, released under a tri-license GNU GPL/GNU LGPL/MPL. Official versions are distributed under the terms of a proprietary EULA.</long-description>
  <section>Browsers</section>

  <installed-size>15026</installed-size>
  <maintainer>Mozilla Foundation&lt;firefox@mozilla.com&gt;</maintainer>
  <creator>Mozilla Foundation&lt;firefox@mozilla.com&gt;</creator>
  <publisher>Mozilla Foundation &lt;firefox@mozilla.com&gt;</publisher>
  <rights-holder>Mozilla Foundation&lt;firefox@mozilla.com&gt;</rights-holder>

  <filename>http://download.mozilla.org/?product=firefox-3.0.11&amp;os=linux&amp;lang=en-US</filename>
  <release-date>09/07/09</release-date>
  <supported xmlns="">
    <version>NT</version>
    <version>XP</version>
  </supported>

  <changes>Firefox 3.0.11 fixes several issues found in Firefox 3.0.10:

    * Fixed several security issues.
    * Fixed several stability issues.
    * Several issues were reported with the internal database, SQLite, which have now been fixed by upgrading to a newer version.
    * Fixed an issue where, in some specific cases, the bookmarks database would become corrupt. (bug 464486)
    * See the Firefox 3.0.10 release notes for changes in previous releases.</changes>
  <size>9500</size>
  <languages xmlns="">
    <language>en</language>
  </languages>
  <license>Mozilla</license>
  <sha256>45asa4s6a4s54as</sha256>

  <homepage>http://www.firefox.com/</homepage>
  <replaces xmlns="">
    <replace>Example 1.0-1</replace>
  </replaces>
  <provides xmlns="" />
  <pre-depends xmlns="" />
  <depends xmlns="" />
  <recommends xmlns="">

    <recommend>Example 1.0-1</recommend>
  </recommends>
  <suggests xmlns="" />
  <conflicts xmlns="" />
  <urls xmlns="" />
</package>
</packages>
```