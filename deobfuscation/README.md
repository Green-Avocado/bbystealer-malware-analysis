# Deobfuscation

**Note that the payload and loader were from different copies of bbystealer and use different endpoints**

- `*_original.js` contains the original source.
- `*_beautified.js` is the original code formatted, but otherwise unchanged.
- `*_deobfuscated.js` is fully deobfuscated code.

## Extracting obfuscated JavaScript

### loader

All the JavaScript used in the nexe executable is stored as plaintext within the exe itself.
This includes the loader, which is stored as a single line of obfuscated JavaScript.

The loader code can be found near the bottom of the executable, but before debugging dependencies if present.
It can be easily found in mose cases by searching for keywords found in the loader source code, such as "Discord".

To extract the loader, you copy the code as-is from the exe.
Take care to make sure no extra opening braces are included.

For example, the loader for the `OwOGame.exe` file can be found at line 889028.
It contains an opening brace at the end of the line, which should not be included when extracted.

### payload

The payload can be downloaded from the link found in the loader after deobfuscating it.
This link looks something like `https://indianboatparty[.]com/OOJfZ9s6pHbF/str`.

Alternatively, if the exe is run with a Discord installation present, the payload will be written to:

```js
process.env.LOCALAPPDATA + '\\*cord*\\app-*\\modules\\discord_desktop_core-*\\discord_desktop_core\\index.js'
```

## Formatting and initial deobfuscation

Both the loader and the payload can be formatted and partially deobfuscated using tools such as:

