# Taiko localization tool

### For *Taiko no Tatsujin: Dokodon! Mystery Adventure*

A small tool can export game text from `.dat` file to `.xlsx` file and game image from `.txp` file to `.png` file.

You can easily write down the translation in the `.xlsx` file and repack to `.dat` file by this tool.

You can easily modify the game png image and repack to `.txp` file by this tool.

All the settings can be modified in the `consts.py`.

### Requirements:

#### Python 3.6 +

```
Beautifulsoup4
openpyxl
fire
```

#### ExtraTools:

1.**lzx** in [Nintendo_DS_Compressors_CUE](http://www.romhacking.net/utilities/826/)

2.[**ctpktool**](https://github.com/dnasdw/ctpktool/releases)

### Usage:

#### Check:

```
Taiko.py check [-t TYPE]
```

`TYPE` is chosen from `sys`, `story`, `chara`.

Check your rom `.dat` format.

#### Text:

```
Taiko.py text -a ACTION [-t TYPE]
```

`ACTION` is `import` or `export`.

`TYPE` is chosen from `sys`, `story`, `chara`.

> **import** means import to the rom text/img file, it can be called `pack`.
>
> **export** means export from the rom text/img file, it can be called `unpack`.

#### Img:

```
Taiko.py img -a ACTION [-t TYPE]
```

`ACTION` is `import` or `export`.

`TYPE` is chosen from `sys`, `story`.

#### Packall/Unpackall:

```
Taiko.py img (packall | unpackall)
```

To pack or unpack at once.

### Attention:

Some `.dat` files has **duplicate** flags, please replace them by the `.dat` files in`DatReplace` dir.

The tool also has some other functions.

> This tool is for everyone who want to translate ***Taiko no Tatsujin: Dokodon! Mystery Adventure***.









