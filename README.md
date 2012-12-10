SublimeBingTranslator
=====================

Bing Translator plugin for Sublime Text 2.

## settings

Preference > Package Settings > SublimeBingTranslator > Settings - Default (or User)
```json
{
    //Translator Language Codes
    //http://msdn.microsoft.com/en-us/library/hh456380.aspx
    "from" : "en",
    "to" : "ja"
}
```

edit to "from" or "to"

Below is a link to the language code. <br/>
[http://msdn.microsoft.com/en-us/library/hh456380.aspx](http://msdn.microsoft.com/en-us/library/hh456380.aspx)


## translate selection

`command+shift+m`

Translate selection and display the results to a new file. (if already opened result view, adds the results.)

ex.  settings: en -> it
```plain
*translate*
------------------------
this is beutiful code!! 
- - - - - - - - - - - - 
Questo è il codice beutiful!! 
------------------------
```

## translate selection(reverse)

`command+shift+alt+m`

Default Settings translate "From" -> "To".
this command translate "To" -> "From" .

ex.  settings: en -> it
```plain
*translate*
------------------------
Questo è il codice beutiful!!  
- - - - - - - - - - - - 
This is the code beutiful!!  
------------------------
```

## If you use frequently...

Bing translator can translate characters has limited.<br/>
if you use frequently, recommend publishing API keys.

Windows Azure Marketplace -Registering your application-<br/>
[https://datamarket.azure.com/developer/applications/register](https://datamarket.azure.com/developer/applications/register)

after published API keys.
edit "SublimeBingTranslator.py"

```
class BingTranslatorSettings:
     ~~ ~~ ~~
	client_id = (new client id)
	client_secret = (new client secret)
     ~~ ~~ ~~
     ...
```