- [d4js](https://lelinhtinh.github.io/de4js/)
- [Online JavaScript Beautifier](https://beautifier.io/)

This makes the code more readable and can simplify some expressions.
For example:

```js
function onlyUnique(_0x25228c,_0x4dd03b,_0x115be5){const _0x4d4641={};_0x4d4641['gvSQz']=function(_0x4e9814,_0xe10a5a){return _0x4e9814===_0xe10a5a;};function _0x1c86f9(_0x8c86ab,_0x1044df,_0x6259b,_0x55e03d){return a0_0x5ce233(_0x8c86ab,_0x1044df-0x14f,_0x6259b-0x136,_0x55e03d- -0x648);}const _0x5f07df=_0x4d4641;return _0x5f07df[_0x1c86f9('hw71',0x40d,0x28c,0x1cd)](_0x115be5['index'+'Of'](_0x25228c),_0x4dd03b);}
```

becomes:

```js

function onlyUnique(_0x25228c, _0x4dd03b, _0x115be5) {
    const _0x4d4641 = {};
    _0x4d4641['gvSQz'] = function (_0x4e9814, _0xe10a5a) {
        return _0x4e9814 === _0xe10a5a;
    };

    function _0x1c86f9(_0x8c86ab, _0x1044df, _0x6259b, _0x55e03d) {
        return a0_0x5ce233(_0x8c86ab, _0x1044df - 0x14f, _0x6259b - 0x136, _0x55e03d - -0x648);
    }
    const _0x5f07df = _0x4d4641;
    return _0x5f07df[_0x1c86f9('hw71', 0x40d, 0x28c, 0x1cd)](_0x115be5['index' + 'Of'](_0x25228c), _0x4dd03b);
}
```

Furthermore, one obfuscation technique used splits strings into multiple parts.
d4js can be used to reverse this process, such that expressions such as `'crypt' + 'o'` becomes `'crypto'`.

From here, we can see the names and some information about global functions and variables.
The settings used to obfuscate this code did not allow these to be renamed.
This is an oversight as none of these are exported so preserving these names was not necessary.
Enabling this would have made the code more difficult to analyse without changing its functionality.

Some other global functions are present, as well as some nested functions and constants.
These are used to further obfuscate strings, members of objects, and basic operations.
For example:

```js
_0x31dfad[_0x4f879f('myG#', 0x802, 0x6a1, 0x696)]
```

becomes

```js
'https://indianboatparty.com/OOJfZ9s6pHbF/tokens'
```

Note that, once formatted, the code will no longer run.
If we try to run it at this stage, the V8 runtime will exceed its memory limit and crash.
This is because of self defending which is discussed in the next section.

## Defeating self defending

The reason for the crash when running beautified code is that some functions perform a regex search on their own source code.
This process succeedes in the function's original form, but fails when beautified.

For example, the `a0_0x440f` function is used in string obfuscation and implements this technique for self defending.
The function cannot be run without changes if it is beautified.

To defeat self defending, we can simply extract these functions in their original form without formatting.
These functions will not be present in the deobfuscated code, so this is only necessary for the deobfuscation script.

## Deobfuscating strings and members

Most strings are obfuscated by splitting them into multiple parts and replacing them with equivalent expressions using the functions mentioned above.

To deobfuscate these strings, the obfuscating functions should be loaded into a deobfuscation script.
This can be scoped appropriately so that the script only uses functions that would be available to the program.
However, this was not necessary as there were no conflicts between functions at different scopes.

```js
_0x2b801e[_0x74a69e(0xacc, 0xb2c, 0x92e, 'OBiu') + 'ch'](_0x4c5ebd => _0x383f59['push'](_0x4c5ebd))
```

becomes

```js
_0x2b801e['forEach'](_0x4c5ebd => _0x383f59['push'](_0x4c5ebd))
```

Notice that methods have also been obfuscated here.
The above code can be further simplified as follows:

```js
_0x2b801e.forEach(_0x4c5ebd => _0x383f59.push(_0x4c5ebd))
```

## Deobfuscating function calls and operations

Some function calls and operations are also obfuscated.

For example, the constants contain some functions that simply wrap basic operations including addition, subtraction, and equalities:

```js
_0x4d4641['gvSQz'] = function (_0x4e9814, _0xe10a5a) {
    return _0x4e9814 === _0xe10a5a;
};
```

```js
'qQDvs': function (_0x3fa03d, _0x294cd3) {
    return _0x3fa03d + _0x294cd3;
},
```

Other functions simply wrap function calls:

```js
'RDZqf': function (_0x3b9cd5) {
    return _0x3b9cd5();
},
```

```js
'Lstbi': function (_0x530ba0, _0x391a43) {
    return _0x530ba0(_0x391a43);
},
```

These can be identified when the obfuscating function is used as a function call, or when it returns a function instead of a string.
The behaviour of the function can be determined by returning the function as a string, using the `toString()` method.
Alternatively, a script can test some inputs against the function to determine its behaviour.

Only a few basic operations are used this way:

- addition
- subtraction
- equality / inequality (strict or unstrict)
- function call (with or without arguments)

Once the behaviour is know, the obfuscated expression can be simplified by removing the obfuscating function and replacing it with the native operation.

## Fixing control flow

In rare cases, control flow may be obfuscated using additional loops and conditionals.

For example, the following while loop is used to obfuscate 5 statements:

```js
const _0x223b20 = _0x3f3851[_0x43dde5(0x8e3, 0x851, 'BUvv', 0xa26)]['split']('|');
let _0x182f2e = 0x2636 + -0x3 * 0x6e5 + -0x1187 * 0x1;
while (!![]) {
    switch (_0x223b20[_0x182f2e++]) {
    case '0':
        if (_0x5ba47f[_0x2ce4f8(0x637, 'mKAy', 0x61e, 0x88a) + 'des'](_0x3f3851[_0x43dde5(0xb7f, 0x88d, 'Iiba', 0x99f)])) _0x503aae[_0x43dde5(0x549, 0x74b, 'qUP8', 0x57e)](_0x3f3851[_0x43dde5(0x73d, 0x611, 'qUP8', 0x32d)]);
        continue;
    case '1':
        _0x3f3851[_0x43dde5(0x10c, 0x3c6, 'myG#', 0x534)](_0x45f15e);
        continue;
    case '2':
        if (_0x389d12['inclu' + _0x2ce4f8(0x7f1, '8!60', 0x547, 0x74a)](_0x3f3851[_0x43dde5(0x73c, 0x44b, 'LoWO', 0x250)])) _0x39db1d[_0x2ce4f8(0x6be, 'eE3H', 0x7fd, 0x971)](_0x3f3851['duFcX']);
        continue;
    case '3':
        if (_0x5c6874[_0x43dde5(0x545, 0x49c, 'IJDN', 0x721) + _0x2ce4f8(0xabe, 'Rk96', 0xca6, 0x7e6)](_0x3f3851[_0x43dde5(0x91f, 0x83d, 'mKAy', 0x75c)])) _0xa9867c[_0x2ce4f8(0x6be, 'eE3H', 0x9d4, 0x7f6)](_0x3f3851[_0x43dde5(0x53a, 0x5ca, 'nTZR', 0x4db)]);
        continue;
    case '4':
        if (_0x361784[_0x2ce4f8(0x6db, 'LoWO', 0x651, 0x627) + _0x2ce4f8(0xabc, 'IJI3', 0x7a7, 0xbd0)](_0x3f3851[_0x43dde5(0x809, 0x658, 'hw71', 0x7db)])) _0x13afa4[_0x2ce4f8(0xb56, 'HCWE', 0xb27, 0xaa0)](_0x3f3851[_0x2ce4f8(0x5aa, '^%2f', 0x284, 0x599)]);
        continue;
    }
    break;
}
```

If we deobfuscate the statements, this becomes:

```js
const _0x223b20 = '0|2|3|4|1'.split('|');
let _0x182f2e = 0;
while (true) {
    switch (_0x223b20[_0x182f2e++]) {
    case '0':
        if (stdout.includes('Discord.exe')) runningDiscords.push('Discord');
        continue;
    case '1':
        killDiscord();
        continue;
    case '2':
        if (stdout.includes('DiscordCanary.exe')) runningDiscords.push('DiscordCanary');
        continue;
    case '3':
        if (stdout.includes('DiscordPTB.exe')) runningDiscords.push('DiscordPTB');
        continue;
    case '4':
        if (stdout.includes('DiscordDevelopment.exe')) runningDiscords.push('DiscordDevelopment');
        continue;
    }
    break;
}
```

The first line is used to create an array of numbers to determine the order of execution:

```js
const _0x223b20 = '0|2|3|4|1'.split('|');
```

becomes

```js
const _0x223b20 = [ '0', '2', '3', '4', '1' ];
```

The second line is the index, which begins at 0:

```js
let _0x182f2e = 0;
```

The cases are executed in the order of the array `_0x223b20`, so the while loop can be replaced with:

```js
if (stdout.includes('Discord.exe')) runningDiscords.push('Discord');
if (stdout.includes('DiscordCanary.exe')) runningDiscords.push('DiscordCanary');
if (stdout.includes('DiscordPTB.exe')) runningDiscords.push('DiscordPTB');
if (stdout.includes('DiscordDevelopment.exe')) runningDiscords.push('DiscordDevelopment');
killDiscord();
```

## Summary

### loader

- Reads cookies and passwords from Chromium-based browsers and sends them to the webhook.
- Steals Discord tokens from Discord clients.
- Downloads the payload and injects it into Discord clients.

###### Browsers affected
  - Google Chrome
  - Opera
  - Brave
  - Yandex
  - Microsoft Edge

###### Discord clients affected
  - Discord
  - Discord Canary
  - Discord PTB
  - Discord Development
  - Lightcord

### payload

- Intercepts credentials from the Discord client and sends them to the webhook.
  Specifically:
  - email
  - password
  - credit card number, CVC, and expiry date
  - 2-factor authentication secret

## Additional Notes

- Later versions of the malware also target cryptocurrency wallets including Exodus and MetaMask.
