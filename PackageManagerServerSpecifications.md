# Introduction #

The Package Manager Server is a Django Application hosted on App Engine.


# Details #
  * [RESTful](http://en.wikipedia.org/wiki/Representational_State_Transfer) interface
  * Formats supported : [JSON](http://www.json.org/), [YAML](http://www.yaml.org/), HTML
  * GET Access : Everyone
  * POST, UPDATE, DELETE : Need authentication
  * Authentication : OpenID / Google Account
  * Will serve Packages and MetaPackages descriptions
  * Replication : synchronize with mirrors

# Data Model #
## Package ##
|Name| Char|
|:---|:----|
|Version| Char|
|Date| Date |
|Is Meta| Boolean |
|Dependencies| Table |
|Tags| Table  |
|Ratings|  |
|Description| Text |
|ScreenShots| Images |
|Logo| Image |
|Package file links (HTTP, FTP, Torrent, File)|  |
|Licence| Char |
|Web | url |
|Sources| url |
|SHA1/MD5|  |
|Supported OS | Table |


## Distribution/ Profile ##
|Name| Char|
|:---|:----|
|Packages| Table|
|Categories|  |
|MetaData|  |
|Version| Char|
|Date| Date |
|Description| Text |

# Package File Structure #
Archive
  * Description File : Package Data Model in YAML
  * Python Scripts : Install, Uninstall, Enumeration, Update
  * Data-File Archive

The packages won't be hosted on the Package manager server but on each project's server.

## Links ##
  * Django: http://www.djangoproject.com/
  * App Engine: http://code.google.com/appengine/
  * Melange : http://code.google.com/p/soc/